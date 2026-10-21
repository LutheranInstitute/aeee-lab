# Instant POS · æQR (LAB)

Name + menu → `ae.json` manifest + æQR + checkout. Open for business in about two minutes, with no card reader, app or terminal.

- **LinkedIn door (simulated):** anyone with a LinkedIn gets a shop. Sign in (name + email; the email stays in the session and never enters the æQR), and you become the shop's principal (`provenance.principal` = provider + sub + name). The real version is LinkedIn OIDC on auth.privateclient.ai with the secret server-side. LinkedIn is identity (æ0); real payouts still need processor onboarding.
- **Make mode:** type a name, type and menu (one line per item: `name price`), then press Generate. The æQR encodes a store URL that carries the manifest. The browser decodes the QR back (jsQR) and confirms the bytes are identical. The production gate is still cv2 + pyzbar agreeing.
- **Store mode (`?m=`):** the customer scans and sees the menu. The agent prepares the charge (`checkout.create`, æ0), and only the buyer can pay (`checkout.pay`, æ2, human_only, single use, expires after 120 s). Every act, refusals included, writes a SHA-256 chained Witness receipt.
- **v0.2 · agent-ready storefront (2026-10-21):**
  - Every shop embeds schema.org JSON-LD (`FoodEstablishment` → `Menu` → `MenuItem`/`Offer`) and its `ae.json` (`application/ae+json`), so any agent can read the menu without a protocol integration. A "Vista de agente" panel shows what agents see.
  - After a human approves, the receipt is also emitted shaped like an **ACP checkout session** and an **AP2 human-present payment mandate**, with the Witness hash as the user authorization. These are shaped like the protocols, not certified implementations.
  - Plan switch: æ0 free with a per-sale fee only, or æ1 at $19/mo. Both are suggestions, and the fee % is still undecided.
  - Directory: `registry.json` (`ae.network/0.1`). Publishing is human_only and opens a public issue labelled `instant-pos-shop`, which the steward approves.
- **Viewport (TV) mode (Yael 2026-10-21):** `?m=…&view=tv` turns any smart TV into a 16:9 menu board. The current item is highlighted, ads rotate (up to 6 lines entered in make mode), and the ordering æQR stays on screen. Make mode also gives a **Viewport æQR** for the screen. The TV only shows; ordering and payment always happen on the buyer's phone.
- **Socios en misión (Yael 2026-10-21):** the store's own partner program. The owner grants a socio æQR (`socio.grant`, human_only æ2; the agent's attempt is refused and recorded): name, commission % (default 10), expiry. The token's grant hash ties it to this store id. In the lab it's a simulated signature; in production the owner's passkey signs. On the socio's link the buyer sees the partner banner, the store ships and stays seller of record, and the checkout.pay receipt records `split` {store_usd, socio_usd, rate_pct, grant}. A tampered or expired token is refused, the sale goes ahead without commission, and the refusal is recorded. Sample: Iglesia Luterana (muestra) for L://Gospel_Bookstore in registry.json.
- **Rail + trail:** in production a payment processor holds the funds and takes the platform fee. We never touch client money.

LAB only. Paper money. Not a payment processor. Fork freely. Preserve attribution. #OPENSOURCEWARE
