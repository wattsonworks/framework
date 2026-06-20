/* ╔══════════════════════════════════════════════════════════════╗
   ║  LIQUIDEX Framework — "Liquidity Field"                       ║
   ║  Three.js particle field — a quiet map of resting liquidity. ║
   ║  Adapted from the LIQUIDEX site background (Fable) and        ║
   ║  re-tuned for the institutional palette: deep ink + gold.     ║
   ║  Self-contained: a gentle breathing swell, a pointer ripple,  ║
   ║  and a slow camera drift driven by page scroll.               ║
   ╚══════════════════════════════════════════════════════════════╝ */
import * as THREE from "three";

const canvas = document.getElementById("liqfield");
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, powerPreference: "high-performance" });
} catch (e) {
  document.body.classList.add("no-webgl");
}

if (renderer) {
  const isMobile = matchMedia("(max-width: 760px)").matches;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, isMobile ? 1.25 : 1.5));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(56, 1, 0.1, 60);

  /* ── particle grid ── */
  const COLS = isMobile ? 140 : 260;
  const ROWS = isMobile ? 90 : 160;
  const W = 24, D = 17;
  const N = COLS * ROWS;
  const pos = new Float32Array(N * 3);
  const seed = new Float32Array(N);
  let i = 0;
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++, i++) {
      pos[i * 3] = (c / (COLS - 1) - 0.5) * W;
      pos[i * 3 + 1] = 0;
      pos[i * 3 + 2] = -(r / (ROWS - 1)) * D + 1.5;
      seed[i] = Math.random();
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aSeed", new THREE.BufferAttribute(seed, 1));

  const uniforms = {
    uTime:    { value: 0 },
    uPointer: { value: new THREE.Vector2(99, 99) },
    uAmp:     { value: 1 },
    uSize:    { value: (isMobile ? 26 : 30) * (devicePixelRatio > 1.4 ? 1.25 : 1) },
    uDeep:    { value: new THREE.Color("#0a0e14") },
    uCrest:   { value: new THREE.Color("#c6a86b") },
    uHot:     { value: new THREE.Color("#e3d4ad") },
  };

  const mat = new THREE.ShaderMaterial({
    uniforms,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexShader: /* glsl */`
      uniform float uTime, uAmp, uSize;
      uniform vec2 uPointer;
      attribute float aSeed;
      varying float vH, vHot, vFog, vSeed;

      void main(){
        vec3 p = position;
        float t = uTime;

        /* layered swell — the breathing order book */
        float w = 0.0;
        w += 0.34 * sin(p.x * 0.46 + t * 0.42);
        w += 0.24 * sin(p.z * 0.80 - t * 0.34);
        w += 0.14 * sin((p.x + p.z) * 1.15 + t * 0.70);
        w += 0.08 * sin((p.x * 1.8 - p.z * 1.2) + t * 1.10) * aSeed;

        /* pointer ripple */
        float dp = distance(p.xz, uPointer);
        float rip = exp(-dp * dp * 0.50);
        w += 0.40 * rip * sin(dp * 4.5 - t * 3.5);

        p.y += w * uAmp;

        vH   = clamp(w * 0.5 + 0.5, 0.0, 1.0);
        vHot = clamp(rip * 0.9, 0.0, 1.0);
        vSeed = aSeed;

        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        vFog = smoothstep(-28.0, -3.0, mv.z);
        gl_PointSize = uSize * (0.55 + 0.45 * vH) * (1.0 / -mv.z);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: /* glsl */`
      uniform vec3 uDeep, uCrest, uHot;
      varying float vH, vHot, vFog, vSeed;
      void main(){
        vec2 uv = gl_PointCoord - 0.5;
        float d = length(uv);
        float a = smoothstep(0.5, 0.06, d);
        vec3 col = mix(uDeep, uCrest, vH * vH);
        col = mix(col, uHot, vHot);
        col += vSeed * 0.04;
        float alpha = a * (0.10 + 0.42 * vH + 0.28 * vHot) * vFog;
        if (alpha < 0.003) discard;
        gl_FragColor = vec4(col, alpha);
      }`,
  });

  scene.add(new THREE.Points(geo, mat));

  /* ── pointer → world xz (plane y=0) ── */
  const ray = new THREE.Raycaster();
  const planeY = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const ndc = new THREE.Vector2();
  const hit = new THREE.Vector3();
  let targetPtr = new THREE.Vector2(99, 99);
  let parXT = 0, parYT = 0, parX = 0, parY = 0;
  addEventListener("pointermove", (e) => {
    ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    parXT = ndc.x; parYT = ndc.y;
    ray.setFromCamera(ndc, camera);
    if (ray.ray.intersectPlane(planeY, hit)) targetPtr.set(hit.x, hit.z);
  }, { passive: true });

  /* ── scroll progress 0→1 (gentle camera dive) ── */
  let progT = 0, progress = 0;
  addEventListener("scroll", () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    progT = max > 0 ? Math.min(scrollY / max, 1) : 0;
  }, { passive: true });

  /* ── resize ── */
  function resize() {
    const w = innerWidth, h = innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  addEventListener("resize", resize);
  resize();

  /* ── render loop (~60fps cap) ── */
  const clock = new THREE.Clock();
  let raf = null, lastFrame = 0;
  function frame(now) {
    raf = null;
    if (!document.hidden) raf = requestAnimationFrame(frame);
    if (now - lastFrame < 15.5) return;
    lastFrame = now;
    const t = reduced ? 6 : clock.getElapsedTime();

    uniforms.uTime.value = t;
    uniforms.uPointer.value.lerp(targetPtr, 0.06);
    parX += (parXT - parX) * 0.04;
    parY += (parYT - parY) * 0.04;
    progress += (progT - progress) * 0.06;

    camera.position.set(parX * 0.5, 2.4 - progress * 1.05 + parY * 0.20, 5.0 - progress * 1.25);
    camera.lookAt(parX * 0.7, -0.4 - progress * 0.4, -5.5);

    renderer.render(scene, camera);
  }
  function wake() { if (!raf && !document.hidden) raf = requestAnimationFrame(frame); }
  document.addEventListener("visibilitychange", wake);
  wake();
} else {
  document.body.classList.add("no-webgl");
}
