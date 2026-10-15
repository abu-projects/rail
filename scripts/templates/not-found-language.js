(() => {
  let language = 'de';
  if (/^\/en(?:\/|$)/.test(location.pathname)) {
    language = 'en';
  } else if (!/^\/404(?:\.html)?\/?$/.test(location.pathname)) {
    let previous;
    try { previous = new URL(document.referrer); } catch {}
    if (previous && previous.origin === location.origin) {
      language = /^\/en(?:\/|$)/.test(previous.pathname) ? 'en' : 'de';
    } else {
      try { language = sessionStorage.getItem('rail-language') || 'de'; } catch {}
    }
  }
  if (language === 'en') {
    document.documentElement.lang = 'en';
    document.title = 'Page not found. — RAIL Cycles';
    const alternate = document.querySelector('[rel="alternate"]');
    alternate.hreflang = 'de-CH';
    alternate.href = '/404.html';
    document.body.replaceChildren(document.querySelector('#not-found-english').content.cloneNode(true));
  } else {
    document.querySelector('#not-found-english').remove();
  }
})();
