// RAIL: image-aligned copy with always-visible enquiry actions.
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const english = document.documentElement.lang === 'en';
  try { sessionStorage.setItem('rail-language', english ? 'en' : 'de'); } catch {}
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
  const enquiry = document.querySelector('[data-contact-form]');
  if (enquiry) {
    const models = new Map([
      ['muetterschwandenberg', 'Muetterschwandeberg'], ['truischjanid', 'Truischjanid'],
      ['wichelsee', 'Wichelsee'], ['lopper', 'Lopper']
    ]);
    const slug = new URLSearchParams(location.search).get('model');
    if (models.has(slug)) {
      const model = models.get(slug);
      const modelSelect = document.querySelector('#contact-model');
      if (modelSelect) modelSelect.value = slug;
      const note = document.querySelector('.selected-model');
      note.textContent = `${english ? 'Your enquiry' : 'Deine Anfrage'}: ${model}`;
      note.hidden = false;
      document.querySelectorAll('.language-bar a').forEach(link => { link.search = `?model=${slug}`; });
    }
  }
  const contactForm = document.querySelector('[data-contact-form]');
  if (contactForm) {
    const nameField = contactForm.elements.namedItem('name');
    const messageField = contactForm.elements.namedItem('message');
    contactForm.addEventListener('input', () => {
      [nameField, messageField].forEach(field => field.setCustomValidity(''));
      contactForm.querySelector('[data-form-status]').hidden = true;
    });
    let sending = false;
    contactForm.addEventListener('submit', async event => {
      event.preventDefault();
      if (sending) return;
      [nameField, messageField].forEach(field => {
        field.setCustomValidity(field.value.trim() ? '' : (english ? 'Please complete this field.' : 'Bitte fülle dieses Feld aus.'));
      });
      if (!contactForm.reportValidity()) return;
      const status = contactForm.querySelector('[data-form-status]');
      const submit = contactForm.querySelector('[type="submit"]');
      const fields = Object.fromEntries(new FormData(contactForm));
      const inputs = [...contactForm.querySelectorAll('input, select, textarea')];
      sending = true;
      submit.disabled = true;
      inputs.forEach(field => { field.disabled = true; });
      contactForm.setAttribute('aria-busy', 'true');
      status.textContent = english ? 'Sending your message…' : 'Deine Nachricht wird gesendet…';
      status.dataset.state = 'sending';
      status.hidden = false;
      try {
        const response = await fetch('/api/contact', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fields), signal: AbortSignal.timeout(15000),
        });
        const result = await response.json();
        if (!response.ok || result.ok !== true) throw new Error('Delivery failed');
        status.textContent = english ? '✓ Thank you! Your message has been sent.' : '✓ Danke! Deine Nachricht wurde gesendet.';
        status.dataset.state = 'success';
        contactForm.reset();
        const note = document.querySelector('.selected-model');
        if (note) note.hidden = true;
      } catch {
        status.dataset.state = 'error';
        status.textContent = english
          ? 'Your message could not be sent. Your entries are still here. Please try again later.'
          : 'Deine Nachricht konnte nicht gesendet werden. Deine Eingaben bleiben erhalten. Bitte versuche es später erneut.';
      } finally {
        sending = false;
        submit.disabled = false;
        inputs.forEach(field => { field.disabled = false; });
        contactForm.removeAttribute('aria-busy');
        status.hidden = false;
      }
    });
    contactForm.querySelector('[type="submit"]').disabled = false;
  }
  const photoDialog = document.querySelector('.photo-dialog');
  if (photoDialog && typeof photoDialog.showModal === 'function') {
    document.querySelectorAll('[data-photo]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        photoDialog.querySelector('[data-dialog-photo]').src = link.href;
        photoDialog.querySelector('[data-dialog-photo]').alt = link.querySelector('img')?.alt || link.dataset.photoTitle;
        const photoTitle = photoDialog.querySelector('#photo-title');
        photoTitle.textContent = link.dataset.photoTitle || photoDialog.querySelector('[data-dialog-photo]').alt;
        photoTitle.hidden = !link.dataset.photoTitle;
        photoDialog.showModal();
      });
    });
    photoDialog.querySelector('[data-close-photo]').addEventListener('click', () => photoDialog.close());
    photoDialog.addEventListener('click', event => {
      if (event.target !== photoDialog) return;
      const bounds = photoDialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) photoDialog.close();
    });
  }
  // Match adjacent copy to its image, revealing complete paragraphs on demand.
  document.querySelectorAll('.model-detail, .home-story, .about-page').forEach((section, index) => {
    const copy = section.querySelector('.model-detail-copy, .home-story-copy, .about-copy');
    const media = section.querySelector('.model-gallery-frame, figure');
    if (!copy || !media) return;
    const image = media.querySelector('img');
    const actions = [...copy.children].filter(child => child.matches('.button'));
    const blocks = [...copy.children].filter(child => !actions.includes(child));
    // Long single paragraphs can also end at a sentence without losing their opening.
    const sentences = [];
    const segmenter = new Intl.Segmenter(english ? 'en' : 'de', { granularity: 'sentence' });
    blocks.filter(block => block.matches('p') && !block.children.length).forEach(block => {
      const parts = [...segmenter.segment(block.textContent)];
      if (parts.length < 2) return;
      block.replaceChildren(...parts.map(({ segment }) => {
        const span = document.createElement('span');
        span.textContent = segment;
        sentences.push(span);
        return span;
      }));
    });
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'copy-toggle';
    toggle.hidden = true;
    copy.id ||= `aligned-copy-${index}`;
    toggle.setAttribute('aria-controls', copy.id);
    const footer = document.createElement('div');
    footer.className = 'copy-actions';
    footer.append(toggle, ...actions);
    copy.append(footer);
    section.classList.add('aligned-story');
    let expanded = false;
    let scheduled = false;
    function update() {
      scheduled = false;
      blocks.forEach(block => { block.hidden = false; });
      sentences.forEach(sentence => { sentence.hidden = false; });
      copy.classList.remove('copy-collapsed');
      const height = (media.matches('.model-gallery-frame') ? media : image)?.getBoundingClientRect().height || 0;
      // Stacked layouts need neither clipping nor a disclosure control.
      if (mobile.matches || height < 160) { toggle.hidden = true; return; }
      const top = copy.getBoundingClientRect().top;
      const bottom = blocks.at(-1).getBoundingClientRect().bottom;
      const actionHeight = footer.getBoundingClientRect().height - (toggle.hidden ? 0 : toggle.getBoundingClientRect().height + parseFloat(getComputedStyle(toggle).marginTop));
      if (bottom - top + actionHeight <= height + 1) { toggle.hidden = true; return; }
      toggle.hidden = false;
      toggle.textContent = english ? (expanded ? 'Read less' : 'Read more') : (expanded ? 'Weniger lesen' : 'Mehr lesen');
      toggle.setAttribute('aria-expanded', String(expanded));
      if (expanded) return;
      const available = height - footer.getBoundingClientRect().height - 24;
      let overflow = false;
      blocks.forEach((block, i) => {
        // Keep the section title visible, then hide at a complete block boundary.
        if (overflow) { block.hidden = true; return; }
        if (i > 1 && block.getBoundingClientRect().bottom - top > available) {
          overflow = true;
          const parts = [...block.children].filter(child => sentences.includes(child));
          if (parts.length) {
            let hide = false;
            parts.forEach(part => {
              if (part.getBoundingClientRect().bottom - top > available) hide = true;
              part.hidden = hide;
            });
            block.hidden = parts.every(part => part.hidden);
          } else block.hidden = true;
        }
      });
      copy.style.setProperty('--copy-height', `${height}px`);
      copy.classList.add('copy-collapsed');
    }
    function schedule() {
      if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
    }
    toggle.addEventListener('click', () => {
      const previousTop = toggle.getBoundingClientRect().top;
      expanded = !expanded;
      update();
      if (!expanded && previousTop > 0) {
        const currentTop = toggle.getBoundingClientRect().top;
        if (currentTop < 100) window.scrollBy(0, currentTop - 120);
      }
      toggle.focus({ preventScroll: true });
    });
    const observer = new ResizeObserver(schedule);
    observer.observe(media);
    observer.observe(copy);
    media.addEventListener('load', schedule, true);
    mobile.addEventListener('change', schedule);
    document.fonts.ready.then(schedule);
    schedule();
  });
  // Inline model galleries keep the existing direct links and load only on demand.
  const galleries = [...document.querySelectorAll('[data-gallery]')].map(element => {
    const picture = element.querySelector('picture');
    const cover = picture.querySelector('img');
    const extra = document.createElement('img');
    extra.hidden = true;
    extra.decoding = 'async';
    element.querySelector('.model-gallery-frame').append(extra);
    return { element, picture, cover, extra, photos: JSON.parse(element.dataset.gallery),
      current: 0, paused: reducedMotion.matches, visible: 0, timer: null, request: 0,
      caption: element.querySelector('[data-gallery-caption]'), coverAlt: cover.alt,
      play: element.querySelector('[data-gallery-play]') };
  });
  let activeGallery = null;
  function galleryControls(gallery) {
    const count = gallery.photos.length + 1;
    gallery.element.querySelector('[data-gallery-count]').textContent = `${gallery.current + 1} / ${count}`;
    gallery.play.textContent = english ? (gallery.paused ? 'Play' : 'Pause') : (gallery.paused ? 'Start' : 'Pause');
    gallery.play.setAttribute('aria-label', english ? (gallery.paused ? 'Play slideshow' : 'Pause slideshow') : (gallery.paused ? 'Diashow starten' : 'Diashow pausieren'));
    gallery.element.querySelector('.model-gallery-controls').hidden = count < 2;
  }
  function scheduleGallery(gallery) {
    clearTimeout(gallery.timer);
    if (gallery !== activeGallery || gallery.paused || document.hidden || menuOpen || gallery.photos.length === 0 || (gallery.element.contains(document.activeElement) && document.activeElement !== gallery.play)) return;
    gallery.timer = setTimeout(() => showGallery(gallery, gallery.current + 1), 4000);
  }
  async function showGallery(gallery, index) {
    clearTimeout(gallery.timer);
    const request = ++gallery.request;
    const next = (index + gallery.photos.length + 1) % (gallery.photos.length + 1);
    if (next === 0) {
      gallery.picture.hidden = false;
      gallery.extra.hidden = true;
      gallery.caption.textContent = gallery.coverAlt;
    } else {
      const photo = gallery.photos[next - 1];
      const candidate = new Image();
      candidate.src = photo.src;
      try { await candidate.decode(); }
      catch { if (request === gallery.request) { gallery.paused = true; galleryControls(gallery); } return; }
      if (request !== gallery.request) return;
      gallery.extra.src = photo.src;
      gallery.extra.alt = photo.alt;
      gallery.extra.hidden = false;
      gallery.picture.hidden = true;
      gallery.caption.textContent = photo.alt;
    }
    gallery.current = next;
    galleryControls(gallery);
    scheduleGallery(gallery);
  }
  function chooseGallery() {
    const next = galleries.filter(gallery => gallery.visible > 0).sort((a, b) => b.visible - a.visible)[0] || null;
    if (next !== activeGallery) {
      if (activeGallery) { clearTimeout(activeGallery.timer); ++activeGallery.request; }
      activeGallery = next;
      if (next) showGallery(next, 0);
    } else if (next) scheduleGallery(next);
  }
  galleries.forEach(gallery => {
    galleryControls(gallery);
    gallery.element.querySelector('[data-gallery-prev]').addEventListener('click', () => showGallery(gallery, gallery.current - 1));
    gallery.element.querySelector('[data-gallery-next]').addEventListener('click', () => showGallery(gallery, gallery.current + 1));
    gallery.play.addEventListener('click', () => { gallery.paused = !gallery.paused; if (gallery.paused) ++gallery.request; galleryControls(gallery); scheduleGallery(gallery); });
    gallery.element.addEventListener('focusin', () => { clearTimeout(gallery.timer); ++gallery.request; });
    gallery.element.addEventListener('focusout', () => setTimeout(() => scheduleGallery(gallery), 0));
  });
  if (galleries.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { galleries.find(gallery => gallery.element === entry.target).visible = entry.intersectionRatio; });
      chooseGallery();
    }, { threshold: [0, .1, .25, .5, .75, 1] });
    galleries.forEach(gallery => observer.observe(gallery.element));
  }
  let galleryMenuOpen = menuOpen;
  syncHero = () => {
    if (menuOpen && !galleryMenuOpen) galleries.forEach(gallery => { ++gallery.request; });
    galleryMenuOpen = menuOpen;
    galleries.forEach(scheduleGallery);
  };
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) galleries.forEach(gallery => { ++gallery.request; });
    galleries.forEach(scheduleGallery);
  });
  window.addEventListener('hashchange', () => {
    const target = galleries.find(gallery => gallery.element.closest('section').id === location.hash.slice(1));
    if (target) showGallery(target, 0);
  });
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) galleries.forEach(gallery => { gallery.paused = true; ++gallery.request; galleryControls(gallery); scheduleGallery(gallery); });
  });
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const slides = [...document.querySelectorAll('[data-slide]')];
  const controls = document.querySelector('.slideshow-controls');
  const playback = document.querySelector('#slide-play');
  let current = 0;
  let manuallyPaused = reducedMotion.matches;
  let timer;
  let slideRequest = 0;
  let requestedSlide = 0;
  let transitionTimer;
  const slideLoads = new Map();
  let heroVisible = true;

  function schedule() {
    clearTimeout(timer);
    const stopped = manuallyPaused || document.hidden || !heroVisible || menuOpen;
    hero.classList.toggle('is-motion-paused', stopped || reducedMotion.matches);
    const focused = hero.contains(document.activeElement) && document.activeElement !== playback && document.activeElement.matches(':focus-visible');
    if (!stopped && !focused) {
      timer = setTimeout(() => changeSlide(1), 6000);
    }
  }
  syncHero = schedule;
  function updatePlayback() {
    playback.setAttribute('aria-label', english ? (manuallyPaused ? 'Resume slideshow' : 'Pause slideshow') : (manuallyPaused ? 'Diashow fortsetzen' : 'Diashow pausieren'));
    playback.firstElementChild.textContent = manuallyPaused ? '▷' : 'Ⅱ';
    schedule();
  }
  function loadSlide(index) {
    if (slideLoads.has(index)) return slideLoads.get(index);
    const image = slides[index].querySelector('img');
    const ready = (async () => {
      if (image.dataset.src) {
        slides[index].querySelectorAll('source[data-srcset]').forEach(source => {
          source.srcset = source.dataset.srcset;
        });
        image.srcset = image.dataset.srcset;
        image.src = image.dataset.src;
        await image.decode();
        delete image.dataset.src;
      }
    })();
    slideLoads.set(index, ready);
    ready.catch(() => slideLoads.delete(index));
    return ready;
  }
  async function changeSlide(direction) {
    clearTimeout(timer);
    const request = ++slideRequest;
    requestedSlide = (requestedSlide + direction + slides.length) % slides.length;
    const next = requestedSlide;
    try {
      await loadSlide(next);
      if (request !== slideRequest) return;
      clearTimeout(transitionTimer);
      slides.forEach(slide => slide.classList.remove('is-leaving'));
      if (next !== current) {
        const outgoing = slides[current];
        outgoing.classList.add('is-leaving');
        outgoing.classList.remove('is-active');
        outgoing.setAttribute('aria-hidden', 'true');
        slides[next].classList.add('is-active');
        slides[next].removeAttribute('aria-hidden');
        current = next;
        document.querySelector('#slide-number').textContent = String(current + 1).padStart(2, '0');
        document.querySelector('.slide-count').setAttribute('aria-label', english ? `Image ${current + 1} of ${slides.length}` : `Bild ${current + 1} von ${slides.length}`);
        // Keep the outgoing photograph moving throughout the dissolve.
        transitionTimer = setTimeout(() => outgoing.classList.remove('is-leaving'), reducedMotion.matches ? 0 : 1200);
      }
    } catch {
      if (request !== slideRequest) return;
      requestedSlide = current;
    } finally {
      if (request === slideRequest) schedule();
    }
  }
  // Warm the remaining images after the initial page load, before the first change.
  function warmSlides() { slides.forEach((_, index) => { loadSlide(index).catch(() => {}); }); }
  if (document.readyState === 'complete') warmSlides();
  else window.addEventListener('load', warmSlides, { once: true });
  controls.hidden = false;
  document.querySelector('#slide-prev').addEventListener('click', () => changeSlide(-1));
  document.querySelector('#slide-next').addEventListener('click', () => changeSlide(1));
  playback.addEventListener('click', () => { manuallyPaused = !manuallyPaused; updatePlayback(); });
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
// Expose the public catalog to supporting browser assistants without submitting enquiries.
(() => {
  const context = document.modelContext || navigator.modelContext;
  if (!context?.registerTool) return;
  context.registerTool({
    name: 'get_rail_catalog',
    description: 'Read RAIL bicycle models, specifications, CHF frame guide prices and official bilingual page links. No enquiry or order is submitted.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true },
    async execute() {
      const response = await fetch('/api/catalog', { credentials: 'omit' });
      if (!response.ok) throw new Error('The public RAIL catalog is temporarily unavailable.');
      const catalog = await response.json();
      return { content: [{ type: 'text', text: JSON.stringify(catalog) }] };
    }
  });
})();
