"""Generate the bilingual static RAIL site. Run from any working directory."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    'de': {'home':'index.html', 'models':'modelle.html', 'workshop':'werkstatt.html', 'about':'ueber-mich.html', 'contact':'kontakt.html', 'legal':'impressum.html', 'privacy':'datenschutz.html'},
    'en': {'home':'index.html', 'models':'models.html', 'workshop':'workshop.html', 'about':'about.html', 'contact':'contact.html', 'legal':'legal-notice.html', 'privacy':'privacy.html'},
}
COPY = {
 'de': {
  'home':'Startseite','models':'Modelle','workshop':'Werkstatt','about':'Über mich','contact':'Kontakt','legal':'Impressum','privacy':'Datenschutz',
  'skip':'Zum Inhalt springen','navigation':'Hauptnavigation','language':'Sprache wählen','menu':'Menü','close':'Schliessen','open_menu':'Menü öffnen','close_menu':'Menü schliessen','top':'Nach oben','country':'Schweiz','pages':'Entdecke RAIL','legal_nav':'Rechtliche Seiten',
  'intro':'Vier Modelle.<br>Eine Handschrift.','intro_text':'RAIL Cycles aus Sarnen. Entdecke die Fahrräder, wirf einen Blick in die Werkstatt und lerne Samuel kennen.',
  'models_teaser':'Von Gravel bis Trail. Vier Fahrräder, jedes mit seinem eigenen Namen.','workshop_teaser':'Dort, wo aus einzelnen Teilen ein Fahrrad wird.','about_teaser':'Samuel Kummrow. Der Mensch hinter RAIL Cycles.',
  'all_models':'Alle Modelle entdecken','see_workshop':'Die Werkstatt entdecken','meet_samuel':'Samuel kennenlernen','talk':'Lass uns über dein Bike sprechen.','contact_title':'Dein Weg zu RAIL.','get_contact':'Kontakt aufnehmen',
  'models_title':'Die RAIL Familie.','models_intro':'Vier Modelle. Von Gravel bis Trail. Entdecke die Fahrräder und sprich mit Samuel über das Modell, das dich interessiert.',
  'model_question':'Du möchtest mehr über dieses Modell erfahren? Samuel beantwortet deine Fragen persönlich.','enquire':'Modell anfragen','category':'Kategorie','model_nav':'Direkt zum Modell',
  'workshop_title':'Hier entsteht<br>dein RAIL.','workshop_intro':'Vom Rahmen an der Werkbank bis zum fertigen Fahrrad: ein Blick dorthin, wo RAIL entsteht.','bench':'An der Werkbank.','details':'Ein Blick auf die Details.','workshop_alt':'Samuel arbeitet an einem Fahrradrahmen an der Werkbank','detail_alt':'Samuel prüft einen eingespannten Fahrradrahmen',
  'about_title':'Der Mensch<br>hinter RAIL.','about_intro':'Ich bin Samuel – der Mensch hinter RAIL Cycles. Du möchtest mehr über meine Fahrräder erfahren? Schreib mir.','portrait_alt':'Samuel Kummrow mit einem RAIL Fahrrad, Schwarz-Weiss-Porträt',
  'contact_intro':'Eine Frage zu einem Modell oder zu RAIL? Schreib Samuel direkt.','email':'E-Mail','address':'Adresse','email_cta':'E-Mail schreiben','subject':'Anfrage: RAIL',
  'legal_title':'Impressum.','operator':'Kontakt und Website-Verantwortlicher','website':'Website','privacy_title':'Datenschutz.',
  'draft':'Entwurf · Angaben zum Hosting und zur Datenbearbeitung sind vor Veröffentlichung zu vervollständigen.',
  'privacy_sections':[
   ('Kontakt','Bei Fragen zum Datenschutz erreichst du Samuel Kummrow unter sam@railcycles.ch oder postalisch: St. Antoniastrasse 17, 6060 Sarnen, Schweiz.'),
   ('Kontakt per E-Mail','Das Kontaktformular bereitet eine Nachricht lokal in deinem Browser vor und speichert keine Eingaben auf einem Server. Der E-Mail-Link öffnet dein E-Mail-Programm. Erst wenn du dort eine Nachricht sendest, werden die von dir eingegebenen Informationen übermittelt. Die Angaben dienen der Bearbeitung deiner Anfrage. Angaben zum E-Mail-Anbieter und zu Aufbewahrungsfristen werden vor Veröffentlichung ergänzt.'),
   ('Cookies und externe Inhalte','Diese Website-Version verwendet keine Analyse- oder Werbeskripte und setzt selbst keine Cookies. Die Sprachwahl erfolgt über Seitenlinks. Bilder und Schriftarten werden zusammen mit der Website bereitgestellt; Karten und Social-Media-Inhalte sind nicht eingebettet.'),
   ('Hosting','Die endgültige Hosting-Konfiguration ist noch zu bestätigen. Anbieter, Serverstandort, technische Protokolldaten, Empfänger und Aufbewahrungsfristen werden entsprechend dem tatsächlich eingesetzten Dienst ergänzt.'),
   ('Deine Anliegen','Für Auskunft, Berichtigung oder Löschung deiner personenbezogenen Daten kannst du dich an die oben genannte Kontaktadresse wenden. Die Bearbeitung richtet sich nach dem anwendbaren Datenschutzrecht.'),
  ],
 },
 'en': {
  'home':'Home','models':'Models','workshop':'Workshop','about':'About me','contact':'Contact','legal':'Legal notice','privacy':'Privacy',
  'skip':'Skip to content','navigation':'Main navigation','language':'Choose language','menu':'Menu','close':'Close','open_menu':'Open menu','close_menu':'Close menu','top':'Back to top','country':'Switzerland','pages':'Discover RAIL','legal_nav':'Legal pages',
  'intro':'Four models.<br>One signature.','intro_text':'RAIL Cycles from Sarnen. Explore the bikes, step inside the workshop and meet Samuel.',
  'models_teaser':'From gravel to trail. Four bikes, each with a name of its own.','workshop_teaser':'Where individual parts become a bicycle.','about_teaser':'Samuel Kummrow. The person behind RAIL Cycles.',
  'all_models':'Explore all models','see_workshop':'Explore the workshop','meet_samuel':'Meet Samuel','talk':'Let’s talk about your bike.','contact_title':'Your way to RAIL.','get_contact':'Get in touch',
  'models_title':'The RAIL family.','models_intro':'Four models. From gravel to trail. Explore the bikes and talk to Samuel about the model that interests you.',
  'model_question':'Want to know more about this model? Samuel will answer your questions personally.','enquire':'Enquire about this model','category':'Category','model_nav':'Jump to a model',
  'workshop_title':'This is where<br>RAIL takes shape.','workshop_intro':'From a frame on the workbench to a finished bicycle: a glimpse into the place where RAIL takes shape.','bench':'At the workbench.','details':'A closer look at the details.','workshop_alt':'Samuel working on a bicycle frame at the workbench','detail_alt':'Samuel inspecting a bicycle frame held in a fixture',
  'about_title':'The person<br>behind RAIL.','about_intro':'I’m Samuel, the person behind RAIL Cycles. Want to know more about my bicycles? Get in touch.','portrait_alt':'Black-and-white portrait of Samuel Kummrow with a RAIL bicycle',
  'contact_intro':'A question about a model or about RAIL? Write to Samuel directly.','email':'Email','address':'Address','email_cta':'Write an email','subject':'Enquiry: RAIL',
  'legal_title':'Legal notice.','operator':'Contact and person responsible for this website','website':'Website','privacy_title':'Privacy.',
  'draft':'Draft · Hosting and data-processing details must be completed before publication.',
  'privacy_sections':[
   ('Contact','For privacy enquiries, contact Samuel Kummrow at sam@railcycles.ch or by post at St. Antoniastrasse 17, 6060 Sarnen, Switzerland.'),
   ('Email enquiries','The contact form prepares a message locally in your browser and does not store entries on a server. The email link opens your email application. The information you enter is transmitted only when you send a message from that application. It is used to respond to your enquiry. Details of the email provider and retention periods will be added before publication.'),
   ('Cookies and external content','This website version uses no analytics or advertising scripts and does not itself set cookies. Language selection uses page links. Images and fonts are served with the website; maps and social-media content are not embedded.'),
   ('Hosting','The final hosting configuration remains to be confirmed. The provider, server location, technical logs, recipients and retention periods will be documented according to the service actually used.'),
   ('Your enquiries','You may use the contact details above to request access to, correction of or deletion of your personal data. Requests are handled under applicable data-protection law.'),
  ],
 }
}
COPY['de'].update({
 'featured':'Ausgewählte Modelle','view_model':'Modell ansehen','form_title':'Schreib Samuel.','form_intro':'Erzähl uns, was du vorhast.','name':'Name','message':'Nachricht','optional':'optional','model_interest':'Welches Modell interessiert dich?','no_model':'Allgemeine Anfrage','prepare_email':'E-Mail vorbereiten','form_note':'Fülle die Pflichtfelder aus. Im nächsten Schritt öffnest du die Nachricht in deinem E-Mail-Programm und sendest sie dort.','required_note':'* Pflichtfeld','privacy_hint':'Informationen zur Bearbeitung deiner Anfrage:','open_email':'E-Mail-Programm öffnen','copy_message':'Nachricht kopieren','email_ready':'Deine Nachricht ist vorbereitet, aber noch nicht gesendet. Öffne dein E-Mail-Programm und sende sie dort an Samuel.','no_js':'Nutze ohne JavaScript bitte den direkten E-Mail-Link oben.'
})
COPY['en'].update({
 'featured':'Featured models','view_model':'View model','form_title':'Write to Samuel.','form_intro':'Tell us what you have in mind.','name':'Name','message':'Message','optional':'optional','model_interest':'Which model interests you?','no_model':'General enquiry','prepare_email':'Prepare email','form_note':'Fill in the required fields. In the next step, open the message in your email application and send it from there.','required_note':'* Required field','privacy_hint':'How your enquiry is handled:','open_email':'Open email application','copy_message':'Copy message','email_ready':'Your message is prepared, but has not been sent. Open your email application and send it to Samuel from there.','no_js':'Without JavaScript, please use the direct email link above.'
})

MODELS = [('muetterschwandenberg','Muetterschwandenberg','Trail'),('truischjanid','Truischjanid','Enduro Hardtail'),('wichelsee','Wichelsee','Gravel'),('lopper','Lopper','Trail')]

def make_site(lang):
 c = COPY[lang]
 prefix = '../' if lang == 'en' else ''
 out = ROOT / 'en' if lang == 'en' else ROOT
 out.mkdir(exist_ok=True)
 def asset(path): return prefix + path
 def route(key): return ROUTES[lang][key]
 def image(name, alt, cls='', eager=False):
  widths = [800,1200,1600] if name == 'workshop' else [480,800] if name == 'workshop-detail' else [480,800,1200]
  w = 1200 if name == 'workshop' else 800
  dims = 'width="4898" height="3265"' if name == 'workshop' else 'width="3265" height="4898"'
  srcset = ', '.join(f'{asset(f"assets/home/{name}-{n}.webp")} {n}w' for n in widths)
  return f'<img class="{cls}" src="{asset(f"assets/home/{name}-{w}.webp")}" srcset="{srcset}" sizes="(max-width: 767px) calc(100vw - 40px), 50vw" {dims} loading="{"eager" if eager else "lazy"}" alt="{escape(alt)}">'
 def link(label, href, cls='text-link'):
  return f'<a class="{cls}" href="{href}">{label} <span aria-hidden="true">↗</span></a>'
 def contact_strip():
  return f'<section class="contact"><div class="contact-inner wrap"><div><p class="eyebrow">{c["talk"]}</p><h2>{c["contact_title"]}</h2></div>{link(c["get_contact"],route("contact"),"button button-outline")}</div></section>'
 def heading(label, title, intro=''):
  return f'<div class="page-heading wrap"><p class="eyebrow">{label}</p><h1>{title}</h1>{f"<p class=page-intro>{intro}</p>" if intro else ""}</div>'

 for page, filename in ROUTES[lang].items():
  nav = ''.join(f'<a href="{route(k)}" {"aria-current=page" if page==k else ""}>{c[k]}</a>' for k in ['models','workshop','about','contact'])
  alternate = '../'+ROUTES['de'][page] if lang=='en' else 'en/'+ROUTES['en'][page]
  de_link = route(page) if lang=='de' else alternate
  en_link = route(page) if lang=='en' else alternate
  languages = f'<nav class="language-bar" aria-label="{c["language"]}"><a href="{de_link}" lang="de" hreflang="de-CH" {"aria-current=page" if lang=="de" else ""} aria-label="Deutsch">DE</a><span aria-hidden="true">/</span><a href="{en_link}" lang="en" hreflang="en" {"aria-current=page" if lang=="en" else ""} aria-label="English">EN</a></nav>'
  brand = f'<a class="brand" href="{route("home")}" aria-label="RAIL Cycles – {c["home"]}"><img src="{asset("assets/rail-transparent.svg")}" width="188" height="50" alt="RAIL"></a>'
  header = f'<header class="site-header" id="start"><div class="header-inner wrap">{brand}<nav class="main-nav" id="hauptnavigation" aria-label="{c["navigation"]}">{nav}</nav>{languages}<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="hauptnavigation" aria-label="{c["open_menu"]}" hidden><span>{c["menu"]}</span><span class="menu-icon" aria-hidden="true"></span></button></div></header>'
  footer = f'<footer class="site-footer"><div class="footer-main wrap"><div>{brand}<p class="footer-tagline">Built by Hand.</p></div><nav class="footer-nav" aria-label="{c["navigation"]}">{nav}</nav><address>Samuel Kummrow<br>St. Antoniastrasse 17<br>6060 Sarnen, {c["country"]}<br><a href="mailto:sam@railcycles.ch">sam@railcycles.ch</a></address></div><div class="footer-bottom wrap"><span>© 2026 RAIL Cycles</span><nav class="legal-nav" aria-label="{c["legal_nav"]}"><a href="{route("legal")}">{c["legal"]}</a><a href="{route("privacy")}">{c["privacy"]}</a></nav><a href="#start" data-back-top>{c["top"]} <span aria-hidden="true">↑</span></a></div></footer>'

  if page == 'home':
   hero = (ROOT/'scripts/templates/home-hero.html').read_text().replace('href="#modelle"',f'href="{route("models")}"')
   hero = hero.replace('class="scroll-link" href="'+route('models')+'"','class="scroll-link" href="#entdecken"')
   if lang=='en':
    for a,b in {'Sarnen, Schweiz':'Sarnen, Switzerland','Modelle entdecken':'Explore the models','Entdecke RAIL':'Discover RAIL','Diashow':'Slideshow','Bild 1 von 3':'Image 1 of 3','Vorheriges Bild':'Previous image','Nächstes Bild':'Next image','Slideshow pausieren':'Pause slideshow','Vier RAIL Fahrräder vor einer alten Verladerampe':'Four RAIL bicycles in front of an old loading platform','Die RAIL Modelle gemeinsam vor der Verladerampe':'The RAIL models together at the loading platform','Das weisse RAIL Lopper vor einem Industriegebäude':'The white RAIL Lopper in front of an industrial building'}.items(): hero=hero.replace(a,b)
    hero=hero.replace('assets/', '../assets/')
   cards=[]
   for slug,name,category in MODELS[:3]:
    cards.append(f'<article class="featured-model"><a class="featured-photo" href="{route("models")}#{slug}" aria-label="{c["view_model"]}: {name}">{image(slug,"RAIL "+name)}</a><p class="eyebrow">{category}</p><h3>{name}</h3>{link(c["view_model"],route("models")+"#"+slug)}</article>')
   content=hero+f'<section class="home-featured section wrap" id="entdecken"><div class="section-heading"><div><p class="eyebrow">{c["featured"]}</p><h2>{c["intro"]}</h2></div><p class="section-intro">{c["models_teaser"]}</p></div><div class="featured-grid">{"".join(cards)}</div><div class="section-view">{link(c["all_models"],route("models"),"button button-outline")}</div></section>'
   content+=f'<section class="home-workshop section"><div class="home-story wrap"><figure>{image("workshop",c["workshop_alt"])}</figure><div class="home-story-copy"><p class="eyebrow">{c["workshop"]}</p><h2>{c["workshop_title"]}</h2><p>{c["workshop_intro"]}</p>{link(c["see_workshop"],route("workshop"),"button button-outline")}</div></div></section>'
   content+=f'<section class="home-story home-about section wrap"><div class="home-story-copy"><p class="eyebrow">{c["about"]}</p><h2>{c["about_title"]}</h2><p>{c["about_teaser"]}</p>{link(c["meet_samuel"],route("about"),"button button-outline")}</div><figure>{image("samuel",c["portrait_alt"])}</figure></section>'+contact_strip()
  elif page=='models':
   jumps=''.join(f'<a href="#{slug}">{name}</a>' for slug,name,_ in MODELS)
   content=heading(c['models'],c['models_title'],c['models_intro'])+f'<nav class="model-jumps wrap" aria-label="{c["model_nav"]}">{jumps}</nav><div class="model-details wrap">'
   for n,(slug,name,category) in enumerate(MODELS,1):
    alt=f'RAIL {name} – '+('vollständige Seitenansicht' if lang=='de' else 'complete side view')
    content+=f'<section class="model-detail" id="{slug}" aria-labelledby="title-{slug}"><div class="model-detail-photo">{image(slug,alt,eager=n==1)}</div><div class="model-detail-copy"><p class="eyebrow">0{n} / {category}</p><h2 id="title-{slug}">{name}</h2><img class="model-wordmark" src="{asset(f"assets/home/{slug}-wordmark.png")}" alt="" loading="lazy"><p>{c["model_question"]}</p>{link(c["enquire"],route("contact")+"?model="+slug,"button button-outline")}</div></section>'
   content+='</div>'+contact_strip()
  elif page=='workshop':
   content=heading(c['workshop'],c['workshop_title'],c['workshop_intro'])+f'<div class="workshop-page wrap"><figure class="workshop-establishing">{image("workshop",c["workshop_alt"],eager=True)}<figcaption>{c["bench"]}</figcaption></figure><figure class="workshop-closeup">{image("workshop-detail",c["detail_alt"])}<figcaption>{c["details"]}</figcaption></figure></div>'+contact_strip()
  elif page=='about':
   content=f'<section class="about-page wrap"><div class="about-copy"><p class="eyebrow">{c["about"]}</p><h1>{c["about_title"]}</h1><h2>Samuel Kummrow</h2><p>{c["about_intro"]}</p>{link(c["get_contact"],route("contact"),"button button-outline")}</div><figure>{image("samuel",c["portrait_alt"],eager=True)}<figcaption>Samuel Kummrow · RAIL Cycles</figcaption></figure></section>'
  elif page=='contact':
   options=''.join(f'<option value="{slug}">{name}</option>' for slug,name,_ in MODELS)
   form=f'''<section class="contact-form-section wrap" aria-labelledby="form-title"><div class="form-heading"><p class="eyebrow">{c['contact']}</p><h2 id="form-title">{c['form_title']}</h2><p>{c['form_intro']}</p><p class="form-delivery-note">{c['form_note']}</p></div><form class="contact-form" data-contact-form><p class="required-note">{c['required_note']}</p><div class="form-row"><div class="form-field"><label for="contact-name">{c['name']} *</label><input id="contact-name" name="name" autocomplete="name" required maxlength="100"></div><div class="form-field"><label for="contact-email">{c['email']} *</label><input id="contact-email" name="email" type="email" autocomplete="email" required maxlength="254"></div></div><div class="form-field"><label for="contact-model">{c['model_interest']} <span>({c['optional']})</span></label><select id="contact-model" name="model"><option value="">{c['no_model']}</option>{options}</select></div><div class="form-field"><label for="contact-message">{c['message']} *</label><textarea id="contact-message" name="message" rows="6" required maxlength="3000"></textarea></div><p class="form-privacy">{c['privacy_hint']} <a href="{route('privacy')}">{c['privacy']}</a>.</p><button class="button button-light" type="submit" disabled>{c['prepare_email']} <span aria-hidden="true">↗</span></button><div class="form-result" hidden><p role="status" data-form-status>{c['email_ready']}</p><a class="text-link" data-email-draft href="mailto:sam@railcycles.ch">{c['open_email']} <span aria-hidden="true">↗</span></a><button class="copy-message" type="button" data-copy-message>{c['copy_message']}</button><textarea class="prepared-message" readonly aria-label="{c['message']}" rows="8" hidden></textarea></div><noscript><p>{c['no_js']}</p></noscript></form></section>'''
   content=heading(c['contact'],c['contact_title'],c['contact_intro'])+f'<section class="contact-page wrap"><div><p class="eyebrow">{c["email"]}</p><a class="contact-email" href="mailto:sam@railcycles.ch" data-enquiry>sam@railcycles.ch <span aria-hidden="true">↗</span></a><p class="selected-model" hidden></p></div><div><p class="eyebrow">{c["address"]}</p><address>Samuel Kummrow<br>St. Antoniastrasse 17<br>6060 Sarnen<br>{c["country"]}</address></div></section>'+form+'<figure class="contact-photo wrap">'+image('workshop',c['workshop_alt'])+'</figure>'
  elif page=='legal':
   content=heading(c['legal_nav'],c['legal_title'])+f'<article class="legal-copy wrap"><h2>{c["operator"]}</h2><address>RAIL Cycles<br>Samuel Kummrow<br>St. Antoniastrasse 17<br>6060 Sarnen, {c["country"]}<br><a href="mailto:sam@railcycles.ch">sam@railcycles.ch</a></address><h2>{c["website"]}</h2><p>railcycles.ch</p>{link(c["privacy"],route("privacy"))}</article>'
  else:
   content=heading(c['legal_nav'],c['privacy_title'])+f'<article class="legal-copy wrap"><p class="draft-note">{c["draft"]}</p>'+''.join(f'<section><h2>{title}</h2><p>{text}</p></section>' for title,text in c['privacy_sections'])+'</article>'

  title='RAIL Cycles — Built by Hand' if page=='home' else c[page]+' — RAIL Cycles'
  description=escape(c.get(page+'_intro',c['intro_text']))
  html=f'''<!doctype html>
<html lang="{'de-CH' if lang=='de' else 'en'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{description}"><meta name="theme-color" content="#0b0b0b"><title>{title}</title>
<link rel="icon" href="{asset('rail.svg')}" type="image/svg+xml"><link rel="alternate" hreflang="{'en' if lang=='de' else 'de-CH'}" href="{alternate}"><link rel="preload" href="{asset('assets/fonts/fjalla-one.woff2')}" as="font" type="font/woff2" crossorigin><link rel="preload" href="{asset('assets/fonts/barlow-regular.woff2')}" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{asset('home.css')}"><script src="{asset('home.js')}" defer></script></head>
<body class="page-{page}"><a class="skip-link" href="#inhalt">{c['skip']}</a>{header}<main id="inhalt">{content}</main>{footer}</body></html>'''
  (out/filename).write_text(html)

for language in ROUTES:
 make_site(language)
print('Generated 14 pages: 5 main pages + 2 legal pages in German and English.')
