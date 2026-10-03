(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const english = document.documentElement.lang === 'en';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let syncHero = () => {};
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.main-nav');
  const header = document.querySelector('.site-header');
  const mobile = matchMedia('(max-width: 767px)');
  const background = [document.querySelector('main'), document.querySelector('footer')];
  let menuOpen = false;
  menuButton.hidden = false;
  function setMenu(open, restoreFocus = false) {
    menuOpen = open;
    navigation.classList.toggle('is-open', open);
    header.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', english ? (open ? 'Close menu' : 'Open menu') : (open ? 'Menü schliessen' : 'Menü öffnen'));
    menuButton.firstElementChild.textContent = english ? (open ? 'Close' : 'Menu') : (open ? 'Schliessen' : 'Menü');
    background.forEach(element => { element.inert = open; });
    document.body.classList.toggle('scroll-locked', open);
    if (open) navigation.querySelector('a').focus();
    else if (restoreFocus) menuButton.focus();
    syncHero();
  }
  menuButton.addEventListener('click', () => setMenu(!menuOpen, menuOpen));
  header.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { if (menuOpen) setMenu(false, true); }));
  mobile.addEventListener('change', () => { if (!mobile.matches && menuOpen) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (!menuOpen) return;
    if (event.key === 'Escape') { setMenu(false, true); return; }
    if (event.key !== 'Tab') return;
    const items = [...header.querySelectorAll('a, button')].filter(item => item.getClientRects().length);
    const first = items[0];
    const last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });


  function updateHeader() { header.classList.toggle('is-scrolled', window.scrollY > 24); }
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();
  document.querySelector('[data-back-top]').addEventListener('click', event => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
    header.querySelector('.brand').focus({ preventScroll: true });
  });
  const enquiry = document.querySelector('[data-enquiry]');
  if (enquiry) {
    const models = new Map([
      ['muetterschwandenberg', 'Muetterschwandenberg'], ['truischjanid', 'Truischjanid'],
      ['wichelsee', 'Wichelsee'], ['lopper', 'Lopper']
    ]);
    const slug = new URLSearchParams(location.search).get('model');
    if (models.has(slug)) {
      const model = models.get(slug);
      const modelSelect = document.querySelector('#contact-model');
      if (modelSelect) modelSelect.value = slug;
      enquiry.href = `mailto:sam@railcycles.ch?subject=${encodeURIComponent(`${english ? 'Enquiry' : 'Anfrage'}: RAIL ${model}`)}`;
      const note = document.querySelector('.selected-model');
      note.textContent = `${english ? 'Your enquiry' : 'Deine Anfrage'}: ${model}`;
      note.hidden = false;
      document.querySelectorAll('.language-bar a').forEach(link => { link.search = `?model=${slug}`; });
    }
  }
  const contactForm = document.querySelector('[data-contact-form]');
  if (contactForm) {
    const result = contactForm.querySelector('.form-result');
    const status = contactForm.querySelector('[data-form-status]');
    const readyMessage = status.textContent;
    const draftLink = contactForm.querySelector('[data-email-draft]');
    const copyButton = contactForm.querySelector('[data-copy-message]');
    const prepared = contactForm.querySelector('.prepared-message');
    const nameField = contactForm.elements.namedItem('name');
    const messageField = contactForm.elements.namedItem('message');
    let draft = '';
    contactForm.addEventListener('input', () => {
      result.hidden = true;
      [nameField, messageField].forEach(field => field.setCustomValidity(''));
    });
    contactForm.addEventListener('submit', event => {
      event.preventDefault();
      [nameField, messageField].forEach(field => {
        field.setCustomValidity(field.value.trim() ? '' : (english ? 'Please complete this field.' : 'Bitte fülle dieses Feld aus.'));
      });
      if (!contactForm.reportValidity()) return;
      const data = new FormData(contactForm);
      const modelSelect = contactForm.elements.namedItem('model');
      const model = modelSelect.value ? modelSelect.selectedOptions[0].textContent : '';
      const subject = `${english ? 'Enquiry' : 'Anfrage'}: RAIL${model ? ' ' + model : ''}`;
      draft = `Name: ${data.get('name').trim()}\n${english ? 'Email' : 'E-Mail'}: ${data.get('email').trim()}${model ? `\n${english ? 'Model' : 'Modell'}: ${model}` : ''}\n\n${data.get('message').trim()}`;
      draftLink.href = `mailto:sam@railcycles.ch?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(draft)}`;
      prepared.value = draft;
      prepared.hidden = true;
      status.textContent = readyMessage;
      result.hidden = false;
      draftLink.focus();
    });
    contactForm.querySelector('[type="submit"]').disabled = false;
    copyButton.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(draft);
        status.textContent = english ? 'Message copied. Paste it into an email to sam@railcycles.ch.' : 'Nachricht kopiert. Füge sie in eine E-Mail an sam@railcycles.ch ein.';
      } catch {
        prepared.hidden = false;
        prepared.focus();
        prepared.select();
        status.textContent = english ? 'Copy the message below and email it to sam@railcycles.ch.' : 'Kopiere die Nachricht unten und sende sie per E-Mail an sam@railcycles.ch.';
      }
    });
  }
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const slides = [...document.querySelectorAll('[data-slide]')];
  const controls = document.querySelector('.slideshow-controls');
  const playback = document.querySelector('#slide-play');
  let current = 0;
  let manuallyPaused = reducedMotion.matches;
  let hovered = false;
  let timer;
  let loading = false;
  let heroVisible = true;

  function schedule() {
    clearTimeout(timer);
    const stopped = manuallyPaused || document.hidden || !heroVisible || menuOpen;
    hero.classList.toggle('is-motion-paused', stopped || reducedMotion.matches);
    const focused = hero.contains(document.activeElement) && document.activeElement !== playback;
    if (!stopped && !hovered && !focused && !loading) {
      timer = setTimeout(() => changeSlide(1), 14000);
    }
  }
  syncHero = schedule;
  function updatePlayback() {
    playback.setAttribute('aria-label', english ? (manuallyPaused ? 'Resume slideshow' : 'Pause slideshow') : (manuallyPaused ? 'Diashow fortsetzen' : 'Diashow pausieren'));
    playback.firstElementChild.textContent = manuallyPaused ? '▷' : 'Ⅱ';
    schedule();
  }
  async function changeSlide(direction) {
    if (loading) return;
    clearTimeout(timer);
    loading = true;
    const next = (current + direction + slides.length) % slides.length;
    const image = slides[next].querySelector('img');
    try {
      if (image.dataset.src) {
        slides[next].querySelectorAll('source[data-srcset]').forEach(source => {
          source.srcset = source.dataset.srcset;
        });
        image.srcset = image.dataset.srcset;
        image.src = image.dataset.src;
        await image.decode();
        delete image.dataset.src;
      }
      const outgoing = slides[current];
      outgoing.classList.add('is-leaving');
      outgoing.classList.remove('is-active');
      outgoing.setAttribute('aria-hidden', 'true');
      slides[next].classList.add('is-active');
      slides[next].removeAttribute('aria-hidden');
      current = next;
      document.querySelector('#slide-number').textContent = String(current + 1).padStart(2, '0');
      document.querySelector('.slide-count').setAttribute('aria-label', english ? `Image ${current + 1} of ${slides.length}` : `Bild ${current + 1} von ${slides.length}`);
      // Keep the outgoing camera moving under the dissolve; reset only when covered.
      if (!reducedMotion.matches) await new Promise(resolve => setTimeout(resolve, 2400));
      outgoing.classList.remove('is-leaving');
    } catch {
      // Keep the last complete photograph visible if the next asset is unavailable.
      manuallyPaused = true;
      updatePlayback();
    } finally {
      loading = false;
      schedule();
    }
  }
  controls.hidden = false;
  document.querySelector('#slide-prev').addEventListener('click', () => changeSlide(-1));
  document.querySelector('#slide-next').addEventListener('click', () => changeSlide(1));
  playback.addEventListener('click', () => { manuallyPaused = !manuallyPaused; updatePlayback(); });
  controls.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse') { hovered = true; schedule(); } });
  controls.addEventListener('pointerleave', () => { hovered = false; schedule(); });
  hero.addEventListener('focusin', schedule);
  hero.addEventListener('focusout', () => setTimeout(schedule, 0));
  document.addEventListener('visibilitychange', schedule);
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) { manuallyPaused = true; updatePlayback(); } });


  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {
    heroVisible = entry.isIntersecting;
    schedule();
  }).observe(hero);
  updatePlayback();
})();
