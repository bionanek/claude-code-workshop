# -*- coding: utf-8 -*-
import json, io, os

import base64
_here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_here, 'assets', 'claude-walk.gif'), 'rb') as _f:
    WALK = 'data:image/gif;base64,' + base64.b64encode(_f.read()).decode('ascii')
with open(os.path.join(_here, 'assets', 'rocketchat.png'), 'rb') as _f:
    RC = 'data:image/png;base64,' + base64.b64encode(_f.read()).decode('ascii')

CSS = r"""
:root{
  --bg:#191820; --panel:#211f2a; --fg:#f4f2ee; --dim:#a09aa8; --rule:#38343f;
  --accent:#e8a878; --demo:#ffd85c; --bad:#f08a7e; --good:#8fd0a0; --code:#141319;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;background:var(--bg)}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  color:var(--fg);-webkit-font-smoothing:antialiased;font-weight:400}
#deck{position:fixed;inset:0;background:var(--bg)}
/* generous safe margins - Zoom/Meet overlay the edges */
.slide{position:absolute;inset:0;display:none;padding:6.5vh 7vw 6vh;overflow:hidden}
.slide.on{display:flex;align-items:center;justify-content:center}
.c{width:100%;max-width:84vw;transform-origin:center center}
.ctr{text-align:center}

/* persistent header: where are we */
.hdr{position:absolute;left:7vw;right:7vw;top:2.4vh;display:flex;justify-content:space-between;
  font:600 1.05vw/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:#5d5867}
.hdr .mod{color:var(--accent)}

.kick{font:700 1.25vw/1.35 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--dim);margin-bottom:1.8vh}
.kick.accent{color:var(--accent)}
.kick b{color:var(--demo);font-weight:700}
.kick code{font-family:var(--mono);color:var(--demo);background:none;padding:0}

/* bordered warning block - non-obvious knowledge that must not be skimmed */
.warnbox{border:2px solid var(--bad);border-radius:.6vw;padding:1.8vh 1.5vw;background:rgba(240,138,126,.07)}
.warnbox .tag{color:var(--bad);margin-bottom:1.2vh}
.warnbox .big-list li{border-bottom-color:rgba(240,138,126,.25)}

/* annotated prompt: one continuous prompt, braces pointing out to labels */
.anno{display:grid;grid-template-columns:21.5vw 3.2vw minmax(0,40vw);
  justify-content:center;align-items:stretch;row-gap:7vh;
  background:var(--code);border:1px solid var(--rule);border-radius:.6vw;
  padding:4vh 2.2vw 4vh 1.8vw}
.anno .what{text-align:right;font-size:1.28vw;line-height:1.35;align-self:center}
.anno .what b{display:block;font-family:var(--mono);font-size:1vw;letter-spacing:.09em;
  text-transform:uppercase;color:var(--accent);margin-bottom:.3vh}
.anno .what i{font-style:normal;color:var(--dim);font-size:1.14vw;display:block;hyphens:none}
.anno .brace{position:relative}
.anno .brace::before{content:'';position:absolute;left:38%;right:.1vw;top:.35vh;bottom:.35vh;
  border:2px solid var(--accent);border-left:0;border-radius:0 .4vw .4vw 0}
.anno .brace::after{content:'';position:absolute;left:0;right:62%;top:50%;
  border-top:2px solid var(--accent)}
.anno .frag{font-family:var(--mono);font-size:1.26vw;line-height:1.6;white-space:pre-wrap;
  padding-left:1.1vw;align-self:center}

/* episode chart: performance climbing across context resets */
.eps{display:flex;align-items:flex-end;justify-content:center;gap:1.8vw;height:30vh;margin:1.5vh 0 0;
  border-bottom:2px solid var(--rule);position:relative}
.eps::before{content:'100%';position:absolute;left:-2.6vw;top:-.6vh;font:600 .9vw/1 var(--mono);color:#5d5867}
.eps::after{content:'0';position:absolute;left:-1.2vw;bottom:-.6vh;font:600 .9vw/1 var(--mono);color:#5d5867}
.ep{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.ep .bar{width:5.2vw;background:linear-gradient(180deg,var(--good),#4e8a5f);
  border-radius:.3vw .3vw 0 0;position:relative}
.ep .pct{position:absolute;top:-2.9vh;left:0;right:0;text-align:center;
  font:700 1.25vw/1 var(--mono);color:var(--good)}
.who{font:600 1.02vw/1.3 var(--mono);color:var(--dim);text-align:center}
.ep{justify-content:flex-end}
.ep .reset{font:700 .92vw/1 var(--mono);color:var(--demo);margin-bottom:.9vh;letter-spacing:.04em}

/* retrieval vs reasoning: same axis, two very different reliable ranges */
.zones{margin-top:1.5vh}
.zbar{height:5vh;border-radius:.35vw;position:relative;
  background:linear-gradient(90deg,var(--good) 0%,var(--good) 22%,#8a7f3a 48%,var(--bad) 82%,var(--bad) 100%)}
.zbar span{position:absolute;top:50%;transform:translateY(-50%);
  font:800 1.15vw/1 var(--mono);letter-spacing:.14em;color:#191820}
.zbar .z1{left:1.6vw} .zbar .z2{right:1.6vw}
.zaxis{position:relative;height:1.6vh;margin-top:.8vh;font:600 1vw/1 var(--mono);color:var(--dim)}
.zaxis span{position:absolute;top:0} .zaxis .a0{left:0} .zaxis .a1{right:0}
.gauge{display:grid;grid-template-columns:13vw 1fr 23vw;gap:2.6vh 1.4vw;align-items:center;text-align:left}
.gauge .gl{font:700 1.15vw/1.25 var(--mono);letter-spacing:.05em;text-transform:uppercase}
.gauge .track{height:3.6vh;border-radius:.3vw;background:#2d2a37;position:relative;
  border:1px solid var(--rule)}
.gauge .fill{position:absolute;left:0;top:0;bottom:0;border-radius:.25vw}
.gauge .fill.hi{background:var(--good);right:0}
.gauge .fill.lo{background:var(--bad);width:9%}
.gauge .fade{position:absolute;top:0;bottom:0;left:5%;width:22%;
  background:linear-gradient(90deg,var(--bad),transparent)}
.gauge .gn{font-size:1.12vw;line-height:1.4;color:var(--dim)}
.gauge .gn b{color:var(--fg)}
.gaxis{position:relative;height:1.5vh;margin-top:.9vh;font:600 1vw/1 var(--mono);
  color:#5d5867;letter-spacing:.06em}
.gaxis span{position:absolute;top:0;white-space:nowrap}
.gaxis .a0{left:0}
.gaxis .a2{left:10%;transform:translateX(-50%);color:var(--bad)}
.gaxis .a1{right:0}
.gauge .tick{position:absolute;left:10%;top:-.5vh;bottom:-.5vh;width:1px;background:var(--bad);opacity:.7}

/* smart zone / dumb zone bar */
.zonebar{position:relative;margin:3vh 0 6vh;height:7vh;border-radius:.5vw;
  background:linear-gradient(90deg,var(--fg) 0%,var(--fg) 12%,#8f8a80 30%,#5a5560 60%,#3a3644 100%)}
.zonemark{position:absolute;top:-1vh;bottom:-1vh;width:3px;background:var(--bad)}
.zonemark span{position:absolute;left:50%;transform:translateX(-50%);bottom:-3.4vh;
  font:700 1.1vw/1 var(--mono);color:var(--bad);white-space:nowrap}
.zoneends{display:flex;justify-content:space-between;font:700 1.25vw/1 var(--mono);
  letter-spacing:.08em;text-transform:uppercase;margin-top:-4.5vh}
.zoneends span:first-child{color:var(--fg);padding-left:1vw}
.zoneends span:last-child{color:var(--dim);padding-right:1vw}
.extras{margin-top:2.4vh;padding-top:1.6vh;border-top:1px solid var(--rule);
  display:grid;grid-template-columns:1fr 1fr;gap:1.6vw;text-align:left}
.extras p{font-size:1.15vw;line-height:1.45;color:var(--dim)}
.extras p b{color:var(--fg);font-family:var(--mono)}
.extras .lbl{font:700 1vw/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  color:var(--dim);grid-column:1/-1;margin-bottom:-.6vh}
.big{font-size:4.6vw;line-height:1.06;letter-spacing:-.02em;font-weight:700}
.mid{font-size:3.1vw;line-height:1.12;font-weight:700;margin-bottom:2.4vh}
blockquote{font-size:3.3vw;line-height:1.26;font-weight:650;letter-spacing:-.012em}
blockquote em{color:var(--accent);font-style:italic}
.sub{font-size:1.5vw;line-height:1.5;color:var(--dim);margin-top:2.1vh;max-width:66vw;margin-left:auto;margin-right:auto}
.sub2{font-size:1.15vw;color:var(--dim);margin-top:1.2vh;line-height:1.5}
.attr{font:1.25vw/1.4 var(--mono);color:var(--accent);margin-top:2.4vh}
.mono{font-family:var(--mono)}
.dim{color:var(--dim)}
.acc{color:var(--accent)}
.num{position:absolute;right:7vw;bottom:2.2vh;font:600 1vw var(--mono);color:#4a4553}

/* the one-line takeaway that makes a slide work without the host */
.takeaway{margin-top:2.2vh;padding:1.3vh 1.4vw;border-left:4px solid var(--accent);
  background:rgba(232,168,120,.08);font-size:1.4vw;line-height:1.45;text-align:left;font-weight:500}
.takeaway b{color:var(--accent)}

/* chat prompt - the online participation primitive */
.chatq{margin-top:2vh;padding:1.4vh 1.6vw;border:2px dashed var(--demo);border-radius:.6vw;
  font-size:1.45vw;line-height:1.45;text-align:left;color:var(--demo);font-weight:600}
.chatq span{color:var(--dim);font-weight:400;display:block;font-size:1.15vw;margin-top:.8vh}

.fig{font-size:12vw;font-weight:800;letter-spacing:-.04em;line-height:1}
.unit{font-size:2.4vw;font-weight:600;color:var(--dim);margin-left:1.2vw;letter-spacing:0}

.spine{display:flex;align-items:center;justify-content:center;gap:1.4vw;flex-wrap:wrap}
.step{font:600 2vw/1 var(--mono);color:#57515f;padding:1.5vh 1.7vw;border:2px solid #403a49;border-radius:.6vw;position:relative}
.step.lit{color:var(--bg);background:var(--fg);border-color:var(--fg)}
.arrow{font-size:1.8vw;color:#57515f}
.opt{position:absolute;left:0;right:0;bottom:-3vh;font-size:.9vw;color:var(--dim);letter-spacing:.1em}

.rc{height:1.4em;width:auto;vertical-align:-.3em;margin-right:.4em}

/* the loop: the three steps as a cycle, with a return arrow closing it */
.loop{position:relative;width:78vw;margin:0 auto}
.loop .spine{margin:0;flex-wrap:nowrap}
.loop svg{display:block;width:100%;height:auto;margin-top:-1vh}

.bg{display:grid;grid-template-columns:1fr 1fr;gap:2vw;margin-top:1vh}
.col{border:1px solid var(--rule);border-radius:.6vw;padding:2.2vh 1.6vw;background:var(--code)}
.col.bad{border-left:4px solid var(--bad)}
.col.good{border-left:4px solid var(--good)}
.tag{font:700 1.05vw/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;margin-bottom:1.6vh}
.col.bad .tag{color:var(--bad)} .col.good .tag{color:var(--good)}
.bg pre{font-size:1.02vw;line-height:1.5}
.two pre.art,.two pre.term{font-size:1.04vw;line-height:1.5}
.col{max-height:66vh;overflow:hidden}

pre{font-family:var(--mono);font-size:1.25vw;line-height:1.55;white-space:pre-wrap;color:var(--fg);font-weight:500}
pre.art{background:var(--code);border:1px solid var(--rule);border-left:4px solid var(--accent);
  border-radius:.6vw;padding:2vh 1.5vw;font-size:1.12vw;line-height:1.55;text-align:left}
pre.term{background:var(--code);border:1px solid var(--rule);border-radius:.6vw;
  padding:2vh 1.5vw;font-size:1.12vw;line-height:1.55;text-align:left}
mark{background:var(--demo);color:#191820;padding:.08em .25em;border-radius:.2em;font-weight:700}
.cmt{color:var(--dim)}
.ok{color:var(--good)} .no{color:var(--bad)}

.big-list{list-style:none;counter-reset:l;text-align:left}
.big-list li{counter-increment:l;font-size:1.8vw;line-height:1.38;padding:1.1vh 0 1.1vh 3.6vw;position:relative;border-bottom:1px solid var(--rule)}
.big-list li:last-child{border-bottom:0}
.big-list li::before{content:counter(l);position:absolute;left:0;font:700 1.4vw var(--mono);color:var(--accent);top:1.9vh}
.big-list li code{font-family:var(--mono);background:var(--code);padding:.08em .3em;border-radius:.2em;font-size:.9em}
.big-list li i{display:block;font-size:1.15vw;font-style:normal;color:var(--dim);margin-top:.5vh;line-height:1.45}

.chain{list-style:none;counter-reset:ch;max-width:44vw;margin:2.2vh auto 0;padding:0;text-align:left}
.chain li{counter-increment:ch;position:relative;padding:0 0 2.5vh 4.4vw;font-size:1.55vw;line-height:1.25;
  color:var(--fg);font-weight:600}
.chain li::before{content:counter(ch);position:absolute;left:0;top:-.35vh;width:2.5vw;height:2.5vw;
  border-radius:50%;border:1px solid var(--accent);background:var(--code);color:var(--accent);
  font:700 1.05vw/2.4vw var(--mono);text-align:center}
.chain li::after{content:'';position:absolute;left:1.2vw;top:2.45vw;bottom:.3vh;width:2px;border-radius:1px;background:rgba(232,168,120,.34)}
.chain li:last-child{padding-bottom:0}
.chain li:last-child::after{display:none}
.chain li:last-child::before{border-color:var(--good);color:var(--good)}

.t{width:100%;border-collapse:collapse;font-size:1.25vw;text-align:left}
.t th{font:700 1vw var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--dim);
  padding:0 1vw 1.2vh 0;border-bottom:1px solid var(--rule);vertical-align:bottom}
.t td{padding:.9vh 1vw .9vh 0;border-bottom:1px solid var(--rule);vertical-align:top}
.t td:first-child{font-family:var(--mono);font-size:.95em;color:var(--fg)}
.t.hl tbody tr:nth-child(-n+3) td:first-child{color:var(--good);font-weight:700}

.two{display:grid;grid-template-columns:1fr 1fr;gap:2.2vw;text-align:left}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6vw;text-align:left}
.card{border:1px solid var(--rule);border-radius:.6vw;padding:2vh 1.4vw;background:var(--code)}
.card.hitl{border-left:4px solid var(--good)} .card.afk{border-left:4px solid var(--demo)}
.card .tag{font-size:1.25vw}
.card.hitl .tag{color:var(--good)} .card.afk .tag{color:var(--demo)}
.card p{font-size:1.2vw;line-height:1.5;color:var(--dim)}
.card p b{color:var(--fg)}
.card h4{font-size:1.6vw;margin-bottom:1vh;font-weight:700}
.card pre{font-size:1.02vw;line-height:1.5;color:var(--fg);font-weight:500;
  background:var(--bg);border:1px solid var(--rule);border-radius:.4vw;
  padding:1.4vh 1vw;margin:1.4vh 0}
.three .card h4{font-size:1.4vw;line-height:1.2;min-height:3.4vw}
.three .card p{font-size:1.15vw}

.five{display:flex;gap:1vw;justify-content:center;flex-wrap:wrap}
.fbox{font-size:1.5vw;font-weight:600;padding:1.8vh 1.4vw;border:1px solid var(--rule);border-radius:.6vw;background:var(--code);font-family:var(--mono)}
.fbox i{display:block;font-style:normal;font-size:1vw;color:var(--dim);font-family:ui-sans-serif,system-ui;margin-top:.6vh;font-weight:400}

.fils{display:flex;gap:1.6vw;justify-content:center;flex-wrap:wrap}
.fil{font-size:1.9vw;font-weight:650;padding:2.4vh 2vw;border:2px solid var(--accent);border-radius:.6vw;color:var(--accent)}
.fil i{display:block;font-style:normal;font-size:1.1vw;color:var(--dim);margin-top:.8vh;font-weight:400}

.mtg{display:flex;align-items:center;justify-content:center;gap:4vw;margin-bottom:1.5vh}
.grp{text-align:center} .grp p{font-size:1.2vw;color:var(--dim);margin-top:1.5vh;font-family:var(--mono)}
.dots{display:flex;gap:.7vw;justify-content:center}
.dots.many{display:grid;grid-template-columns:repeat(12,1fr);gap:.45vw;max-width:22vw}
.dot{width:1.4vw;height:1.4vw;border-radius:50%;background:var(--fg)}
.dots.many .dot{width:1.25vw;height:1.25vw;background:#57515f}
.vs{font:600 1.4vw var(--mono);color:var(--dim)}

.own{border:1px solid var(--rule);border-radius:.6vw;overflow:hidden;background:var(--code);text-align:left}
.own .row{display:flex;align-items:flex-start;gap:1vw;padding:2.2vh 1.3vw;border-bottom:1px solid var(--rule)}
.own .row:last-child{border-bottom:0}
.own .mine{border-left:4px solid var(--accent);background:rgba(232,168,120,.07)}
.own .theirs{border-left:4px solid var(--rule)}
.own h5{font:700 1.5vw/1.15 ui-sans-serif,system-ui;color:var(--fg);margin:0}
.own .theirs h5{color:var(--dim);font-weight:600}
.own i{display:block;font-style:normal;font-size:1.05vw;line-height:1.4;color:var(--dim);margin-top:.6vh}
.own .who{font:700 .92vw/1.6 var(--mono);letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent);margin-left:auto;white-space:nowrap;padding-top:.3vh}
.own .theirs .who{color:var(--dim);font-weight:500}

.ladder{display:flex;flex-direction:column;gap:1.8vh;text-align:left}
.rung{font-size:1.8vw;font-weight:650;padding:1.5vh 1.8vw;border-left:4px solid var(--accent);background:var(--code)}
.rung i{display:block;font-style:normal;font-size:1.25vw;color:var(--dim);font-weight:400;margin-top:.6vh}

.dense{display:flex;flex-direction:column;gap:1.8vh;margin-top:1vh;text-align:left}
.drow{display:grid;grid-template-columns:11vw 1fr;gap:1.8vw;align-items:baseline}
.dk{font-size:1.25vw;letter-spacing:.06em;text-transform:uppercase;font-weight:700;font-family:var(--mono)}
.dv{font-size:1.4vw;line-height:1.48}
.dv b{color:var(--demo)}

.steps li{opacity:.42} .steps li.lit{opacity:1}

#bar{position:fixed;left:0;top:0;height:3px;background:var(--accent);z-index:20;transition:width .15s}
#black{position:fixed;inset:0;background:var(--bg);z-index:30;display:none;align-items:center;justify-content:center;text-align:center;padding:7vw 6.5vh}
#black.on{display:flex}
#black .bigbrk{font-size:4.6vw;line-height:1.16;letter-spacing:-.02em;font-weight:700;margin:0}
#black .brkin{font:inherit;color:var(--accent);background:transparent;border:0;border-bottom:.5vh solid var(--dim);width:6.5ch;text-align:center;padding:0 .2ch;outline:none;caret-color:var(--accent);border-radius:0}
#black .brkin:focus{border-bottom-color:var(--accent)}
#black .subbrk{font-family:var(--mono);font-size:1.5vw;line-height:1.5;color:var(--dim);margin-top:2.1vh}
#ov{position:fixed;inset:0;background:rgba(12,11,15,.97);z-index:40;display:none;overflow:auto;padding:5vh 5vw}
#ov h2{font:600 1.1rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-bottom:1.6rem}
#ov .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(17rem,1fr));gap:.5rem}
#ov button{text-align:left;background:#211f2a;border:1px solid var(--rule);color:var(--fg);
  border-radius:4px;padding:.6rem .7rem;font:inherit;font-size:.8rem;cursor:pointer;display:flex;gap:.6rem}
#ov button:hover{border-color:var(--accent)}
#ov button b{color:var(--accent);font-family:var(--mono);font-size:.72rem;flex:0 0 1.8rem}
#help{position:fixed;left:7vw;bottom:2.2vh;font:1vw var(--mono);color:#4a4553;z-index:20}

/* laptop / narrow-window safety: nothing may fall under a readable floor */
@media (max-width:1100px){
  .big{font-size:5.6vw} blockquote{font-size:4vw} .sub{font-size:1.9vw}
  pre{font-size:1.5vw} pre.art,pre.term{font-size:1.45vw} .bg pre{font-size:1.3vw}
  .two pre.art,.two pre.term{font-size:1.32vw}
  .t{font-size:1.6vw} .t th{font-size:1.25vw}
  .takeaway{font-size:1.75vw} .chatq{font-size:1.8vw} .kick{font-size:1.6vw} .sub2{font-size:1.45vw}
  .big-list li{font-size:2.2vw} .big-list li i{font-size:1.5vw}
  .card p{font-size:1.55vw} .card h4{font-size:1.85vw} .dv{font-size:1.75vw} .dk{font-size:1.45vw}
  .hdr{font-size:1.3vw} .rung{font-size:2.1vw} .rung i{font-size:1.5vw}
  .step{font-size:2.4vw} .fbox{font-size:1.8vw} .fil{font-size:2.1vw}
  .anno{grid-template-columns:25vw 3.6vw minmax(0,44vw)}
  .anno .frag{font-size:1.45vw} .anno .what{font-size:1.5vw} .anno .what i{font-size:1.4vw}
  .anno .what b{font-size:1.22vw} .anno{row-gap:7vh} .extras p{font-size:1.45vw} .extras .lbl{font-size:1.25vw}
}
@media (max-aspect-ratio:4/3){.big{font-size:7vw}blockquote{font-size:5.2vw}}
"""

S = []  # (module_label, index_title, inner_html)

def add(mod, title, html):
    html = html.replace('__RC__', RC).replace('__WALK__', WALK)
    S.append((mod, title, html))

# ---------- OPENING ----------
add("", "Building Your Own Claude Code Practice", """
<div class="c ctr"><p class="kick">Claude Code Workshop - online edition</p>
<h1 class="big">Building Your Own Claude&nbsp;Code Practice</h1>
<p class="sub mono">Context in - Verify - Persist - Automate</p>
<p class="sub" style="margin-top:3.2vh"><b class="mono" style="color:var(--accent);font-size:1.9vw"><img class="rc" src="__RC__" alt="Rocket Chat">#Claude_szkolenie</b></p></div>""")

add("", "The entire workshop, apparently", """
<div class="c ctr"><p class="kick">The entire workshop, apparently</p>
<pre class="art" style="font-size:1.9vw;line-height:1.7;display:inline-block;text-align:left"># CLAUDE.md

Write good code.
Make no mistakes.</pre>
<div class="takeaway" style="max-width:64vw;margin-left:auto;margin-right:auto">Every one of us has written some version of this and quietly hoped. <b>It does not work</b>, and the reason it does not work is what everything after this slide is about: the model has no idea what <i>good</i> means in your repo, no way to check whether it made a mistake, and no memory of the last time you told it.</div></div>""")

add("", "Before we start", """
<div class="c"><p class="kick accent">Before we start</p>
<ul class="big-list">
<li><b>Questions go in the channel, any time.</b><i><img class="rc" src="__RC__" alt="">Rocket Chat, <b style="color:var(--accent)">#Claude_szkolenie</b>. Don't wait for a gap and don't unmute unless you want to.</i></li>
<li><b>Your own experience goes in the channel too.</b><i>What worked for you, what didn't, where you disagree with something on a slide. That is more useful to the room than anything I can say about it.</i></li>
<li><b>Try things as we go if you want.</b><i>If something on a slide is worth running against your own repo while we talk, go ahead. Nothing here needs your full attention to follow.</i></li>
<li><b>Two breaks, 10 minutes each.</b><i>Roughly a third and two thirds of the way through.</i></li>
</ul></div>""")

add("", "Context in → Verify → Persist → Automate", """
<div class="c ctr"><div class="spine">
<div class="step">Context in</div><div class="arrow">&rarr;</div>
<div class="step">Verify</div><div class="arrow">&rarr;</div>
<div class="step">Persist</div><div class="arrow">&rarr;</div>
<div class="step">Automate</div></div>
<div class="takeaway">Four moves, and the day is built out of them in this order. <b>The last one is optional</b> - automating a workflow you never verified just scales the mistake.</div></div>""")

# ---------- PART A ----------
add("Part A", "Foundations", """
<div class="c ctr"><p class="kick accent">Part one</p><h1 class="big">Foundations</h1>
<p class="sub mono">Works out of the box - zero setup, nothing to install</p></div>""")

add("M0", "What this thing actually is", """
<div class="c"><p class="kick">What this thing actually is</p>
<div class="spine"><div class="step">Gather context</div><div class="arrow">&rarr;</div>
<div class="step">Take action</div><div class="arrow">&rarr;</div><div class="step lit">Verify results</div></div>
<p class="sub">It reads your files, runs commands and edits code in a loop. The phases blend: a question may only need the first, a bug fix cycles all three. And <b>you are inside the loop, not waiting outside it</b> - you can interrupt and steer at any point.</p>
<div class="takeaway"><b>The third phase is the one people skip</b>, and every tool we build later exists to protect it. Note also: almost none of this is really about Claude Code. The same moves work in any CLI coding agent.</div></div>""")

add("M0", "Same model, same repo, same minute", """
<div class="c"><p class="kick">Same model, same repo, same minute</p>
<div class="bg">
<div class="col bad"><p class="tag">Vague</p><pre>add validation to the signup endpoint</pre></div>
<div class="col good"><p class="tag">Concrete</p><pre>The signup endpoint at src/api/signup.ts accepts
any email string.

Add input validation: reject missing email,
malformed email, and password under 12 chars.

Return the existing ApiError shape, do not
invent a new error format.

Do not touch the login endpoint or the
shared middleware.

Verify with: npm test -- signup</pre></div></div>
<div class="takeaway">Four differences: <b>named the file - said what &ldquo;done&rdquo; means - said what not to touch - gave it a command that proves it.</b> The left one usually invents an error shape or wanders into a neighbouring file. And precision is not length: a four-paragraph prompt that never says what done means is worse than two sentences that do.</div></div>""")

add("M0", "The good prompt, taken apart", """
<div class="c"><p class="kick">The good prompt, taken apart. Five things, and you can put all five in any request.</p>
<div class="anno">
<div class="what"><b>Where to look</b><i>A path, not a description</i></div>
<div class="brace"></div>
<div class="frag">The signup endpoint at <b class="acc">src/api/signup.ts</b>
accepts any email string.</div>

<div class="what"><b>What done means</b><i>Enumerated, so it can check itself</i></div>
<div class="brace"></div>
<div class="frag">Add input validation: reject missing email,
malformed email, and password under 12 chars.</div>

<div class="what"><b>What to reuse</b><i>Point at the shape that already exists, so it does not invent a new one</i></div>
<div class="brace"></div>
<div class="frag">Return the existing ApiError shape, do not
invent a new error format.</div>

<div class="what"><b>What not to do</b><i>Prevents most over-reach</i></div>
<div class="brace"></div>
<div class="frag">Do not touch the login endpoint or the
shared middleware.</div>

<div class="what"><b>How we will know</b><i>Decided before the work, not after</i></div>
<div class="brace"></div>
<div class="frag">Verify with: npm test -- signup</div>
</div>
<div class="takeaway"><b>Where to look - what done means - what to reuse - what not to do - how we will know.</b> Write those five and you have written a good prompt. Miss the last one and you have written a wish.</div></div>""")

add("M0", "Two properties you cannot prompt away", """
<div class="c"><p class="kick">Two properties you cannot prompt away</p>
<div class="dense">
<div class="drow"><div class="dk">Not<br>deterministic</div><div class="dv"><b>Same prompt, same repo, genuinely different runs. There is no seed to find.</b> You already know why. What matters is the consequence: you cannot rely on having got a good result once.</div></div>
<div class="drow"><div class="dk">It<br>forgets</div><div class="dv">Every session starts with a fresh context window. Yesterday's conversation is gone. So it has no private memory of your landmines - <b>it copies whatever is already in the codebase.</b> A human in a messy repo builds up scar tissue and routes around it. An agent starts cold every time.</div></div>
</div>
<div class="takeaway">You don't fix either one by prompting harder. You fix the <i>outcome</i> by making it checkable, and you fix the forgetting by <b>writing things down instead of saying them once</b>.</div></div>""")

add("M0", "The smart zone and the dumb zone", """
<div class="c"><p class="kick">The idea everybody repeats. Worth knowing exactly how firm it is.</p>
<div class="zones">
<div class="zbar"><span class="z1">SMART ZONE</span><span class="z2">DUMB ZONE</span></div>
<div class="zaxis"><span class="a0">empty session</span><span class="a1">full window</span></div>
</div>
<p class="sub" style="max-width:none;margin-top:2.6vh">As a session fills up, <b>quality drops before capacity runs out.</b> Finding a fact deep in the window is fine. Reasoning over everything that piled up is the part that goes - and it never stops sounding confident while it happens.</p>
<div class="two" style="margin-top:3vh">
<div class="card"><h4>Whose idea this is</h4><p><b>Matt Pocock (AI Hero)</b> named the smart zone / dumb zone; <b>Dex Horthy (HumanLayer)</b> argues the same thing as a context-utilization budget. It comes from people who use these tools all day, not from a benchmark. <b>Treat it as a working rule of thumb, because that is what its own authors call it.</b></p></div>
<div class="card"><h4 class="no">Nobody has published the number</h4><p>The people who do this all day land near <b>100K</b>. The defaults ship far higher:</p>
<p class="mono" style="font-size:1.05vw;line-height:1.75;margin-top:.6vh"><b>80-100K</b> Pocock's smart zone, restated after 1M shipped<br><b>~100K</b> Horthy: do the work in the first 100K<br><b>100K</b> Anthropic starts clearing tool results<br><b>~967K</b> Claude Code's auto-compact default</p>
<p style="margin-top:.8vh">Your tool will let you run to <b>967K</b>. Nobody who writes about this works anywhere near it.</p></div></div>
</div>""")

add("M0", "/context - the one claim you can just look at", """
<div class="c"><p class="kick"><code>/context</code> - the one claim here you can just look at</p>
<div class="two"><div>
<pre class="term" style="font-size:.92vw;line-height:1.45">&gt; /context
  &#9500;  Context Usage
     &#9921; &#9921; &#9921; &#9920; &#9920; &#9921; &#9921; &#9921; &#9921; &#9921;   Sonnet 5
     &#9921; &#9921; &#9921; &#9921; &#9921; &#9921; &#9921; &#9921; &#9921; &#9974;   claude-sonnet-5
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   <span class="no">172.3k/967k tokens (18%)</span>
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   <span class="cmt">Estimated usage by category</span>
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   &#9921; System prompt: 9.4k (1.0%)
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   &#9921; System tools: 24.3k (2.5%)
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   &#9921; Memory files: 5.1k (0.5%)
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974;   &#9921; Skills: 7.7k (0.8%)
     &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9974; &#9949; &#9949; &#9949;   <span class="no">&#9921; Messages: 125.8k (13.0%)</span>
                           &#9974; Free space: 761.7k (78.8%)
                           &#9949; Autocompact buffer: 33k (3.4%)

     MCP tools - /mcp (loaded on-demand)
     &#9492; <span class="ok">154 tools - 0 tokens</span>
     Memory files - /memory
     &#9492; 2 files - 5.1k tokens
     Skills - /skills
     &#9492; 57 skills - 7.7k tokens</pre>
</div><div>
<p class="tag acc">Read it in this order</p>
<ul class="big-list" style="margin-top:1vh">
<li><b>The startup block.</b><i>System prompt, tools, memory files, skill descriptions - 46.5k here, and it existed before anyone typed a word.</i></li>
<li><b>Then the conversation.</b><i>125.8k of messages. <span class="no">This is the number I would act on</span> - not because 172k of a million is too much, but because <b>accumulated turns are the worst-aged context you own.</b></i></li>
<li><b>Ignore &ldquo;free space&rdquo;.</b><i>78.8% free tells you when you will hard-stop. It tells you nothing about quality, because the reliable range is a token count and it does not grow with the window.</i></li>
</ul>
<p class="sub2" style="text-align:left"><b>154 MCP tools, 0 tokens.</b> Tool definitions are deferred until something needs them - so a big MCP setup is no longer a big standing bill. Skill descriptions are, though: 57 skills, 7.7k, permanently.</p>
</div></div>
<div class="takeaway"><b>The percentage is not the question - the kind of context is.</b> 172k of one pasted document is fine. 125k of accumulated turns and tool results is the part worth clearing, because its own output became its input. <b>The meter cannot tell those two apart. You can.</b></div></div>""")

add("M0", "/clear or /compact - the reset", """
<div class="c"><p class="kick">You have a meter and a red line. This is what you do about it.</p>
<div class="two"><div>
<table class="t"><thead><tr><th>Command</th><th>What it does</th><th>When</th></tr></thead><tbody>
<tr><td>/clear</td><td>new conversation, empty context</td><td>switching to unrelated work</td></tr>
<tr><td>/compact</td><td>replaces history with a summary</td><td>mid-task, need room, not a reset</td></tr>
<tr><td>/compact &lt;focus&gt;</td><td>same, steered</td><td>say what you're about to do next</td></tr>
</tbody></table>
<p class="sub2" style="text-align:left">That third row: you can type a sentence <i>after</i> <code>/compact</code> telling it what the summary should hold on to. Say <b>what you are about to do next</b>, not what you want kept - <code>/compact I'm moving from building to QA</code> beats guessing which parts of the last hour mattered, because you always know your next task and you rarely know that.</p>
</div><div>
<div class="card"><h4>If in doubt, clear</h4><p>Every compaction is a model summarising your conversation, and <b>each pass leaves sediment</b> - summaries layered on summaries, including work you finished an hour ago. Compact a few times in a row and it is reasoning from compressed leftovers. Compact only when you would genuinely lose something expensive, like a long debugging session where you have ruled things out.</p></div>
<div class="card" style="margin-top:1.8vh"><h4>Clearing is not losing</h4><p><code>/resume</code> brings the conversation back, scoped to the repo you are standing in - which is where people trip. And a second, less obvious reason to clear: <b>you cannot tell what your own setup did if the agent already knew it from twenty messages ago.</b> Test your own files in a fresh session.</p></div>
</div></div>
<div class="takeaway"><b>Files on disk survive a reset. Things you only said in chat do not.</b> Which is the entire argument for writing your setup down instead of explaining it again every morning.</div></div>""")

add("M0", "Esc and Esc Esc - the rewind menu", """
<div class="c"><p class="kick"><b>Esc Esc</b> on an empty input - the rewind menu</p>
<div class="two"><div>
<pre class="term">&gt; Restore code only
  Restore conversation only
  Restore code and conversation
<span class="cmt">  Summarize from here</span>
<span class="cmt">  Summarize up to here</span>
<span class="cmt">  Never mind</span></pre>
<p class="sub2" style="text-align:left"><b class="acc">Esc</b> interrupts mid-turn so you can redirect - work done so far is kept. If a dialog is open it closes the dialog instead.<br><br><b class="acc">Esc Esc</b> on an <i>empty</i> input opens this menu. With text in the input it clears your draft instead, and saves it, so Up gets it back.<br><br>The first entry is the one nobody expects: <b>bin the bad edits, keep everything it figured out.</b></p>
</div><div class="warnbox">
<p class="tag">What rewind does not cover</p>
<ul class="big-list" style="margin-top:1vh">
<li><b>Bash changes aren't tracked.</b><i>If it ran <code>rm</code> or <code>mv</code>, rewind will not bring it back.</i></li>
<li><b>Most subagent edits aren't restored.</b></li>
<li><b>Symlinked and hard-linked files aren't either.</b><i>A restore skips them and prints &ldquo;Restored the code, but skipped N files&rdquo;. If you use pnpm or a dotfile manager, that's you.</i></li>
<li><b>It is not version control.</b><i>Session-level undo. Commit before you let it do anything big and you always have the real floor underneath.</i></li>
</ul></div></div>
</div>""")

# ---------- M1 ----------
add("M1", "! - stop copy-pasting your test output", """
<div class="c"><p class="kick">Prefix any command with <b>!</b> and Claude sees the result without you pasting it</p>
<div class="two"><div>
<pre class="term">&gt; <span class="acc">!</span> pytest -k test_expired_token

<span class="no">FAILED test_expired_token
  AssertionError: expected 401, got 500</span>

<span class="cmt">Claude reads that output and answers it
on its own - no second prompt from you.</span></pre>
<p class="sub2" style="text-align:left">The universal beginner habit is: run the test in a second terminal, read the failure, select it, copy it, alt-tab back, paste it. <b>Thirty seconds of clerical work per loop, so you stop closing the loop.</b></p>
</div><div>
<div class="card"><h4>Why one character is worth a slide</h4><p>The habit is <i>make the check happen, and put the result in front of the model.</i> This is that with the friction removed - no second terminal, no selecting, no alt-tab. If you take one keystroke away from this session, take this one.</p></div>
<div class="card" style="margin-top:1.8vh"><h4 class="no">Two warnings</h4><p><b>Output in context is context spent.</b> Anthropic's own docs: the window holds every message, every file read <i>and every command output</i>, and performance degrades as it fills. <code>!</code> on something that prints ten thousand lines of build log spends your window on build log. Narrow the command first.<br><br><b>It actually runs it.</b> This is not a preview. <code>!</code> on something that flashes a device flashes the device.</p></div>
</div></div>
<div class="extras">
<span class="lbl">Three more, and the first one is worth memorising</span>
<p><b>@</b> a path puts that file in context for certain instead of hoping it gets found - but you pay for the whole file, plus the CLAUDE.md from its directory and every parent above it. <b>@</b> a 3,000-line file and you have spent your window on it.</p>
<p><b>Ctrl+B</b> runs something alongside, when you do not want to block on it. Long-lived processes. (In tmux, press it twice.)</p>
<p><b>Ctrl+Z</b> then <code>fg</code> keeps a command private - Claude sees neither the command nor the output. Unix only.</p>
</div></div>""")

add("M1", "Name the check first - and one that should fail", """
<div class="c"><p class="kick">Name the check first, and name one thing that should still fail</p>
<pre class="art" style="font-size:1.35vw">Verify with: &lt;command&gt;.
It must also still &lt;the thing that should NOT happen&gt;.</pre>
<p class="sub2" style="max-width:none;margin-top:2vh">It gives the agent a target it can check itself against instead of its own opinion of &ldquo;done&rdquo; - and it forces <b>you</b> to state the requirement precisely. Half the time you discover, while writing the verify sentence, that you had not actually decided what you wanted.</p>
<div style="margin-top:4.5vh;display:flex;justify-content:center">
<div class="card good" style="border-left:4px solid var(--good);display:inline-block"><pre style="font-size:1.25vw">Verify with: just raf-test

It must also still write the same JSON
keys recipe_adjustments_frontend already
sends to Datadog, and one log event must
still land as exactly one record.</pre></div></div>
<div class="takeaway">Most agent output passes the happy path and quietly breaks the negative case. <b>&ldquo;It works&rdquo; usually means &ldquo;the case I thought of works&rdquo;.</b></div></div>""")

add("M1", "Your tests are even more important now", """
<div class="c"><p class="kick">Your tests are even more important now</p>
<div class="two"><div>
<p class="sub" style="margin-top:0;text-align:left;max-width:none;color:var(--fg);font-size:1.5vw">A repo with fast, real tests is a repo where an agent can work and check itself. A repo without them is one where <b>you</b> review every line, forever.</p>
<p class="sub2" style="text-align:left">That is the whole reason the test suite stops being hygiene you keep postponing and becomes the thing that decides whether any of this is useful here.</p>
<p class="sub2" style="text-align:left"><b>The agent will also be the one writing new tests</b> - and left alone it writes them in five different styles, mocks things it should not, and produces a suite nobody trusts. Which means it cannot trust it either, and you are back to reviewing every line.</p>
<p class="sub2" style="text-align:left">So write down <b>how</b> tests get written here. Once.</p>
</div><div>
<p class="tag acc">.claude/rules/testing.md</p>
<pre class="art" style="font-size:1.02vw">---
paths:
  - "**/*.test.ts"
  - "tests/**"
---
- One behaviour per test. No test
  asserts two unrelated things.
- Mock the network boundary only.
  Never mock something we own.
- Test names read as sentences:
  "rejects an expired token".
- No snapshot tests for logic.
- A new test must fail before the
  change that makes it pass.
- If a test needs a comment to
  explain it, rewrite the test.</pre>
<p class="sub2" style="text-align:left">The <code>paths:</code> - they make sure this loads <b>only when Claude touches a test file</b>, so it costs you nothing on every other request.</p>
</div></div>
<div class="takeaway"><b>Your tests are the ceiling on how much you can trust your agent working in your repo</b> - and <b>your rules for writing tests are the ceiling on how long that stays true.</b></div></div>""")

add("M1", "The guardrails - you already own all six", """
<div class="c"><p class="kick">The guardrails - you already own all six</p>
<p class="sub2" style="max-width:none;margin-top:0;margin-bottom:1.6vh">These are how the work gets checked: they tell you and the agent whether it worked, they catch what it broke on the way, and <b>they are the only way it can correct itself without asking you.</b> The split that matters is which ones it can run on its own.</p>
<table class="t hl"><thead><tr><th>Loop</th><th>Agent can run it alone?</th></tr></thead><tbody>
<tr><td>Typecheck / compile</td><td>yes, unattended</td></tr>
<tr><td>Tests</td><td>yes, unattended - <i>if</i> you can run one by name</td></tr>
<tr><td>Lint / static analysis</td><td>yes, unattended</td></tr>
<tr><td>Code review</td><td>no - a person, or a pipeline you build later</td></tr>
<tr><td>Manual QA</td><td>no - a person at a screen or a rig</td></tr>
<tr><td>CI</td><td>no - runs after the fact, not in the loop</td></tr>
</tbody></table>
<div class="two" style="margin-top:2.2vh">
<div class="card"><h4>Give each one a name it can type</h4><p>Do not leave these as flags people have to remember. Put every loop behind <b>one short prepared command</b> - a <code>justfile</code> target, an npm script, a make rule, a shell script in the repo - and commit it.</p>
<pre style="font-size:1vw;margin-top:1vh">just check      # typecheck
just test auth  # one test by name
just lint</pre></div>
<div class="card"><h4>Why that is the whole trick</h4><p><b>You and the agent then run the identical command</b>, so &ldquo;it passes on my machine&rdquo; stops being a conversation. It is one line in your CLAUDE.md instead of six. And when the command changes you fix it in one place rather than in everybody's habits.</p></div></div></div>""")

add("M1", "Two clauses almost nobody writes", """
<div class="c"><p class="kick mono accent">Paste at the end of any non-trivial request</p>
<pre class="art">If you are not sure about something do not
assume - interview me relentlessly.

Write the result to docs/notes/&lt;thing&gt;.md</pre>
<div class="two" style="margin-top:2.4vh">
<div class="card"><h4>Make it interview you</h4><p>Left alone it answers from assumptions rather than asking. Forcing it to interrogate you first is what stops it doing the wrong thing extremely well.</p></div>
<div class="card"><h4>Write it to an <i>exact</i> path</h4><p>An answer in a chat window dies with the session. A named file is a thing your team can read, review and commit. Note <b>exact</b> - &ldquo;write it to a file&rdquo; gets you a file somewhere you will not find.</p></div></div>
<div class="extras" style="grid-template-columns:1fr 1fr 1fr">
<span class="lbl">Things genuinely worth having it write down</span>
<p><b>A research note.</b> Three approaches to a problem you have not solved, the trade-offs, and which one you picked. Pay the research cost once instead of every session.</p>
<p><b>An ADR.</b> What was decided, what else was considered, why. The one thing an agent can never work out from the code.</p>
<p><b>A glossary.</b> Your team's private words, one line each. This is also the honest answer to &ldquo;what do I put in a CLAUDE.md?&rdquo;</p>
<p><b>An analysis.</b> A call-graph walk, a memory-layout note, &ldquo;here is where this state machine can deadlock&rdquo;. Useless in a scrollback buffer, valuable in a repo.</p>
<p><b>The plan itself.</b> Phases, in a file you can review in a minute instead of a diff you would review in a day.</p>
<p><b>A spec, with an Out of Scope section.</b> The part of a spec that actually stops an agent is the list of what it must not build.</p>
</div></div>""")

# ---------- PART B ----------
add("Part B", "Your setup is a product you build", """
<div class="c ctr"><p class="kick accent">Part two</p><h1 class="big">Your setup is a product you build</h1>
<p class="sub mono">Start from an empty .claude/</p></div>""")

add("M2", "Why bother writing markdown for a robot", """
<div class="c"><p class="kick">Why bother writing markdown for a robot</p>
<p class="sub" style="max-width:none;margin-top:0;font-size:1.7vw;color:var(--fg)">Agents perform better in well-organised codebases for exactly the same reasons new hires do. <b>The agent is a new hire who starts fresh every twenty minutes.</b> So &ldquo;how well does Claude do in my repo?&rdquo; is really &ldquo;how fast could a competent stranger orient in my repo?&rdquo; Are related things grouped. Is anything named for what it does. Is there any written statement of how the thing gets built.</p>
<div class="five" style="margin-top:4vh">
<div class="fbox">CLAUDE.md<i>always loaded</i></div>
<div class="fbox">.claude/rules/<i>loaded by path</i></div>
<div class="fbox">.claude/skills/<i>loaded on demand</i></div>
<div class="fbox">hooks<i>run on an event</i></div>
<div class="fbox">settings.json<i>permission policy</i></div></div>
<div class="takeaway">None of this is Claude Code magic. It's <b>five kinds of file, and the whole skill is knowing which one a given piece of knowledge belongs in.</b> If your repo isn't well-organised and you can't fix that: this file is where you write down <i>how</i> it's a mess so the agent stops tripping on it.</div></div>""")

add("M2", "How to deal with CLAUDE.md after /init", """
<div class="c"><p class="kick">How to deal with CLAUDE.md after /init</p>
<div class="bg">
<div class="col bad"><p class="tag">What /init generated</p><pre># Project Structure
- `src/api/` - REST handlers
- `src/api/middleware/` - auth, logging
- `src/services/` - business logic
- `src/db/` - Drizzle schema + migrations
- `test/` - Vitest specs, mirrors src/

## Dependencies
express, drizzle-orm, zod, vitest,
pino, dotenv, bcrypt, jsonwebtoken...

## Overview
This project is a REST API for managing
customer orders. It exposes endpoints
for creating, reading and updating...

## Commands
- `npm test`  - run tests
- `npm run build` - build</pre></div>
<div class="col good"><p class="tag">What survives</p><pre>Order management API for the
warehouse team. Not customer-facing.

Package manager is pnpm, not npm.

Tests run through a preset:
`pnpm test:ci`, not `pnpm test`.

Errors return the existing ApiError
shape - never a bare Error.

Before writing code, list the modules
you will add or change and their public
interfaces, then wait for my confirmation.</pre></div></div>
<div class="takeaway"><b>Every line in this file is loaded on every request, forever.</b> That is the only sentence you need to decide what stays. The directory tour moves next quarter - the lockfile already lists the dependencies, accurately - the overview pays for the README twice, every request - it can infer <code>npm test</code>, but not that you run it through a preset. <b>Run <code>/init</code> as a first draft. Never ship a generated briefing file unread.</b></div></div>""")

add("M2", "Three rules that decide whether the file works", """
<div class="c"><p class="kick">Three rules - and the third is the highest-value line in the file</p>
<p class="sub" style="max-width:none;margin-top:0;margin-bottom:2.4vh">These apply to <b>anything you write for the agent to read</b> - the always-on <code>CLAUDE.md</code>, a scoped file in <code>.claude/rules/</code>, the body of a skill. Where a thing lives is the next slide; <b>how to write it so it survives contact with the repo is the same in all three.</b></p>
<div class="three">
<div class="card"><p class="tag acc">Rule 1</p><h4>Patterns, not paths and signatures</h4>
<pre>Rules describe patterns, not
APIs. The source is the
reference for signatures
and types.</pre>
<p>&ldquo;Auth lives in <code>src/auth/handlers.ts</code>&rdquo; is true for about a month, then it's a confident wrong turn. <b>Humans skim a stale doc sceptically. Agents do not</b> - it re-reads yours every request. Describe what the code does and let it find the files. <b>Its map is current. Yours is not.</b></p></div>
<div class="card"><p class="tag acc">Rule 2</p><h4>One sentence, then a rejected example</h4>
<pre>Errors return the existing
ApiError shape.
BAD:  throw new Error("bad email")
GOOD: return apiError(400, "...")</pre>
<p>Not a paragraph in capital letters. <b>Shouting at a model doesn't work; showing it something you rejected does.</b> One line of intent, one pair, done.</p></div>
<div class="card"><p class="tag acc">Rule 3</p><h4>A required planning step</h4>
<pre>Before writing code, list the
modules you will add or change
and their public interfaces,
then wait for my confirmation.</pre>
<p>One sentence, and it changes the shape of what comes back: <b>you review a five-line sketch instead of a diff.</b> Generalises to anything you want always considered - security, migration safety - as an explicit step with a human checkpoint.</p></div></div>
<div class="takeaway">The honest caveat, and you need it: <b>three things steer a session - your prompt, this file, and the code already in the repo. The code is the strongest.</b> If the pattern you banned appears fifty times in the codebase, the ban often loses. Writing the rule down is necessary, not sufficient. Two real fixes, both better than a longer file: point at a good reference file to imitate, or back the rule with a hook.</div></div>""")

add("M2", "Intentional - the rule type nobody writes", """
<div class="c ctr"><p class="kick">Everything so far is what <i>should</i> happen. This is the other half.</p>
<p class="sub" style="max-width:none;margin-top:1vh;font-size:1.9vw;color:var(--fg)">An agent tidies up whatever looks like a mistake, because <b>it cannot tell a deliberate oddity from an accident.</b> Nobody writes these down, and they are one line each.</p>
<pre class="art" style="font-size:1.5vw;line-height:1.65;margin-top:4vh;display:inline-block;text-align:left"># Intentional - do not &ldquo;fix&rdquo;

attrs, not Pydantic, for observable models.
  __attrs_post_init__ is what the validation needs.

time.sleep(2) in DriverBase.__init__.
  Known workaround for a ZMQ binding race. Tracked.

Global mutable callback registry in reactivity.py.
  Deliberate, MobX-style.</pre>
<div class="takeaway">Every one of those is code an agent would confidently clean up. <b>Writing them down is the difference between a session that ships and one that quietly reintroduces a race condition.</b></div></div>""")

add("M2", "Move it out of CLAUDE.md and link to it", """
<div class="c"><p class="kick">Move it out of CLAUDE.md and link to it</p>
<div class="bg">
<div class="col bad"><p class="tag">One file, everything in it</p><pre># CLAUDE.md          <span class="cmt">140 lines</span>

Order management API for the
warehouse team.

## Testing conventions
&lt;22 lines: mocking policy,
 fixtures, naming&gt;

## Deploying
&lt;30 lines: steps, rollback,
 the staging URL&gt;

## Database conventions
&lt;40 lines: migrations,
 naming, the two gotchas&gt;</pre>
<p style="font-size:1vw;color:var(--bad);margin-top:1.5vh;line-height:1.5">A front-end session pays for the migration rules. Every request, forever - and they are competing for attention with the prompt you just typed.</p></div>
<div class="col good"><p class="tag">The same knowledge, moved out</p><pre># CLAUDE.md          <span class="cmt">9 lines</span>

Order management API for the
warehouse team.
Package manager is pnpm.
Tests run through a preset:
pnpm test:ci

<span class="acc">@docs/testing.md</span> - how we write
  tests here: mocking policy,
  fixtures, and the two things
  that must never be mocked.

<span class="cmt"># and the rest are just files:</span>
<span class="acc">.claude/rules/db.md</span>    paths: db/**
<span class="acc">.claude/skills/deploy/</span>  on demand</pre>
<p style="font-size:1vw;color:var(--good);margin-top:1.5vh;line-height:1.5">Nothing is lost. The db rules load when Claude touches <code>db/</code>. The deploy steps load the day somebody deploys.</p></div></div>
<div class="takeaway"><b>The path is not the part that matters. The sentence after it is.</b> That sentence is all the agent sees before deciding whether to open the file - the same job a skill description does, and it fails the same way when it is vague. <b>Write the link like you are selling the file to someone with no time.</b></div></div>""")

add("M2", "Progressive disclosure - which file a thing belongs in", """
<div class="c"><p class="kick">Progressive disclosure - deciding which file a thing belongs in</p>
<table class="t"><thead><tr><th>If it is&hellip;</th><th>It lives in&hellip;</th><th>What that costs you</th></tr></thead><tbody>
<tr><td>relevant to <b>every</b> task in the repo</td><td>root <code>CLAUDE.md</code></td><td>every token, every request, forever</td></tr>
<tr><td>relevant to <b>one domain</b></td><td><code>.claude/rules/*.md</code> with <code>paths:</code> frontmatter, or a plain linked markdown file</td><td>nothing until Claude touches a matching file</td></tr>
<tr><td><b>rare</b>, but the agent genuinely doesn't know it</td><td>a skill</td><td>one line of description, until the day you need it</td></tr>
</tbody></table>
<div class="takeaway">It isn't free and it isn't infinite: <b>a link the agent has no reason to follow is a link it doesn't follow</b>, so moving something out of CLAUDE.md can quietly turn a rule you rely on into a rule that never fires. The description on the link is doing real work. A <code>paths:</code>-scoped rule is the one case where the risk disappears - the trigger is the file being read, not the agent choosing.</div></div>""")

add("M2", "Skills - a folder, not a loose file", """
<div class="c"><p class="kick mono accent">.claude/skills/&lt;name&gt;/SKILL.md</p>
<div class="two"><div>
<pre class="art">---
name: fix-corepack
description: Fix "pnpm: command not found"
  by enabling corepack. Use when pnpm
  cannot be found or corepack errors appear.
---

Run `corepack enable`, then
`corepack prepare pnpm@&lt;version&gt; --activate`
using the version in package.json's
packageManager field.

If that fails, the Node install is
missing corepack - see ./fallback.md</pre>
<p class="sub2" style="text-align:left">A folder, not a loose file, so it can carry a script or a longer reference next to it. <code>/skills</code> lists what you have; project skills are committed, which is how you hand your setup to a teammate.</p>
</div><div>
<p class="sub" style="margin-top:0;max-width:none;text-align:left;color:var(--fg);font-size:1.5vw"><b>Only the name and the description sit in context.</b> The body is not loaded until the skill is actually invoked.</p>
<p class="sub2" style="text-align:left"><b>The description is the entire routing surface.</b> It's the only thing the model sees before deciding whether to invoke. Write it as capability plus trigger, and <b>put the literal error text in it.</b> A skill with a vague description doesn't fail loudly - it silently never fires, and you conclude skills don't work.</p>
</div></div></div>""")

add("M2", "/commit-msg - the whole magic command", """
<div class="c"><p class="kick mono accent">.claude/skills/commit-msg/SKILL.md</p>
<div class="two"><div>
<pre class="art">---
name: commit-msg
description: Write a commit message for the
  staged diff in our house conventions. Use
  when asked to commit or to write a commit
  message.
---

Read the staged diff with `git diff --cached`.

Write one commit message:
- imperative mood, under 72 chars on the
  subject line
- body explains why, not what - the diff
  already says what
- reference the ticket id if the branch
  name contains one

Never:
- write "various fixes", "updates", "misc"
- claim a test passed unless you ran it
  in this session
- stage or commit anything yourself -
  output the message only

Output the message and nothing else.</pre>
</div><div>
<div class="card"><h4>The <span class="mono">Never</span> block is the interesting half</h4><p>&ldquo;What should this <i>refuse</i> to do?&rdquo; is the question nobody thinks to ask, and it's where your house style actually lives. The description above is capability plus trigger, exactly as the last slide said.</p></div>
<div class="card" style="margin-top:2vh"><h4>Any prompt you write more than twice should be a file</h4><p>That's the whole rule. <code>.claude/commands/deploy.md</code> and <code>.claude/skills/deploy/SKILL.md</code> both give you <code>/deploy</code> in the same install. Skills are the form to write now - the folder can carry files - and the skill wins a name collision.</p></div>
</div></div>
</div>""")

add("M2", "Prompts are suggestions. Hooks are guarantees.", """
<div class="c"><p class="kick">A shell command the harness runs on an event</p>
<blockquote style="font-size:2.6vw">Prompts are suggestions.<br><em>Hooks are guarantees.</em></blockquote>
<div class="two" style="margin-top:3.5vh">
<div class="card"><h4>SessionStart</h4><p>Force-load a rulebook, so the thing you care about is in context before anyone types a word. <b>This one does spend context, by design</b> - SessionStart output goes to Claude.</p></div>
<div class="card"><h4>PostToolUse</h4><p>Run your formatter after every edit. This is the one that converts &ldquo;please match our style&rdquo; from a paragraph in CLAUDE.md into something that simply <i>is</i> true. <code>clang-format -i</code> - <code>ruff check --fix</code> - <code>spotlessApply</code> - Prettier - same trade, different body.</p></div></div>
<div class="takeaway" style="margin-top:3vh"><b>Same rule, two places.</b> Put <i>always run Prettier after editing</i> in CLAUDE.md and it is a sentence the model re-reads every session and follows most of the time - it costs you those tokens in every session forever, and it gets less reliable the longer the session runs. Put it on <code>PostToolUse</code> and the harness runs <code>prettier --write</code> itself: <b>edit 300 behaves exactly like edit 1, it costs zero context until it fires, and it also catches the teammate who never read your CLAUDE.md.</b></div>
</div>""")

add("M2", "The events - and where a hook can say no", """
<div class="c"><p class="kick">About thirty events exist. These are the ones people actually use.</p>
<div class="two" style="grid-template-columns:1.1fr 1fr">
<div>
<table class="t"><thead><tr><th>Event</th><th>Fires</th><th>What you'd use it for</th></tr></thead><tbody>
<tr><td>SessionStart</td><td>session begins or resumes</td><td>force-load a rulebook before anyone types</td></tr>
<tr><td>UserPromptSubmit</td><td>you send a prompt, before Claude sees it</td><td>inject a standing reminder</td></tr>
<tr><td class="ok">PreToolUse</td><td>before a tool call runs</td><td><b>block it outright</b></td></tr>
<tr><td class="ok">PostToolUse</td><td>after a tool call succeeds</td><td><b>run your formatter</b></td></tr>
<tr><td class="ok">Stop</td><td>Claude finishes responding</td><td><b>refuse to finish until the check passes</b></td></tr>
<tr><td>PreCompact</td><td>before context is compacted</td><td>write state to a file first</td></tr>
</tbody></table>
<p class="sub2" style="text-align:left">You do not need to memorise the rest, and you do not need to write the JSON by hand either: <b>ask Claude Code to list the events it supports, or to write the hook for you.</b> It knows its own harness.</p>
</div><div>
<p class="tag acc">.claude/settings.json</p>
<pre class="art" style="font-size:.92vw">{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/format.sh"
      }]
    }]
  }
}</pre>
<p class="sub2" style="text-align:left"><b>A matcher and a command.</b> That is the whole thing. The script gets the tool call on stdin as JSON, so it can read which file was just written. (Prefix the path with <code>${CLAUDE_PROJECT_DIR}/</code> if it has to work from any directory.)</p>
<p class="sub2" style="text-align:left"><b>Exit 0 lets it through. Exit 2 blocks</b>, and whatever the script printed to stderr goes to Claude as the reason. That is the entire contract.</p>
</div></div>
<div class="takeaway"><b>The one thing worth getting right is where a hook can say no.</b> <span class="ok">PreToolUse</span> blocks the call before it happens and <span class="ok">Stop</span> blocks the turn from ending. <b><span class="no">PostToolUse</span> cannot block anything</b> - the tool already ran, so it can fix and it can complain, but it can never prevent. If the rule must hold, it goes on the event that fires <i>first</i>.</div></div>""")

add("M2", "Setting permissions for your agents", """
<div class="c"><p class="kick">Setting permissions for your agents</p>
<div class="two"><div>
<pre class="art" style="margin-top:0">{
  "permissions": {
    "allow": [
      "&lt;your test command&gt;",
      "&lt;your build command&gt;",
      "&lt;your linter&gt;",
      "&lt;read-only git&gt;"
    ],
    "ask":   [ "&lt;warn me, don't block me&gt;" ],
    "deny":  [ "&lt;push&gt;",
               "&lt;force-push&gt;",
               "&lt;anything destructive&gt;" ]
  }
}</pre>
</div><div>
<ul class="big-list" style="margin-top:0">
<li><b>Allow broadly.</b><i>Wildcard the safe families so you're not clicking approve all day. Build, test, lint, read-only git.</i></li>
<li><b>Deny narrowly.</b><i>Blocks outright - no dialog, no override. This is the answer to &ldquo;but what if it does something stupid&rdquo;: write down the handful of things it's never allowed to do, once, and stop worrying.</i></li>
<li><b>Yours vs the team's.</b><i>Keep it to yourself and it is your own safety net. <b>Share it with your team and everyone on the repo gets the same permissions with zero setup</b> - nobody has to remember which commands are safe, and nobody has their own private version of the answer. That is the difference between a personal setup and a team toolkit.</i></li>
</ul></div></div>
<div class="takeaway"><b>Isolation is a boundary. Instructions are a suggestion.</b> A rule in CLAUDE.md is a preference the model can drift away from. A deny rule, a hook, or a checkout it cannot write to is not.</div></div>""")

# ---------- PART C ----------
add("Part C", "Real workflows", """
<div class="c ctr"><p class="kick accent">Part three</p><h1 class="big">Real workflows</h1>
<p class="sub mono">All of it, applied to work you actually do</p></div>""")

add("M4", "Two plans - layered vs vertical slices", """
<div class="c"><p class="kick">Two plans for the same feature: layered vs vertical slices</p>
<p class="sub2" style="max-width:none;margin:-0.8vh 0 1.5vh;font-size:1.22vw;color:var(--fg)"><b>A vertical slice is one phase that cuts through every layer at once</b> - schema, endpoint, UI, test - so it runs end to end on its own. A layered plan builds one floor at a time, which is why <b>nothing works until the last phase, and every integration problem waits until then to show up.</b></p>
<div class="bg">
<div class="col bad"><p class="tag">Layered</p><pre>Phase 1: Data layer
  - orders.schema.ts, migration 0007
  - OrderRepo.findById(id: string)
  - OrderRepo.create(dto: CreateOrderDto)

Phase 2: Service layer
  - OrderService with 6 methods

Phase 3: API layer
  - POST /orders  &rarr; createOrder()
  - GET  /orders/:id &rarr; getOrder()
  - error middleware in
    src/api/middleware/errors.ts

Phase 4: UI
Phase 5: Tests</pre>
<p style="font-size:1vw;color:var(--bad);margin-top:1.5vh;line-height:1.5"><b>Nothing runs end to end until phase 4.</b> Exact paths and signatures for phase 3, which phase 1 will change. No link back to any user story - nothing says what it's <i>for</i>.</p></div>
<div class="col good"><p class="tag">Vertical slices</p><pre>Durable decisions
  - orders own their own line items
  - money is integer minor units
  - one write endpoint, idempotency key

Phase 1 (tracer bullet)
  One hardcoded order renders on the
  order page, through a real DB read,
  a real endpoint and a real test.
  Serves story: "see my order".

Phase 2
  Real order from the DB. Same route.

Phase 3
  Create an order. Same shape.

Out of scope: refunds, multi-currency.</pre>
<p style="font-size:1vw;color:var(--good);margin-top:1.5vh;line-height:1.5"><b>Every phase runs, so every phase can be tested and demoed.</b> Prose, not pseudocode. Durable decisions in a header; nothing brittle in later phases.</p></div></div>
<div class="takeaway"><b>Reviewing these two plans took you a minute. Reviewing the two diffs they produce would take way longer.</b> And the tell you can use this afternoon: <b>a plan that comes back instantly, with no questions asked, is a bad plan.</b> Every ambiguity in it got resolved by guessing. If it didn't ask you anything, ask it what it assumed.</div></div>""")

add("M4", "How to go from an idea to shipped code", """
<div class="c"><p class="kick">How to go from an idea to shipped code</p>
<ol class="chain">
<li>capture the idea</li>
<li>capture decisions</li>
<li>write a spec</li>
<li>write a plan with thin vertical slices</li>
<li>tag each slice: watched, or safe unattended</li>
<li>implement slice by slice</li>
<li>review each</li>
</ol>
<div class="two" style="margin-top:2.6vh">
<div class="card"><h4>The spec, or PRD</h4><p>What to build and what <b>done</b> means, in prose. The behaviour, the decisions that outlive implementation - data model, interfaces, dependencies - and an explicit <b>Out of scope</b>. <b>The destination.</b></p></div>
<div class="card"><h4>The plan</h4><p>How to get there. The same feature cut into thin vertical slices, each small enough to finish in one session, each tagged watched or safe unattended, each pointing back at the spec. <b>The journey.</b></p></div></div>
<p class="sub2" style="max-width:none;text-align:left;margin-top:1.5vh;font-size:1.12vw"><b>Why an agent needs both:</b> spec without plan, it takes one enormous swing at the whole thing. Plan without spec, it builds the wrong thing efficiently. <b>Together they give it a fixed target and a session-sized next step, so no phase depends on it remembering the conversation.</b></p></div>""")

add("M4", "/grill-me - ten lines of English", """
<div class="c"><p class="kick mono accent">.claude/skills/grill-me/SKILL.md</p>
<div class="two"><div>
<pre class="art">Interview me about the feature below until we
have shared understanding. Do not write any code.

Rules:
- Ask ONE question at a time. Wait for my answer.
- Every question ships your recommended answer
  and a one-line reason. I react, I don't compose.
- If the codebase can answer it, go read the
  codebase instead of asking me.
- Make me tier my wish list 1/2/3, then cut to
  Tier 1. The cut list becomes Out of Scope.
- Stop when you stop discovering things, not
  after N questions.</pre>
</div><div>
<p class="tag acc">Why each rule is there</p>
<p class="sub2" style="text-align:left"><b>Recommended answers.</b> &ldquo;Should comments be soft- or hard-deleted? I'd suggest soft, because moderation needs an audit trail&rdquo; is answerable in three seconds.</p>
<p class="sub2" style="text-align:left"><b>Don't ask the human what the code can answer.</b> Your attention is only for the things only you can decide.</p>
<p class="sub2" style="text-align:left"><b>Enumerate first, cut second.</b> If you never write down the Tier 3 stuff it leaks back in during implementation. And the cut list isn't waste - <b>Out of Scope is the part of a spec that actually stops the agent.</b></p>
</div></div>
<div class="takeaway">What you want before code exists is not a document, it's <b>shared understanding</b> - a plan is an artefact people mistake for it (Fred Brooks, <i>The Design of Design</i>). Ten lines of English in a markdown file, and you can write your own on the train home. <b>What it can't do: interrogation removes ambiguity, not bad ideas.</b></div></div>""")

add("M4", "The two lines that pay for themselves", """
<div class="c"><p class="kick mono accent">Appended to the same interview command</p>
<pre class="art">- Whenever a domain term comes up that isn't in the glossary,
  propose a one-line definition.
- Whenever an architecture decision is settled, offer to write a
  short ADR: what was decided, what else was considered, why.
- Both get committed BEFORE the spec is written.</pre>
<p class="sub" style="max-width:none">Two things an agent can <b>never</b> work out from code, commits or the tracker: <b>why an unusual trade-off was chosen</b>, and <b>what your team's private words mean.</b> The interview is where both fall out. Catch them there or lose them. (ADR is Michael Nygard's format, 2011.)</p>
<div class="takeaway">In practice these get wrapped. <b><code>/grill-prd</code> runs the interview, then writes the spec from it</b> - one command covering the first three steps. And a command that calls two commands is still ten lines of English.</div>
<p class="tag acc" style="margin-top:2.4vh">That is the whole of it - five more lines on top of the file above</p>
<pre class="art">Run /grill-me on the feature below.
Do not start the spec until the interview stops discovering things.

Then write plans/&lt;feature&gt;/prd-&lt;feature&gt;.md, in this order:
problem - solution - user stories - decisions we settled -
what we will test - <b>Out of Scope</b>.</pre></div>""")

add("M4", "/prd-to-plan - a durable header, then thin slices", """
<div class="c"><p class="kick mono accent">.claude/skills/prd-to-plan/SKILL.md</p>
<div class="two"><div>
<pre class="art">Turn the spec below into a plan, as one markdown file.
Read the codebase before you write anything.

Rules:
- Open with the decisions that outlive the work - routes,
  schema, key models. Every slice points back at that header.
- Vertical slices only: each one cuts through ALL layers,
  never just one, and runs on its own. A hardcoded value is
  fine. Many thin beat a few thick.
- TDD in every slice: tests first, then code until they pass.
- No file names, no signatures - they go stale fastest.
- Docs: name the ones this makes stale, in the slice that
  breaks them.
- Show me the list to merge or split BEFORE you write the file.</pre>
</div><div>
<p class="tag acc">The four rules that do the work</p>
<p class="sub2" style="text-align:left"><b>Vertical slices.</b> Each one cuts through every layer and runs on its own, so it can be demoed and tested. A layered plan works nothing end to end until the last slice.</p>
<p class="sub2" style="text-align:left"><b>TDD in every slice.</b> Tests first, then code until they pass. This is also what buys you the review shift later - <b>no real tests, no reviewing the interface instead of the diff.</b></p>
<p class="sub2" style="text-align:left"><b>Name the docs it makes stale.</b> Attached to the slice that breaks them, so they ship with the code instead of never.</p>
<p class="sub2" style="text-align:left"><b>A checkpoint before it writes.</b> Reviewing a list costs seconds. Reviewing the finished plan costs you the session.</p>
</div></div>
<p class="sub2" style="max-width:none">Then, running it: feed each slice <b>three</b> things - the spec, the <i>whole</i> plan, and which slice to build. Seeing what the later ones are for is how the agent knows what <i>not</i> to build now. Skip this and they duplicate and contradict each other.</p>
<div class="takeaway"><b>This is the last step that deserves your full attention.</b> After this the agent implements the plan and you review the result - so <b>anything you didn't decide here, it decides for you.</b></div></div>""")

# ---------- M6 ----------
add("M6", "Review the interface and the tests, not the bodies", """
<div class="c"><p class="kick">Review the interface and the tests, not the function bodies</p>
<div class="two" style="align-items:start"><div>
<div class="own">
<div class="row mine"><div><h5>The interface</h5><i>the names, the shape, what it promises to callers</i></div><span class="who">you</span></div>
<div class="row theirs"><div><h5>The implementation</h5><i>function bodies</i></div><span class="who">the agent</span></div>
<div class="row mine"><div><h5>The tests</h5><i>what counts as proof it actually works</i></div><span class="who">you</span></div>
</div>
<p class="sub2" style="text-align:left;margin-top:2vh"><b>You become the interface designer. The agent becomes the implementation specialist.</b></p>
</div><div>
<p class="sub" style="margin-top:0;text-align:left;max-width:none;color:var(--fg);font-size:1.5vw"><b>The shift is what you review, not how fast.</b> You stop reviewing implementation and start reviewing architecture: the boundary, the contract, and the evidence it holds. Not opaque - you can open any function any time, and sometimes you will. But by default your attention goes to the edges of the module, not its interior.</p>
<table class="t" style="font-size:1.3vw;margin-top:2.5vh"><tbody>
<tr><td>Python</td><td>the module's public functions, their type hints, and the test file</td></tr>
<tr><td>React</td><td>the component's props and the store's actions, plus what the tests assert</td></tr>
</tbody></table>
<p class="sub2" style="text-align:left">Same move in any stack: <b>the surface other code depends on, plus the tests that pin it down.</b></p>
</div></div>
<div class="takeaway"><b>This only holds where the tests are real.</b> Weak feedback loop and it collapses - slow builds, hardware in the loop, mocks that pass while the feature is broken. Then you go back to reading the diff.</div></div>""")

add("M6", "/prepush - and the one load-bearing line", """
<div class="c"><p class="kick mono accent">.claude/commands/prepush.md - kept in the repo, so everyone runs the same review</p>
<div class="two"><div>
<pre class="art">---
description: Review the current diff before pushing
---

Run `pnpm test` and `pnpm lint`.  <span class="cmt"># your checks</span>
If anything fails, stop. Report the failures
and nothing else.
<mark>Do not review red code.</mark>

If the tests pass:
1. Run `git diff main...HEAD` and read the
   whole diff.
2. Judge it against exactly one acceptance
   criterion: $ARGUMENTS
3. List anything in the diff that does not
   serve that criterion.
4. Check it against docs/standards.md. Cite
   rules only from files you have read in
   this session - if you did not read one,
   say "no rules file read". Never cite a
   rule from memory.

Output: PASS, or the numbered list. Nothing else.</pre>
</div><div>
<p class="tag acc">Four properties. Only the first is non-negotiable.</p>
<ul class="big-list" style="margin-top:1vh">
<li><b>Refuses to review red code.</b><i>Reviewing a diff whose tests fail is theatre. It is what makes this a gate rather than a summariser, and it is the line people leave out.</i></li>
<li><b>Checks against a stated criterion.</b><i>Not &ldquo;good practice&rdquo;. <b>One criterion, not five</b> - a command asked to check five things checks none properly.</i></li>
<li><b>Cites rules only from files it read.</b><i>Rules &ldquo;from memory&rdquo; are the most confident wrong output you'll get all day.</i></li>
<li><b>Runs every check you own, not just tests.</b><i>Lint, typecheck, formatter, your coding standards. <b>Write the standards down and point the command at the file</b> - otherwise it guesses at them.</i></li>
</ul>
<div class="card" style="margin-top:1.4vh"><h4>Why not the built-in one?</h4><p>Claude Code ships <code>/code-review</code> (aliased <code>/review</code>) and <code>/security-review</code>. Build your own anyway: <b>the shipped one doesn't know your acceptance criterion and won't refuse to run on red.</b> Name it <code>/prepush</code> - a project command overrides a bundled skill of the same name, but not its aliases.</p></div>
</div></div></div>""")

add("M6", "Red then green - the refusal, then the finding", """
<div class="c"><p class="kick">Tests failing: it refuses to review. Tests passing: one finding against the criterion.</p>
<div class="bg">
<div class="col bad"><p class="tag">Tests red</p><pre>&gt; /prepush the discount must never apply
  to already-discounted items

<span class="no">✗ 2 tests failed</span>

  cart.test.ts &gt; stacks discounts
  cart.test.ts &gt; respects the flag

<span class="no">Not reviewing. Tests are failing.</span></pre></div>
<div class="col good"><p class="tag">Tests green, criterion violated</p><pre><span class="ok">✓ 47 tests passed</span>

1. src/pricing/cart.ts:88 - applies the
   discount before checking the
   already-discounted flag. Does not
   serve the criterion.

<span class="cmt">No rules file read.</span></pre></div></div>
<div class="takeaway"><b>This is not code review and it is not CI.</b> It's a sanity check before the agent tells you it's ready - so neither you nor your teammate spends a review catching the obvious things.</div></div>""")

add("M6", "/implement-plan - one agent per slice, review and fix until clean", """
<div class="c"><p class="kick mono accent">.claude/skills/implement-plan/SKILL.md</p>
<div class="takeaway" style="margin:0 0 2.4vh"><b>One more command, and this one runs the others.</b> You give it the plan and the name of your review command. It takes the slices one at a time, and for each slice it starts an agent that <b>writes the code, reviews its own work with your command, fixes what the review found, and reviews again</b> - looping until the review comes back clean or it runs out of tries.</div>
<div class="two"><div>
<pre class="art">You are the orchestrator. Never write code yourself.
Args: the plan, and the review command to run.

Rules:
- First read CLAUDE.md, .claude/rules/ and any contract
  files. Condense them into one context block.
- Run the slices in order, one at a time. Wait for each.
- Start a fresh agent per slice. Give it the context
  block, the slice, and what earlier slices built.
- Each agent: implement, run the review, fix what it
  found, run the review again. Three cycles maximum.
- Then say "slice N complete", or stop and list what
  is still open.
- Never carry on past a slice that did not complete.</pre>
</div><div>
<p class="tag acc">Why it is shaped like this</p>
<p class="sub2" style="text-align:left"><b>The orchestrator never writes code.</b> It starts one agent per slice and reads the result, so its own window stays small enough to still be reliable at slice six.</p>
<p class="sub2" style="text-align:left"><b>Every slice agent starts on a fresh window.</b> It inherits the codebase, not the transcript - the same trick as clearing between tasks, applied automatically.</p>
<p class="sub2" style="text-align:left"><b>Three cycles, not &ldquo;until clean&rdquo;.</b> Then it stops and tells you. An unbounded fix loop is how you get a green suite and the wrong feature.</p>
<p class="sub2" style="text-align:left"><b>Conventions do not travel.</b> A fresh agent knows nothing about your repo, so the rules get pasted into every single one.</p>
<p class="sub2" style="text-align:left"><b>It never carries on past a failure.</b> A slice that cannot pass its own review stops the run instead of landing.</p>
</div></div></div>""")

add("M6", "/implement-plan-workflow - the same loop, run as a workflow", """
<div class="c"><p class="kick mono accent">.claude/skills/implement-plan-workflow/SKILL.md</p>
<div class="takeaway" style="margin:0 0 2vh"><b>Same loop, one change: it stops being a conversation.</b> The skill writes the loop as a script and hands it to <b>Claude Code's workflow runner</b>, which runs it as a background job under <code>/workflows</code>.</div>
<pre class="art" style="margin-bottom:2vh">Same as /implement-plan, except:
- Do not run the loop here. Write it as a workflow script and launch it.
- Every slice returns a fixed shape: status, summary, newFiles,
  changedContracts. The next slice gets that object, not a summary.
- Sequential only. Never in parallel, never in separate worktrees.
- Stop at the first slice that comes back blocked, and report it.</pre>
<p class="sub2" style="max-width:none;margin:-0.6vh 0 1.8vh"><b>You don't have to write this one by hand.</b> Point Claude at your <code>/implement-plan</code> and ask it to turn it into a skill that uses Claude Code's workflow runner.</p>
<table class="t" style="font-size:1.16vw"><thead><tr><th style="width:19%">&nbsp;</th><th style="width:38%">Run by hand</th><th class="acc" style="width:43%">Run as a workflow</th></tr></thead><tbody>
<tr><td>the loop</td><td>the orchestrator decides what to do next, every turn</td><td><b>fixed in code before it starts</b> - order, cycles, stop condition</td></tr>
<tr><td>handoff</td><td>a prose summary the next agent has to interpret</td><td><b>a checked object</b> - status, files, changed contracts</td></tr>
<tr><td>a twelve-slice plan</td><td>the orchestrator's own window fills up as it goes</td><td><b>the script holds the state</b>, so nothing degrades</td></tr>
<tr><td>a blocked slice</td><td>fix it, then run the plan again</td><td><b>fix it and re-run</b> - earlier slices come back from cache</td></tr>
<tr><td>while it runs</td><td>you watch a wall of text go past</td><td><b>a background job</b> you can leave running</td></tr>
</tbody></table></div>""")

add("M6", "/pr-comments - the triage runs while you work on something else", """
<div class="c"><p class="kick mono accent">.claude/skills/pr-comments/SKILL.md</p>
<div class="takeaway" style="margin:0 0 1.6vh"><b>You start this one and go do something else.</b> It finds the unresolved threads, reads the code each one points at <b>as it exists now</b>, and returns a verdict per comment - because <b>checking whether a comment is still true is verification, not judgment.</b></div>
<div class="two"><div>
<pre class="art">Fetch the unresolved review comments on a PR, check
each one against the CURRENT code, output a triage list.

Rules:
- Report only. Never edit code, never post a reply,
  never resolve a thread. Produce the list and stop.
- Verify, do not trust. Read the lines as they are
  now, not the snippet the bot quoted.
- Check cited rules. Does this repo even run that
  linter, and do the docs record an exception?
- Trace consumers when scope is unclear - shared
  config, a port, an env var.
- Flag uncertainty. If intent is not in the code, ask.

Read the threads over GraphQL, keep isResolved == false.
isOutdated == true means the code already moved.
One entry per comment, most actionable first. Then stop.</pre>
</div><div>
<p class="tag acc">What you give it</p>
<pre class="art">/pr-comments            <span class="cmt">the branch's PR</span>
/pr-comments 482        <span class="cmt">a number, this repo</span>
/pr-comments &lt;url&gt;      <span class="cmt">any repo you can read</span></pre>
<p class="tag acc" style="margin-top:1.8vh">What comes back, one entry per comment</p>
<div class="three" style="grid-template-columns:1fr;gap:.6vh">
<div class="card" style="padding:1vh 1.2vw"><h4 style="font-size:1.3vw">Apply</h4><p style="font-size:1.15vw">Still true now. It describes the fix, it does not make it.</p></div>
<div class="card" style="padding:1vh 1.2vw"><h4 style="font-size:1.3vw">Dismiss</h4><p style="font-size:1.15vw">Already fixed, stale, or citing a rule this repo doesn't enforce.</p></div>
<div class="card" style="padding:1vh 1.2vw"><h4 style="font-size:1.3vw">Needs decision</h4><p style="font-size:1.15vw"><b>The important one.</b> It turns on intent that isn't in the code, so the output is a question.</p></div>
<div class="card" style="padding:1vh 1.2vw"><h4 style="font-size:1.3vw">Reply</h4><p style="font-size:1.15vw">No code change. It drafts the explanation.</p></div></div>
</div></div></div>""")

# ---------- M7 ----------
add("M7", "Help the agent find the bug - show it, then frame it", """
<div class="c"><p class="kick">Help the agent find the bug instead of making it guess where to look</p>
<pre class="art">I expected the retry to stop after three attempts.
It kept going - the log shows attempt 9.

&lt;paste the actual log lines here&gt;</pre>
<div class="two" style="margin-top:3vh">
<div class="card"><h4>Show, don't describe</h4><p>Paste the stack trace, the failing input, the screenshot, the log line. <b>Your summary of an error is lossy; the error is not.</b></p></div>
<div class="card"><h4>Then frame it</h4><p>A pasted trace with no sentence around it makes the agent guess what &ldquo;correct&rdquo; looked like, so it debugs the error message instead of the problem. Two clauses fix that: <b>what you expected, and what actually happened.</b></p></div></div>
<p class="sub2" style="max-width:none">Works identically for a hardware trace, a serial dump, a failing assertion, a red CI job.</p>
<div class="takeaway"><b>Past a few hundred lines, don't paste the log - point at it.</b> Write it to a file and say which part matters, and it greps to that region instead of swallowing the file. <b>A paste also dies with the session; the file survives a <code>/clear</code>.</b></div></div>""")

add("M7", "Write down what you learn, or pay for it twice", """
<div class="c ctr"><p class="big" style="font-size:3.5vw;max-width:66vw;margin:0 auto">Write down every non-obvious finding, so the next agent does not rediscover it the hard way</p>
<div class="fils" style="margin-top:7vh;gap:1.4vw">
<div class="fil">CLAUDE.md<i>conventions every session loads</i></div>
<div class="fil">.claude/rules/<i>scoped rules, loaded per path</i></div>
<div class="fil">ADRs<i>what we chose, and what we rejected</i></div>
<div class="fil">guides<i>how a subsystem actually works</i></div>
<div class="fil">ERRORS.md<i>approaches that failed, and why</i></div>
</div></div>""")

add("M7", "Refactoring - the tests go in first, and then they don't move", """
<div class="c"><p class="kick">A refactor is the one change where you already know what correct means: exactly what it did before</p>
<pre class="art" style="font-size:1.5vw;line-height:1.7">Before you refactor, write tests that pass against the
CURRENT behaviour. Then refactor. Those same tests must
still pass, untouched.

Never edit a test during a refactor. If a test has to
change, it is not a refactor - stop and tell me which
behaviour you are changing.</pre>
<p class="sub2" style="max-width:none;margin-top:2.4vh">Worth making permanent rather than retyping: a <code>/refactor</code> skill, or three lines in <code>CLAUDE.md</code> so it applies to every refactor without you asking for it.</p>
<div class="takeaway"><b>Without this, the refactor and the regression arrive in the same diff</b> - and the tests the agent quietly adjusted on the way through will tell you everything is fine.</div></div>""")

add("Wrap", "The new mental model... again", """
<div class="c ctr"><p class="kick">The new mental model... again</p>
<p class="big" style="font-size:3.8vw;margin:7vh 0 9vh">Let that sink in...</p>
<div class="loop">
<div class="spine">
<div class="step lit" style="font-size:1.6vw">Write and approve the work<span class="opt">human</span></div><div class="arrow">&rarr;</div>
<div class="step" style="font-size:1.6vw">Do the work<span class="opt">agent</span></div><div class="arrow">&rarr;</div>
<div class="step lit" style="font-size:1.6vw">Review and merge<span class="opt">human</span></div></div>
</div></div>""")

add("Wrap", "The principles, in one list", """
<div class="c"><p class="kick">If you keep seven things from today, keep these</p>
<ul class="big-list">
<li><b>A good prompt is the base.</b><i>Concrete, constrained, and it says how you will know it worked.</i></li>
<li><b>Stay out of the dumb zone.</b><i>One task per window. When in doubt, clear rather than compact.</i></li>
<li><b>Prompts are suggestions. Hooks are guarantees.</b><i>Anything that must never be skipped does not belong in prose.</i></li>
<li><b>Anything you have typed twice becomes a skill.</b><i>A file in the repo, so your team gets it too.</i></li>
<li><b>Your repo is the ceiling.</b><i>Tests, commands and written-down knowledge decide how good the agent can be.</i></li>
<li><b>Plan, implement, verify, repeat.</b><i>Thin vertical slices, and never carry on past one that did not pass.</i></li>
<li><b>You keep the judgement, the agent does the work.</b><i>You write and approve, it builds, you review and merge.</i></li>
</ul>
<div class="takeaway"><b>Keep improving. Nothing from today is a finished concept.</b> Adjust it to your needs, your project and your team - the version that works is the one you changed.</div></div>""")

add("", "Happy Claude-ing", """
<div class="c ctr"><h1 class="big">Happy Claude-ing!</h1>
<p class="sub" style="margin-top:5vh">More questions? Want to share an idea? Want to discuss anything?</p>
<p class="sub" style="margin-top:2vh">Drop a message on Rocket Chat: <b class="mono" style="color:var(--accent)"><img class="rc" src="__RC__" alt="">#Claude_szkolenie</b></p>
<img src="__WALK__" alt="" style="width:17vw;height:auto;margin-top:3vh;image-rendering:pixelated"></div>""")

# ---------- emit ----------
out = io.StringIO()
out.write('<!doctype html><html lang="en"><head><meta charset="utf-8">\n')
out.write('<meta name="viewport" content="width=device-width,initial-scale=1">\n')
out.write('<title>Claude Code Workshop - slides v2, online edition</title>\n<style>')
out.write(CSS)
out.write('</style></head><body>\n<div id="bar"></div><div id="deck">\n')
N = len(S)
# the header is for the audience, not the host - no module numbers on screen
HDR = {'M0':'Foundations','M1':'Foundations','M2':'Your setup','M3':'Your setup',
       'M4':'Real workflows','M6':'Real workflows','M7':'Real workflows','Wrap':'Wrapping up'}
for i,(mod,title,html) in enumerate(S):
    out.write('<section class="slide" data-i="%d">' % i)
    out.write('<div class="hdr"><span class="mod">%s</span><span></span></div>' % HDR.get(mod,''))
    out.write(html.strip())
    out.write('<div class="num">%d / %d</div></section>\n' % (i+1, N))
out.write('</div>\n')
out.write('<div id="black"><div><h1 class="bigbrk">&#9749; Back at <input id="brktime" class="brkin" type="text" maxlength="7" autocomplete="off" spellcheck="false"></h1><p class="subbrk">10 minutes</p></div></div>\n<div id="ov"><h2>All slides - click to jump</h2><div class="grid" id="ovg"></div></div>\n')
out.write('<div id="help">&larr; &rarr; move - O overview - B break screen - click it to type the time - F fullscreen</div>\n')
out.write('<script>\nvar L=' + json.dumps([t for _,t,_ in S], ensure_ascii=False) + ', cur=0, N=document.querySelectorAll(".slide").length;\n')
out.write("""var slides=document.querySelectorAll('.slide'), bar=document.getElementById('bar');
function fit(s){var c=s.querySelector('.c'); if(!c) return;
  c.style.transform='none';
  var avail=s.clientHeight - (parseFloat(getComputedStyle(s).paddingTop)+parseFloat(getComputedStyle(s).paddingBottom));
  var h=c.scrollHeight;
  if(h>avail){var k=Math.max(0.78, avail/h); c.style.transform='scale('+k.toFixed(3)+')';}}
function go(i){cur=Math.max(0,Math.min(N-1,i));slides.forEach(function(s,k){s.classList.toggle('on',k===cur)});
  fit(slides[cur]);
  bar.style.width=((cur+1)/N*100)+'%';history.replaceState(null,'','#'+(cur+1));}
window.addEventListener('resize',function(){fit(slides[cur]);});
var bt=document.getElementById('brktime');
try{bt.value=sessionStorage.getItem('ccw-brk')||'';}catch(err){}
bt.addEventListener('input',function(){try{sessionStorage.setItem('ccw-brk',bt.value);}catch(err){}});
function brk(on){var bl=document.getElementById('black');
  bl.classList.toggle('on',on);
  if(!on) bt.blur();}
// click anywhere on the break screen to type the time - keeps B a reliable toggle.
// never select(): a click on the field itself bubbles here, and re-selecting on every
// click makes the highlight impossible to get rid of. Caret to the end instead.
document.getElementById('black').addEventListener('click',function(e){
  if(e.target===bt) return;               // let the field place its own caret
  bt.focus();
  var n=bt.value.length; try{bt.setSelectionRange(n,n);}catch(err){}});
bt.addEventListener('keydown',function(e){
  // the field owns every key while it has focus, so the deck never navigates mid-typing
  if(e.key==='Enter'){bt.blur();e.preventDefault();}        // commit, screen stays up
  else if(e.key==='Escape'){brk(false);e.preventDefault();} // Escape is the way out
  e.stopPropagation();});
document.addEventListener('keydown',function(e){
  var k=e.key, ov=document.getElementById('ov'), bl=document.getElementById('black');
  if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'){go(cur+1);e.preventDefault();}
  else if(k==='ArrowLeft'||k==='PageUp'){go(cur-1);}
  else if(k==='Home'){go(0);} else if(k==='End'){go(N-1);}
  else if(k==='b'||k==='B'){brk(!bl.classList.contains('on'));}
  else if(k==='o'||k==='O'){ov.style.display=ov.style.display==='block'?'none':'block';}
  else if(k==='Escape'){ov.style.display='none';brk(false);}
  else if(k==='f'||k==='F'){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen();}
});
var g=document.getElementById('ovg');
L.forEach(function(t,i){var b=document.createElement('button');
  b.innerHTML='<b>'+(i+1)+'</b><span>'+t.replace(/</g,'&lt;')+'</span>';
  b.onclick=function(){go(i);document.getElementById('ov').style.display='none';};g.appendChild(b);});
go(location.hash?parseInt(location.hash.slice(1))-1||0:0);
</script></body></html>""")

open(os.path.join(os.path.dirname(_here), 'slides.html'), 'w', encoding='utf-8').write(out.getvalue())
print("slides:", N)
