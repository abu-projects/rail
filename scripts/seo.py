"""Search metadata shared by both languages; URLs match Cloudflare's clean routes."""
from html import escape
import json
from xml.etree import ElementTree as ET

ORIGIN = 'https://railcycles.ch'
META = {
 'de': {
  'home': ('Handgefertigte Fahrräder aus der Zentralschweiz | RAIL Cycles', 'Handgefertigte Stahlrahmen von Sam in der Zentralschweiz. Entdecke RAIL Gravel-, Trail- und Enduro-Bikes sowie die Werkstatt hinter den vier Modellen.'),
  'models': ('Gravel-, Trail- und Enduro-Modelle | RAIL Cycles', 'Entdecke Truischjanid, Lopper, Muetterschwandeberg und Wichelsee: handgefertigte RAIL Stahlrahmen mit Geometrie, Federweg und Richtpreisen in CHF.'),
  'workshop': ('Rahmenbau & Werkstatt in der Zentralschweiz | RAIL Cycles', 'Einblick in Sams Werkstatt: handgefeilte Rohrverbindungen, WIG-Schweissen und die Fertigung der handgemachten RAIL Fahrradrahmen.'),
  'about': ('Sam – der Mensch hinter RAIL Cycles', 'Lerne Sam kennen, den Menschen hinter RAIL Cycles und den handgefertigten Fahrradrahmen aus der Zentralschweiz.'),
  'contact': ('Kontakt & Rahmenanfrage an Sam | RAIL Cycles', 'Sprich mit Sam über dein RAIL Bike. Frage einen Gravel-, Trail- oder Enduro-Rahmen an oder stelle eine allgemeine Frage über das Kontaktformular.'),
  'legal': ('Impressum | RAIL Cycles', 'Kontakt, Website-Verantwortlicher und Hinweise zum Urheberrecht der Fotografien von RAIL Cycles aus der Zentralschweiz.'),
  'privacy': ('Datenschutz | RAIL Cycles', 'Informationen von RAIL Cycles zum Datenschutz, zum Kontaktformular und zu deinen Anliegen bezüglich personenbezogener Daten.'),
 },
 'en': {
  'home': ('Handmade bicycles from Central Switzerland | RAIL Cycles', 'Handmade steel bicycle frames by Sam in Central Switzerland. Discover RAIL gravel, trail and enduro bikes and the workshop behind the four models.'),
  'models': ('Gravel, trail & enduro bike models | RAIL Cycles', 'Explore Truischjanid, Lopper, Muetterschwandeberg and Wichelsee: handmade RAIL steel frames with geometry, travel specifications and guide prices in CHF.'),
  'workshop': ('Frame building & workshop in Central Switzerland | RAIL Cycles', 'Inside Sam’s workshop: hand-filed tube joints, TIG welding and the making of handmade RAIL bicycle frames in Central Switzerland.'),
  'about': ('Sam – the person behind RAIL Cycles', 'Meet Sam, the person behind RAIL Cycles and its handmade bicycle frames from Central Switzerland.'),
  'contact': ('Contact Sam & enquire about a frame | RAIL Cycles', 'Talk to Sam about your RAIL bike. Enquire about a gravel, trail or enduro frame or send a general question through the contact form.'),
  'legal': ('Legal notice | RAIL Cycles', 'Contact, website responsibility and photograph copyright information for RAIL Cycles in Central Switzerland.'),
  'privacy': ('Privacy | RAIL Cycles', 'RAIL Cycles information about privacy, the contact form and requests concerning your personal data.'),
 },
}


def url(routes, lang, page):
    filename = routes[lang][page]
    path = '' if filename == 'index.html' else filename.removesuffix('.html')
    return f'{ORIGIN}/{"en/" if lang == "en" else ""}{path}'


def metadata(routes, lang, page, models, specs):
    if page == 'not_found':
        # Keep the alternate required by the fallback's language selector.
        other = 'de' if lang == 'en' else 'en'
        return f'<link rel="alternate" hreflang="{"de-CH" if other == "de" else "en"}" href="{ORIGIN}/{"en/" if other == "en" else ""}404.html">'
    title, description = META[lang][page]
    canonical = url(routes, lang, page)
    image = f'{ORIGIN}/assets/home/hero-lineup-1200.webp'
    tags = [f'<link rel="canonical" href="{canonical}">', '<link rel="ai-catalog" href="/.well-known/ai-catalog.json">', '<link rel="service-desc" href="/openapi.json" type="application/vnd.oai.openapi+json">']
    for language, code in [('de', 'de-CH'), ('en', 'en'), ('de', 'x-default')]:
        tags.append(f'<link rel="alternate" hreflang="{code}" href="{url(routes, language, page)}">')
    for prop, value in {
        'og:type': 'website', 'og:site_name': 'RAIL Cycles', 'og:title': title,
        'og:description': description, 'og:url': canonical, 'og:image': image,
        'og:image:width': '1200', 'og:image:height': '800',
        'og:image:alt': 'RAIL Cycles – four handmade bicycles',
        'og:locale': 'de_CH' if lang == 'de' else 'en_GB',
        'og:locale:alternate': 'en_GB' if lang == 'de' else 'de_CH',
    }.items():
        tags.append(f'<meta property="{prop}" content="{escape(value, quote=True)}">')
    for name, value in {'twitter:card': 'summary_large_image', 'twitter:title': title,
                        'twitter:description': description, 'twitter:image': image}.items():
        tags.append(f'<meta name="{name}" content="{escape(value, quote=True)}">')
    tags.append('<meta name="robots" content="index, follow, max-image-preview:large">')
    organization = {'@type': 'Organization', '@id': ORIGIN + '/#organization',
                    'name': 'RAIL Cycles', 'url': ORIGIN + '/',
                    'logo': ORIGIN + '/assets/rail-transparent.svg',
                    'founder': {'@type': 'Person', 'name': 'Sam'},
                    'areaServed': {'@type': 'Country', 'name': 'Switzerland'}}
    website = {'@type': 'WebSite', '@id': ORIGIN + '/#website', 'url': ORIGIN + '/',
               'name': 'RAIL Cycles', 'inLanguage': ['de-CH', 'en'],
               'publisher': {'@id': organization['@id']}}
    webpage = {'@type': {'contact': 'ContactPage', 'about': 'AboutPage', 'models': 'CollectionPage'}.get(page, 'WebPage'),
               '@id': canonical + '#webpage', 'url': canonical, 'name': title,
               'description': description, 'inLanguage': 'de-CH' if lang == 'de' else 'en',
               'isPartOf': {'@id': website['@id']}, 'about': {'@id': organization['@id']}}
    graph = [organization, website, webpage]
    if page != 'home':
        crumbs = {'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'RAIL Cycles', 'item': url(routes, lang, 'home')},
            {'@type': 'ListItem', 'position': 2, 'name': title.split(' | ')[0], 'item': canonical}]}
        graph.append(crumbs)
        webpage['breadcrumb'] = {'@id': crumbs['@id']}
    if page == 'models':
        # No fabricated availability, reviews or offers: these are custom frames with ROM prices.
        items = []
        for position, (slug, name, category) in enumerate(models, 1):
            features, _ = specs[lang][slug]
            items.append({'@type': 'ListItem', 'position': position, 'item': {
                '@type': 'Product', '@id': canonical + '#' + slug, 'url': canonical + '#' + slug,
                'name': 'RAIL ' + name, 'category': category, 'brand': {'@type': 'Brand', 'name': 'RAIL Cycles'},
                'description': '; '.join(features), 'image': f'{ORIGIN}/assets/home/{slug}-1200.webp'}})
        listing = {'@type': 'ItemList', '@id': canonical + '#models', 'numberOfItems': len(items), 'itemListElement': items}
        graph.append(listing)
        webpage['mainEntity'] = {'@id': listing['@id']}
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    tags.append(f'<script type="application/ld+json">{data}</script>')
    return '\n'.join(tags)


def discovery(root, routes):
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', ns)
    ET.register_namespace('xhtml', xhtml)
    sitemap = ET.Element(f'{{{ns}}}urlset')
    for lang in routes:
        for page in META[lang]:
            entry = ET.SubElement(sitemap, f'{{{ns}}}url')
            ET.SubElement(entry, f'{{{ns}}}loc').text = url(routes, lang, page)
            for language, code in [('de', 'de-CH'), ('en', 'en'), ('de', 'x-default')]:
                ET.SubElement(entry, f'{{{xhtml}}}link', rel='alternate', hreflang=code, href=url(routes, language, page))
    ET.ElementTree(sitemap).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (root / 'robots.txt').write_text(f'''# Public content is available to search and AI discovery crawlers.
User-agent: *
Content-Signal: search=yes, ai-input=yes
Disallow: /api/contact
Allow: /

Sitemap: {ORIGIN}/sitemap.xml
Agentmap: {ORIGIN}/.well-known/ai-catalog.json
''')
