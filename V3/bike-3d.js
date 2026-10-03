import * as THREE from './vendor/three.module.js';
import { GLTFLoader } from './vendor/GLTFLoader.js';

const desktopMount = document.querySelector('.persistent-bike-scene');
const compactMount = document.querySelector('.product-stage > .bike-scene');
let mount = matchMedia('(min-width: 1024px)').matches ? desktopMount : compactMount;

// Keep the photographed bicycle available until the real mesh has loaded.
if (desktopMount && compactMount && 'WebGL2RenderingContext' in window) {
  try {
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.35;
    renderer.domElement.className = 'bike-canvas';
    renderer.domElement.setAttribute('aria-hidden', 'true');
    mount.append(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-3, 3, 1.5, -1.5, .1, 100);
    // The wheel tyres reach slightly below the model origin after placement.
    // Centre the view lower so the orthographic frustum includes both tyres.
    camera.position.set(0, 1.10, 10);
    camera.lookAt(0, 0.95, 0);

    scene.add(new THREE.HemisphereLight(0xdde8d8, 0x1c211c, 2.1));
    const key = new THREE.DirectionalLight(0xfff7e9, 3.6);
    key.position.set(-3.5, 6, 7);
    scene.add(key);
    const fill = new THREE.DirectionalLight(0x98b9a3, 1.9);
    fill.position.set(4, 3, -6);
    scene.add(fill);

    const turntable = new THREE.Group();
    scene.add(turntable);
    let angle = 0;
    let renderedWidth = 0;
    let renderedHeight = 0;

    function render() {
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      if (!width || !height) return;
      if (width !== renderedWidth || height !== renderedHeight) {
        renderer.setSize(width, height, false);
        renderedWidth = width;
        renderedHeight = height;
      }
      const aspect = width / height;
      const vertical = Math.max(2.65, 4.2 / aspect);
      camera.left = -vertical * aspect / 2;
      camera.right = vertical * aspect / 2;
      camera.top = vertical / 2;
      camera.bottom = -vertical / 2;
      camera.updateProjectionMatrix();
      turntable.rotation.y = angle * Math.PI / 180;
      renderer.render(scene, camera);
    }

    function placeCanvas() {
      const nextMount = matchMedia('(min-width: 1024px)').matches ? desktopMount : compactMount;
      if (nextMount !== mount) {
        mount = nextMount;
        mount.append(renderer.domElement);
      }
      render();
    }

    window.RailBike3D = {
      setAngle(value) { angle = value; render(); },
      resize: placeCanvas
    };
    const observer = new ResizeObserver(render);
    observer.observe(desktopMount);
    observer.observe(compactMount);
    window.addEventListener('resize', placeCanvas, { passive: true });

    new GLTFLoader().load(
      './3d-brief/smsm-v2/RAIL_Wichelsee_visual_v2.glb',
      gltf => {
        const model = gltf.scene;
        // The GLB is in metres, centred on the ground between both wheel axles.
        model.scale.setScalar(2.02);
        model.position.y = -0.15;
        model.traverse(object => {
          if (!object.isMesh) return;
          object.frustumCulled = false;
          if (Array.isArray(object.material)) object.material.forEach(material => { material.side = THREE.DoubleSide; });
          else object.material.side = THREE.DoubleSide;
        });
        turntable.add(model);
        render();
        document.documentElement.classList.add('webgl-ready');
        window.dispatchEvent(new Event('rail-bike-ready'));
      },
      undefined,
      error => {
        renderer.domElement.remove();
        console.warn('RAIL 3D model unavailable; keeping image fallback.', error);
        document.documentElement.classList.add('webgl-failed');
        window.dispatchEvent(new Event('rail-bike-error'));
      }
    );
  } catch (error) {
    console.warn('RAIL 3D view unavailable; keeping image fallback.', error);
    document.documentElement.classList.add('webgl-failed');
    window.dispatchEvent(new Event('rail-bike-error'));
  }
} else {
  document.documentElement.classList.add('webgl-failed');
  window.dispatchEvent(new Event('rail-bike-error'));
}
