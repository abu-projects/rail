import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { onRequest as mcp } from '../functions/mcp.js';
import { onRequest as middleware } from '../functions/_middleware.js';
import { onRequest as publicCatalog } from '../functions/api/catalog.js';

const catalog = JSON.parse(await readFile(new URL('../agent/catalog.json', import.meta.url), 'utf8'));
const rpc = (method, params, options = {}) => mcp({ request: new Request('https://railcycles.ch/mcp', {
  method: 'POST', headers: { 'Content-Type': 'application/json', ...options.headers },
  body: JSON.stringify({ jsonrpc: '2.0', ...(options.notification ? {} : { id: 1 }), method, params })
}) });

test('a native MCP client initializes, lists and reads the published catalog', async () => {
  const initialized = await (await rpc('initialize', { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'test-client', version: '1' } })).json();
  assert.equal(initialized.result.protocolVersion, '2025-11-25');
  assert.equal((await rpc('notifications/initialized', {}, { notification: true })).status, 202);
  const list = await (await rpc('tools/list')).json();
  assert.deepEqual(list.result.tools.map(tool => tool.name), ['get_rail_catalog']);
  assert.equal(list.result.tools[0].annotations.readOnlyHint, true);
  const response = await (await rpc('tools/call', { name: 'get_rail_catalog', arguments: {} })).json();
  assert.deepEqual(JSON.parse(response.result.content[0].text), catalog);
  const api = await publicCatalog({ request: new Request('https://railcycles.ch/api/catalog') });
  assert.deepEqual(await api.json(), catalog);
  assert.equal(api.headers.get('Access-Control-Allow-Origin'), '*');
});

test('MCP rejects external origins, unsupported versions and undeclared actions', async () => {
  assert.equal((await rpc('tools/list', {}, { headers: { Origin: 'https://external.example' } })).status, 403);
  assert.equal((await rpc('tools/list', {}, { headers: { 'MCP-Protocol-Version': 'unsupported' } })).status, 400);
  for (const params of [{ name: 'send_contact', arguments: {} }, { name: 'get_rail_catalog', arguments: { email: 'rider@example.com' } }]) {
    assert.equal((await (await rpc('tools/call', params)).json()).error.code, -32602);
  }
  assert.equal((await mcp({ request: new Request('https://railcycles.ch/mcp') })).status, 405);
});

test('Markdown negotiation preserves discovery and browser HTML preference', async () => {
  const discovery = '</.well-known/api-catalog>; rel="api-catalog"';
  for (const [accept, markdown] of [
    ['text/markdown', true], ['text/markdown;q=.1, */*;q=1', false],
    ['text/markdown;q=0, text/html', false], ['text/html, */*;q=.8', false]
  ]) {
    const response = await middleware({
      request: new Request('https://railcycles.ch/en/index.html', { headers: { Accept: accept } }),
      env: { ASSETS: { async fetch(request) {
        return new Response(await readFile(new URL('../dist' + new URL(request.url).pathname, import.meta.url)),
          { headers: { Link: discovery } });
      } } },
      next: async () => new Response('<html>RAIL</html>', { headers: { 'Content-Type': 'text/html', Link: discovery } })
    });
    assert.ok(response.headers.get('Vary').includes('Accept'));
    assert.equal(response.headers.get('Link'), discovery);
    assert.equal(response.headers.get('Content-Type').startsWith('text/markdown'), markdown);
    assert.ok((await response.text()).includes(markdown ? 'Source: https://railcycles.ch/en/' : '<html>'));
  }
});

test('browser assistants can read the same catalog through the declared WebMCP tool', async () => {
  const source = (await readFile(new URL('../home.js', import.meta.url), 'utf8')).split('// Expose the public catalog')[1];
  let tool;
  vm.runInNewContext(source.slice(source.indexOf('(() =>')), {
    document: { modelContext: { registerTool(value) { tool = value; } } }, navigator: {},
    fetch: async () => Response.json(catalog)
  });
  assert.equal(tool.name, 'get_rail_catalog');
  const result = await tool.execute({});
  assert.deepEqual(JSON.parse(result.content[0].text), catalog);
});
