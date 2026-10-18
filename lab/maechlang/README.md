# mæchlæng · LAB

æ authority, written as Mech state machines, **running live on the real Mech runtime**. LAB only, noindex.

- Base language: [Mech](https://mech-lang.org) by Corey Montella, Apache-2.0, beta. mæchlæng is not affiliated with the Mech project.
- `authority.mec`: the æ0–æ3 authority axis as `#Authority`. **Runs** on Mech (wasm, Version 0.3.5): `:Context → :Evidence → :Granted`, guard `pk && wr`, otherwise `:Waiting ⇒ :evidence`.
- `face.mec`: Asimov face moods (same rules as Robot ae-face/ae/face.py). **Runs** on Mech 0.3.5.
- `face-v2.mec`: extended face draft. Still a sketch, not yet run.
- `index.html`: reactive page. Every input change re-runs the whole `.mec` program in Mech, highlights the active branch and appends a Witness SHA-256 receipt. Optional ▶ trace replay.
- `runtime/`: vendored Mech wasm runtime (unmodified, with LICENSE + NOTICE) and `maech-run.js` (our bridge). No CDN.
- `test.mjs`: `node test.mjs` runs all 208 input combinations on the real runtime and checks Mech == JS mirror and no æ2/æ3 without `pk && wr`.
- Rule inherited from Mech: kebab-case, no underscores (`agentic-environments`). Learned by running it: `--` comments go on their own line (a trailing comment on a `├ … → …` arm breaks the 0.3.5 parser).
- Sources: https://xn--l-3fa.net/mech-lang · https://docs.mech-lang.org/guides/mech-in-fifteen-minutes.html · https://github.com/mech-lang/mech

## Lineage

- 2026-10-17: guard explícito pk && wr en `#Authority` (`:Evidence(r, pk, wr)`; sin passkey + Witness, espera).
- 2026-10-18: "mæchlæng no es estático!" · `authority.mec` y `face.mec` reescritos en la sintaxis que acepta el runtime real (Mech wasm, Version 0.3.5) y ejecutados de verdad; la espera pasa a ser el estado final `:Waiting(r) ⇒ :evidence`. La página deja el flujo de pasos: es reactiva (Δ input → Δ estado), recibo Witness por cambio, ▶ trace opcional. Runtime vendorizado en `runtime/` sin CDN.
