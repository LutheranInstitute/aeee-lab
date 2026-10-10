# teologia.ai · æ://

Plataforma soberana de devoción — 5 superficies æqr verificadas, cero servidores, cero llaves.

## Artefactos

| # | Artefacto | HTML | PDF | Badge æqr | Decode |
|---|---|---|---|---|---|
| 01 | Una manera sencilla de orar | 65 KB | 179 KB | ✅ | PASS |
| 02 | Catecismo Menor | 103 KB | 430 KB | ✅ | PASS |
| 03 | Enchiridion | 77 KB | 247 KB | ✅ | PASS |
| 04 | Catecismo Mayor | 86 KB | 306 KB | ✅ | PASS |
| — | Plataforma (index) | 67 KB | 137 KB | ✅ | PASS |

## Estructura

```
teologia/
├── index.html                    ← Plataforma 9:16 (Three.js, gold-on-void)
├── una-manera-sencilla-de-orar.html / .pdf
├── catecismo-menor.html / .pdf
├── catecismo-mayor.html / .pdf
├── enchiridion.html / .pdf
├── aeqr-badge-*.svg              ← Chips verificados (5)
├── *.aqr.json                    ← Receipts con payload/hash/issuer
├── platform-manifest.json        ← Agregado sobre los 5 artefactos
├── scripts/
│   ├── make_aqr.py               ← Badge æqr del panfleto de orar
│   ├── make_aqr_catecismo.py     ← Badge æqr del Catecismo Menor
│   ├── make_aqr_enchiridion.py   ← Badge æqr del Enchiridion
│   ├── make_aqr_mayor.py         ← Badge æqr del Catecismo Mayor
│   ├── make_aqr_platform.py      ← Badge æqr de plataforma (agregado)
│   ├── verify_pamphlet.py        ← Verificación del panfleto
│   ├── verify_catecismo.py       ← Verificación del Menor
│   ├── verify_enchiridion.py     ← Verificación del Enchiridion
│   ├── verify_mayor.py           ← Verificación del Mayor
│   ├── verify_platform.py        ← Verificación de plataforma
│   └── update_index_mayor.py     ← Actualización del index con 4ta tarjeta
├── wasm/
│   ├── Cargo.toml                ← Rust→WASM core (scaffold)
│   └── src/lib.rs                ← Artifact metadata, æqr payloads
└── vendor/
    ├── three.module.js           ← Three.js r186 (local, sin CDN)
    ├── three.core.js
    └── OrbitControls.js
```

## Pipeline æqr

Cada artefacto tiene su badge æqr generado desde una matriz real (librería `qrcode`) y verificado decodificándolo de vuelta (OpenCV). El hash se calcula sobre el texto canónico del artefacto — quitar el badge no cambia el hash, porque el badge es contenedor, no mensaje.

El badge de plataforma es un agregado: el hash cubre un manifiesto JSON con los SHA-256 reales de los 5 HTML en disco.

## Reproducibilidad

```bash
# Generar todos los badges æqr
python scripts/make_aqr.py
python scripts/make_aqr_catecismo.py
python scripts/make_aqr_enchiridion.py
python scripts/make_aqr_mayor.py
python scripts/make_aqr_platform.py

# Verificar todos los PDFs (badge æqr sobrevive al papel)
python scripts/verify_pamphlet.py
python scripts/verify_catecismo.py
python scripts/verify_enchiridion.py
python scripts/verify_mayor.py
python scripts/verify_platform.py
```

## Canon

- solo scriptura · solo fide · solo gratia
- un archivo · se copia · se pasa · no se pide permiso
- Truth over marketing: "when you tell the truth you don't have to remember anything."

## Issuer

☺://cc · æ:// namespace · sovereign operator of the æ:// namespace
