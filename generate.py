#!/usr/bin/env python3
"""
Generates profile/trophy.svg and profile/stats.svg for a GitHub profile README.
Everything is drawn locally -> no vercel / third-party image servers needed,
so the images never "break".

Usage:
  python scripts/generate.py            # live data from GitHub API
  python scripts/generate.py --demo     # sample data (offline test)

Env vars (set automatically in the workflow):
  GH_USER, GH_NAME, GITHUB_TOKEN
"""
import json, os, sys, datetime, urllib.request

USER = os.environ.get("GH_USER", "YOUR_USERNAME")
NAME = os.environ.get("GH_NAME", "YOUR NAME")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
DEMO = "--demo" in sys.argv
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- data
def api(url, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", "profile-readme-generator")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def safe(fn, default):
    try:
        return fn()
    except Exception as e:  # never crash the workflow because of one call
        print("warn:", e)
        return default

def fetch():
    u = api(f"https://api.github.com/users/{USER}")
    repos = safe(lambda: api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"), [])
    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    langs = {}
    for r in own[:30]:
        l = safe(lambda: api(r["languages_url"]), {})
        for k, v in l.items():
            langs[k] = langs.get(k, 0) + v
    q = lambda s: safe(lambda: api("https://api.github.com/search/" + s)["total_count"], 0)
    commits = q(f"commits?q=author:{USER}")
    prs = q(f"issues?q=author:{USER}+type:pr")
    issues = q(f"issues?q=author:{USER}+type:issue")
    reviews = q(f"issues?q=reviewed-by:{USER}+type:pr")
    orgs = len(safe(lambda: api(f"https://api.github.com/users/{USER}/orgs"), []))
    created = datetime.datetime.strptime(u["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    years = max(0, int((datetime.datetime.utcnow() - created).days / 365))
    year_contrib = 0
    if TOKEN:
        gql = json.dumps({"query": 'query{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions}}}}' % USER}).encode()
        year_contrib = safe(lambda: api("https://api.github.com/graphql", gql)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"], 0)
    year_contrib = year_contrib or commits
    return dict(stars=stars, commits=commits, followers=u["followers"], issues=issues,
                prs=prs, repos=u["public_repos"], reviews=reviews, experience=years,
                orgs=orgs, gists=u["public_gists"], languages=len(langs),
                contributions=year_contrib, year_contrib=year_contrib, langs=langs)

def demo():
    return dict(stars=3, commits=74, followers=2, issues=0, prs=0, repos=4, reviews=0,
                experience=0, orgs=0, gists=0, languages=3, contributions=81, year_contrib=81,
                langs={"HTML": 4939, "CSS": 4145, "JavaScript": 917})

S = demo() if DEMO else fetch()

# ---------------------------------------------------------------- theme
BG, CARD, BORDER = "#000000", "#0b0b0b", "#222a35"
ACCENT, TEXT, MUTED = "#58a6ff", "#ffffff", "#8b949e"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
GH_PATH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z")

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- trophies
RANKS = ["LOCKED", "C", "B", "A", "AA", "AAA", "S", "SS", "SSS"]
RANK_COLOR = ["#3b4350", "#8b949e", "#6cb6ff", "#58a6ff", "#39c5ff", "#7ee8fa",
              "#e6edf3", "#f5d56b", "#ffb703"]
METRICS = [  # label, key, 8 thresholds for C..SSS
    ("Stars", "stars", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Commits", "commits", [10, 50, 100, 250, 500, 1000, 2500, 5000]),
    ("Followers", "followers", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Issues", "issues", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Pull Requests", "prs", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Repositories", "repos", [1, 5, 10, 20, 35, 50, 75, 100]),
    ("Reviews", "reviews", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Experience", "experience", [1, 2, 3, 5, 7, 10, 12, 15]),
    ("Organizations", "orgs", [1, 2, 3, 4, 5, 7, 9, 12]),
    ("Gists", "gists", [1, 5, 10, 25, 50, 100, 250, 500]),
    ("Languages", "languages", [1, 3, 5, 7, 10, 12, 15, 20]),
    ("Contributions", "contributions", [10, 50, 100, 250, 500, 1000, 2500, 5000]),
]

def rank_of(v, th):
    return sum(1 for t in th if v >= t)

def star(cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

def trophy_icon(cx, cy, color, locked):
    g = f'<g transform="translate({cx},{cy})" opacity="{0.55 if locked else 1}">'
    g += f'<path d="M-15,-20 H15 V-6 C15,6 8,13 0,13 C-8,13 -15,6 -15,-6 Z" fill="{color}"/>'
    g += f'<path d="M-15,-16 H-23 C-23,-5 -19,0 -13,0 M15,-16 H23 C23,-5 19,0 13,0" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
    g += f'<rect x="-3" y="13" width="6" height="8" fill="{color}"/>'
    g += f'<rect x="-12" y="21" width="24" height="5" rx="2" fill="{color}"/>'
    if locked:  # little padlock
        g += '<rect x="-5" y="-9" width="10" height="9" rx="1.5" fill="#000"/>'
        g += '<path d="M-3,-9 V-12 a3,3 0 0 1 6,0 V-9" fill="none" stroke="#000" stroke-width="1.8"/>'
    else:
        g += star(0, -6, 6.5, "#000")
    return g + "</g>"

def build_trophies():
    cw, ch, gap, pad = 124, 168, 12, 24
    cols, rows = 6, 2
    W = pad * 2 + cols * cw + (cols - 1) * gap
    H = pad * 2 + rows * ch + gap + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<style>@keyframes pop{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'
         '.c{animation:pop .6s ease both}</style>',
         f'<rect width="{W}" height="{H}" rx="18" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>']
    for i, (label, key, th) in enumerate(METRICS):
        v = S[key]
        rk = rank_of(v, th)
        goal = th[min(rk, 7)]
        locked = rk == 0
        col = RANK_COLOR[rk]
        x = pad + (i % cols) * (cw + gap)
        y = pad + (i // cols) * (ch + gap)
        pr = min(1.0, v / goal) if goal else 1
        bw = cw - 36
        o.append(f'<g class="c" style="animation-delay:{i*0.06:.2f}s">')
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{CARD}" stroke="{col if not locked else BORDER}" stroke-opacity="{0.9 if not locked else 1}"/>')
        o.append(f'<rect x="{x+cw/2-24}" y="{y+12}" width="48" height="18" rx="9" fill="none" stroke="{col}" stroke-opacity=".7"/>')
        o.append(f'<text x="{x+cw/2}" y="{y+25}" font-size="10" font-weight="700" text-anchor="middle" fill="{col}">{RANKS[rk]}</text>')
        o.append(trophy_icon(x + cw / 2, y + 68, col, locked))
        o.append(f'<text x="{x+cw/2}" y="{y+114}" font-size="11" font-weight="700" text-anchor="middle" fill="{TEXT}">{esc(label)}</text>')
        o.append(f'<text x="{x+cw/2}" y="{y+132}" font-size="13" font-weight="700" text-anchor="middle" fill="{col if not locked else MUTED}">{v}</text>')
        o.append(f'<rect x="{x+18}" y="{y+141}" width="{bw}" height="4" rx="2" fill="#1b222c"/>')
        o.append(f'<rect x="{x+18}" y="{y+141}" width="{bw*pr:.1f}" height="4" rx="2" fill="{col}"/>')
        o.append(f'<text x="{x+cw/2}" y="{y+159}" font-size="8.5" text-anchor="middle" fill="{MUTED}">{v} / {goal}</text>')
        o.append("</g>")
    ly = H - 22
    lx = W / 2 - 4.5 * 52
    for j, r in enumerate(RANKS[1:]):
        px = lx + j * 52 + 10
        o.append(f'<circle cx="{px}" cy="{ly}" r="4" fill="{RANK_COLOR[j+1]}"/>')
        o.append(f'<text x="{px+9}" y="{ly+3.5}" font-size="9" fill="{MUTED}">{r}</text>')
    o.append("</svg>")
    return "\n".join(o)

# ---------------------------------------------------------------- stats card
LANG_COL = {"HTML": "#e34c26", "CSS": "#8957e5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
            "Python": "#3572A5", "Java": "#b07219", "C++": "#f34b7d", "C": "#8b949e", "PHP": "#4F5D95",
            "Shell": "#89e051", "Dart": "#00B4AB", "Kotlin": "#A97BFF", "Go": "#00ADD8"}
EXTRA = ["#58a6ff", "#3fb950", "#d29922", "#f778ba", "#a371f7"]

def build_stats():
    W, H = 828, 300
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<style>@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}'
         '.bar{transform-origin:left;animation:grow 1.2s ease both}</style>',
         '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#58a6ff"/><stop offset="1" stop-color="#7ee8fa"/></linearGradient></defs>',
         f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="18" fill="{BG}" stroke="url(#g)" stroke-width="3"/>',
         f'<g transform="translate(30,26) scale(2.4)" fill="#fff"><path d="{GH_PATH}"/></g>',
         f'<g transform="translate({W-68},26) scale(2.4)" fill="#fff"><path d="{GH_PATH}"/></g>',
         f'<text x="{W/2}" y="56" font-size="22" font-weight="800" text-anchor="middle" fill="#fff">{esc(NAME)} — GitHub Stats</text>']
    tiles = [("Contributions", S["year_contrib"], "past year"), ("Commits", S["commits"], "total"),
             ("Stars", S["stars"], "earned"), ("Followers", S["followers"], "people"),
             ("Repos", S["repos"], "public")]
    tw = (W - 60 - 4 * 12) / 5
    for i, (lab, val, sub) in enumerate(tiles):
        x = 30 + i * (tw + 12)
        o.append(f'<rect x="{x:.1f}" y="88" width="{tw:.1f}" height="92" rx="12" fill="{CARD}" stroke="{BORDER}"/>')
        o.append(f'<text x="{x+tw/2:.1f}" y="128" font-size="28" font-weight="800" text-anchor="middle" fill="{ACCENT}">{val}</text>')
        o.append(f'<text x="{x+tw/2:.1f}" y="150" font-size="11.5" font-weight="700" text-anchor="middle" fill="#fff">{lab}</text>')
        o.append(f'<text x="{x+tw/2:.1f}" y="166" font-size="9.5" text-anchor="middle" fill="{MUTED}">{sub}</text>')
    # languages
    o.append(f'<text x="30" y="212" font-size="13" font-weight="700" fill="#fff">Most Used Languages</text>')
    langs = sorted(S["langs"].items(), key=lambda kv: -kv[1])[:6]
    tot = sum(v for _, v in langs) or 1
    x0, bw = 30, W - 60
    o.append(f'<clipPath id="lc"><rect x="{x0}" y="222" width="{bw}" height="10" rx="5"/></clipPath><g clip-path="url(#lc)" class="bar">')
    cx = x0
    for i, (k, v) in enumerate(langs):
        w = bw * v / tot
        o.append(f'<rect x="{cx:.1f}" y="222" width="{w:.1f}" height="10" fill="{LANG_COL.get(k, EXTRA[i % 5])}"/>')
        cx += w
    o.append("</g>")
    for i, (k, v) in enumerate(langs):
        x = 30 + (i % 3) * 262
        y = 256 + (i // 3) * 20
        o.append(f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{LANG_COL.get(k, EXTRA[i % 5])}"/>')
        o.append(f'<text x="{x+16}" y="{y}" font-size="11" fill="#c9d1d9">{esc(k)} {100*v/tot:.1f}%</text>')
    o.append("</svg>")
    return "\n".join(o)

open(os.path.join(OUT, "trophy.svg"), "w", encoding="utf-8").write(build_trophies())
open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8").write(build_stats())
print("generated profile/trophy.svg and profile/stats.svg for", USER)
