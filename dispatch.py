#!/usr/bin/env python
"""æææ:///dispatch — Command Prompt AI's primitive, in Python.

Route note: the address is lowercase ``æææ:///dispatch``. In the resolver's
``resolveNavigation`` the lookup is exact -> partial -> raw-path fallback, so a
capitalised ``/Dispatch`` silently degrades into navigation. The brand is
"Command Prompt AI"; the route is lowercase ``dispatch``.

Two halves, deliberately separate, mirroring the resolver contract in
C:/æ/site/aaa-resolver.js where ``resolveASK`` returns typed intent
``{type:'api', endpoint:'/api/ask', data:{...}}`` and never performs I/O:

  resolve_dispatch() -> typed intent. Touches nothing.
  Dispatcher.run()   -> executes ONLY allowlisted commands.

Why Python: this is composition and orchestration, not VS Code UI. The
extension host owns in-workbench ``executeCommand``; anything reachable from
outside is second-tier, so this module says so instead of pretending otherwise.

Sovereign by construction: stdlib only, local only, no cloud, no shell=True.
Windows note: .cmd cannot be spawned directly (EINVAL) — routed via cmd.exe /c.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

CODE_CLI = r"C:\Users\yaelm\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

DEFAULT_ROOTS: tuple[Path, ...] = (Path("C:/æ"), Path("C:/Users/yaelm/AppData/Local/hermes"))
MAX_OUTPUT_CHARS = 8000


@dataclass(frozen=True)
class Spec:
    """A single allowlisted command."""

    argv: tuple[str, ...]
    passthrough: bool = False      # caller may append args
    paths: bool = False            # appended args are filesystem paths to validate
    timeout: float = 20.0
    cwd: str | None = None
    note: str = ""


ALLOWED: dict[str, dict[str, Spec]] = {
    # read-only OS facts; deliberately narrow, deliberate least privilege
    "win": {
        "whoami": Spec(("whoami",), timeout=10),
        "hostname": Spec(("hostname",), timeout=10),
        "list_processes": Spec(("tasklist",), timeout=15),
    },
    # the exact CLI surface we have already verified end-to-end
    "vscode": {
        "list_extensions": Spec((CODE_CLI, "--list-extensions"), timeout=30),
        "goto": Spec((CODE_CLI, "--goto"), passthrough=True, paths=True, note="file:line:col"),
        "diff": Spec((CODE_CLI, "--diff"), passthrough=True, paths=True, note="two paths"),
        "open": Spec((CODE_CLI, "--reuse-window"), passthrough=True, paths=True),
        "new_window": Spec((CODE_CLI, "--new-window"), passthrough=True, paths=True),
        "add_folder": Spec((CODE_CLI, "--add"), passthrough=True, paths=True),
    },
}

REFUSALS: dict[str, str] = {
    "workbench": (
        "In-workbench executeCommand is owned by the extension host and is NOT "
        "reachable from an external process. Refusing to fake it."
    ),
}


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def resolve_dispatch(args: Sequence[str]) -> dict[str, Any]:
    """Typed intent only — no I/O. Mirrors the resolver's shape."""
    surface, command, rest = (list(args) + ["", "", ""])[:3] if args else ["", "", []]
    rest = list(args[2:]) if len(args) > 2 else []
    return {
        "type": "api",
        "endpoint": "/api/dispatch",
        "data": {"surface": surface, "command": command, "args": rest},
    }


def _within_roots(path: str, roots: Iterable[Path]) -> bool:
    try:
        p = Path(path).resolve()
    except OSError:
        return False
    for root in roots:
        try:
            p.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


@dataclass
class Dispatcher:
    roots: tuple[Path, ...] = DEFAULT_ROOTS
    chain: list[dict[str, Any]] = field(default_factory=list)

    def allowed(self) -> dict[str, list[str]]:
        return {surface: sorted(cmds) for surface, cmds in ALLOWED.items()}

    def available_surfaces(self) -> list[str]:
        return sorted(set(ALLOWED) | set(REFUSALS))

    def _receipt(self, payload: dict[str, Any]) -> dict[str, Any]:
        prev = self.chain[-1]["hash"] if self.chain else "genesis"
        body = {"prevHash": prev, **payload}
        body["hash"] = hashlib.sha256(_canon(body).encode("utf-8")).hexdigest()
        self.chain.append(body)
        return body

    def run(self, surface: str, command: str, args: Sequence[str] | None = None) -> dict[str, Any]:
        args = list(args or [])
        base = {"surface": surface, "command": command, "args": args}

        if surface in REFUSALS:
            return {**base, "ok": False, "refused": REFUSALS[surface]}

        spec = ALLOWED.get(surface, {}).get(command)
        if spec is None:
            known = sorted(ALLOWED.get(surface, {}))
            return {
                **base,
                "ok": False,
                "refused": f"not allowlisted for surface '{surface}'",
                "allowed": known or self.available_surfaces(),
                "note": "least-privilege allowlist — add explicitly, never widen by default",
            }

        if args and not spec.passthrough:
            return {**base, "ok": False, "refused": f"'{command}' accepts no arguments"}

        if spec.paths:
            bad = [a for a in args if "/" in a or "\\" in a or ":" in a
                   and not _within_roots(a.split(":")[0] if spec is ALLOWED["vscode"]["goto"] else a, self.roots)]
            bad = [a for a in args if _looks_like_path(a) and not _within_roots(_strip_colon(a), self.roots)]
            if bad:
                return {**base, "ok": False, "refused": f"path outside allowed roots: {bad}",
                        "roots": [str(r) for r in self.roots]}

        argv = list(spec.argv) + args
        if str(argv[0]).lower().endswith(".cmd"):
            argv = ["cmd.exe", "/c", *argv]

        try:
            proc = subprocess.run(
                argv, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=spec.timeout, cwd=spec.cwd, shell=False,
            )
            stdout, stderr = proc.stdout, proc.stderr
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            return {**base, "ok": False, "refused": f"timeout after {spec.timeout}s"}
        except OSError as exc:
            return {**base, "ok": False, "refused": f"spawn failed: {exc}"}

        truncated = len(stdout) > MAX_OUTPUT_CHARS
        receipt = self._receipt({**base, "rc": rc, "stdout_sha256":
                                 hashlib.sha256(stdout.encode("utf-8")).hexdigest()})
        return {
            **base,
            "ok": rc == 0,
            "rc": rc,
            "stdout": stdout[:MAX_OUTPUT_CHARS],
            "stderr": stderr[:MAX_OUTPUT_CHARS],
            "truncated": truncated,
            "receipt": receipt,
        }


def _looks_like_path(value: str) -> bool:
    return "/" in value or "\\" in value or (len(value) > 1 and value[1] == ":")


def _strip_colon(value: str) -> str:
    return value.split(":")[0] if _looks_like_path(value) else value


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        print("usage: dispatch.py list | resolve <surface> <command> [args] | "
              "run <surface> <command> [args]")
        return 0

    cmd, *rest = argv
    disp = Dispatcher()

    if cmd == "list":
        print(json.dumps({"surfaces": disp.available_surfaces(),
                          "allowed": disp.allowed(),
                          "refusals": sorted(REFUSALS)}, indent=2))
        return 0

    if cmd == "resolve":
        print(json.dumps(resolve_dispatch(rest), indent=2))
        return 0

    if cmd == "run":
        if len(rest) < 2:
            print("usage: dispatch.py run <surface> <command> [args]", file=sys.stderr)
            return 2
        surface, command, *args = rest
        out = disp.run(surface, command, args)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    print(f"unknown subcommand: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
