// requires: objects/Water
// Golden-hour open ocean. The sea is the one from the AI Short Film Fes remake (ystknsh/media PR #5), which got its
// colour right: a bounded sky gradient instead of three's Sky (whose broad white solar halo washed the frame out),
// Water with a real swell, and one display transform at the end (Sky/Water give linear light). Palette moved from
// dawn red-violet to golden hour. P.line is the caption.
let oceanState;
async function setupOcean() {
  await waitFonts();
  const s = makeRenderer('ocean', [0.14, 0.25, 1.1]);
  s.cam.fov = 47; s.cam.near = 0.1; s.cam.far = 250000; s.cam.updateProjectionMatrix();
  // Keep the sky, water reflection and bloom linear; apply exposure only once, at output.
  s.R.toneMapping = THREE.NoToneMapping;
  // mulmocast rewrites only html src attributes to absolute paths, so the texture comes from the hidden <img>
  const normals = await new THREE.TextureLoader().loadAsync(el('ocean_normals').src);
  normals.wrapS = normals.wrapT = THREE.RepeatWrapping;
  normals.anisotropy = Math.min(8, s.R.capabilities.getMaxAnisotropy());
  const sun = new THREE.Vector3(-0.18, 0.04, -1).normalize();
  // A bounded dawn palette avoids the atmospheric Sky shader's broad white solar halo.
  // The same sphere is captured by Water's mirror camera, so the colours reflect in the sea.
  const sky = new THREE.Mesh(new THREE.SphereGeometry(100000, 48, 24), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: { sunDirection: { value: sun } },
    vertexShader: `varying vec3 skyDirection;
      void main(){skyDirection=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `uniform vec3 sunDirection; varying vec3 skyDirection;
      void main(){
        vec3 d=normalize(skyDirection);
        float h=max(d.y,0.);
        vec3 horizon=vec3(1.05,.42,.1), rose=vec3(.62,.28,.12);
        vec3 violet=vec3(.2,.17,.2), blue=vec3(.06,.1,.2);
        vec3 c=mix(horizon,rose,smoothstep(0.,.12,h));
        c=mix(c,violet,smoothstep(.07,.29,h));
        c=mix(c,blue,smoothstep(.22,.52,h));
        float angle=acos(clamp(dot(d,sunDirection),-1.,1.));
        c+=vec3(.5,.24,.05)*exp(-angle*angle/.004);
        float disc=1.-smoothstep(.009,.0105,angle);
        c=mix(c,vec3(3.2,1.25,.25),disc);
        gl_FragColor=vec4(c,1.);
      }`
  }));
  s.scene.add(sky);
  // Dense near-field mesh grades logarithmically into the horizon; no faceted distant grid.
  const geom = new THREE.PlaneGeometry(1, 1, 300, 230);
  const p = geom.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const u = p.getX(i) + 0.5, v = p.getY(i) + 0.5;
    const distance = Math.expm1(v * Math.log(16001));
    p.setXYZ(i, (u - 0.5) * (180 + distance * 3), distance - 65, 0);
  }
  geom.computeBoundingSphere();
  const water = new THREE.Water(geom, { textureWidth: 1024, textureHeight: 512,
    waterNormals: normals, sunDirection: sun, sunColor: 0xffb657,
    waterColor: 0x021219, distortionScale: 2.0 });
  water.rotation.x = -Math.PI / 2; s.scene.add(water); s.water = water;
  water.material.uniforms.size.value = 2.0;
  // Swell displaces real geometry. Its analytic derivatives also tilt the normal-map lighting.
  const swell = `
    float swell(vec2 p) { return .19*sin(dot(p,vec2(.19,.31))+time*.8)
      +.095*sin(dot(p,vec2(-.41,.22))-time*.65)
      +.045*sin(dot(p,vec2(.73,.51))+time*1.1); }
    vec2 slope(vec2 p) { return .19*vec2(.19,.31)*cos(dot(p,vec2(.19,.31))+time*.8)
      +.095*vec2(-.41,.22)*cos(dot(p,vec2(-.41,.22))-time*.65)
      +.045*vec2(.73,.51)*cos(dot(p,vec2(.73,.51))+time*1.1); }
  `;
  water.material.vertexShader = water.material.vertexShader.replace('void main() {', swell + '\nvoid main() {\n vec3 displaced = position; displaced.z += swell(vec2(position.x,-position.y));')
    .replaceAll('vec4( position, 1.0 )', 'vec4( displaced, 1.0 )');
  water.material.fragmentShader = water.material.fragmentShader.replace('void main() {', swell + '\nvoid main() {')
    .replace('vec3 surfaceNormal = normalize( noise.xzy * vec3( 1.5, 1.0, 1.5 ) );',
      'vec2 ds = slope(worldPosition.xz); vec3 surfaceNormal = normalize(noise.xzy * vec3(.72,1.0,.72) + vec3(-ds.x,0.0,-ds.y));')
    .replace('100.0, 2.0, 0.5', '240.0, 4.5, 0.35')
    .replace('float rf0 = 0.3;', 'float rf0 = 0.045;')
    // Remove Water's constant grey fill; preserve dark troughs and add direct amber glints.
    .replace('vec3 outgoingLight = albedo;', `
      vec3 deepWater = waterColor * (.32 + .68 * max(surfaceNormal.y,0.));
      vec3 reflected = reflectionSample * .82;
      vec3 outgoingLight = mix(deepWater + scatter*.22, reflected, reflectance)
        + specularLight * .9;`);

  // Display transform after bloom (r147 composer does not automatically encode its output).
  const finish = new THREE.ShaderPass({ uniforms: { tDiffuse: { value: null } },
    vertexShader: 'varying vec2 vUv; void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader: `uniform sampler2D tDiffuse; varying vec2 vUv;
      void main(){vec3 c=texture2D(tDiffuse,vUv).rgb;
      c=max(c,vec3(0.))*.9;
      c=clamp((c*(2.51*c+.03))/(c*(2.43*c+.59)+.14),0.,1.);
      c=mix(12.92*c,1.055*pow(c,vec3(1./2.4))-.055,step(vec3(.0031308),c));
      c*=1.-.13*pow(length((vUv-.5)*vec2(1.,.75)),1.5);
      gl_FragColor=vec4(c,1.);}` });
  s.composer.addPass(finish);
  return s;
}
async function render(frame, totalFrames, fps) {
  if (!oceanState) oceanState = setupOcean();
  const s = await oceanState, t = frame / fps, u = t / D;
  // a low glide toward the sun, rising a touch
  s.cam.position.set(lerp(-1.4, 0.8, u), lerp(2.4, 3.0, u) + 0.06 * Math.sin(t * 0.7), lerp(26, 10, ease(u)));
  s.cam.lookAt(lerp(-1.4, 0.2, u), -3.4, -120);
  s.water.material.uniforms.time.value = t * 0.55;
  const appear = ease(seg(t, D * 0.12, D * 0.3));
  el('ocean_caption').textContent = P.line;
  el('ocean_caption').style.opacity = appear;
  el('ocean_caption').style.transform = `translateY(${(1 - appear) * 12}px)`;
  s.composer.render();
  beatFade(t, D, 0.3, 0.3);
}
