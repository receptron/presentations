// requires: geometries/RoundedBoxGeometry
let S;
async function setupUI() {
  await waitFonts();
  el('ui-app').textContent=P.app;el('ui-logo').textContent=Array.from(P.app)[0];el('ui-headline').textContent=P.headline;el('ui-chart-label').textContent=P.app;
  // Values are sample chart data; optional P.series and P.metrics replace them without changing the shot.
  const data=P.series || Array.from({length:25},(_,i)=>.18+i*.024+rnd(i+27)*.18);
  const metrics=P.metrics || [{value:Math.round(data.reduce((a,b)=>a+b,0)*1000)},{value:Math.round(data.length*38)},{value:Math.round(data[data.length-1]*100),suffix:'%'}];
  metrics.slice(0,3).forEach((m,i)=>{
    const card=document.createElement('div');card.className='ui-card';
    card.innerHTML='<div class="ui-card-label"><i class="ui-indicator"></i><span></span></div><div class="ui-number"><span></span><small></small></div><svg viewBox="0 0 109 42"><path fill="none" stroke="#92c9b9" stroke-width="1.7"/></svg>';
    card.querySelector('.ui-card-label span').textContent=m.label || P.app;
    card.querySelector('small').textContent=m.suffix || '';
    card.querySelector('path').setAttribute('d',data.filter((_,j)=>j%2===0).map((v,j)=>`${j?'L':'M'}${j*9} ${39-v*32}`).join(' '));
    el('ui-metrics').appendChild(card);
  });
  for(let i=0;i<4;i++){
    const row=document.createElement('div');row.className='ui-row';row.innerHTML='<div class="ui-row-icon"></div><div class="ui-row-data"><i></i><i></i></div><div class="ui-row-value"></div>';
    row.querySelector('.ui-row-icon').textContent=String(i+1).padStart(2,'0');row.querySelector('.ui-row-data i').style.width=`${55+rnd(i+6)*40}%`;el('ui-rows').appendChild(row);
  }
  const ns='http://www.w3.org/2000/svg';for(let i=0;i<5;i++){const l=document.createElementNS(ns,'path');l.setAttribute('d',`M0 ${12+i*44}H568`);l.setAttribute('stroke','#ffffff0c');el('ui-grid').appendChild(l);}
  const points=data.map((v,i)=>[i*568/(data.length-1),188-v*168]);const path=points.map((p,i)=>`${i?'L':'M'}${p.join(' ')}`).join(' ');
  el('ui-line').setAttribute('d',path);el('ui-area').setAttribute('d',`${path}L568 205L0 205Z`);
  el('ui-baseline').setAttribute('d',data.map((v,i)=>`${i?'L':'M'}${i*568/(data.length-1)} ${190-v*95}`).join(' '));
  const s=makeRenderer('ui-canvas',[.22,.4,1.2]);s.points=points;s.metrics=metrics;
  s.cam.fov=31;s.cam.updateProjectionMatrix();
  s.scene.background=new THREE.Color(0x03070d);
  const env=new StudioEnv(),pm=new THREE.PMREMGenerator(s.R);s.env=pm.fromScene(env,.06);s.scene.environment=s.env.texture;env.dispose();pm.dispose();
  const panel=new THREE.Group();panel.position.y=2.92;s.scene.add(panel);s.panel=panel;
  const chassis=new THREE.Mesh(new THREE.RoundedBoxGeometry(10.12,5.76,.13,4,.13),new THREE.MeshStandardMaterial({color:0x8198a9,metalness:1,roughness:.23}));panel.add(chassis);
  const lip=new THREE.Mesh(new THREE.RoundedBoxGeometry(10.04,5.68,.06,4,.12),new THREE.MeshPhysicalMaterial({color:0x09121d,metalness:.5,roughness:.14,clearcoat:1}));lip.position.z=.075;panel.add(lip);
  // Ground catches a broad screen-coloured light pool, with clear falloff into black.
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0x07101b,roughness:.3,metalness:.3}));floor.rotation.x=-Math.PI/2;floor.position.y=-.62;s.scene.add(floor);
  const pool=new THREE.Mesh(new THREE.PlaneGeometry(15,10),new THREE.MeshBasicMaterial({map:dotTex('83,141,175'),transparent:true,opacity:.12,depthWrite:false,blending:THREE.AdditiveBlending}));pool.rotation.x=-Math.PI/2;pool.position.set(0,-.61,.5);s.scene.add(pool);
  const key=new THREE.DirectionalLight(0xc8e7ff,1.2);key.position.set(-4,8,6);s.scene.add(key);
  const rim=new THREE.PointLight(0x68a2ff,2.4,20,2);rim.position.set(6,3,-1);s.scene.add(rim);
  s.scene.add(new THREE.HemisphereLight(0x7395af,0x06090d,.15));
  return s;
}
// Homography from the four projected glass corners. The z diagonal must stay 1.
function projectUI(panel,cam) {
  const q=[[-5,2.818],[5,2.818],[5,-2.818],[-5,-2.818]].map(([x,y])=>{const v=new THREE.Vector3(x,y,.112);panel.localToWorld(v);v.project(cam);return {x:(v.x+1)*640,y:(1-v.y)*360};});
  const [a,b,c,d]=q;const dx1=b.x-c.x,dx2=d.x-c.x,dx3=a.x-b.x+c.x-d.x,dy1=b.y-c.y,dy2=d.y-c.y,dy3=a.y-b.y+c.y-d.y;
  const det=dx1*dy2-dx2*dy1,g=(dx3*dy2-dx2*dy3)/det,h=(dx1*dy3-dx3*dy1)/det;
  const m=[(b.x-a.x+g*b.x)/1100,(b.y-a.y+g*b.y)/1100,0,g/1100,(d.x-a.x+h*d.x)/620,(d.y-a.y+h*d.y)/620,0,h/620,0,0,1,0,a.x,a.y,0,1];
  el('ui-plane').style.transform=`matrix3d(${m.join(',')})`;
}
async function render(frame,totalFrames,fps) {
  if(!S)S=setupUI();const s=await S,t=frame/fps,u=clamp01(t/D),k=ease(u);
  s.panel.rotation.y=lerp(-.055,.035,k);s.panel.rotation.z=lerp(-.018,.012,k);s.panel.position.y=2.92+Math.sin(u*Math.PI)*.065;
  s.cam.position.set(lerp(-3.5,2.5,k),lerp(4.4,3.7,k),lerp(13.9,13.15,k));s.cam.lookAt(0,2.88,0);s.cam.updateMatrixWorld();s.panel.updateMatrixWorld(true);
  projectUI(s.panel,s.cam);
  const count=easeOut(seg(t,D*.12,D*.62));document.querySelectorAll('.ui-number>span').forEach((n,i)=>{n.textContent=Math.round(s.metrics[i].value*count).toLocaleString('en-US');});
  document.querySelectorAll('.ui-row-value').forEach((n,i)=>{n.textContent=Math.round(s.points[i*3][1]*count).toLocaleString('en-US');});
  const draw=easeOut(seg(t,D*.16,D*.74));el('ui-reveal').setAttribute('width',568*draw);
  const idx=draw*(s.points.length-1),j=Math.min(s.points.length-2,Math.floor(idx)),p=s.points[j],q=s.points[j+1];el('ui-point').setAttribute('cx',lerp(p[0],q[0],idx-j));el('ui-point').setAttribute('cy',lerp(p[1],q[1],idx-j));el('ui-point').style.opacity=seg(t,D*.16,D*.23);
  s.composer.render();beatFade(t,D,.3,.3);
}
