import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const [chrome, url, outDir] = process.argv.slice(2);
const port = 9333;
const proc = spawn(chrome, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`,
  `--user-data-dir=${outDir}/profile`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === 'page'); } catch {}
  if (!target) await sleep(200);
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const waiters = [];
ws.addEventListener('message', (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method) waiters.filter((w) => w.method === m.method).forEach((w) => { w.resolve(m); waiters.splice(waiters.indexOf(w), 1); });
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const once = (method) => new Promise((resolve) => waiters.push({ method, resolve }));
const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Page.enable');

const audit = `(() => {
  const vw = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).join('.') : '');
  const clippedBy = (el) => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { const r = p.getBoundingClientRect(); if (r.left >= -1 && r.right <= vw + 1) return true; } } return false; };
  const off = [], cut = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (!r.width || getComputedStyle(el).visibility === 'hidden') continue;
    if ((r.right > vw + 1 || r.left < -1) && !clippedBy(el)) off.push(name(el) + ' [' + Math.round(r.left) + ' → ' + Math.round(r.right) + ']');
    const cs = getComputedStyle(el);
    if (el.children.length === 0 && el.textContent.trim() && cs.overflow !== 'visible' && el.scrollWidth > el.clientWidth + 1 && cs.textOverflow !== 'ellipsis') cut.push(name(el) + ' "' + el.textContent.trim().slice(0, 30) + '"');
  }
  return { vw, sw, deborde: sw > vw, horsEcran: off.slice(0, 12), texteCoupe: cut.slice(0, 8) };
})()`;

const widths = [320, 375, 390, 768, 1024, 1440];
for (const w of widths) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 800 });
  const loaded = once('Page.loadEventFired');
  await send('Page.navigate', { url });
  await loaded; await evaluate('document.fonts.ready.then(() => true)'); await sleep(400);
  console.log(`\n=== ${w}px ===`, JSON.stringify(await evaluate(audit)));
  if ([375, 768, 1440].includes(w)) {
    const { cssContentSize } = (await send('Page.getLayoutMetrics')).result;
    const h = Math.ceil(cssContentSize.height);
    const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: w, height: h, scale: 1 } });
    writeFileSync(`${outDir}/w${w}.png`, Buffer.from(shot.result.data, 'base64'));
    console.log(`capture w${w}.png : ${w} x ${h}`);
  }
}
// Menu mobile ouvert
await send('Emulation.setDeviceMetricsOverride', { width: 375, height: 760, deviceScaleFactor: 1, mobile: true });
const l2 = once('Page.loadEventFired'); await send('Page.navigate', { url }); await l2;
await evaluate('document.fonts.ready.then(() => true)');
await evaluate("document.getElementById('nav-toggle').click(), true"); await sleep(300);
const m = await send('Page.captureScreenshot', { format: 'png' });
writeFileSync(`${outDir}/menu375.png`, Buffer.from(m.result.data, 'base64'));
console.log('capture menu375.png');
ws.close(); proc.kill();
process.exit(0);
