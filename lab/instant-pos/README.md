# Instant POS · æQR (LAB)

Name + menu → `ae.json` manifest + æQR + checkout. Open for business in about two minutes, with no card reader, app or terminal.

- **LinkedIn door (simulated):** anyone with a LinkedIn gets a shop. Sign in (name + email; the email stays in the session and never enters the æQR), and you become the shop's principal (`provenance.principal` = provider + sub + name). The real version is LinkedIn OIDC on auth.privateclient.ai with the secret server-side. LinkedIn is identity (æ0); real payouts still need processor onboarding.
- **Make mode:** type a name, type and menu (one line per item: `name price`), then press Generate. The æQR encodes a store URL that carries the manifest. The browser decodes the QR back (jsQR) and confirms the bytes are identical. The production gate is still cv2 + pyzbar agreeing.
- **Store mode (`?m=`):** the customer scans and sees the menu. The agent prepares the charge (`checkout.create`, æ0), and only the buyer can pay (`checkout.pay`, æ2, human_only, single use, expires after 120 s). Every act, refusals included, writes a SHA-256 chained Witness receipt.
- **Rail + trail:** in production a payment processor holds the funds and takes the platform fee. We never touch client money.

LAB only. Paper money. Not a payment processor. Fork freely. Preserve attribution. #OPENSOURCEWARE
