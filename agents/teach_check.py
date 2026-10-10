#!/usr/bin/env python3
"""
teach_check.py — is every agent actually taught to use the chain?

TEACHING IS NOT A SKILL FILE
----------------------------
A skill only loads when its trigger matches. That is not teaching — it is
documentation that hopes to be found. A fleet learns through surfaces it is
FORCED to read:

    1. AGENTS.md              auto-loaded into every agent in C:\\æ
    2. kænbæn system-map      "every agent reads this before acting"
    3. capability-contracts   "what each agent can do — read before dispatching"

If the chain is not in those three, an agent can work a whole session without
knowing it exists. This script checks that it IS, and reports exactly which
surface has drifted.

It also checks the inverse: that the surfaces do not point at things that no
longer exist. A stale instruction is worse than a missing one — it sends an
agent confidently to a dead end.

USAGE
    python teach_check.py            check every surface, exit 1 if any is stale
    python teach_check.py --json     machine-readable
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

BASE = pathlib.Path(os.environ.get("AE_BASE", r"C:\æ"))
AGENTS_MD = BASE / "AGENTS.md"
K_BASE = pathlib.Path(os.environ.get("KAENBAEN_BASE", str(BASE / "kænbæn")))
SYS_MAP = K_BASE / "system-map.json"
SOUL_MD = pathlib.Path(os.environ.get("HERMES_HOME",
    str(pathlib.Path.home() / "AppData" / "Local" / "hermes"))) / "SOUL.md"
CONTRACTS = K_BASE / "capability-contracts.json"

# What a taught agent must be able to find, and where it must be findable.
REQUIRED_TERMS = {
    "AGENTS.md": ["væult", "væult://chain", "kanban_push.py", "agent_pledge.py"],
    "system-map": ["vaeult-chain"],
    "capability-contracts": ["vaeult_chain"],
    # SOUL.md is loaded from HERMES_HOME and is CWD-INDEPENDENT — the only
    # context surface that reaches an agent no matter where it runs.
    "SOUL.md": ["væult_chain.py", "Claim before you act", "Never move a secret"],
}

# A subagent is built with skip_context_files=True, so it inherits neither
# SOUL.md nor AGENTS.md. Its rules must live in the child prompt itself.
DELEGATE_PROMPT = pathlib.Path(
    os.environ.get("DELEGATE_TOOL", r"C:\æ\hermes-fork\tools\delegate_tool.py"))
SUBAGENT_TERMS = ["CLAIM BEFORE YOU ACT", "VERIFY BEFORE YOU CLAIM",
                  "NEVER MOVE A SECRET", "væult_chain.py"]


def _read_text(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def _read_json(p: pathlib.Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def check() -> dict:
    results = []

    # 1. AGENTS.md — the highest-reach surface
    md = _read_text(AGENTS_MD)
    missing = [t for t in REQUIRED_TERMS["AGENTS.md"] if t not in md]
    results.append({
        "surface": "AGENTS.md", "path": str(AGENTS_MD),
        "exists": AGENTS_MD.exists(), "reach": "every agent in C:\\æ (auto-loaded)",
        "required": REQUIRED_TERMS["AGENTS.md"], "missing": missing,
        "ok": AGENTS_MD.exists() and not missing,
    })

    # 2. system-map — "every agent reads this before acting"
    smap = _read_json(SYS_MAP)
    surfaces = smap.get("surfaces", {})
    missing = [t for t in REQUIRED_TERMS["system-map"] if t not in surfaces]
    results.append({
        "surface": "kænbæn system-map", "path": str(SYS_MAP),
        "exists": SYS_MAP.exists(), "reach": "every agent reads this before acting",
        "required": REQUIRED_TERMS["system-map"], "missing": missing,
        "ok": SYS_MAP.exists() and not missing,
    })

    # 3. capability-contracts — what each agent can do
    con = _read_json(CONTRACTS)
    agents = con.get("agents", {})
    # an agent may be registered under its canonical name with aliases; the
    # chain is present if ANY of them resolves.
    known = set(agents.keys())
    for _n, _a in agents.items():
        known.update(_a.get("aliases", []))
    missing = [t for t in REQUIRED_TERMS["capability-contracts"] if t not in known]
    results.append({
        "surface": "capability-contracts", "path": str(CONTRACTS),
        "exists": CONTRACTS.exists(), "reach": "read before dispatching",
        "required": REQUIRED_TERMS["capability-contracts"], "missing": missing,
        "ok": CONTRACTS.exists() and not missing,
    })

    # 3b. SOUL.md — the ONLY cwd-independent surface. AGENTS.md is anchored to
    # the working directory and only walks DOWN, so an agent running in
    # C:\æ\agents or C:\Users\yaelm gets nothing from it.
    soul = _read_text(SOUL_MD)
    missing = [x for x in REQUIRED_TERMS["SOUL.md"] if x not in soul]
    results.append({
        "surface": "SOUL.md", "path": str(SOUL_MD),
        "exists": SOUL_MD.exists(), "reach": "every agent, ANY cwd (HERMES_HOME)",
        "required": REQUIRED_TERMS["SOUL.md"], "missing": missing,
        "ok": SOUL_MD.exists() and not missing,
    })

    # 3c. the subagent prompt — children skip context files entirely
    dp = _read_text(DELEGATE_PROMPT)
    missing = [x for x in SUBAGENT_TERMS if x not in dp]
    results.append({
        "surface": "subagent prompt", "path": str(DELEGATE_PROMPT),
        "exists": DELEGATE_PROMPT.exists(),
        "reach": "every delegated child (skip_context_files=True)",
        "required": SUBAGENT_TERMS, "missing": missing,
        "ok": DELEGATE_PROMPT.exists() and not missing,
    })

    # 3d. THE REGISTRY MUST BE TRUE (E6). Every registered path resolves, and
    # every `cannot` is in the `cannot` list — not stuffed into `can`.
    # An agent contract that lies about itself is the first thing to fix.
    reg_bad = []
    for name, a in agents.items():
        if a.get("status") == "scratch":
            continue
        for pth in [a.get("path", "")] + list(a.get("also", [])):
            if pth and not pathlib.Path(pth).exists():
                reg_bad.append(f"{name}: dead path {pth}")
        stuffed = [x for x in a.get("can", []) if str(x).startswith("cannot:")]
        if stuffed:
            reg_bad.append(f"{name}: {len(stuffed)} cannot(s) stuffed into can")
    results.append({
        "surface": "registry is true", "path": str(CONTRACTS),
        "exists": CONTRACTS.exists(), "reach": "an agent contract that lies about itself",
        "required": ["every path resolves", "cannots live in cannot"],
        "missing": reg_bad, "ok": not reg_bad,
    })

    # 3e. RUNE PATHS MUST RESOLVE. github.io does not serve raw UTF-8 in URLs,
    # so a rune-named artifact is unreachable without an ASCII alias. This cost
    # a cycle four times; now it is checked instead of remembered.
    try:
        import ascii_alias as aa
        gp = pathlib.Path(os.environ.get("GITHUB_PAGES", r"C:\æ\github-pages"))
        rune_paths = aa.scan(gp)
        unaliased = [str(i["path"].relative_to(gp)) for i in rune_paths
                     if not i["alias_exists"]]
    except Exception as e:
        unaliased = [f"could not scan: {type(e).__name__}"]
    results.append({
        "surface": "rune paths resolve", "path": "github-pages",
        "exists": True, "reach": "a rune path 404s on github.io without an alias",
        "required": ["every rune path has an ASCII alias"],
        "missing": unaliased, "ok": not unaliased,
    })

    # 4. INVERSE CHECK — do the surfaces point at files that exist?
    # A stale instruction is worse than a missing one.
    dead = []
    chain = BASE / "agents" / "væult_chain.py"
    if "væult_chain.py" in md and not chain.exists():
        dead.append({"referenced": str(chain), "in": "AGENTS.md"})
    for name, rel in (("kanban_push.py", "agents/kanban_push.py"),
                      ("agent_pledge.py", "agents/agent_pledge.py")):
        if name in md and not (BASE / rel).exists():
            dead.append({"referenced": str(BASE / rel), "in": "AGENTS.md"})
    if "vaeult-chain" in surfaces:
        m = surfaces["vaeult-chain"].get("cli", "")
        p = m.split("python", 1)[-1].strip() if "python" in m else ""
        if p and not pathlib.Path(p).exists():
            dead.append({"referenced": p, "in": "system-map"})
    results.append({
        "surface": "pointers resolve", "path": "-",
        "exists": True, "reach": "a stale instruction sends an agent to a dead end",
        "required": ["every referenced path exists"], "missing": [d["referenced"] for d in dead],
        "ok": not dead, "dead": dead,
    })

    ok = all(r["ok"] for r in results)
    return {"ok": ok, "surfaces": results,
            "taught": sum(1 for r in results if r["ok"]), "total": len(results)}


def main(argv):
    ap = argparse.ArgumentParser(description="is every agent taught to use the chain?")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])

    r = check()
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0 if r["ok"] else 1

    print(f"TEACHING CHECK — {r['taught']}/{r['total']} surfaces carry the chain\n")
    for s in r["surfaces"]:
        mark = "✓" if s["ok"] else "✗"
        print(f"  {mark} {s['surface']}")
        print(f"      reach: {s['reach']}")
        if s["missing"]:
            print(f"      MISSING: {', '.join(s['missing'])}")
        if s.get("dead"):
            for d in s["dead"]:
                print(f"      DEAD POINTER: {d['referenced']} (referenced in {d['in']})")
    if not r["ok"]:
        print("\n  An agent can work a whole session without knowing the chain exists.")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
