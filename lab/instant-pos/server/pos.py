#!/usr/bin/env python3
"""PrivateClient💸 · pc://pos server Witness (stdlib only).
Append-only, hash-chained receipts per shop. Paper money: no funds move here.
Agents may prepare; checkout.pay / socio.grant must come from a human (by != 'agent')."""
import json, hashlib, os, re, time, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
DATA = os.environ.get('PCPOS_DATA', '/var/lib/pcpos')
ALLOWED = {'checkout.create', 'checkout.pay', 'refused', 'socio.grant'}
HUMAN_ONLY = {'checkout.pay', 'socio.grant'}
SHOP = re.compile(r'^instant-pos/[a-z0-9-]{1,40}$')
lock = threading.Lock()
def path(shop): return os.path.join(DATA, shop.split('/')[1] + '.jsonl')
def read(shop):
    try:
        with open(path(shop)) as f: return [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError: return []
def h(body): return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
def verify(chain):
    prev = 'GENESIS'
    for r in chain:
        b = {k: v for k, v in r.items() if k != 'hash'}
        if b.get('prev') != prev or h(b) != r.get('hash'): return False
        prev = r['hash']
    return True
class H(BaseHTTPRequestHandler):
    server_version = 'pcpos/0.1'
    def log_message(self, *a): pass
    def send(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith('/pos/api/health'): return self.send(200, {'ok': True, 'service': 'pc://pos', 'money': 'paper'})
        if self.path.startswith('/pos/api/chain'):
            from urllib.parse import urlparse, parse_qs
            shop = (parse_qs(urlparse(self.path).query).get('shop') or [''])[0]
            if not SHOP.match(shop): return self.send(400, {'error': 'bad shop'})
            c = read(shop); return self.send(200, {'shop': shop, 'count': len(c), 'intact': verify(c), 'tail': c[-20:]})
        self.send(404, {'error': 'not found'})
    def do_POST(self):
        if self.path != '/pos/api/witness': return self.send(404, {'error': 'not found'})
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > 8192: return self.send(413, {'error': 'size'})
        try: req = json.loads(self.rfile.read(n))
        except Exception: return self.send(400, {'error': 'json'})
        shop, ev = req.get('shop', ''), req.get('ev') or {}
        if not SHOP.match(shop) or not isinstance(ev, dict): return self.send(400, {'error': 'bad request'})
        t = ev.get('type')
        if t not in ALLOWED: t, ev = 'refused', {'action': str(t)[:40], 'reason': 'unknown_event (default deny)'}
        elif t in HUMAN_ONLY and ev.get('by') == 'agent': ev = {'action': t, 'reason': f'{t} is human_only'}; t = 'refused'
        ev = {k: v for k, v in ev.items() if k not in ('hash', 'prev', 'server_at', 'type')}
        with lock:
            c = read(shop); prev = c[-1]['hash'] if c else 'GENESIS'
            body = {'type': t, **ev, 'shop': shop, 'server_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'prev': prev}
            rec = {**body, 'hash': h(body)}
            with open(path(shop), 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        self.send(200, {'ok': True, 'hash': rec['hash'], 'type': t, 'count': len(c) + 1})
if __name__ == '__main__':
    os.makedirs(DATA, exist_ok=True)
    ThreadingHTTPServer(('127.0.0.1', 8790), H).serve_forever()
