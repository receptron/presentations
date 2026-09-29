// requires: geometries/RoundedBoxGeometry
let notesScene;
async function setupNotes(){
  await waitFonts();
  const video=el('notes-video');
  // P stays the single source of truth, including relative local footage paths.
  const base=new URL('../',el('notes-asset-base').src);
  video.src=new URL(String(P.footage),base).href;
  await new Promise((resolve,reject)=>{
    video.addEventListener('loadeddata',resolve,{once:true});
    video.addEventListener('error',()=>reject(new Error(`Cannot load P.footage: ${P.footage}`)),{once:true});
    video.load();
  });
  const s=makeRenderer('notes-stage',[.3,.4,1.05]);
  s.scene.background=new THREE.Color(0x020405);
  const studio=new StudioEnv(),pmrem=new THREE.PMREMGenerator(s.R);
  s.env=pmrem.fromScene(studio,.03);s.scene.environment=s.env.texture;studio.dispose();pmrem.dispose();
  const body=new THREE.MeshStandardMaterial({color:0x101619,metalness:.65,roughness:.27});
  const silver=new THREE.MeshStandardMaterial({color:0xa6afb4,metalness:.92,roughness:.21});
  const screenBody=new THREE.Mesh(new THREE.RoundedBoxGeometry(16.35,9.35,.3,3,.12),body);
  screenBody.position.z=-.18;s.scene.add(screenBody);
  const edge=new THREE.Mesh(ringOf(16.24,9.24,.10,.022),silver);edge.position.z=-.012;s.scene.add(edge);
  s.texture=new THREE.CanvasTexture(el('notes-composite'));s.texture.minFilter=THREE.LinearFilter;
  s.screen=new THREE.Mesh(new THREE.PlaneGeometry(16,9),new THREE.MeshBasicMaterial({map:s.texture}));
  s.scene.add(s.screen);
  s.lens=new THREE.Group();s.scene.add(s.lens);
  const rim=new THREE.Mesh(new THREE.TorusGeometry(1.58,.065,12,100),silver);s.lens.add(rim);
  const inner=new THREE.Mesh(new THREE.TorusGeometry(1.505,.019,8,100),new THREE.MeshBasicMaterial({color:0x070a0d}));inner.position.z=.03;s.lens.add(inner);
  s.loupeCanvas=document.createElement('canvas');s.loupeCanvas.width=s.loupeCanvas.height=640;
  s.loupeTexture=new THREE.CanvasTexture(s.loupeCanvas);
  const lensFace=new THREE.Mesh(new THREE.CircleGeometry(1.51,100),new THREE.MeshBasicMaterial({map:s.loupeTexture}));
  lensFace.position.z=.008;s.lens.add(lensFace);
  // A very restrained glass highlight, away from the magnified detail.
  const glassCanvas=document.createElement('canvas');glassCanvas.width=glassCanvas.height=256;
  const gg=glassCanvas.getContext('2d'),shine=gg.createLinearGradient(0,0,256,256);
  shine.addColorStop(0,'rgba(221,239,255,.28)');shine.addColorStop(.28,'rgba(220,239,255,.035)');shine.addColorStop(.55,'rgba(255,255,255,0)');
  gg.fillStyle=shine;gg.fillRect(0,0,256,256);
  const glass=new THREE.Mesh(new THREE.CircleGeometry(1.51,100),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(glassCanvas),transparent:true,depthWrite:false}));
  glass.position.z=.025;s.lens.add(glass);
  const light=new THREE.DirectionalLight(0xffe3bc,1.4);light.position.set(-6,8,10);s.scene.add(light);
  const cool=new THREE.DirectionalLight(0x86bbdd,.5);cool.position.set(8,-2,5);s.scene.add(cool);
  s.scene.add(new THREE.AmbientLight(0xffffff,.12));
  const lineGeo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3()]);
  s.leader=new THREE.Line(lineGeo,new THREE.LineBasicMaterial({color:0xe0ccac,transparent:true,opacity:0}));s.scene.add(s.leader);
  s.flash=new THREE.Mesh(new THREE.PlaneGeometry(16,.025),new THREE.MeshBasicMaterial({color:new THREE.Color(2.1,2.3,2.5),transparent:true,opacity:0,depthWrite:false}));
  s.flash.position.z=.1;s.scene.add(s.flash);
  el('notes-caption').textContent=String(P.note);
  return s;
}
async function render(frame,totalFrames,fps){
  if(!notesScene) notesScene=setupNotes();
  const s=await notesScene,t=frame/fps,u=seg(t,0,D),video=el('notes-video');
  // The integral of a linearly falling playback rate: 1x -> 0x, then a stable frame.
  const decel=seg(t,D*.28,D*.48);
  const sourceTime=t<D*.28?t:D*(.28+.20*(decel-decel*decel/2));
  const source=el('notes-frame');
  // Centre-crop once in source coordinates, preserving the footage aspect ratio.
  const aspect=16/9,vw=video.videoWidth,vh=video.videoHeight;
  const sw=Math.min(vw,vh*aspect),sh=sw/aspect;
  await paint('notes-video','notes-frame',Math.min(sourceTime,Math.max(0,video.duration-.001)),(vw-sw)/2,(vh-sh)/2,sw,sh);
  const canvas=el('notes-composite'),g=canvas.getContext('2d');
  g.clearRect(0,0,1600,900);g.drawImage(source,0,0);
  const reveal=easeOut(seg(t,D*.40,D*.54));
  // Burn down the surrounds, keeping the circular area of interest at full exposure.
  const fx=744,fy=410;
  g.save();g.beginPath();g.rect(0,0,1600,900);g.arc(fx,fy,115,0,Math.PI*2,true);
  g.fillStyle=`rgba(0,3,8,${reveal*.27})`;g.fill('evenodd');g.restore();
  const circle=seg(t,D*.49,D*.64);
  g.save();g.strokeStyle='#ff4d43';g.lineWidth=5.5;g.lineCap='round';g.lineJoin='round';
  g.shadowColor='rgba(0,0,0,.75)';g.shadowBlur=5;g.beginPath();
  const end=circle*Math.PI*2.16,steps=Math.ceil(end*45);
  for(let i=0;i<=steps&&circle>0;i++){
    const a=-.45+end*i/Math.max(1,steps),radius=112+Math.sin(a*3+.5)*4+Math.cos(a*7)*1.6;
    const x=fx+Math.cos(a)*radius,y=fy+Math.sin(a)*radius*.82;
    i?g.lineTo(x,y):g.moveTo(x,y);
  }g.stroke();g.restore();
  // Faint phosphor lines add a screen texture without obscuring small UI text.
  g.fillStyle='rgba(0,0,0,.055)';for(let y=0;y<900;y+=3)g.fillRect(0,y,1600,1);
  s.texture.needsUpdate=true;
  const lg=s.loupeCanvas.getContext('2d');lg.clearRect(0,0,640,640);
  lg.drawImage(source,fx-105,fy-105,210,210,0,0,640,640);s.loupeTexture.needsUpdate=true;
  const dismiss=1-ease(seg(t,D*.82,D*.87)),visible=reveal*dismiss;
  s.lens.visible=visible>.001;s.lens.scale.setScalar(Math.max(.001,visible));
  s.lens.position.set(4.85,lerp(.95,1.2,ease(u)),1.0);
  const line=s.leader.geometry.attributes.position;
  line.setXYZ(0,(fx+100)/100-8,4.5-fy/100,.045);
  line.setXYZ(1,2.7,.4,.15);line.setXYZ(2,3.4,.75,.8);line.needsUpdate=true;
  s.leader.material.opacity=visible*.65;
  // Collapse the raster vertically, then contract its final bright horizontal line.
  const collapse=easeIn(seg(t,D*.875,D*.92));
  s.screen.scale.y=Math.max(.0005,1-collapse);
  s.screen.material.color.setScalar(1+collapse*.65);
  s.screen.visible=u<.937;
  s.flash.material.opacity=seg(t,D*.908,D*.92)*(1-seg(t,D*.937,D*.951));
  s.flash.scale.x=Math.max(.001,1-easeIn(seg(t,D*.92,D*.947)));
  s.cam.position.set(lerp(.55,-.22,ease(u)),lerp(.3,.1,u),lerp(17.6,16.3,ease(u)));
  s.cam.lookAt(0,0,0);s.cam.updateMatrixWorld(true);
  const caption=el('notes-caption');
  const p=new THREE.Vector3(3.25,-1.22,1).project(s.cam);
  caption.style.transform=`translate(${(p.x*.5+.5)*1280}px,${(-p.y*.5+.5)*720}px)`;
  caption.style.opacity=easeOut(seg(t,D*.61,D*.7))*dismiss;
  s.composer.render();beatFade(t,D,0.3,0.3);
}
