// node test.mjs · runs the vendored Mech runtime (runtime/) on authority.mec + face.mec for every input combo
import fs from 'fs'; import zlib from 'zlib'; import assert from 'assert'; import { createRequire } from 'module';
const D = new URL('.', import.meta.url).pathname;
const P = new Proxy(function () {}, { get: (t, k) => k === Symbol.toPrimitive ? () => '' : (k === 'then' ? undefined : P), apply: () => P, construct: () => P });
globalThis.window ??= P; globalThis.document ??= P;
const M = createRequire(import.meta.url)(D + 'runtime/maech-run.js');
assert.strictEqual(M.AUTH_SRC, fs.readFileSync(D + 'authority.mec', 'utf8'), 'embedded authority.mec drifted');
assert.strictEqual(M.FACE_SRC, fs.readFileSync(D + 'face.mec', 'utf8'), 'embedded face.mec drifted');
const mod = await import(D + 'runtime/mech_wasm.js');
mod.initSync({ module: zlib.gunzipSync(fs.readFileSync(D + 'runtime/mech_wasm_bg.wasm.gz')) });
const ver = M.useModule(mod); assert.ok(M.ready());
let n = 0, ms = 0;
for (const agent of M.AGENTS) for (const r of [0, 1, 2, 3]) for (const pk of [false, true]) for (const wr of [false, true]) {
  const x = M.run(M.withInputs(M.AUTH_SRC, M.authInputs(agent, r, pk, wr))); ms += x.ms;
  assert.ok(x.ok, 'mech error: ' + x.err);
  const p = M.parseAuth(x.out), j = M.authEval(r, pk, wr);
  assert.ok(p, 'unparsed: ' + x.out);
  assert.deepStrictEqual([p.state, p.hi, p.guard, p.known], [j.state, j.hi, j.guard, true], `auth ${agent} æ${r} pk${pk} wr${wr}`);
  if (r > 1 && !(pk && wr)) { assert.strictEqual(p.state, 'evidence', 'NO æ2/æ3 grant without pk&&wr'); assert.ok(!j.path.includes('ev-ok')); }
  if (r > 1 && pk && wr) assert.strictEqual(p.state, 'granted');
  if (r < 2) assert.strictEqual(p.state, 'granted');
  n++;
}
// truthy non-bool must not grant in the mirror; unknown agent is coerced to a known one
assert.strictEqual(M.authEval(3, 1, 1).state, 'evidence');
assert.strictEqual(M.authInputs('evil"; x := 1', 3, true, true).agent, '"hark-pro"');
// replay trace agrees with reactive eval
for (const r of [0, 1, 2, 3]) for (const pk of [false, true]) for (const wr of [false, true]) {
  let s = null, b = []; for (let i = 0; i < 4; i++) { const t = M.authStep(s, r, pk, wr); s = t.s; b.push(t.b); if (t.b === 'done' || t.b === 'ev-wait') break; }
  assert.strictEqual(s === 'gr' ? 'granted' : 'evidence', M.authEval(r, pk, wr).state);
}
for (const md of ['DAMP', 'STAND', 'MOVE', 'FAULT_DAMP']) for (const ar of [false, true]) for (const ft of [false, true]) for (const ag of [0.05, 0.9]) for (const sc of [0, 19, 20, 50, 100]) {
  const x = M.run(M.withInputs(M.FACE_SRC, M.faceInputs(md, ar, ft, ag, sc))); ms += x.ms;
  assert.ok(x.ok, 'mech error: ' + x.err);
  const m = M.parseFace(x.out); assert.strictEqual(m, M.faceEval(md, ar, ft, ag, sc).m, `face ${md} ${ar} ${ft} ${ag} ${sc}`); n++;
}
const f = (...a) => M.faceEval(...a).m;
assert.strictEqual(f('MOVE', true, true, 0.9, 5), 'hold'); assert.strictEqual(f('FAULT_DAMP', false, false, 0.05, 80), 'hold');
assert.strictEqual(f('MOVE', true, false, 0.9, 5), 'lost'); assert.strictEqual(f('MOVE', true, false, 0.05, 5), 'tired');
assert.strictEqual(f('DAMP', false, false, 0.05, 80), 'sleep'); assert.strictEqual(f('STAND', false, false, 0.05, 80), 'think');
assert.strictEqual(f('STAND', true, false, 0.05, 80), 'ready'); assert.strictEqual(f('MOVE', true, false, 0.05, 80), 'work');
// the unknown-mode arm runs in Mech too
const xu = M.run(M.withInputs(M.FACE_SRC, M.faceInputs('WALK', true, false, 0.05, 80))); assert.strictEqual(M.parseFace(xu.out), 'lost');
// ▶ demo tour: every step makes Mech choose its mood, and the tour covers all 7 moods
const AF = createRequire(import.meta.url)(D + 'runtime/aesymov-face.js');
assert.deepStrictEqual(AF.TOUR.map(s => s.m).sort(), [...AF.MOODS].sort(), 'tour must cover all 7 moods');
for (const s of AF.TOUR) { const v = s.v, ag = v.st ? 0.9 : 0.05;
  const x = M.run(M.withInputs(M.FACE_SRC, M.faceInputs(v.md, v.ar, v.ft, ag, v.sc))); ms += x.ms; n++;
  assert.strictEqual(M.parseFace(x.out), s.m, 'tour step ' + s.m); assert.ok(AF.FIL[s.m] && AF.POSTURE[s.m] && AF.ES[s.m]); }
assert.ok(/viewBox="40 6 160 252"/.test(AF.svg()), 'æsymov face svg');
console.log(`ALL TESTS PASS · real Mech runtime ${ver} · ${n} programs run · avg ${(ms / n).toFixed(1)} ms/run`);
