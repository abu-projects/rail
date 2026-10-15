// Negotiate generated Markdown only for public HTML pages. Browser HTML stays the default.
function quality(accept, type, wildcards = true) {
  const entries = accept.split(',').map(item => item.trim().split(';'));
  const entry = entries.find(parts => parts[0].toLowerCase() === type)
    || (wildcards && (entries.find(parts => parts[0].toLowerCase() === type.split('/')[0] + '/*')
      || entries.find(parts => parts[0] === '*/*')));
  if (!entry) return 0;
  const q = entry.slice(1).find(part => part.trim().startsWith('q='));
  const value = q ? Number(q.trim().slice(2)) : 1;
  return Number.isFinite(value) && value >= 0 && value <= 1 ? value : 0;
}

export async function onRequest({ request, next, env }) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\.html$/, '').replace(/\/index$/, '').replace(/\/$/, '') || '/';
  const pages = ['/', '/modelle', '/werkstatt', '/ueber-mich', '/kontakt', '/impressum', '/datenschutz',
    '/en', '/en/models', '/en/workshop', '/en/about', '/en/contact', '/en/legal-notice', '/en/privacy'];
  if (!['GET', 'HEAD'].includes(request.method) || !pages.includes(path)) return next();
  const accept = request.headers.get('Accept') || '';
  if (quality(accept, 'text/markdown', false) > 0 && quality(accept, 'text/markdown', false) >= quality(accept, 'text/html')) {
    const file = path === '/' ? '/index' : path === '/en' ? '/en/index' : path;
    url.pathname = '/agent/pages' + file + '.md';
    url.search = '';
    const asset = await env.ASSETS.fetch(new Request(url, { method: request.method }));
    if (!asset.ok) return asset;
    const headers = new Headers(asset.headers);
    headers.set('Content-Type', 'text/markdown; charset=utf-8');
    headers.set('Vary', 'Accept');
    headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
    headers.set('Content-Location', url.pathname);
    return new Response(request.method === 'HEAD' ? null : asset.body, { headers });
  }
  const response = await next();
  const headers = new Headers(response.headers);
  const vary = headers.get('Vary');
  headers.set('Vary', vary ? vary + ', Accept' : 'Accept');
  return new Response(response.body, { status: response.status, headers });
}
