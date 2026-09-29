let metalState;
async function setupMetal() {
  await waitFonts();
  el('metal_sub').textContent = P.sub;
  const s = makeRenderer('metal', [.19, .5, 1.25]);
  const { R, scene, cam } = s;
  R.toneMapping = THREE.ACESFilmicToneMapping;
  R.toneMappingExposure = .82;
  scene.background = new THREE.Color(0x020305);
  cam.fov = 34; cam.updateProjectionMatrix();
  const studio = new StudioEnv();
  const pmrem = new THREE.PMREMGenerator(R);
  const env = pmrem.fromScene(studio, .025);
  scene.environment = env.texture;
  studio.dispose(); pmrem.dispose();
  // A genuine typeface is outlined at runtime: counters, curves, kerning and
  // arbitrary user wording are preserved, rather than a hand-built alphabet.
  const response = await fetch('https://cdn.jsdelivr.net/npm/@fontsource/inter-tight@5.0.8/files/inter-tight-latin-800-normal.woff');
  if (!response.ok) throw new Error('Could not load title outline font');
  const font = opentype.parse(await response.arrayBuffer());
  const palette = {
    gold: { face: 0xeac17a, side: 0xc79952, light: 0xffddb0, dust: '232,190,127' },
    silver: { face: 0xdde5ed, side: 0xabb9cb, light: 0xe5f3ff, dust: '196,217,237' },
    copper: { face: 0xeaa17e, side: 0xbf7153, light: 0xffc3a4, dust: '225,164,133' }
  };
  const colors = palette[P.metal] || palette.gold;
  const face = new THREE.MeshStandardMaterial({ color: colors.face, metalness: 1, roughness: .215, envMapIntensity: 1.85 });
  const side = new THREE.MeshStandardMaterial({ color: colors.side, metalness: 1, roughness: .155, envMapIntensity: 2.05 });
  // Very fine machining marks catch grazing light without dirtying the face.
  const scratch = document.createElement('canvas'); scratch.width = scratch.height = 256;
  const ctx = scratch.getContext('2d');
  ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 700; i++) {
    const v = Math.floor(109 + rnd(i * 2.13) * 38);
    ctx.strokeStyle = `rgba(${v},${v},${v},.36)`; ctx.lineWidth = .45;
    const x = rnd(i + 70) * 256, y = rnd(i + 40) * 256;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 8 + rnd(i + 3) * 50, y + .4); ctx.stroke();
  }
  const bump = new THREE.CanvasTexture(scratch);
  bump.wrapS = bump.wrapT = THREE.RepeatWrapping; bump.repeat.set(3, 3);
  face.bumpMap = bump; face.bumpScale = .0012;
  const title = new THREE.Group(); scene.add(title);
  const lines = Array.isArray(P.lines) ? P.lines.map(String) : [String(P.lines)];
  const meshes = [];
  lines.forEach((line, row) => {
    const outline = font.getPath(line, 0, 0, 1, { kerning: true });
    const path = new THREE.ShapePath();
    for (const c of outline.commands) {
      if (c.type === 'M') path.moveTo(c.x, -c.y);
      else if (c.type === 'L') path.lineTo(c.x, -c.y);
      else if (c.type === 'Q') path.quadraticCurveTo(c.x1, -c.y1, c.x, -c.y);
      else if (c.type === 'C') path.bezierCurveTo(c.x1, -c.y1, c.x2, -c.y2, c.x, -c.y);
      else if (c.type === 'Z') path.currentPath.closePath();
    }
    const shapes = path.toShapes(false);
    if (!shapes.length) return;
    const geometry = new THREE.ExtrudeGeometry(shapes, {
      depth: .13, bevelEnabled: true, bevelThickness: .018, bevelSize: .013,
      bevelSegments: 4, steps: 1, curveSegments: 12
    });
    geometry.computeBoundingBox();
    const box = geometry.boundingBox;
    geometry.translate(-(box.min.x + box.max.x) / 2, -row * .97, -.065);
    const mesh = new THREE.Mesh(geometry, [face, side]);
    title.add(mesh); meshes.push(mesh);
  });
  if (meshes.length) {
    const bounds = new THREE.Box3().setFromObject(title);
    const size = bounds.getSize(new THREE.Vector3());
    const center = bounds.getCenter(new THREE.Vector3());
    title.children.forEach(m => m.position.sub(center));
    // Fit both the longest line and the whole stack, retaining a common font size.
    title.scale.setScalar(Math.min(10.8 / size.x, 4.25 / size.y));
  }
  s.title = title;
  const key = new THREE.DirectionalLight(0xffedd7, 1.25); key.position.set(-4, 7, 8); scene.add(key);
  const rim = new THREE.DirectionalLight(0x9bbfe8, 1.65); rim.position.set(6, 2, -2); scene.add(rim);
  const sweep = new THREE.SpotLight(colors.light, 14, 35, .43, .8, 1);
  sweep.position.set(-8, 4, 7); sweep.target.position.set(-4, 0, 0);
  scene.add(sweep, sweep.target); s.sweep = sweep;
  // A large, almost black cyclorama picks up a quiet pool behind the lettering.
  const backdrop = new THREE.Mesh(new THREE.PlaneGeometry(80, 40), new THREE.ShaderMaterial({
    uniforms: { tint: { value: new THREE.Color(colors.face) } },
    vertexShader: `varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `varying vec2 v;uniform vec3 tint;
      void main(){vec2 p=(v-.5)*vec2(5.,3.);float pool=exp(-dot(p,p)*8.);
        gl_FragColor=vec4(vec3(.003,.004,.007)+tint*pool*.018,1.);}`
  }));
  backdrop.position.z = -5; scene.add(backdrop);
  const dustCount = 320, positions = new Float32Array(dustCount * 3);
  for (let i = 0; i < dustCount; i++) {
    positions[i * 3] = (rnd(i * 3 + 1) - .5) * 22;
    positions[i * 3 + 1] = (rnd(i * 3 + 2) - .5) * 12;
    positions[i * 3 + 2] = (rnd(i * 3 + 3) - .5) * 11;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const dust = new THREE.Points(geometry, new THREE.PointsMaterial({
    size: .028, map: dotTex(colors.dust), color: colors.face, transparent: true,
    opacity: .22, depthWrite: false, blending: THREE.AdditiveBlending
  }));
  scene.add(dust); s.dust = dust;
  return s;
}
async function render(frame, totalFrames, fps) {
  if (!metalState) metalState = setupMetal();
  const s = await metalState, t = frame / fps, q = clamp01(t / D);
  s.cam.position.set(lerp(-1.3, .55, q), lerp(.8, .25, q), lerp(14.5, 12.7, ease(q)));
  s.cam.lookAt(0, -.22, 0);
  s.title.rotation.set(.018, lerp(-.065, .035, q), -.012);
  const sweep = ease(seg(t, D * .08, D * .91));
  s.sweep.position.set(lerp(-8, 8, sweep), 3.5, 6);
  s.sweep.target.position.set(lerp(-6, 6, sweep), .2, 0);
  s.dust.position.set(q * .3, q * .2, 0); s.dust.rotation.z = q * .016;
  el('metal_sub').style.opacity = ease(seg(t, D * .25, D * .51)) * .85;
  s.composer.render();
  beatFade(t, D, 0.3, 0.3);
}
