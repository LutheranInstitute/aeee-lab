# mæchlæng + HARK_PRO æ · unified · v1 (LAB · simulación)

Una sola página (index.html, sin CDN): **Hark Pro es el agente; mæchlæng es el lenguaje de su autoridad.**

> &gt;_ mæch: muchos agentes · un principal · el humano es root · Evidence ≠ Authority

## Qué contiene
1. **Hero** con descarga: hark.com/download, App Store (id6772362941), Google Play (com.hark.android), hark.com.
2. **#Authority en vivo**: un agente de `{"hark-pro", "hermes", "codex"}` pide æ0–æ3; la petición recorre `:Context → :Evidence → :Granted` con el guard `├ pk && wr → :Granted(r)` / `└ * → :Evidence(r, pk, wr)`. æ0/æ1 se conceden directo; æ2/æ3 solo con passkey de la persona principal (`yæl`) + recibo Witness. El recibo es SHA-256 real (`crypto.subtle`), encadenado desde `GENESIS`: `h(n) = sha256(h(n-1) + "|" + evento)`. La línea Mech activa se ilumina.
3. **#Face · Asimov en vivo**: reglas de ánimo de `lab/maechlang/face.mec` (hold > lost > tired > sleep > think > ready > work), regla ganadora iluminada; solo lectura, autoridad æ1.
4. **Demos como mæch**: ZACAPA.DAO (#Regla), DAOLLC.ai (#Propuesta · #Gobernanza), æsymov face v1 y v2.3 (#Cara), MathByte (#Byte, boceto nuevo), mæchlæng (#Authority con guard). Vista previa en iframe solo al tocar.
5. **Tu turno**: convierte una idea en un prompt para Hark que también pide su máquina de estados mæch. Todo local.
6. Principios, créditos y aviso.

## Notas
- **boceto · sketch, not yet run on a Mech runtime.** Los simuladores son JavaScript que imita los bocetos.
- Mech: https://mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng es un experimento del Instituto, sin afiliación con Mech.
- Sintaxis mæch: kebab-case, sin guiones bajos en identificadores (`"FAULT_DAMP"` aparece solo como texto: es el nombre del modo en el SDK del robot).
- noindex, toques ≥44px, inputs 16px, prefers-reduced-motion.
- Página independiente del Instituto Luterano Latinoamericano; no es un sitio oficial de Hark.

☕ Apoya al Instituto: https://buymeacoffee.com/daollc

## Linaje
- v0 (`lab/hark-pro/v0/`): portal de demos + bocetos mæch estáticos. Sin cambios.
- v1 (2026-10-17): unificado con `lab/maechlang/` (guard `pk && wr`): simuladores vivos #Authority + Witness y #Face, cada demo con su boceto mæch.
