import catalog from './_catalog.js';

const versions = ['2025-11-25', '2025-06-18', '2025-03-26'];
const tool = { name: 'get_rail_catalog', description: 'Read the public RAIL bicycle models, specifications, CHF frame guide prices and bilingual page links. No enquiries or orders are submitted.',
  inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false } };

export async function onRequest({ request }) {
  const origin = request.headers.get('Origin');
  if (origin && origin !== new URL(request.url).origin) return new Response('Forbidden', { status: 403 });
  if (request.method !== 'POST') return new Response(null, { status: 405, headers: { Allow: 'POST' } });
  if (!request.headers.get('Content-Type')?.startsWith('application/json')) return new Response(null, { status: 415 });
  const version = request.headers.get('MCP-Protocol-Version');
  if (version && !versions.includes(version)) return new Response('Unsupported MCP version', { status: 400 });
  let message;
  const result = (id, value) => Response.json({ jsonrpc: '2.0', id, result: value }, { headers: { 'Cache-Control': 'no-store' } });
  const error = (id, code, text) => Response.json({ jsonrpc: '2.0', id, error: { code, message: text } }, { headers: { 'Cache-Control': 'no-store' } });
  try {
    const body = await request.text();
    if (new TextEncoder().encode(body).length > 8192) return new Response(null, { status: 413 });
    message = JSON.parse(body);
  } catch { return error(null, -32700, 'Parse error'); }
  if (!message || Array.isArray(message) || message.jsonrpc !== '2.0' || typeof message.method !== 'string') return error(null, -32600, 'Invalid request');
  const { id, method, params } = message;
  if (id === undefined) return new Response(null, { status: 202 });
  if (method === 'initialize') return result(id, { protocolVersion: versions.includes(params?.protocolVersion) ? params.protocolVersion : versions[0],
    capabilities: { tools: {} }, serverInfo: { name: 'ch.railcycles/catalog', version: '1.0.0' }, instructions: 'Public read-only bicycle information. Guide prices are not binding quotes. Contact Sam for custom geometry, availability and final pricing.' });
  if (method === 'ping') return result(id, {});
  if (method === 'tools/list') return result(id, { tools: [tool] });
  if (method === 'tools/call') {
    if (params?.name !== tool.name) return error(id, -32602, 'Unknown tool');
    if (params.arguments !== undefined && (!params.arguments || typeof params.arguments !== 'object' || Array.isArray(params.arguments) || Object.keys(params.arguments).length)) return error(id, -32602, 'This tool takes no arguments');
    return result(id, { content: [{ type: 'text', text: JSON.stringify(catalog) }] });
  }
  return error(id, -32601, 'Method not found');
}
