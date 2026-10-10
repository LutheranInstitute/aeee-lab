# Diagnóstico de Servidores — 2026-10-08

> Verificado con probes propios (socket + HTTP + SSH). Los outputs de referencia
> estaban corruptos (loops); este documento es ground truth.

## 1. File Organization (hecho, no borrado)

Commit `09782fa` en `C:\æ` (branch master). Solo `.gitignore` staged.

| Movido | Desde | Hacia |
|---|---|---|
| 11 archivos `scratch-*` | raíz | `scratch/` |
| 5 `qc64*.txt` | raíz | `qc64_tmp/` |
| `rustup-init.exe`, `vs_buildtools.exe` | raíz | `_installers/` |
| `curriculo-threejs-agentic.md` | raíz | `threejs-curriculum/` |

`.gitignore` += `scratch/`, `_installers/`.
Limpiado: `.git/index.lock` stale (edad ~13 h, sin git corriendo).
Quedan en raíz (tracked o secreto): `.gitignore`, `AGENTS.md`, `probe_qc64.py`,
`vscode_wiki.html`, `ice40` (28 B), `secrets.json` (SECRETO — nunca se mueve), `nul` (0 B).

## 2. Matriz de estado (PROVEN)

### Victus (local)
| Puerto | Servicio | Estado |
|---|---|---|
| :3051 | `qr_server.py` (QR keys/contracts) | ✅ OPEN · `/api/status` **200** |
| :3052 | `cri_server.py` (Consumer Redline Index) | ✅ OPEN · `/api/status` **200** |
| :3050 | `rtx_leaf.py` (RTX hands) | ❌ ConnectionRefused |
| :8080 | mirror público (esperado) | ❌ ConnectionRefused |
| :8123 | http.server (scenes) | ❌ (no requerido ahora) |

### Droplet `129.212.180.252`
| Puerto | Estado |
|---|---|
| :22 SSH | ✅ OPEN |
| :80 nginx | ✅ OPEN — pero `/` → **502 Bad Gateway** |
| :443 TLS | ❌ ConnectionRefused (sin listener) |
| :3000 broker `vps_node.py` | ✅ OPEN · `/` → `{"vps":"up"}` **200** |
| :3050 (tunnel `-R`) | ⚠️ loopback-only, upstream muerto |
| :8080 (upstream nginx) | ❌ TimeoutError — **NADIE escucha** |

### Público (truth surface)
| URL | Estado |
|---|---|
| `myaelmendez.github.io/aipodcast_me/cri_surface.html` | ✅ 200 |
| `myaelmendez.github.io/aipodcast_me/qr_keys.html` | ✅ 200 |
| `http://llm.store/` | ✅ 200 |

## 3. Causas raíz

**RC1 — nginx `/` → `127.0.0.1:8080` muerto → 502.**
`/etc/nginx/sites-enabled/llm.store` hace `proxy_pass http://127.0.0.1:8080`
pero `ss -ltnp` en el droplet NO muestra nada en 8080. El upstream que debería
llegar por túnel reverso (`-R 8080:127.0.0.1:8080` desde Victus) no existe.
El único túnel activo es `-R 3050` (rtx leaf). **Mismatch 8080 vs 3050.**

**RC2 — `aevps.service` FAILED (desde Oct 5, hace 3 días).**
`IndentationError: expected an indented block after 'if' statement on line 287`.
El archivo YA compila (`py_compile` → YES) — fue corregido. Pero systemd quedó en
`start-limit-hit` (6 reintentos rápidos). Un **instancia manual** (pid 2365508,
arrancada Oct 8 14:33) es la que hoy sirve :3000. Un `systemctl restart aevps`
fallaría: puerto :3000 ya ocupado por la instancia manual.

**RC3 — sin TLS en :443.**
No hay Caddy ni listener TLS. `rtx.æææ.com` (skill deploy-surfaces) no responde.

**RC4 — rtx leaf muerto.**
`127.0.0.1:3050` en Victus → ConnectionRefused. El túnel del droplet apunta ahí,
así que el endpoint remoto queda vacío (`curl` → 000).

## 4. Correcciones

### ✅ RESUELTO (2026-10-08 15:08 UTC)
**aevps.service** — estaba `failed` (systemd en `start-limit-hit`, NRestarts=6); una
instancia manual (pid 2365508) enmascaraba el fallo sirviendo :3000.
Fix aplicado: `systemctl stop aevps; kill 2365508; systemctl reset-failed aevps;
systemctl start aevps` → ahora **active · enabled · NRestarts=0** (systemd pid 2377592).
`:3000 /` → 200, `/xrpc/ae.vps.audit` → 200.

### ⏳ PENDIENTE — droplet `/` 502
nginx `location / { proxy_pass http://127.0.0.1:8080 }` pero NADIE escucha :8080
en el droplet. Victus nginx SÍ está configurado para :8080 (`nginx -t` OK) pero
**no corre**, y el único túnel vivo es `-R 3050`, no `-R 8080`.

- **Opción A (stopgap):** droplet nginx `proxy_pass → :3000`. Mata el 502 al instante;
  `/` devuelve el JSON del broker, no una página.
- **Opción B (intención):** apuntar root de Victus nginx a `C:\æ\store`, correrlo en
  :8080, túnel `-R 8080:127.0.0.1:8080`. `/` sirve las superficies reales.

Nota: la superficie real del droplet (API/PDS) YA funciona (`:3000` + `/xrpc/` = 200).
El 502 solo afecta el root del vhost `llm.store`, y `llm.store` resuelve a otro host
(88.222.222.37) — solo afecta acceso por IP directa.

### Otras (sin cambio)
- **TLS :443:** levantar Caddy `rtx.æææ.com { reverse_proxy 127.0.0.1:3000 }`.
- **rtx leaf:** relanzar `rtx-bridge.sh` (leaf Victus:3050 + túnel).
