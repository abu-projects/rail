(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');

  function initLoader() {
    const loader = document.querySelector('.site-loader');
    const fill = loader.querySelector('.loader-fill');
    const percent = loader.querySelector('.loader-percent');
    const started = performance.now();
    let imageReady = false;
    let bikeReady = location.protocol === 'file:' || root.classList.contains('webgl-ready') || root.classList.contains('webgl-failed');
    let finished = false;
    let progress = 0;
    let timeout;

    function showProgress(value) {
      progress = Math.max(progress, value);
      fill.style.width = `${progress}%`;
      percent.textContent = `${progress}%`;
    }

    function finish() {
      if (finished || !imageReady || !bikeReady) return;
      finished = true;
      clearTimeout(timeout);
      showProgress(100);
      window.setTimeout(() => {
        root.classList.remove('is-loading');
        root.classList.add('is-loaded');
        window.setTimeout(() => root.classList.remove('is-loaded'), 700);
      }, Math.max(0, 750 - (performance.now() - started)));
    }

    function imageDone() {
      imageReady = true;
      showProgress(bikeReady ? 100 : 45);
      finish();
    }

    function bikeDone() {
      bikeReady = true;
      showProgress(imageReady ? 100 : 90);
      finish();
    }

    window.addEventListener('rail-bike-ready', bikeDone, { once: true });
    window.addEventListener('rail-bike-error', bikeDone, { once: true });
    const heroImage = new Image();
    heroImage.src = new URL('assets/hero-road.jpg', location.href).href;
    if (heroImage.decode) heroImage.decode().then(imageDone, imageDone);
    else {
      heroImage.onload = imageDone;
      heroImage.onerror = imageDone;
    }
    // A failed module import cannot report an error to this script.
    // In that case reveal the photographic fallback instead of trapping visitors.
    timeout = window.setTimeout(() => {
      imageReady = true;
      bikeReady = true;
      finish();
    }, 30000);
  }
  initLoader();

  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  const mobile = matchMedia('(max-width: 767px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  menu.hidden = false;

  function closeMenu(returnFocus = false) {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    document.body.classList.remove('menu-open');
    if (returnFocus) menu.focus();
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });

  const story = document.querySelector('[data-product-story]');
  const stage = document.querySelector('.product-stage');
  const landscape = document.querySelector('.hero-landscape');
  const bike = document.querySelector('.persistent-bike-scene');
  const bikeImage = bike.querySelector('.hero-bike');
  const asphalt = bike.querySelector('.asphalt-ground');
  const halo = bike.querySelector('.scene-halo');
  const floor = bike.querySelector('.bike-floor');
  const shadow = bike.querySelector('.bike-shadow');
  const main = document.querySelector('main');
  const models = document.querySelector('.models-section');
  const firstModel = document.querySelector('.model-trail');
  const secondModel = document.querySelector('.model-enduro');
  const thirdModel = document.querySelector('.model-gravel');
  const workshop = document.querySelector('.workshop-section');
  const about = document.querySelector('.about-section');
  const contact = document.querySelector('.contact-section');
  const hero = document.querySelector('.hero-copy');
  const intro = document.querySelector('.models-intro');
  const progressBar = document.querySelector('.story-progress span');
  const scrollLink = document.querySelector('.scroll-link');
  let enabled = false;
  let frame = 0;
  let displayY = scrollY;
  const clamp = value => Math.max(0, Math.min(1, value));
  const smooth = value => value * value * (3 - 2 * value);
  const topOf = element => element.getBoundingClientRect().top + scrollY;

  function moveBike(position) {
    const storyTop = topOf(story);
    const storyTravel = Math.max(1, story.offsetHeight - stage.offsetHeight);
    const modelTop = topOf(models);
    const firstModelTop = topOf(firstModel);
    const secondModelTop = topOf(secondModel);
    const thirdModelTop = topOf(thirdModel);
    const workshopTop = topOf(workshop);
    const aboutTop = topOf(about);
    const contactTop = topOf(contact);
    // Keep the angles unwrapped so each scroll interval follows the intended
    // direction. The object rests at its key views, then makes one slow orbit.
    const stops = [
      // Hero: front wheel comes toward the viewer at roughly 30° off head-on.
      { at: storyTop, x: -16, y: 0, scale: 1.06, angle: 0, yaw: -60 },
      { at: storyTop + storyTravel * .2, x: -16, y: 0, scale: 1.06, angle: 0, yaw: -60 },
      // Opening story: ease into a complete side profile and let it breathe.
      { at: storyTop + storyTravel * .78, x: 5, y: 0, scale: .95, angle: 0, yaw: 0 },
      { at: modelTop + innerHeight * .35, x: 5, y: 1, scale: .86, angle: 0, yaw: 0 },
      { at: firstModelTop + innerHeight * .6, x: 5, y: 1, scale: .86, angle: 0, yaw: 0 },
      // Cross the space between model cards gradually while showing the rear.
      { at: secondModelTop + innerHeight * .45, x: -40, y: 2, scale: .83, angle: 0, yaw: 55 },
      { at: secondModelTop + innerHeight * .72, x: -40, y: 2, scale: .83, angle: 0, yaw: 55 },
      // A broad, continuous orbit through the next story panel.
      { at: thirdModelTop + innerHeight * .5, x: -46, y: 2, scale: .81, angle: 0, yaw: 130 },
      { at: workshopTop + innerHeight * .52, x: -20, y: 6, scale: .67, angle: 0, yaw: 270 },
      // Settle on the front view in the centre of the closing sections.
      { at: aboutTop + innerHeight * .5, x: -20, y: 6, scale: .52, angle: 0, yaw: 270 },
      { at: contactTop + innerHeight * .5, x: -20, y: 6, scale: .46, angle: 0, yaw: 270 },
      { at: topOf(main) + main.offsetHeight, x: -20, y: 6, scale: .46, angle: 0, yaw: 270 }
    ];
    let before = stops[0];
    let after = stops[stops.length - 1];
    for (let index = 1; index < stops.length; index++) {
      if (position <= stops[index].at) {
        after = stops[index];
        break;
      }
      before = stops[index];
    }
    const amount = smooth(clamp((position - before.at) / Math.max(1, after.at - before.at)));
    const between = key => before[key] + (after[key] - before[key]) * amount;
    bike.style.transform = `translate3d(${between('x')}%, ${between('y')}%, 0) scale(${between('scale')}) rotate(${between('angle')}deg)`;
    const yaw = between('yaw');
    if (window.RailBike3D) window.RailBike3D.setAngle(yaw);
    else bikeImage.style.transform = ((-yaw % 360) + 360) % 360 > 90 && ((-yaw % 360) + 360) % 360 < 270 ? 'scaleX(-1)' : '';
    const exit = topOf(main) + main.offsetHeight - innerHeight * .6;
    bike.style.opacity = String(smooth(clamp((exit - position) / (innerHeight * .5))));
    const groundExit = smooth(clamp((position - storyTop - storyTravel * .16) / (storyTravel * .48)));
    asphalt.style.opacity = String(1 - groundExit);
    asphalt.style.transform = `translate3d(0, ${groundExit * 42}%, 0) scale(${1 + groundExit * .08})`;
    halo.style.opacity = String(.95 - groundExit * .45);
    halo.style.transform = `scale(${1.1 + groundExit * .18})`;
    const secondScene = smooth(clamp((position - modelTop + innerHeight * .15) / innerHeight));
    const floorIn = smooth(clamp((position - storyTop - storyTravel * .6) / (storyTravel * .45)));
    const floorOut = smooth(clamp((position - contactTop + innerHeight * .15) / innerHeight));
    floor.style.opacity = String(floorIn * (1 - floorOut) * .96);
    floor.style.transform = `scale(${.85 + secondScene * .15})`;
    const sideView = Math.abs(Math.cos(yaw * Math.PI / 180));
    shadow.style.opacity = String(.62 + secondScene * .2 + sideView * .15);
    shadow.style.transform = `translate3d(0, ${-secondScene * 5}%, 0) scale(${(.42 + sideView * .58) * (1 - secondScene * .10)}, ${.9 + sideView * .1})`;
  }

  function update() {
    frame = 0;
    if (!enabled && reducedMotion.matches) return;
    displayY += (scrollY - displayY) * .16;
    if (Math.abs(scrollY - displayY) < .35) displayY = scrollY;
    if (!enabled) {
      const start = topOf(story) + innerHeight * .2;
      const end = topOf(story) + story.offsetHeight - innerHeight * .2;
      const progress = clamp((displayY - start) / Math.max(1, end - start));
      if (window.RailBike3D) window.RailBike3D.setAngle(-60 + 60 * smooth(progress));
      if (displayY !== scrollY) frame = requestAnimationFrame(update);
      return;
    }
    const travel = Math.max(1, story.offsetHeight - stage.offsetHeight);
    const p = clamp((displayY - topOf(story)) / travel);
    const heroOut = smooth(clamp((p - .22) / .25));
    const introIn = smooth(clamp((p - .53) / .27));
    const landscapeOut = smooth(clamp((p - .12) / .46));
    moveBike(displayY);
    landscape.style.opacity = String(1 - landscapeOut);
    landscape.style.transform = `scale(${1 + landscapeOut * .035})`;
    hero.style.opacity = String(1 - heroOut);
    hero.style.transform = `translate3d(0, ${-heroOut * 44}px, 0)`;
    hero.style.visibility = heroOut >= .99 ? 'hidden' : 'visible';
    hero.inert = heroOut >= .99;
    intro.style.opacity = String(introIn);
    intro.style.transform = `translate3d(0, ${(1 - introIn) * 35}px, 0)`;
    intro.style.visibility = introIn > 0 ? 'visible' : 'hidden';
    intro.inert = introIn === 0;
    progressBar.style.transform = `scaleX(${p})`;
    scrollLink.style.opacity = String(1 - introIn);
    scrollLink.style.visibility = introIn >= .99 ? 'hidden' : 'visible';
    if (displayY !== scrollY) frame = requestAnimationFrame(update);
  }
  function schedule() {
    if (!frame && !reducedMotion.matches) frame = requestAnimationFrame(update);
  }
  function configure() {
    enabled = innerWidth >= 1024 && !reducedMotion.matches;
    root.classList.toggle('motion-story', enabled);
    closeMenu();
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    displayY = scrollY;
    for (const element of [bike, bikeImage, asphalt, halo, floor, shadow, landscape, hero, intro, progressBar, scrollLink]) element.removeAttribute('style');
    hero.inert = false;
    intro.inert = false;
    if (!reducedMotion.matches) update();
  }
  function revealIntro(event) {
    if (!enabled) return;
    event.preventDefault();
    const travel = Math.max(1, story.offsetHeight - stage.offsetHeight);
    const top = story.getBoundingClientRect().top + scrollY + travel * .82;
    window.scrollTo({ top, behavior: 'smooth' });
    history.replaceState(null, '', '#entdecken');
  }
  scrollLink.addEventListener('click', revealIntro);
  // Keyboard focus reveals its own panel; hidden panels cannot capture Tab focus.
  hero.addEventListener('focusin', () => {
    if (enabled && Number(hero.style.opacity) < 1) window.scrollTo({top:story.offsetTop,behavior:'instant'});
  });
  document.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', configure, { passive: true });
  reducedMotion.addEventListener('change', configure);
  mobile.addEventListener('change', configure);
  window.addEventListener('pageshow', () => { if (!reducedMotion.matches) update(); });
  window.addEventListener('rail-bike-ready', () => { if (!reducedMotion.matches) update(); });
  configure();
  if (location.hash === '#entdecken' && enabled) requestAnimationFrame(() => {
    window.scrollTo({ top: story.offsetTop + (story.offsetHeight - stage.offsetHeight) * .82, behavior: 'instant' });
    update();
  });
})();
