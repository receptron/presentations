// Alpine dawn: deterministic heightfields, horizon shadows and a lit cloud inversion.
let peaksState;

function peaksNoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  let u = x - ix, v = y - iy;
  u = u * u * (3 - 2 * u); v = v * v * (3 - 2 * v);
  return lerp(lerp(rnd(ix + iy * 173.17), rnd(ix + 1 + iy * 173.17), u),
    lerp(rnd(ix + (iy + 1) * 173.17), rnd(ix + 1 + (iy + 1) * 173.17), u), v);
}
function peaksFbm(x, y, octaves = 5) {
  let value = 0, weight = .5;
  for (let i = 0; i < octaves; i++) {
    value += weight * peaksNoise(x, y);
    const nx = 1.72 * x + 1.07 * y + 13.8;
    y = -1.07 * x + 1.72 * y + 8.3; x = nx; weight *= .5;
  }
  return value;
}
const peaksGLSL = `
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+1.),f.x),f.y);}
float fbm(vec2 p){float f=0.,a=.5;for(int i=0;i<4;i++){f+=a*noise(p);p=mat2(1.72,-1.07,1.07,1.72)*p+13.7;a*=.5;}return f;}
`;

function peaksTerrain(scene, config) {
  const { z, width, depth, height, seed, centers } = config;
  const nx = 300, nz = 100;
  const geo = new THREE.PlaneGeometry(width, depth, nx, nz);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position, heights = new Float32Array(pos.count);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), localZ = pos.getZ(i);
    const warp = (peaksFbm(x * .014 + seed, localZ * .015) - .45) * 25;
    let massif = 0;
    for (const peak of centers) {
      const dx = (x - peak[0] + warp) / peak[2];
      const dz = (localZ - peak[1]) / (depth * .34);
      massif = Math.max(massif, peak[3] * Math.exp(-dx * dx * 1.6 - dz * dz * 1.8));
    }
    let ridge = 0, amplitude = .55, frequency = .026;
    for (let k = 0; k < 6; k++) {
      const n = peaksNoise((x + warp) * frequency + seed * 11, localZ * frequency + seed);
      ridge += amplitude * (1 - Math.abs(n * 2 - 1));
      frequency *= 2.12; amplitude *= .49;
    }
    // Eroded ribs reach down from each summit; a broad envelope avoids isolated cones.
    const h = 5 + height * massif * (.48 + .62 * ridge) + 6 * peaksFbm(x * .06, localZ * .07 + seed);
    heights[i] = h; pos.setY(i, h); pos.setZ(i, localZ + z);
  }
  geo.computeVertexNormals();
  const shadows = new Float32Array(pos.count);
  // Trace the heightfield toward the low sun. This bakes cast shadows into the actual valleys.
  for (let j = 0; j <= nz; j++) for (let i = 0; i <= nx; i++) {
    const index = j * (nx + 1) + i, h = heights[index];
    let blocked = 0;
    for (let step = 1; step <= 22; step++) {
      const sx = i + Math.round(step * 1.35), sz = j - step;
      if (sx > nx || sz < 0) break;
      const distance = Math.hypot((sx - i) * width / nx, step * depth / nz);
      blocked = Math.max(blocked, clamp01((heights[sz * (nx + 1) + sx] - h - distance * .095) / 5));
    }
    shadows[index] = 1 - blocked * .91;
  }
  geo.setAttribute('sunVisibility', new THREE.BufferAttribute(shadows, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { snowLine: { value: height * .59 }, sun: { value: new THREE.Vector3(.41, .075, -.907).normalize() } },
    vertexShader: `attribute float sunVisibility; varying vec3 w,n; varying float visibility;
      void main(){w=position;n=normal;visibility=sunVisibility;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `${peaksGLSL}
      uniform float snowLine;uniform vec3 sun;varying vec3 w,n;varying float visibility;
      void main(){
        vec3 normal=normalize(n);
        float detail=fbm(w.xz*.38);
        float strata=noise(vec2(w.x*.11+w.y*.45,w.z*.14))* .5+.5;
        float snow=smoothstep(snowLine-9.,snowLine+13.,w.y+detail*16.) * smoothstep(.38,.77,normal.y+(detail-.5)*.3);
        vec3 rock=mix(vec3(.071,.087,.109),vec3(.26,.235,.209),detail)*strata;
        vec3 albedo=mix(rock,vec3(.72,.79,.85),snow);
        float diffuse=max(0.,dot(normal,sun))*visibility;
        // Cool open-sky fill keeps the unlit rock readable. A broad warm horizon
        // wraps the grazing key around east-facing ribs without lifting all shadows.
        float east=smoothstep(-.12,.65,normal.x)*visibility;
        float summit=smoothstep(snowLine-24.,snowLine+18.,w.y);
        float rim=pow(1.-max(0.,dot(normal,normalize(cameraPosition-w))),2.);
        vec3 light=vec3(.40,.56,.84)*(.55+.45*max(normal.y,0.))
          +vec3(2.35,1.18,.52)*diffuse
          +vec3(.95,.40,.22)*east*(.3+.7*summit);
        vec3 color=albedo*light;
        color+=vec3(.43,.20,.09)*rim*east*summit;
        // Gentle highlight shoulder: retain pink/gold in snow, never clip it white.
        color=color/(vec3(1.)+color*.48);
        float dist=length(cameraPosition-w);
        float haze=1.-exp(-max(0.,dist-85.)*.00185);
        vec3 air=mix(vec3(.20,.29,.40),vec3(.47,.43,.43),exp(-max(w.y-22.,0.)*.045));
        color=mix(color,air,haze*.83);
        gl_FragColor=vec4(color,1.);
      }`
  });
  const mesh = new THREE.Mesh(geo, mat); scene.add(mesh);
  return mat;
}

async function setupPeaks() {
  await waitFonts();
  el('peaks-eyebrow').textContent = P.eyebrow;
  el('peaks-title').textContent = P.title;
  // Fit arbitrary replacement titles while retaining the airy one-line default.
  const title = el('peaks-title');
  if (title.scrollWidth > 760) title.style.fontSize = `${Math.max(54, 100 * 760 / title.scrollWidth)}px`;
  const S = makeRenderer('peaks-canvas', [.30, .72, .94]);
  const { scene, cam } = S;
  cam.fov = 43; cam.near = 1; cam.far = 2400; cam.updateProjectionMatrix();
  const sunDirection = new THREE.Vector3(.41, .075, -.907).normalize();
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1700, 48, 24), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: { sunDirection: { value: sunDirection }, phase: { value: 0 } },
    vertexShader: `varying vec3 direction;void main(){direction=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `${peaksGLSL}
      varying vec3 direction;uniform vec3 sunDirection;uniform float phase;
      void main(){vec3 d=normalize(direction);float h=max(d.y,0.);float alignment=max(0.,dot(d,sunDirection));
        float horizon=exp(-h*5.8);
        vec3 c=mix(vec3(.075,.18,.34),vec3(.89,.47,.29),horizon);
        // A broad aureole and a tighter amber halo read even before the disc clears rock.
        float halo=pow(alignment,100.);
        c=mix(c,vec3(.98,.70,.39),halo*.64);
        c=mix(c,vec3(1.,.82,.51),pow(alignment,950.)*.75);
        float disc=smoothstep(.99977,.99984,alignment);
        c=mix(c,vec3(1.35,1.10,.72),disc);
        vec2 cloudUV=d.xz/max(.10,d.y)*vec2(1.5,5.);
        float veil=smoothstep(.52,.76,fbm(cloudUV+vec2(phase*.035,0.)));
        veil*=smoothstep(.025,.12,h)*(1.-smoothstep(.35,.65,h));
        c=mix(c,mix(vec3(.66,.49,.53),vec3(.98,.71,.48),pow(alignment,8.)),veil*.68);
        gl_FragColor=vec4(c,1.);
      }`
  }));
  scene.add(sky); S.sky = sky;
  // Layer widths exceed the entire camera frustum, including the crane's final position.
  S.terrainMaterials = [
    { z:-610,width:1600,depth:210,height:143,seed:41,centers:[[-520,0,280,.9],[-190,-12,170,1],[125,10,200,.92],[470,0,230,1.13]] },
    { z:-420,width:1250,depth:185,height:141,seed:12,centers:[[-440,0,170,.9],[-160,-10,150,1.06],[140,8,175,.9],[390,0,170,1.08]] },
    { z:-247,width:1000,depth:166,height:147,seed:7,centers:[[-310,0,150,1.02],[-75,-16,107,.79],[124,5,118,1.11],[360,-9,135,.9]] },
    { z:-92,width:780,depth:155,height:142,seed:25,centers:[[-270,-5,130,.98],[42,-14,88,1.03],[245,4,108,.88]] },
    { z:49,width:680,depth:133,height:113,seed:32,centers:[[-238,0,112,1.18],[224,8,95,.94]] }
  ].map(c => peaksTerrain(scene, c));

  // An opaque, gently turbulent cloud ceiling fills every valley. Geometry provides
  // parallax and mountain intersections; the shader adds small-scale illuminated billows.
  const cloudGeo = new THREE.PlaneGeometry(1850, 1700, 230, 220);
  cloudGeo.rotateX(-Math.PI / 2);
  const cp = cloudGeo.attributes.position;
  for (let i=0;i<cp.count;i++) {
    const x=cp.getX(i),z=cp.getZ(i)-600;
    cp.setXYZ(i,x,20+9*peaksFbm(x*.025,z*.023)+3*peaksFbm(x*.09,z*.09),z);
  }
  cloudGeo.computeVertexNormals();
  const cloudMat = new THREE.ShaderMaterial({
    uniforms: { phase: { value:0 } },
    vertexShader: `varying vec3 w,n;void main(){w=position;n=normal;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `${peaksGLSL}
      uniform float phase;varying vec3 w,n;
      void main(){
        vec2 p=w.xz*.072+vec2(phase*.16,phase*.035);
        float a=fbm(p),b=fbm(p+vec2(.17,-.25));
        float ridge=clamp(.5+(a-b)*3.8,0.,1.);
        float top=max(0.,dot(normalize(n),normalize(vec3(.41,.15,-.907))));
        float crown=smoothstep(.30,.65,a)*.42+smoothstep(24.,29.,w.y)*.25;
        float lighting=clamp(crown+ridge*.23+top*.55,0.,1.);
        vec3 shadow=vec3(.24,.35,.52), lit=vec3(.98,.70,.49);
        vec3 color=mix(shadow,lit,smoothstep(.16,.85,lighting));
        color+=vec3(.10,.035,.04)*smoothstep(.48,.72,a);
        color*=.92+.13*a;
        float distance=length(cameraPosition-w);
        color=mix(color,vec3(.69,.51,.46),1.-exp(-distance*.00095));
        gl_FragColor=vec4(color,1.);
      }`
  });
  scene.add(new THREE.Mesh(cloudGeo,cloudMat)); S.cloudMat=cloudMat;

  // Soft, internally shaded cloud crowns break the otherwise continuous inversion.
  // A single procedural texture is shared by all billboards; no external assets.
  const canvas=document.createElement('canvas');canvas.width=256;canvas.height=128;
  const ctx=canvas.getContext('2d'), pixels=ctx.createImageData(256,128);
  for(let y=0;y<128;y++) for(let x=0;x<256;x++){
    const u=(x-128)/122,v=(y-69)/54;
    const f=peaksFbm(x*.036,y*.036,5);
    const edge=1-u*u-v*v+(f-.5)*.58;
    const alpha=clamp01(edge*2.2)*clamp01((128-y)/30);
    const light=clamp01(.55-v*.27+(f-.5)*.65);
    const k=(y*256+x)*4;
    pixels.data[k]=lerp(61,249,light);pixels.data[k+1]=lerp(89,184,light);
    pixels.data[k+2]=lerp(136,140,light);pixels.data[k+3]=alpha*178;
  }
  ctx.putImageData(pixels,0,0);
  const cloudTexture=new THREE.CanvasTexture(canvas);
  S.clouds=[];
  for(let i=0;i<68;i++){
    const z=lerp(-740,30,rnd(i*4.33+7));
    const x=lerp(-600,600,rnd(i*8.71+5));
    const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:cloudTexture,transparent:true,opacity:.43,depthWrite:false}));
    const width=lerp(65,140,rnd(i*2.7+9));
    sprite.position.set(x,29+9*rnd(i+11),z);sprite.scale.set(width,width*.29,1);
    scene.add(sprite);S.clouds.push({sprite,x,z});
  }
  // Airborne shafts descend through the right-hand saddle into the valley.
  const shaftMat=new THREE.ShaderMaterial({
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,
    vertexShader:`varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader:`varying vec2 v;void main(){float edge=pow(sin(v.x*3.14159265),2.);float fade=sin(v.y*3.14159265);gl_FragColor=vec4(.91,.51,.21,edge*fade*.12);}`
  });
  for(let i=0;i<5;i++){
    const g=new THREE.BufferGeometry();
    const x=102+i*27,z=-185-i*32;
    g.setAttribute('position',new THREE.Float32BufferAttribute([x,112,z,x+7,112,z,x-62,30,z+190,x-103,30,z+190],3));
    g.setAttribute('uv',new THREE.Float32BufferAttribute([0,1,1,1,1,0,0,0],2));g.setIndex([0,1,2,0,2,3]);
    scene.add(new THREE.Mesh(g,shaftMat));
  }
  return S;
}

async function render(frame,totalFrames,fps) {
  if(!peaksState) peaksState=setupPeaks();
  const S=await peaksState,t=frame/fps,u=clamp01(t/D);
  // Constant-speed travel keeps the landscape alive even while the card is held.
  S.cam.position.set(lerp(-25,22,u),lerp(72,112,u),lerp(178,112,u));
  S.cam.lookAt(lerp(0,12,u),lerp(70,88,u),-210);
  // The disc clears the saddle as the crane reveals more of the illuminated cloud sea.
  S.sky.material.uniforms.sunDirection.value.set(.41,lerp(.055,.095,u),-.907).normalize();
  for(const mat of S.terrainMaterials) mat.uniforms.sun.value.copy(S.sky.material.uniforms.sunDirection.value);
  S.sky.position.copy(S.cam.position);
  S.sky.material.uniforms.phase.value=u;
  S.cloudMat.uniforms.phase.value=u;
  for(const c of S.clouds){c.sprite.position.x=c.x+u*5;c.sprite.position.z=c.z+u*1.5;}
  const reveal=easeOut(seg(t,D*.15,D*.33));
  el('peaks-card').style.opacity=reveal*(1-ease(seg(t,D*.85,D*.97)));
  el('peaks-card').style.transform=`translateY(${(1-reveal)*17}px)`;
  S.composer.render();
  beatFade(t,D,.3,.3);
}
