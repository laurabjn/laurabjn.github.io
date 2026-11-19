import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const [chrome, url, sel, outDir, ...widths] = process.argv.slice(2);
const port = 9335;
const proc = spawn(chrome, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=${outDir}/profile3`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target; for (let i = 0; i < 50 && !target; i++) { try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === 'page'); } catch {} if (!target) await sleep(200); }
const ws = new WebSocket(target.webSocketDebuggerUrl); await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); let loaded = false;
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } if (m.method === 'Page.loadEventFired') loaded = true; });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Page.enable');
for (const w of widths.map(Number)) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 800 });
  loaded = false; await send('Page.navigate', { url }); for (let i = 0; i < 60 && !loaded; i++) await sleep(200);
  await evaluate(`(async () => { document.querySelectorAll('img').forEach(i => i.loading = 'eager'); await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); return true; })()`);
  await sleep(300);
  const r = await evaluate(`(() => { const b = document.querySelector('${sel}').getBoundingClientRect(); return { y: b.top + scrollY, h: b.height, ok: [...document.querySelectorAll('.thumb-img img')].map(i => i.naturalWidth > 0) }; })()`);
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: r.y, width: w, height: r.h, scale: 1 } });
  writeFileSync(`${outDir}/projets-${w}.png`, Buffer.from(shot.result.data, 'base64'));
  console.log(`projets-${w}.png`, w, 'x', Math.round(r.h), '| images chargées :', r.ok.join(','));
}
ws.close(); proc.kill(); process.exit(0);
