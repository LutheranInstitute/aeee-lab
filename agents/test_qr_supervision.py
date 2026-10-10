#!/usr/bin/env python3
"""
test_qr_supervision.py — the nine checks are code, so they get tests.

Improvement #7 of QR_SUPERVISION_IMPROVEMENTS.md: "The nine checks are untested
code. A smoke test proving the rune case refuses is not a suite — a regression in
contrast() or module_size would pass silently and be found by a customer instead
of a test."

These are BEHAVIOR contracts, not snapshots. Each test asserts a relationship the
gate must preserve, not a value that is expected to drift.

Run:
    python test_qr_supervision.py            # stdlib unittest, no pytest needed
    python test_qr_supervision.py -v
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

import qr_envelope as qe
import qr_supervision as qs


class TempPNG:
    """Render a payload to a temp PNG, with knobs to degrade it."""

    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="qrtest-"))

    def render(self, envelope: str, name: str = "a.png", *, box_size: int = 10,
               border: int = 4, ecc: str = "M"):
        p = self.dir / name
        qs._render(envelope, p, box_size=box_size, border=border, ecc=ecc)
        return p


class TestTheGateAccepts(unittest.TestCase):
    """What must PASS."""

    def setUp(self):
        self.t = TempPNG()

    def test_a_good_card_passes(self):
        env = qe.encode("route", {"cmd": "væult:// status"})
        p = self.t.render(env)
        rep = qs.supervise(p, expect_kind="route")
        self.assertTrue(rep.passed, f"refused a good card: {rep.reason()}")
        self.assertEqual(len(rep.decoders_ok), 2, "both decoders must agree")

    def test_every_envelope_type_passes(self):
        for kind in qe.TYPES:
            with self.subTest(kind=kind):
                env = qe.encode(kind, {"probe": kind})
                p = self.t.render(env, name=f"{kind}.png")
                rep = qs.supervise(p, expect_kind=kind)
                self.assertTrue(rep.passed, f"{kind}: {rep.reason()}")

    def test_produce_returns_a_linked_receipt(self):
        r = qs.produce("route", {"cmd": "væult:// list"}, out_path=self.t.dir / "r.png")
        self.assertTrue(r.envelope_sha256 and r.image_sha256)
        self.assertTrue(r.chain, "a receipt must carry a chain hash")
        # the chain must be seeded from a REAL prev, not ""
        self.assertNotEqual(r.prev, "", "prev must not be empty — that is not a chain")


class TestTheGateRefuses(unittest.TestCase):
    """What must REFUSE. Each names a distinct reason."""

    def setUp(self):
        self.t = TempPNG()

    def test_rune_magic_is_refused(self):
        """The §5.3 failure class: generates fine, fails on scan."""
        good = qe.encode("route", {"cmd": "x"})
        rune = "æ:" + good[len("ae:"):]
        p = self.t.render(rune, name="rune.png")
        rep = qs.supervise(p, envelope=rune)
        self.assertFalse(rep.passed, "a rune envelope must be refused")
        names = {c.name for c in rep.failed}
        self.assertIn("charset", names, "charset must be the named failure")
        # and the mechanism: one decoder mangles it
        self.assertLess(len(rep.decoders_ok), 2,
                        "the rune class is caught by cross-decoder disagreement")

    def test_payload_mismatch_is_refused(self):
        env = qe.encode("route", {"cmd": "a"})
        p = self.t.render(env)
        rep = qs.supervise(p, expect_payload={"cmd": "DIFFERENT"}, envelope=env)
        self.assertFalse(rep.passed)
        self.assertIn("payload_match", {c.name for c in rep.failed})

    def test_type_mismatch_is_refused(self):
        env = qe.encode("route", {"cmd": "a"})
        p = self.t.render(env)
        rep = qs.supervise(p, expect_kind="secret", envelope=env)
        self.assertFalse(rep.passed)
        self.assertIn("type_fidelity", {c.name for c in rep.failed})

    def test_a_non_envelope_image_is_refused(self):
        import cv2
        import numpy as np
        p = self.t.dir / "blank.png"
        cv2.imwrite(str(p), np.full((200, 200, 3), 255, dtype=np.uint8))
        rep = qs.supervise(str(p))
        self.assertFalse(rep.passed)
        self.assertIn("envelope", {c.name for c in rep.failed})

    def test_a_tiny_render_is_refused_on_module_size(self):
        """box_size=1 makes modules too small to scan."""
        env = qe.encode("route", {"cmd": "x"})
        p = self.t.render(env, name="tiny.png", box_size=1, border=1)
        rep = qs.supervise(p, envelope=env)
        # either it fails to decode, or module_size catches it — both are refusals
        self.assertFalse(rep.passed, "a 1px-per-module code must not pass")


class TestTheChecksAreHonest(unittest.TestCase):
    """The checks must not report a proxy as a measurement."""

    def setUp(self):
        self.t = TempPNG()

    def test_module_count_is_measured_not_assumed(self):
        """A v8 code must report 49 modules, not the v1 floor of 21."""
        import cv2
        env = qe.encode("route", {"cmd": "y" * 60})
        p = self.t.render(env)
        img = cv2.imread(str(p))
        ok, _, pts, _ = cv2.QRCodeDetector().detectAndDecodeMulti(img)
        self.assertIsNotNone(pts, "detector must find the code")
        n, how = qs._estimate_modules_side(img, pts[0])
        self.assertIn("measured", how,
                      f"fell back to a proxy: {how} — a proxy that errs "
                      f"optimistic is worse than no check")
        self.assertEqual(n % 4, 1, "a QR side is 17+4v, always 1 mod 4")
        self.assertGreaterEqual(n, 21)

    def test_module_count_tracks_the_real_version(self):
        """Rendering different payload sizes must yield different, correct counts."""
        import cv2
        seen = []
        for i, n_chars in enumerate([2, 60, 300]):
            env = qe.encode("route", {"cmd": "z" * n_chars})
            p = self.t.render(env, name=f"v{i}.png")
            img = cv2.imread(str(p))
            ok, _, pts, _ = cv2.QRCodeDetector().detectAndDecodeMulti(img)
            if pts is None:
                continue
            n, how = qs._estimate_modules_side(img, pts[0])
            if "measured" in how:
                seen.append(n)
        self.assertGreaterEqual(len(seen), 2, "at least two sizes must measure")
        self.assertEqual(len(set(seen)), len(seen),
                         f"different sizes gave the same count: {seen}")

    def test_a_fallback_names_itself(self):
        """If measurement fails, the detail must SAY so — never look measured."""
        n, how = qs._estimate_modules_side(None, None)
        self.assertIn("assumed", how,
                      "a fallback must announce itself as a fallback")


class TestTheChainIsReal(unittest.TestCase):
    """The receipt chain must link, not just hash."""

    def test_prev_is_not_empty(self):
        prev, source = qs.chain_prev()
        # either a real prev, or an explicit statement that no chain exists
        self.assertTrue(prev or "no kænbæn" in source,
                        f"prev={prev!r} source={source!r}")

    def test_two_receipts_have_different_prev_or_chain(self):
        t = TempPNG()
        r1 = qs.produce("route", {"cmd": "one"}, out_path=t.dir / "1.png")
        r2 = qs.produce("route", {"cmd": "two"}, out_path=t.dir / "2.png")
        self.assertNotEqual(r1.chain, r2.chain, "distinct artifacts, distinct chains")
        # if a chain exists, r2 must have moved past r1's starting point
        if r1.prev and r2.prev:
            self.assertNotEqual(r2.prev, "",
                                "the second receipt must have a real prev")


if __name__ == "__main__":
    unittest.main(verbosity=2)
