import random
random.seed(7)
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ---------------- ID CARD ----------------
bars, x = [], 0
while x < 220:
    w = random.choice([1.5, 2, 3, 4]); g = random.choice([1.5, 2, 3])
    bars.append(f'<rect x="{x:.1f}" y="0" width="{w}" height="46"/>'); x += w + g
barcode = "".join(bars)
chips = ["JS", "TS", "React", "Node", "Mongo"]
cx, chip_svg = 0, ""
for c in chips:
    w = 14 + len(c) * 7.2
    chip_svg += f'<rect x="{cx:.1f}" y="0" width="{w:.1f}" height="22" rx="11" fill="none" stroke="#58a6ff" stroke-opacity=".7"/><text x="{cx+w/2:.1f}" y="15" font-size="10.5" font-weight="700" text-anchor="middle" fill="#cfe3ff">{c}</text>'
    cx += w + 8
chip_total = cx - 8

idcard = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="640" viewBox="0 0 400 640" font-family="{FONT}">
<!-- EDIT: YOUR NAME / ROLE / @USERNAME / CITY below. Photo: run scripts/embed_photo.py -->
<style>
@keyframes scan{{0%{{transform:translateX(-4px)}}100%{{transform:translateX(224px)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes sway{{0%,100%{{transform:rotate(-1.5deg)}}50%{{transform:rotate(1.5deg)}}}}
.scan{{animation:scan 2.4s ease-in-out infinite alternate}}
.ring{{transform-origin:200px 262px;animation:spin 14s linear infinite}}
.dot{{animation:blink 1.6s infinite}}
.sway{{transform-origin:200px 20px;animation:sway 6s ease-in-out infinite}}
</style>
<defs>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#58a6ff"/><stop offset="1" stop-color="#1b2735"/></linearGradient>
<linearGradient id="strap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2a44"/><stop offset="1" stop-color="#0b1424"/></linearGradient>
<clipPath id="photoClip"><circle cx="200" cy="262" r="50"/></clipPath>
<filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g class="sway">
<rect x="188" y="0" width="24" height="112" fill="url(#strap)"/>
<text transform="translate(205,10) rotate(90)" font-size="7.5" letter-spacing="2" fill="#58a6ff" opacity=".8">KEEP CODING • KEEP BUILDING • KEEP CODING •</text>
<rect x="186" y="104" width="28" height="26" rx="5" fill="#2a3340" stroke="#58a6ff" stroke-opacity=".5"/>
<rect x="30" y="126" width="340" height="490" rx="26" fill="#050505" stroke="url(#edge)" stroke-width="2.5"/>
<rect x="190" y="136" width="20" height="6" rx="3" fill="#000" stroke="#2a3340"/>
<text x="62" y="168" font-size="11" font-weight="800" letter-spacing="3" fill="#58a6ff">&lt;/&gt;</text>
<text x="200" y="168" font-size="12" font-weight="800" letter-spacing="3" text-anchor="middle" fill="#fff">DEVELOPER ID</text>
<circle class="dot" cx="338" cy="164" r="4.5" fill="#22c55e" filter="url(#glow)"/>
<line x1="52" y1="182" x2="348" y2="182" stroke="#1b2735"/>
<!-- photo ring -->
<circle cx="200" cy="262" r="64" fill="none" stroke="#1b2735" stroke-width="2"/>
<circle class="ring" cx="200" cy="262" r="64" fill="none" stroke="#58a6ff" stroke-width="2" stroke-dasharray="55 347" stroke-linecap="round" filter="url(#glow)"/>
<circle cx="200" cy="262" r="50" fill="#0d1520"/>
<!--PHOTO-->
<g clip-path="url(#photoClip)" fill="#2b3a52"><circle cx="200" cy="252" r="18"/><path d="M155,320 C155,282 245,282 245,320 Z"/></g>
<!--/PHOTO-->
<text x="200" y="356" font-size="24" font-weight="800" text-anchor="middle" fill="#fff">YOUR NAME</text>
<text x="200" y="380" font-size="12" font-weight="700" letter-spacing="3" text-anchor="middle" fill="#58a6ff">FRONTEND DEVELOPER</text>
<text x="200" y="398" font-size="10.5" text-anchor="middle" fill="#8b949e">@YOUR_USERNAME</text>
<path d="M188,412 L200,418 L212,412 L200,406 Z" fill="#58a6ff"/>
<text x="56" y="442" font-size="9" letter-spacing="1.5" fill="#6b7686">BASED IN</text>
<text x="344" y="442" font-size="12" font-weight="700" text-anchor="end" fill="#fff">YOUR CITY, COUNTRY</text>
<text x="56" y="464" font-size="9" letter-spacing="1.5" fill="#6b7686">STATUS</text>
<text x="344" y="464" font-size="12" font-weight="700" text-anchor="end" fill="#58a6ff">Always learning</text>
<g transform="translate({200 - chip_total/2:.1f},480)">{chip_svg}</g>
<g transform="translate(90,516)" fill="#cfe3ff">{barcode}
<rect class="scan" x="0" y="-4" width="2.5" height="54" fill="#58a6ff" filter="url(#glow)"/></g>
<text x="200" y="586" font-size="9" letter-spacing="3" text-anchor="middle" fill="#58a6ff">SCANNING...</text>
<text x="200" y="604" font-size="8" letter-spacing="1.5" text-anchor="middle" fill="#6b7686">ID: DEV-2026 • WEB DEV</text>
</g>
</svg>'''
open("idcard.svg", "w", encoding="utf-8").write(idcard)

# ---------------- BANNER ----------------
lines = ["Frontend Developer", "JavaScript &amp; React Enthusiast", "Always Learning, Always Building", "Turning Ideas Into Real Websites"]
tx = ""
for i, t in enumerate(lines):
    tx += f'<text class="l l{i}" x="470" y="228" font-size="30" font-weight="800" fill="#fff">{t}</text>'
rnd = random.Random(3)
items = []
while len(items) < 30:
    x, y = rnd.randint(30,1170), rnd.randint(30,370)
    if 440 < x < 1010 and 110 < y < 320: continue
    if 40 < x < 410 and 60 < y < 320: continue
    items.append(f'<text x="{x}" y="{y}" font-size="{rnd.randint(14,26)}" fill="#58a6ff" opacity="{rnd.uniform(.12,.35):.2f}">{rnd.choice(["&lt;/&gt;","{ }","01","=&gt;","( )","[ ]","&lt;div&gt;","++"])}</text>')
codes = "".join(items)
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" font-family="{FONT}">
<style>
@keyframes cyc{{0%,2%{{opacity:0}}6%,22%{{opacity:1}}27%,100%{{opacity:0}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
@keyframes caret{{50%{{opacity:0}}}}
.l{{opacity:0;animation:cyc 12s infinite}} .l1{{animation-delay:3s}} .l2{{animation-delay:6s}} .l3{{animation-delay:9s}}
.fl{{animation:float 5s ease-in-out infinite}} .caret{{animation:caret 1s steps(1) infinite}}
</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0a1626"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#58a6ff"/><stop offset="1" stop-color="#7ee8fa"/></linearGradient></defs>
<rect width="1200" height="400" rx="22" fill="url(#bg)" stroke="#1b2735" stroke-width="2"/>
{codes}
<g class="fl">
<rect x="60" y="70" width="330" height="240" rx="14" fill="#060a10" stroke="#1f2b3b"/>
<rect x="60" y="70" width="330" height="34" rx="14" fill="#0c131d"/>
<circle cx="84" cy="87" r="6" fill="#ff5f56"/><circle cx="104" cy="87" r="6" fill="#ffbd2e"/><circle cx="124" cy="87" r="6" fill="#27c93f"/>
<text x="225" y="92" font-size="11" fill="#8b949e" text-anchor="middle">developer.js</text>
<g font-size="13" fill="#58a6ff"><text x="82" y="136">const dev = {{</text><text x="104" y="160" fill="#cfe3ff">name: "YOUR NAME",</text><text x="104" y="184" fill="#cfe3ff">role: "Frontend",</text><text x="104" y="208" fill="#cfe3ff">stack: ["JS","React"],</text><text x="104" y="232" fill="#7ee8fa">coffee: true,</text><text x="82" y="256">}};</text><text x="82" y="288" fill="#3fb950">dev.build();</text><rect class="caret" x="170" y="277" width="8" height="14" fill="#58a6ff"/></g>
</g>
<text x="470" y="150" font-size="14" letter-spacing="6" fill="#58a6ff">&lt; HELLO WORLD /&gt;</text>
<text x="470" y="192" font-size="22" font-weight="700" fill="#8b949e">Hi, I'm YOUR NAME</text>
{tx}
<rect x="470" y="262" width="300" height="4" rx="2" fill="url(#ln)"/>
<text x="470" y="300" font-size="13" fill="#6b7686">HTML • CSS • JavaScript • TypeScript • React • Node.js</text>
</svg>'''
open("banner.svg", "w", encoding="utf-8").write(banner)
