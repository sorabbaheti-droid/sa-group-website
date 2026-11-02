// Procedural 3D castings for the Standard Alloys India website (three.js r170).
// Shapes are simplified stand-ins for real parts (cone crusher mantle, concave ring,
// impact crusher blow bar, crusher hammer, VRM table liner) until CAD/scan models arrive.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';

// ---------- scanned parts: simplified, scale-free shells (not the customer's CAD) ----------
const MODELS = new URL('../models/', import.meta.url), cache = {};
function loadModel(name) {
  return cache[name] ||= fetch(new URL(name + '.bin', MODELS)).then(r => r.arrayBuffer()).then(buf => {
    const dv = new DataView(buf), nv = dv.getUint32(4, true), nf = dv.getUint32(8, true);
    const q = new Int16Array(buf, 12, nv * 3), pos = new Float32Array(nv * 3);
    for (let i = 0; i < q.length; i++) pos[i] = q[i] * 1.3 / 32767;
    const off = 12 + nv * 6, idx = nv < 65536 ? new Uint16Array(buf.slice(off, off + nf * 6)) : new Uint32Array(buf.slice(off, off + nf * 12));
    let g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setIndex(new THREE.BufferAttribute(idx, 1));
    g = toCreasedNormals(g, 0.6);
    return g;
  });
}
function scanned(name, label, rot = [0, 0, 0]) {
  return { label, build() {
    const grp = new THREE.Group(), mesh = new THREE.Mesh(new THREE.BufferGeometry());
    mesh.rotation.set(...rot); grp.add(mesh);
    loadModel(name).then(g => { mesh.geometry.dispose(); mesh.geometry = g; });
    return grp;
  } };
}

// ---------- surface textures drawn in code (cast skin vs machined) ----------
function noiseCanvas(size, fn) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const g = c.getContext('2d');
  const img = g.createImageData(size, size);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    const v = fn(x, y);
    const i = (y * size + x) * 4;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}
let castRough, castBump, machinedRough;
function textures() {
  if (castRough) return;
  // sand-cast skin: fine grain plus a few larger pits
  const rnd = (x, y) => { const s = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453; return s - Math.floor(s); };
  castRough = noiseCanvas(256, (x, y) => 150 + rnd(x, y) * 90);
  castBump = noiseCanvas(256, (x, y) => {
    let v = rnd(x, y) * 120 + 70;
    if (rnd(x * 0.31 | 0, y * 0.31 | 0) > 0.985) v -= 60;
    return Math.max(0, Math.min(255, v));
  });
  // machined: turning marks running one way
  machinedRough = noiseCanvas(256, (x, y) => 70 + ((Math.sin(y * 1.7) * 0.5 + 0.5) * 50) + rnd(x, y) * 20);
  castRough.repeat.set(4, 4); castBump.repeat.set(4, 4); machinedRough.repeat.set(1, 12);
}

export const FINISHES = {
  cast: { label: 'As cast', make: () => new THREE.MeshPhysicalMaterial({ color: 0x5b6065, metalness: 0.9, roughness: 0.55, roughnessMap: castRough, bumpMap: castBump, bumpScale: 0.6, envMapIntensity: 1.0 }) },
  machined: { label: 'Machined', make: () => new THREE.MeshPhysicalMaterial({ color: 0xa9adb2, metalness: 1.0, roughness: 0.22, roughnessMap: machinedRough, clearcoat: 0.3, clearcoatRoughness: 0.3, envMapIntensity: 1.25 }) },
  primer: { label: 'Primer', make: () => new THREE.MeshPhysicalMaterial({ color: 0x8c2a1a, metalness: 0.15, roughness: 0.68, bumpMap: castBump, bumpScale: 0.25, envMapIntensity: 0.7 }) },
  hot: { label: 'Fresh from the quench', make: () => new THREE.MeshPhysicalMaterial({ color: 0x1e1410, metalness: 0.7, roughness: 0.45, emissive: 0xff4a0c, emissiveIntensity: 0.9, emissiveMap: castRough, bumpMap: castBump, bumpScale: 0.6 }) },
};

// ---------- geometry ----------
function lathe(points, segs = 160) {
  const g = new THREE.LatheGeometry(points.map(([x, y]) => new THREE.Vector2(x, y)), segs);
  g.computeVertexNormals();
  return g;
}
function bevelExtrude(shape, depth, bevel = 0.04) {
  const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 3, curveSegments: 32 });
  g.center();
  return g;
}

export const PARTS = {
  mantle: scanned('mantle', 'Cone crusher mantle'),
  concave: scanned('concave', 'Cone crusher concave'),
  head: scanned('head', 'Cone crusher head'),
  jaw: scanned('jaw', 'Jaw plate', [0, 0, 0]),
  cheek: scanned('cheek', 'Cheek plate'),
  trunnion: scanned('trunnion', 'Ball mill trunnion'),
  blowbar: {
    label: 'Impact crusher blow bar',
    weight: '310 kg',
    build() {
      const s = new THREE.Shape();
      // cross-section with two wear faces and a clamping groove
      s.moveTo(-0.32, -0.55); s.lineTo(0.32, -0.55); s.lineTo(0.34, -0.2); s.lineTo(0.22, -0.12); s.lineTo(0.22, 0.12);
      s.lineTo(0.34, 0.2); s.lineTo(0.32, 0.55); s.lineTo(-0.32, 0.55); s.lineTo(-0.34, 0.2); s.lineTo(-0.22, 0.12);
      s.lineTo(-0.22, -0.12); s.lineTo(-0.34, -0.2); s.closePath();
      const g = bevelExtrude(s, 2.4, 0.03);
      const m = new THREE.Mesh(g);
      m.rotation.y = Math.PI / 2; m.rotation.z = 0.12;
      const grp = new THREE.Group(); grp.add(m); return grp;
    },
  },
  hammer: {
    label: 'Crusher hammer',
    weight: '95 kg',
    build() {
      const s = new THREE.Shape();
      s.moveTo(-0.38, -0.95); s.lineTo(0.38, -0.95); s.lineTo(0.42, 0.05); s.quadraticCurveTo(0.42, 0.62, 0.0, 0.66);
      s.quadraticCurveTo(-0.42, 0.62, -0.42, 0.05); s.closePath();
      const hole = new THREE.Path(); hole.absarc(0, 0.22, 0.17, 0, Math.PI * 2, true); s.holes.push(hole);
      const g = bevelExtrude(s, 0.5, 0.05);
      const grp = new THREE.Group(); const m = new THREE.Mesh(g); m.scale.setScalar(1.25); grp.add(m); return grp;
    },
  },
  table: {
    label: 'VRM table liner segment',
    weight: '1,200 kg',
    build() {
      // annular segment with a dished grinding track
      const shape = new THREE.Shape();
      const r0 = 0.55, r1 = 1.35, a0 = -0.55, a1 = 0.55;
      shape.absarc(0, 0, r1, a0, a1, false);
      shape.lineTo(Math.cos(a1) * r0, Math.sin(a1) * r0);
      shape.absarc(0, 0, r0, a1, a0, true);
      shape.closePath();
      const g = new THREE.ExtrudeGeometry(shape, { depth: 0.32, bevelEnabled: true, bevelThickness: 0.04, bevelSize: 0.04, bevelSegments: 3, curveSegments: 48 });
      g.center();
      const m = new THREE.Mesh(g); m.rotation.x = -Math.PI / 2.4;
      const grp = new THREE.Group(); grp.add(m); return grp;
    },
  },
};

// ---------- a small viewer ----------
export function createViewer(canvas, opts = {}) {
  textures();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: !!opts.preserve });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = opts.exposure ?? 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(opts.fov ?? 30, 1, 0.1, 100);
  camera.position.set(0, 0.5, opts.distance ?? 6.2);
  camera.lookAt(0, 0, 0);
  const key = new THREE.DirectionalLight(0xffffff, opts.keyLight ?? 2.2); key.position.set(3, 4, 5); scene.add(key);
  const rim = new THREE.DirectionalLight(opts.rimColor ?? 0xffffff, opts.rimLight ?? 1.4); rim.position.set(-4, 1.5, -3); scene.add(rim);

  const holder = new THREE.Group(); scene.add(holder);
  let part = null, finish = opts.finish || 'cast', partId = opts.part || 'mantle';
  let rotY = opts.startRotation ?? -0.5, rotX = 0.18, velY = 0, dragging = false, lastX = 0, lastY = 0, idle = true;
  let targetScale = 1, curScale = 1;

  function setPart(id) {
    partId = id;
    if (part) { holder.remove(part); part.traverse(o => { if (o.geometry) o.geometry.dispose(); }); }
    part = PARTS[id].build();
    const mat = FINISHES[finish].make();
    part.traverse(o => { if (o.isMesh) o.material = mat; });
    holder.add(part);
    curScale = 0.82;
  }
  function setFinish(f) {
    finish = f;
    const mat = FINISHES[f].make();
    part && part.traverse(o => { if (o.isMesh) { o.material.dispose(); o.material = mat; } });
  }
  function setScale(s) { targetScale = s; }
  setPart(partId);

  function resize() {
    const r = canvas.getBoundingClientRect();
    const w = Math.max(1, r.width), h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(canvas); resize();

  if (opts.interactive !== false) {
    canvas.style.touchAction = 'pan-y';
    canvas.addEventListener('pointerdown', e => { dragging = true; idle = false; lastX = e.clientX; lastY = e.clientY; canvas.setPointerCapture(e.pointerId); canvas.style.cursor = 'grabbing'; });
    canvas.addEventListener('pointermove', e => {
      if (!dragging) return;
      const dx = e.clientX - lastX, dy = e.clientY - lastY; lastX = e.clientX; lastY = e.clientY;
      velY = dx * 0.008; rotY += velY; rotX = Math.max(-0.5, Math.min(0.9, rotX + dy * 0.005));
    });
    const end = () => { dragging = false; canvas.style.cursor = 'grab'; setTimeout(() => { idle = true; }, 2500); };
    canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end);
    canvas.style.cursor = 'grab';
  }
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let visible = true, external = 0;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
  function frame() {
    requestAnimationFrame(frame);
    if (!visible || parseFloat(canvas.style.opacity) === 0) return;
    if (!dragging) { velY *= 0.94; rotY += velY; if (idle && !reduce) rotY += 0.0035; }
    curScale += (targetScale - curScale) * 0.08;
    holder.rotation.set(rotX + external * 0.4, rotY + external * 1.2, 0);
    holder.scale.setScalar(curScale);
    renderer.render(scene, camera);
  }
  frame();
  return { setPart, setFinish, setScale, setExternal: v => { external = v; }, get part() { return partId; }, renderer, camera };
}
