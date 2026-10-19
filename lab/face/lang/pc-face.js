/* <pc-face> · the æsymov face as one shared component.
   One head everywhere. mood = system state · crown = product · color = edition.
   Read-only: the face shows, it never decides. Human stays root.
   <pc-face mood="ready" crown="pc" size="96"></pc-face>  ·  el.mood = "checking"  */
(()=>{
const CROWN={pc:"#00f3ff",week:"#3ddc84",moon:"#ffb020",qr:"#4c9be8",sun:"#f2d16b"};
const MOOD={ /* visor eyes · mouth · visor tint · meaning */
 ready:   {eyes:"M88 120H106M134 120H152", mouth:"M100 196Q120 206 140 196", tint:null,  say:"ready · I watch the door"},
 think:   {eyes:"dots",                    mouth:"M104 198H136",              tint:null,  say:"thinking · reading your words"},
 checking:{eyes:"scan",                    mouth:"M104 198H136",              tint:null,  say:"checking · spelling, tone, rules"},
 ok:      {eyes:"M88 126L97 114L106 126M134 126L143 114L152 126", mouth:"M96 192Q120 214 144 192", tint:"#3ee08f", say:"approved · a human held it"},
 stop:    {eyes:"M90 114L104 128M104 114L90 128M136 114L150 128M150 114L136 128", mouth:"M100 204Q120 194 140 204", tint:"#ff6b6b", say:"stop · nothing leaves without you"},
 sleep:   {eyes:"M88 124Q97 130 106 124M134 124Q143 130 152 124", mouth:"M108 200H132", tint:"#557", say:"asleep · no human signed in"},
 lost:    {eyes:"M92 112Q97 104 102 112Q102 118 97 120M97 128V129M138 112Q143 104 148 112Q148 118 143 120M143 128V129", mouth:"M106 200Q120 196 134 200", tint:"#ffcf5c", say:"lost · I don't have a door for that"}};
const CROWNPATH={
 pc:'<path d="M111 40L115.5 45L120 40M125 31V45" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
 week:[0,1,2,3,4,5,6].map(k=>{const a=-Math.PI/2+k*2*Math.PI/7;return `<circle cx="${(120+15*Math.cos(a)).toFixed(1)}" cy="${(40+15*Math.sin(a)).toFixed(1)}" r="3" ${k?'fill="none" stroke-width="1.6"':'stroke="none"'}/>`}).join(""),
 moon:'<circle cx="120" cy="40" r="13" stroke="none"/><circle cx="127" cy="35" r="11" fill="#141416" stroke="none"/>',
 qr:'<rect x="108" y="28" width="24" height="24" fill="none" stroke-width="2"/><rect x="113" y="33" width="6" height="6" stroke="none"/><rect x="121" y="41" width="6" height="6" stroke="none"/>',
 sun:'<circle cx="120" cy="40" r="7" stroke="none"/>'+[...Array(12)].map((_,k)=>{const a=k*Math.PI/6;return `<path d="M${(120+11*Math.cos(a)).toFixed(1)} ${(40+11*Math.sin(a)).toFixed(1)}L${(120+17*Math.cos(a)).toFixed(1)} ${(40+17*Math.sin(a)).toFixed(1)}" stroke-width="2" stroke-linecap="round"/>`}).join("")};
const RM=()=>matchMedia("(prefers-reduced-motion:reduce)").matches;
class PCFace extends HTMLElement{
 static get observedAttributes(){return["mood","crown","size","label"]}
 constructor(){super();this.attachShadow({mode:"open"})}
 get mood(){return this.getAttribute("mood")||"ready"} set mood(v){this.setAttribute("mood",v)}
 connectedCallback(){this.render();this._pm=e=>this.look(e);addEventListener("pointermove",this._pm,{passive:true})}
 disconnectedCallback(){removeEventListener("pointermove",this._pm)}
 attributeChangedCallback(){if(this.isConnected)this.render()}
 look(e){if(RM()||!this._g)return;const r=this.getBoundingClientRect();if(!r.width)return;
  const dx=Math.max(-1,Math.min(1,(e.clientX-(r.left+r.width/2))/400)),dy=Math.max(-1,Math.min(1,(e.clientY-(r.top+r.height/2))/400));
  this._g.style.transform=`translate(${(dx*7).toFixed(1)}px,${(dy*4).toFixed(1)}px)`}
 render(){
  const m=MOOD[this.mood]||MOOD.ready,crown=CROWN[this.getAttribute("crown")]?this.getAttribute("crown"):"pc",c=CROWN[crown],tint=m.tint||c,size=+this.getAttribute("size")||96;
  let eyes;
  if(m.eyes==="dots")eyes=`<g class="dots"><circle cx="100" cy="120" r="5"/><circle cx="120" cy="120" r="5"/><circle cx="140" cy="120" r="5"/></g>`;
  else if(m.eyes==="scan")eyes=`<rect class="scan" x="72" y="98" width="8" height="44" rx="3" stroke="none"/><path d="M88 120H106M134 120H152" stroke-width="4" stroke-linecap="round" opacity=".35"/>`;
  else eyes=`<path d="${m.eyes}" fill="none" stroke-width="${this.mood==="ready"?5:4}" stroke-linecap="round" stroke-linejoin="round"/>`;
  this.shadowRoot.innerHTML=`<style>
   :host{display:inline-block;width:${size}px;height:${(size*260/240).toFixed(0)}px;line-height:0}
   svg{width:100%;height:100%;overflow:visible}
   .eyes{transition:transform .9s cubic-bezier(.2,.8,.2,1)}
   .dots circle{animation:d 1.2s ease-in-out infinite}.dots circle:nth-child(2){animation-delay:.2s}.dots circle:nth-child(3){animation-delay:.4s}
   @keyframes d{50%{opacity:.25;transform:translateY(-3px)}}
   .scan{animation:s 1.4s ease-in-out infinite alternate}@keyframes s{to{transform:translateX(88px)}}
   .z{animation:z 2.4s ease-in-out infinite;font:700 22px ui-monospace,monospace}@keyframes z{50%{opacity:.2;transform:translateY(-6px)}}
   @media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
  </style>
  <svg viewBox="0 0 240 260" role="img" aria-label="${(this.getAttribute("label")||"æsymov")+" · "+m.say}">
   <path d="M52 78Q52 18 120 18Q188 18 188 78V176Q188 246 120 250Q52 246 52 176Z" fill="#141416" stroke="#3a3a3e" stroke-width="3"/>
   <g fill="${c}" stroke="${c}">${CROWNPATH[crown]}</g>
   <rect x="66" y="92" width="108" height="56" rx="26" fill="#030a0b" stroke="${tint}" stroke-width="3"/>
   <g class="eyes" fill="${tint}" stroke="${tint}" style="filter:drop-shadow(0 0 4px ${tint})">${eyes}</g>
   <path d="${m.mouth}" fill="none" stroke="${tint}" stroke-width="4" stroke-linecap="round"/>
   <path d="M52 176Q60 232 120 240Q180 232 188 176" fill="none" stroke="#b87333" stroke-opacity=".6" stroke-width="2.5"/>
   ${this.mood==="sleep"?`<text class="z" x="184" y="70" fill="${c}">z</text>`:""}
  </svg>`;
  this._g=this.shadowRoot.querySelector(".eyes");
  this.dispatchEvent(new CustomEvent("pc-face",{detail:{mood:this.mood,crown,say:m.say},bubbles:true}))}
}
if(!customElements.get("pc-face"))customElements.define("pc-face",PCFace);
window.PC_FACE={schema:"ae.face/0.1",moods:Object.fromEntries(Object.entries(MOOD).map(([k,v])=>[k,v.say])),crowns:CROWN,rule:"the face shows, it never decides"};
})();
