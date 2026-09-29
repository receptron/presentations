// requires: geometries/RoundedBoxGeometry, objects/Reflector
let S;
async function setupProduct() {
  await waitFonts();
  el('ph-name').textContent = P.name;
  el('ph-tagline').textContent = P.tagline;
  const s = makeRenderer('ph-canvas', [0.24, 0.42, 1.15]);
  const {scene, R} = s;
  s.cam.fov=30;s.cam.updateProjectionMatrix();
  scene.background = new THREE.Color(0x030509);
  const env = new StudioEnv(), pm = new THREE.PMREMGenerator(R);
  s.env = pm.fromScene(env, .04); scene.environment = s.env.texture; env.dispose(); pm.dispose();
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  const metal = new THREE.MeshStandardMaterial({color:0xa4b4bc,metalness:1,roughness:.22});
  const dark = new THREE.MeshStandardMaterial({color:0x070c13,metalness:.5,roughness:.23});
  const mesh = (geo, mat, parent, x=0,y=0,z=0) => {
    const m = new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
  };
  // A real planar reflection, tinted down at the shader, keeps the floor black.
  const floor = new THREE.Reflector(new THREE.PlaneGeometry(80,80), {color:0x252c36,textureWidth:1024,textureHeight:576,clipBias:.003});
  floor.rotation.x=-Math.PI/2;floor.position.y=-.012;scene.add(floor);
  const pedestal = new THREE.Group();pedestal.position.x=1.55;scene.add(pedestal);
  mesh(new THREE.CylinderGeometry(1.92,2.04,.32,96),dark,pedestal,0,.16);
  mesh(new THREE.CylinderGeometry(1.93,1.93,.035,96),metal,pedestal,0,.32);
  mesh(new THREE.CylinderGeometry(1.89,1.89,.04,96),new THREE.MeshStandardMaterial({color:0x10151c,roughness:.32,metalness:.45}),pedestal,0,.355);
  const device = new THREE.Group();device.position.set(1.55,2.43,0);scene.add(device);s.device=device;
  mesh(new THREE.RoundedBoxGeometry(2.2,4.08,.28,5,.16),metal,device);
  mesh(new THREE.RoundedBoxGeometry(2.12,4,.055,5,.15),dark,device,0,0,.147);
  mesh(new THREE.RoundedBoxGeometry(2.07,3.94,.018,5,.145),new THREE.MeshPhysicalMaterial({color:0x050a10,metalness:.24,roughness:.12,clearcoat:1,clearcoatRoughness:.075}),device,0,0,.181);
  // Luminous, folded interference ribbons beneath the glass. No texture gamma conversion.
  const shader = new THREE.ShaderMaterial({uniforms:{phase:{value:0}},vertexShader:`varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,fragmentShader:`varying vec2 v;uniform float phase;
    void main(){vec2 p=v-.5;float edge=pow(abs(p.x)/.5,12.)+pow(abs(p.y)/.5,18.);if(edge>.86)discard;
    vec3 c=vec3(.005,.012,.022);
    for(int i=0;i<5;i++){float f=float(i);float curve=.27*sin(p.y*4.6+phase+f*.19)+.12*sin(p.y*9.+f*.2);float d=p.x-curve+(f-2.)*.064;
    float ribbon=exp(-d*d/ (.0006+f*.0002));float halo=exp(-d*d/.018)*.08;
    vec3 tint=mix(vec3(.035,.39,.48),vec3(.6,.24,.10),smoothstep(-.35,.4,p.y+f*.025));c+=(ribbon*.55+halo)*tint;}
    c*=smoothstep(.51,.31,abs(p.y));gl_FragColor=vec4(c,1.);}`});
  mesh(new THREE.PlaneGeometry(1.98,3.81),shader,device,0,0,.195);s.screen=shader;
  const slot = new THREE.MeshStandardMaterial({color:0x010203,roughness:.28,metalness:.4});
  mesh(new THREE.RoundedBoxGeometry(.34,.035,.018,2,.015),slot,device,0,1.87,.208);
  mesh(new THREE.SphereGeometry(.033,16,12),new THREE.MeshPhysicalMaterial({color:0x172b39,metalness:.7,roughness:.08,clearcoat:1}),device,.32,1.87,.192);
  mesh(new THREE.RoundedBoxGeometry(.027,.49,.105,3,.012),metal,device,1.104,.72,-.01);
  mesh(new THREE.RoundedBoxGeometry(.027,.25,.105,3,.012),metal,device,-1.104,.65,-.01);
  // Small dark antenna breaks make the continuous machined rim feel manufactured.
  for(const y of [-1.55,1.55]) for(const x of [-1.101,1.101]) mesh(new THREE.BoxGeometry(.015,.024,.24),slot,device,x,y,0);
  const key=new THREE.SpotLight(0xffe0bd,2.7,26,.55,.75,1.2);key.position.set(-3,8,6);key.target=device;key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.bias=-.00015;key.shadow.normalBias=.025;scene.add(key);
  const rim=new THREE.SpotLight(0x9dd9ff,3.7,23,.65,.8,1.2);rim.position.set(5,5,-4);rim.target=device;scene.add(rim);s.rim=rim;
  scene.add(new THREE.HemisphereLight(0x829eaf,0x030405,.17));
  // Soft contact shadow lies over the mirror, beneath the plinth.
  const shadow=mesh(new THREE.PlaneGeometry(6,6),new THREE.MeshBasicMaterial({map:dotTex('0,0,0'),color:0x000000,transparent:true,opacity:.8,depthWrite:false}),scene,1.55,.006,0);shadow.rotation.x=-Math.PI/2;
  return s;
}
async function render(frame,totalFrames,fps) {
  if(!S) S=setupProduct();const s=await S;const t=frame/fps,u=clamp01(t/D),k=ease(u);
  s.device.rotation.y=lerp(-.92,.30,k);s.device.rotation.z=-.022;
  s.screen.uniforms.phase.value=lerp(-.4,.6,u);
  s.cam.position.set(lerp(6.2,5.15,k),lerp(4.35,3.75,k),lerp(12.9,11.9,k));
  s.cam.lookAt(-.58,2.25,0);
  s.rim.position.x=lerp(3.8,6.2,u);
  const copy=easeOut(seg(t,D*.14,D*.37));el('ph-copy').style.opacity=copy;el('ph-copy').style.transform=`translateY(${(1-copy)*22}px)`;
  s.composer.render();beatFade(t,D,.3,.3);
}
