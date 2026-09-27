// Procedural sleeves and local-space hands. H is the cuff / wrist, not the fingertip.
const MAN_JS = `
const RAD = Math.PI / 180;
const rotP = (p,c,deg) => { const a=deg*RAD, x=p[0]-c[0], y=p[1]-c[1]; return [c[0]+x*Math.cos(a)-y*Math.sin(a),c[1]+x*Math.sin(a)+y*Math.cos(a)]; };
const lerpP = (a,b,t) => [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];
const lerpPose = (a,b,t) => ({E:lerpP(a.E,b.E,t),H:lerpP(a.H,b.H,t)});
const mirPose = p => ({E:[400-p.E[0],p.E[1]],H:[400-p.H[0],p.H[1]]});
const SL=[152,290], SR=[248,290], NECK=[200,250];
const P={
 down:{E:[112,331],H:[131,381]},
 head:{E:[99,303],H:[139,211]},
 cheer:{E:[72,210],H:[92,100]},
 point:{E:[99,252],H:[61,181]}
};
const armUnit=(a,b) => { const x=b[0]-a[0], y=b[1]-a[1], n=Math.hypot(x,y); return n>0.001?[x/n,y/n]:[0,-1]; };
const armAdd=(a,b,k=1) => [a[0]+b[0]*k,a[1]+b[1]*k];
const armXY=p => p.map(x=>Number(x.toFixed(3))).join(' ');
const HANDS={
 relaxed:{outline:'M-8 0 C-10 -8 -12 -14 -10 -20 Q-8 -24 -5 -21 L-2 -15 L-1 -30 Q0 -35 3 -33 L6 -19 L6 -31 Q8 -35 11 -31 L13 -17 L14 -26 Q17 -30 19 -25 L20 -11 Q20 -3 9 2 Z', lines:'M6 -19 L8 -9 M13 -17 L14 -9 M-2 -15 Q1 -8 -2 -5'},
 palm:{outline:'M-9 1 C-12 -8 -14 -17 -13 -26 L-12 -39 Q-11 -44 -8 -42 L-6 -27 L-6 -46 Q-5 -51 -2 -48 L0 -28 L1 -48 Q3 -53 6 -48 L7 -28 L9 -43 Q12 -47 14 -42 L14 -20 L20 -27 Q24 -30 26 -26 Q27 -24 24 -20 L18 -9 Q15 -3 9 1 Z',lines:'M-6 -27 L-5 -17 M0 -28 L1 -18 M7 -28 L7 -18 M18 -16 Q9 -17 7 -9'},
 point:{outline:'M-9 0 L-13 -13 Q-16 -22 -11 -25 Q-8 -27 -5 -22 L-5 -45 Q-5 -51 -1 -51 Q3 -51 3 -46 L4 -25 Q7 -29 11 -24 Q16 -27 19 -20 Q23 -21 24 -15 L22 -6 Q19 0 9 2 Z',lines:'M4 -25 L5 -15 Q8 -12 11 -16 L11 -23 M11 -16 Q15 -12 18 -16 L18 -20 M-11 -23 L-3 -14 Q2 -11 4 -6'},
 fist:{outline:'M-9 1 L-13 -9 L-14 -24 Q-13 -30 -8 -30 Q-4 -35 1 -31 Q6 -35 11 -30 Q17 -32 20 -26 L22 -15 Q23 -5 10 2 Z',lines:'M-8 -29 L-7 -21 M1 -30 L2 -22 M11 -29 L12 -22 M-12 -15 Q-7 -21 -2 -18 L11 -13 Q15 -9 10 -6 L-1 -9 M16 -23 L17 -18'}
};
const setArm=(id,side,S,pose,hand='relaxed')=>{
 const E=pose.E,H=pose.H,u=armUnit(S,E),v=armUnit(E,H),n=[-u[1],u[0]],m=[-v[1],v[0]];
 // A rounded, tapered silhouette: the elbow is a quadratic fold, never a stroked tube.
 const a=armAdd(S,n,22), b=armAdd(S,n,-22), tip=armAdd(H,v,-12);
 const bend=u[0]*v[1]-u[1]*v[0], dot=u[0]*v[0]+u[1]*v[1];
 const edge=k=>{
   const q=armAdd(E,n,16*k), r=armAdd(E,m,16*k);
   const bis=[n[0]+m[0],n[1]+m[1]];
   const join=armAdd(E,bis,16*k/Math.max(0.18,1+dot));
   if(k*bend>0) return {d:' L'+armXY(join),end:armAdd(tip,m,11*k),join};
   return {d:' L'+armXY(armAdd(q,u,-8))+' Q'+armXY(q)+' '+armXY(armAdd(E,bis,8*k))+' Q'+armXY(r)+' '+armXY(armAdd(r,v,8)),end:armAdd(tip,m,11*k),join};
 };
 const l=edge(1),r=edge(-1),f=armXY;
 // Trace each side in the same direction, then reverse the second through explicit points.
 const reverse=k=>{
   const q=armAdd(E,n,16*k),r=armAdd(E,m,16*k),bis=[n[0]+m[0],n[1]+m[1]];
   if(k*bend>0)return ' L'+f(armAdd(E,bis,16*k/Math.max(0.18,1+dot)));
   return ' L'+f(armAdd(r,v,8))+' Q'+f(r)+' '+f(armAdd(E,bis,8*k))+' Q'+f(q)+' '+f(armAdd(q,u,-8));
 };
 const d='M'+f(a)+l.d+' L'+f(l.end)+' L'+f(r.end)+reverse(-1)+' L'+f(b)+' Q'+f(armAdd(S,u,-12))+' '+f(a)+' Z';
 el(id+'-sleeve'+side).setAttribute('d',d);
 const angle=Math.atan2(v[1],v[0])/RAD+90, transform='translate('+H.join(' ')+') rotate('+angle+')';
 el(id+'-cuff'+side).setAttribute('transform',transform);
 const handScale=hand==='fist'?1.18:1;
 el(id+'-hand'+side).setAttribute('transform',transform+' scale('+((side==='R'?-1:1)*handScale)+' '+handScale+')');
 const shape=HANDS[hand]||HANDS.relaxed;
 el(id+'-hand'+side+'-shape').setAttribute('d',shape.outline);
 el(id+'-hand'+side+'-lines').setAttribute('d',shape.lines);
 const foldStart=armAdd(armAdd(E,u,-9),n,-Math.sign(bend)*5),foldEnd=armAdd(E,v,7);
 el(id+'-fold'+side).setAttribute('d','M'+f(foldStart)+' Q'+f(E)+' '+f(foldEnd));
 // Raised arm: the shoulder belongs to the arm, so cover the torso's shoulder line with a cap
 // whose top contour runs from the neck base into the sleeve's inner edge.
 const capFill=el(id+'-cap'+side+'-fill'), capLine=el(id+'-cap'+side+'-line');
 const raised=E[1]<S[1]-20;
 capFill.style.display=raised?'':'none'; capLine.style.display=raised?'':'none';
 if(raised){
   const dist=p=>Math.hypot(p[0]-NECK[0],p[1]-NECK[1]);
   const inner=dist(a)<dist(b)?a:b, outer=inner===a?b:a;
   const isL=side==='L', nb=isL?[182,261]:[218,261], pit=isL?[137,312]:[263,312];
   const in2=armAdd(inner,u,30), out2=armAdd(outer,u,30);
   const ctrl=[nb[0]+(in2[0]-nb[0])*0.55, nb[1]+2];
   capFill.setAttribute('d','M'+f(nb)+' Q'+f(ctrl)+' '+f(in2)+' L'+f(out2)+' L'+f(outer)+' L'+f(pit)+' L'+f(isL?[176,300]:[224,300])+' Z');
   capLine.setAttribute('d','M'+f(nb)+' Q'+f(ctrl)+' '+f(in2)+' M'+f(out2)+' L'+f(outer)+' L'+f(pit));
 }
};
const face=(id,expr)=>['worried','happy','neutral'].forEach(e=>{el(id+'-'+e).style.display=e===expr?'':'none';});
const headRot=(id,deg)=>el(id+'-head').setAttribute('transform','rotate('+deg+' '+NECK.join(' ')+')');
const blinkEyes=(id,t,offset=0)=>{const s=((t+offset)%2.6)<0.1?0.1:1;el(id+'-eyes').setAttribute('transform','translate(0 '+180*(1-s)+') scale(1 '+s+')');};
`;

const manSVG = id => `<svg id="${id}" viewBox="0 0 400 420" width="100%" height="100%" style="overflow:visible" fill="white" stroke="#222" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
${['L','R'].map(s=>`<path id="${id}-sleeve${s}"/><path id="${id}-fold${s}" fill="none" stroke-width="1.7"/>`).join('')}
<!-- Sloped shoulders disappear beneath the animated sleeves. -->
<path d="M126 426 Q128 372 134 329 L137 286 Q151 271 174 265 L184 256 L216 255 L226 265 Q249 270 263 286 L266 329 Q272 374 274 426 Z"/>
<path d="M139 294 Q145 313 145 330 L151 349 Q142 325 139 294 M256 294 Q249 321 249 341 L243 356 Q258 329 256 294 M140 384 L148 414 L154 421 Q144 398 140 384" fill="#e6e6e6" stroke="none"/>
<path d="M140 291 Q145 317 145 330 M257 294 Q249 319 249 337 M151 373 Q155 393 166 402 M254 373 Q246 390 233 400" fill="none" stroke-width="1.5"/>
${['L','R'].map(s=>`<path id="${id}-cap${s}-fill" fill="white" stroke="none" style="display:none"/><path id="${id}-cap${s}-line" fill="none" style="display:none"/>`).join('')}
<path d="M184 245 L182 265 L199 280 L220 263 L216 241 Z"/>
<path d="M185 249 Q199 261 215 245 L216 254 Q200 270 184 258 Z" fill="#e6e6e6" stroke="none"/>
<path d="M183 259 L199 278 L184 303 L176 270 Z M218 256 L228 269 L217 303 L200 279 Z"/>
<path d="M192 281 Q200 277 208 282 L205 296 L198 300 L190 290 Z" fill="#233a8b" stroke-width="2.7"/>
<path d="M198 299 L205 296 Q207 330 211 396 L199 412 L187 397 Q190 340 198 299 Z" fill="#233a8b" stroke-width="2.7"/>
<path d="M193 348 L208 337 L209 346 L192 358 Z" stroke="none"/>
<g id="${id}-head">
<!-- A tapered jaw, asymmetric ears, and an open forehead under layered bangs. -->
<path d="M147 174 Q132 162 137 184 Q138 197 149 198 L157 187 Z"/>
<path d="M247 174 Q258 160 264 173 Q269 186 256 198 L245 201 Z"/>
<path d="M255 179 Q261 172 260 181 L253 189 M142 177 Q146 179 146 187" fill="none" stroke-width="1.6"/>
<path d="M144 158 Q145 133 170 122 Q211 104 241 135 Q254 155 251 187 Q247 215 231 233 Q215 249 202 252 Q187 250 171 233 Q155 218 149 198 Z"/>
<path d="M245 190 Q239 222 218 240 L203 249 Q221 247 235 230 Q251 210 251 188 Z" fill="#e6e6e6" stroke="none"/>
<path d="M144 158 Q145 133 170 122 Q211 104 241 135 Q254 155 251 187 Q247 215 231 233 Q215 249 202 252 Q187 250 171 233 Q155 218 149 198 Z" fill="none"/>
<!-- Broken, swept silhouette with overlapping locks; no smooth hair cap. -->
<path d="M141 181 L137 160 L132 173 Q128 153 135 132 L120 141 Q135 124 140 109 L132 111 Q150 96 170 93 Q155 88 143 80 Q159 84 177 78 Q195 71 210 81 Q207 72 201 66 Q218 71 223 85 Q239 77 252 88 L241 88 Q263 99 267 119 Q271 128 278 132 L266 131 L271 146 L259 140 Q265 160 252 182 L249 163 Q232 154 225 134 Q225 151 237 157 Q220 152 212 127 Q202 146 183 157 L191 141 Q177 157 160 165 L169 150 Q157 157 147 164 Z"/>
<path d="M137 145 Q145 124 163 112 Q147 120 136 138 Z M153 107 Q177 86 202 89 Q184 90 170 102 Z M224 95 Q248 102 256 123 Q247 107 233 106 Z M240 133 L253 157 L253 167 Q245 153 240 133 Z" fill="#e6e6e6" stroke="none"/>
<path d="M144 143 Q157 119 184 109 M158 147 Q182 131 198 110 M178 143 Q199 123 206 104 M169 98 Q186 87 207 91 M223 101 Q227 121 239 133 M239 99 Q251 111 255 124" fill="none" stroke-width="1.7"/>
<!-- The lens shapes follow the brow, with a low bridge and fine temples. -->
<path d="M148 175 L139 169 M242 174 L255 169" fill="none" stroke-width="3"/>
<path d="M152 169 Q169 166 190 169 Q195 170 194 177 L192 191 Q191 195 185 195 L160 194 Q154 194 153 189 L151 175 Q150 172 152 169 Z M208 169 Q223 166 241 168 Q246 169 245 175 L243 188 Q242 193 237 194 L214 195 Q207 195 206 189 L204 177 Q203 171 208 169 Z" fill="none" stroke-width="3.5"/>
<path d="M195 176 Q199 173 204 176" fill="none" stroke-width="2.8"/>
<g id="${id}-eyes" stroke="none">
<ellipse cx="176" cy="181" rx="4.1" ry="7" fill="#222"/><ellipse cx="224" cy="180" rx="4.1" ry="7" fill="#222"/>
<ellipse cx="175" cy="178" rx="1.1" ry="1.6"/><ellipse cx="223" cy="177" rx="1.1" ry="1.6"/>
</g>
<path d="M200 188 Q196 199 198 201 M200 207 Q205 210 209 207" fill="none" stroke-width="1.9"/>
<g id="${id}-worried">
<path d="M155 162 Q169 162 187 155 M211 155 Q226 161 241 160" fill="none" stroke-width="4.4"/>
<path d="M184 226 Q197 217 214 225 M194 235 Q200 232 207 234" fill="none" stroke-width="2.3"/>
<path d="M273 155 Q267 168 272 172 Q281 173 273 155 Z" stroke-width="1.7"/>
</g>
<g id="${id}-happy">
<path d="M155 161 Q171 150 187 160 Q172 156 155 161 Z M210 159 Q225 148 242 159 Q225 154 210 159 Z" fill="#222" stroke-width="1.7"/>
<path d="M182 217 Q202 220 224 216 Q219 239 203 239 Q190 238 182 217 Z" fill="#222" stroke-width="2.5"/>
<path d="M185 218 Q203 222 221 217 L218 224 Q204 229 190 225 Z" stroke="none"/>
<path d="M192 234 Q205 225 216 232 Q207 241 199 237 Z" fill="#e6e6e6" stroke="none"/>
<path d="M198 246 Q204 248 211 244" fill="none" stroke-width="1.3"/>
</g>
<g id="${id}-neutral">
<path d="M155 161 Q171 155 187 160 M211 159 Q227 153 241 158" fill="none" stroke-width="4"/>
<path d="M188 223 Q203 230 217 222 M198 235 Q204 237 209 234" fill="none" stroke-width="1.9"/>
</g>
</g>
${['L','R'].map(s=>`<g id="${id}-hand${s}"><path id="${id}-hand${s}-shape"/><path id="${id}-hand${s}-lines" fill="none" stroke-width="1.7"/></g><g id="${id}-cuff${s}"><path d="M-11 12 L11 12 L10 0 L-10 0 Z"/><path d="M-6 8 L-6 5" fill="none" stroke-width="1.5"/></g>`).join('')}
</svg>`;

export {manSVG,MAN_JS};
