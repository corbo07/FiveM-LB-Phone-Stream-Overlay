// Lokaler Server: empfängt Trigger von FiveM, schickt sie per SSE an die OBS-Browserquelle.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3981;
const clients = new Set();
let phoneOpen = false;

const send = (res, code, body, type = 'text/plain') => {
  res.writeHead(code, { 'Content-Type': type, 'Access-Control-Allow-Origin': '*' });
  res.end(body);
};

http.createServer((req, res) => {
  if (req.method === 'OPTIONS') return send(res, 204, '');

  if (req.url === '/toggle') {
    phoneOpen = !phoneOpen;
    for (const c of clients) c.write(`data: ${JSON.stringify({ open: phoneOpen })}\n\n`);
    console.log(new Date().toLocaleTimeString(), 'phone:togglephone ->', phoneOpen ? 'AN' : 'AUS');
    return send(res, 200, 'ok');
  }

  if (req.url.startsWith('/set')) {
    const open = new URL(req.url, 'http://x').searchParams.get('open') === '1';
    if (open !== phoneOpen) {
      phoneOpen = open;
      for (const c of clients) c.write(`data: ${JSON.stringify({ open: phoneOpen })}

`);
      console.log(new Date().toLocaleTimeString(), 'Telefon erkannt ->', phoneOpen ? 'AN' : 'AUS');
    }
    return send(res, 200, 'ok');
  }

  if (req.url === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    });
    res.write(`data: ${JSON.stringify({ open: phoneOpen })}\n\n`);
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  const file = req.url === '/' ? 'index.html' : path.basename(req.url.split('?')[0]);
  const full = path.join(__dirname, file);
  fs.readFile(full, (err, data) => {
    if (err) return send(res, 404, 'not found');
    const types = { '.html': 'text/html', '.png': 'image/png', '.css': 'text/css', '.js': 'text/javascript' };
    send(res, 200, data, types[path.extname(full)] || 'application/octet-stream');
  });
}).listen(PORT, '127.0.0.1', () => console.log(`Overlay: http://localhost:${PORT}  |  Trigger: http://localhost:${PORT}/toggle`));
