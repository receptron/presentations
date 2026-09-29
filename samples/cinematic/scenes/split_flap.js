// requires: geometries/RoundedBoxGeometry
let flapScene;
async function setupFlaps() {
  await waitFonts();
  const s = makeRenderer('flap-stage', [.18, .25, 1.15]);
  s.scene.background = new THREE.Color(0x030609);
  const studio = new StudioEnv(), pmrem = new THREE.PMREMGenerator(s.R);
  s.environment = pmrem.fromScene(studio, .04); s.scene.environment = s.environment.texture;
  studio.dispose(); pmrem.dispose();
  s.R.shadowMap.enabled = true; s.R.shadowMap.type = THREE.PCFSoftShadowMap;
  const rows = P.rows.map(row => [String(row[0]), Array.from(String(row[1]))]);
  const columns = Math.max(8, ...rows.map(row => row[1].length));
  const W = 13.6, H = Math.max(1, rows.length) * 2.5 + .8;
  s.distance = Math.max(W / .93, H / .50);
  const board = new THREE.Group(); s.scene.add(board); s.board = board;
  const material = (color, metalness, roughness) => new THREE.MeshStandardMaterial({color, metalness, roughness});
  const body = material(0x11171d, .68, .3), brass = material(0xbca579, .86, .27);
  const black = material(0x050709, .2, .43), steel = material(0x8f9ba1, .9, .23);
  const box = (w, h, d, radius, mat, x, y, z) => {
    const m = new THREE.Mesh(new THREE.RoundedBoxGeometry(w, h, d, 2, radius), mat);
    m.position.set(x,y,z); m.castShadow = true; m.receiveShadow = true; board.add(m); return m;
  };
  box(W,H,.65,.15,body,0,0,-.2);
  const rim = new THREE.Mesh(ringOf(W-.16,H-.16,.13,.035),brass); rim.position.z=.145; board.add(rim);
  box(W-.5,H-.5,.12,.07,black,0,0,.14);
  // Countersunk screws with an actual dark slot, catching the grazing key.
  for (const x of [-W/2+.19,W/2-.19]) for (const y of [-H/2+.19,H/2-.19]) {
    const screw = new THREE.Mesh(new THREE.CylinderGeometry(.055,.055,.025,16),steel);
    screw.rotation.x=Math.PI/2; screw.position.set(x,y,.148); board.add(screw);
    const slot = new THREE.Mesh(new THREE.BoxGeometry(.067,.009,.006),black);
    slot.position.set(x,y,.164); slot.rotation.z=.4; board.add(slot);
  }
  const cache = new Map();
  function glyph(ch) {
    if (cache.has(ch)) return cache.get(ch);
    const c = document.createElement('canvas'); c.width = 160; c.height = 256;
    const g = c.getContext('2d');
    const bg = g.createLinearGradient(0,0,0,256); bg.addColorStop(0,'#1c2329'); bg.addColorStop(.49,'#10161c'); bg.addColorStop(.51,'#192026'); bg.addColorStop(1,'#10161b');
    g.fillStyle=bg; g.fillRect(0,0,160,256);
    // Very fine moulded grain, fixed per glyph and independent of render order.
    for (let i=0;i<850;i++) {g.fillStyle=`rgba(150,165,175,${rnd(i+1)*.045})`;g.fillRect(rnd(i+5)*160,rnd(i+9)*256,1,1);}
    g.fillStyle='#e4dfcc'; g.textAlign='center'; g.textBaseline='middle';
    g.font='600 184px "JetBrains Mono"';
    const size = Math.min(184, 144 / Math.max(1,g.measureText(ch).width) * 184);
    g.font=`600 ${size}px "JetBrains Mono"`; g.fillText(ch,80,134);
    const textures = [0,1].map(half => {
      const part=document.createElement('canvas');part.width=160;part.height=128;
      part.getContext('2d').drawImage(c,0,half*128,160,128,0,0,160,128);
      const tex=new THREE.CanvasTexture(part); tex.anisotropy=4; return tex;
    }); cache.set(ch,textures);return textures;
  }
  function ink(ch,half) { return new THREE.MeshStandardMaterial({map:glyph(ch)[half],color:0xd0d0d0,metalness:.05,roughness:.52}); }
  const pitch=11.9/columns, cw=pitch-.065, ch=Math.min(1.68,pitch*1.55);
  const halfGeo = new THREE.PlaneGeometry(cw,ch/2-.016);
  s.cells=[];
  rows.forEach((row,r)=>{
    const y=H/2-1.75-r*2.5;
    const label=document.createElement('canvas');label.width=1536;label.height=72;
    const g=label.getContext('2d');g.fillStyle='#b1a58c';g.font='600 44px "JetBrains Mono"';g.textBaseline='middle';
    const fs=Math.min(44,1480/Math.max(1,g.measureText(row[0]).width)*44);
    g.font=`600 ${fs}px "JetBrains Mono"`;g.fillText(row[0],12,38);
    const lm=new THREE.Mesh(new THREE.PlaneGeometry(11.9,.56),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(label),transparent:true,depthWrite:false}));
    lm.position.set(0,y+1.09,.225);board.add(lm);
    for(let col=0;col<columns;col++){
      const x=(col-(columns-1)/2)*pitch;
      box(cw+.042,ch+.09,.14,.028,black,x,y,.27);
      const upper=new THREE.Mesh(halfGeo,ink(' ',0)); upper.position.set(x,y+ch/4,.36);board.add(upper);
      const lower=new THREE.Mesh(halfGeo,ink(' ',1)); lower.position.set(x,y-ch/4,.36);board.add(lower);
      const hinge=new THREE.Group();hinge.position.set(x,y,.389);board.add(hinge);
      const front=new THREE.Mesh(halfGeo,ink(' ',0));front.position.set(0,ch/4,.012);hinge.add(front);
      const back=new THREE.Mesh(halfGeo,ink(' ',1));back.position.set(0,ch/4,-.012);back.rotation.x=Math.PI;hinge.add(back);
      front.castShadow=back.castShadow=true; front.receiveShadow=back.receiveShadow=true;
      for(const dx of [-cw/2+.025,cw/2-.025]){
        const pin=new THREE.Mesh(new THREE.CylinderGeometry(.027,.027,.07,8),steel);
        pin.rotation.z=Math.PI/2;pin.position.set(x+dx,y,.405);board.add(pin);
      }
      s.cells.push({upper,lower,front,back,hinge, r,col, final:row[1][col]||' ', last:''});
    }
  });
  s.glyph=glyph; s.rowCount=rows.length;s.columns=columns;
  s.pool=Array.from(new Set([' ',...rows.flatMap(row=>row[1])]));
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(100,70),material(0x080e14,.1,.88));
  wall.position.z=-1.05;wall.receiveShadow=true;s.scene.add(wall);
  const key=new THREE.SpotLight(0xffdfad,1.55,60,.69,.65,1);
  key.position.set(-5,H/2+5,7);key.target.position.set(-1,0,0);key.castShadow=true;
  key.shadow.mapSize.set(1024,1024);key.shadow.bias=-.00015;key.shadow.normalBias=.02;
  s.scene.add(key,key.target);s.key=key;
  const fill=new THREE.DirectionalLight(0x779dcb,.32);fill.position.set(7,1,5);s.scene.add(fill);
  s.scene.add(new THREE.AmbientLight(0x8297a9,.16));
  return s;
}
async function render(frame,totalFrames,fps){
  if(!flapScene) flapScene=setupFlaps();
  const s=await flapScene,t=frame/fps,u=seg(t,0,D);
  for(const cell of s.cells){
    const start=.075+cell.r*.24/Math.max(1,s.rowCount-1)+cell.col*.075/s.columns;
    const q=seg(t,D*start,D*(start+.36))*6;
    const cycle=Math.min(5,Math.floor(q)),f=q>=6?1:q-cycle;
    const previous=cycle===0?' ':s.pool[(cycle*3+cell.col*2+cell.r)%s.pool.length];
    const next=cycle===5?cell.final:s.pool[((cycle+1)*3+cell.col*2+cell.r)%s.pool.length];
    const cacheKey=previous+'\u0000'+next;
    if(cell.last!==cacheKey){
      cell.upper.material.map=s.glyph(next)[0];cell.lower.material.map=s.glyph(previous)[1];
      cell.front.material.map=s.glyph(previous)[0];cell.back.material.map=s.glyph(next)[1];cell.last=cacheKey;
    }
    // A top leaf drops towards camera, passes the hinge and lands face-down.
    cell.hinge.rotation.x=Math.PI*easeIn(Math.min(1,f/.88));
    if(f>.88&&f<1) cell.hinge.rotation.x-=Math.sin((f-.88)/.12*Math.PI)*.035;
  }
  s.cam.position.set(lerp(2.6,.45,ease(u)),lerp(1.05,.38,u),s.distance*lerp(1.10,1.0,ease(u)));
  s.cam.lookAt(0,0,0);s.key.position.x=lerp(-5,-3,u);
  s.composer.render();beatFade(t,D,0.3,0.3);
}
