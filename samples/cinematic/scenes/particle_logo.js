let particleScene;
async function setupParticles() {
  await waitFonts();
  const s = makeRenderer('particle-stage', [1.05, 0.42, 0.32]);
  s.scene.background = new THREE.Color(0x000001);
  const measure = document.createElement('canvas').getContext('2d');
  measure.font = '800 240px "Inter Tight"';
  const fontSize = Math.min(240, 1050 / Math.max(1, measure.measureText(String(P.word)).width) * 240);
  const letters = textTargets(String(P.word), `800 ${fontSize}px "Inter Tight"`, 1120, 360, 2);
  if (!letters.length) letters.push([560, 180]);
  // Rasterise arbitrary SVG path data in its own bounds; no assumed viewBox.
  const mask = document.createElement('canvas'); mask.width = mask.height = 600;
  const g = mask.getContext('2d');
  let data = String(P.logo);
  if (data === 'star') {
    data = Array.from({ length: 10 }, (_, i) => {
      const a = i * Math.PI / 5 - Math.PI / 2, r = i % 2 ? 116 : 280;
      return `${i ? 'L' : 'M'}${300 + Math.cos(a) * r},${300 + Math.sin(a) * r}`;
    }).join(' ') + ' Z';
  }
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  const path = document.createElementNS(svg.namespaceURI, 'path'); path.setAttribute('d', data);
  svg.style.cssText = 'position:absolute;visibility:hidden;width:1px;height:1px';
  svg.appendChild(path); document.body.appendChild(svg);
  const b = path.getBBox(), scale = 540 / Math.max(b.width, b.height, 1);
  g.translate(300, 300); g.scale(scale, scale); g.translate(-b.x - b.width / 2, -b.y - b.height / 2);
  g.fillStyle = '#fff'; g.fill(new Path2D(data)); svg.remove();
  const pixels = g.getImageData(0, 0, 600, 600).data, logo = [];
  for (let y = 0; y < 600; y += 2) for (let x = 0; x < 600; x += 2)
    if (pixels[(y * 600 + x) * 4 + 3] > 128) logo.push([x, y]);
  if (!logo.length) throw new Error('P.logo must be star or a non-empty filled SVG path');
  // Fit the sampled silhouettes, rather than their padded raster canvases.
  const bounds = (points) => points.reduce((b, p) => [Math.min(b[0], p[0]),
    Math.min(b[1], p[1]), Math.max(b[2], p[0]), Math.max(b[3], p[1])],
    [Infinity, Infinity, -Infinity, -Infinity]);
  const wb = bounds(letters), lb = bounds(logo);
  const wordScale = Math.min(10.4 / Math.max(1, wb[2] - wb[0]), 5.8 / Math.max(1, wb[3] - wb[1]));
  const logoScale = 9.9 / Math.max(1, lb[2] - lb[0]);
  const logoHeightScale = Math.min(logoScale, 7.6 / Math.max(1, lb[3] - lb[1]));
  const count = 32000, geo = new THREE.BufferGeometry();
  const cloud = new Float32Array(count * 3), word = new Float32Array(count * 3);
  const emblem = new Float32Array(count * 3), seeds = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    const angle = rnd(i + 3) * Math.PI * 2, radius = Math.pow(rnd(i + 91), 0.4);  // 0.65 packed the core so densely that additive blending blew it to white
    const arm = angle + radius * 5.8;
    cloud.set([Math.cos(arm) * radius * 12, Math.sin(arm) * radius * 5.5,
      (rnd(i + 209) - 0.5) * 9 + Math.sin(arm * 2) * 0.7], i * 3);
    const a = letters[Math.floor(rnd(i * 3.73 + 8) * letters.length)];
    word.set([(a[0] - (wb[0] + wb[2]) / 2 + rnd(i + 40) * 2 - 1) * wordScale,
      ((wb[1] + wb[3]) / 2 - a[1] + rnd(i + 88) * 2 - 1) * wordScale, (rnd(i + 97) - 0.5) * 0.32], i * 3);
    const l = logo[Math.floor(rnd(i * 7.17 + 26) * logo.length)];
    emblem.set([(l[0] - (lb[0] + lb[2]) / 2 + rnd(i + 51) * 2 - 1) * logoScale,
      ((lb[1] + lb[3]) / 2 - l[1] + rnd(i + 73) * 2 - 1) * logoHeightScale, (rnd(i + 64) - 0.5) * 0.48], i * 3);
    seeds[i] = rnd(i * 1.33 + 20);
  }
  geo.setAttribute('position', new THREE.BufferAttribute(cloud, 3));
  geo.setAttribute('word', new THREE.BufferAttribute(word, 3));
  geo.setAttribute('emblem', new THREE.BufferAttribute(emblem, 3));
  geo.setAttribute('seed', new THREE.BufferAttribute(seeds, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { u: { value: 0 }, focus: { value: 15 } }, transparent: true, depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexShader: `attribute vec3 word; attribute vec3 emblem; attribute float seed;
      uniform float u; uniform float focus; varying vec3 tint; varying float energy; varying float blur;
      void main() {
        float gather = smoothstep(.12 + seed*.07, .39 + seed*.035, u);
        float morph = smoothstep(.59 + seed*.045, .83 + seed*.025, u);
        vec3 p = position;
        float a = u*.48; p.xy = mat2(cos(a),-sin(a),sin(a),cos(a))*p.xy;
        p.y += sin(seed*45. + u*5.)*.22;
        p = mix(p, word, gather);
        p = mix(p, emblem, morph);
        float arc = sin(morph*3.14159265);
        p.x += sin(seed*24.)*arc*1.9;
        p.y += cos(seed*24.)*arc*1.6;
        p.z += sin(seed*17.)*arc*2.8;
        vec4 mv = modelViewMatrix*vec4(p,1.);
        // Focus follows the logo plane; nearer motes spread into soft bokeh.
        blur = min(8., abs(-mv.z - focus)*1.05);
        float sizeSeed = fract(seed*137.31);
        gl_PointSize = clamp((3.0 + sizeSeed*2.0 + blur*1.65)*15./(-mv.z),2.5,24.);
        gl_Position = projectionMatrix*mv;
        vec3 gold = vec3(1., .59, .16);
        vec3 violet = vec3(.58, .28, 1.);
        vec3 cyan = vec3(.16, .78, 1.);
        tint = seed < .55 ? gold : (seed < .79 ? violet : cyan);
        energy = mix(2.4,1.8,gather)*(1.+step(.986,seed)*1.6);
        energy *= (.88 + .12*sin(seed*91.+u*9.))/(1.+blur*.28);
      }`,
    fragmentShader: `varying vec3 tint; varying float energy; varying float blur;
      void main() {
        float r = length(gl_PointCoord-.5)*2.; if(r>1.) discard;
        float defocus = clamp(blur/6.,0.,1.);
        float edge = 1.-smoothstep(.72,1.,r);
        float core = exp(-r*r*mix(16.,4.,defocus));
        float halo = exp(-r*r*3.8)*.20;
        vec3 light = mix(vec3(1.,.94,.80),tint,defocus*.38)*core + tint*halo;
        // HDR emission crosses the bloom threshold even for ordinary motes.
        gl_FragColor = vec4(light*energy,edge);
      }`
  });
  s.points = new THREE.Points(geo, mat); s.points.frustumCulled = false; s.scene.add(s.points);
  // Out-of-focus foreground motes give the typography a real depth plane.
  const dust = new Float32Array(1800 * 3);
  for (let i = 0; i < 1800; i++) dust.set([(rnd(i + 410) - .5) * 32, (rnd(i + 620) - .5) * 18, (rnd(i + 820) - .5) * 15], i * 3);
  const dg = new THREE.BufferGeometry(); dg.setAttribute('position', new THREE.BufferAttribute(dust, 3));
  s.dust = new THREE.Points(dg, new THREE.PointsMaterial({ color: 0x829fc8, size: .033,
    map: dotTex('120,162,220'), transparent: true, opacity: .33, blending: THREE.AdditiveBlending, depthWrite: false }));
  s.scene.add(s.dust);
  return s;
}
async function render(frame, totalFrames, fps) {
  if (!particleScene) particleScene = setupParticles();
  const s = await particleScene, t = frame / fps, u = seg(t, 0, D);
  s.points.material.uniforms.u.value = u;
  s.points.rotation.y = lerp(-.045, .06, u);
  s.dust.rotation.z = u * .07;
  s.cam.position.set(lerp(.45, -.25, u), lerp(.12, -.08, u), lerp(16.2, 14.4, ease(u)));
  s.cam.lookAt(0, 0, 0);
  s.points.material.uniforms.focus.value = s.cam.position.length();
  s.composer.render();
  beatFade(t, D, 0.3, 0.3);
}
