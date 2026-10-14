#!/usr/bin/env python3
"""Generates the pages of the Institute's site from one shared shell.

    python3 tools/build.py

Every page is written to the folder above this one. The copy lives here as
plain HTML strings; the three figures on the research page are drawn as SVG
from the numbers in the tables below, so that the chart and its data table
can never disagree.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

NAME = 'Institute for AI, Financial Risk and Stability'
CODE = 'IAFRS'
CITY = 'Austin, Texas'
EMAIL = 'contact@iafrs.org'            # placeholder until the Institute's address exists
SITE = 'https://dgodorozha.github.io/iafrs/'   # the address the site is served from, used for link previews
BASE = '/iafrs/'                                # the path it is served under; the 404 page links from here
PROBATIO_URL = ''                      # the platform's own site, once it has one; empty means no link
YEAR = '2026'

NAV = [('research.html', 'Research'), ('probatio.html', 'Probatio'), ('people.html', 'People'),
       ('about.html', 'About'), ('support.html', 'Support')]


def tag(letter, code):
    return f'<span class="tag"><b>{letter}</b><span>{code}</span></span>'


def shell(path, title, description, body, home=False):
    full = NAME if home else f'{title}: {NAME}'
    root = BASE if path == '404.html' else ''
    nav = '\n'.join(
        '        <a href="%s%s"%s>%s</a>' % (root, href, ' aria-current="page"' if href == path else '', label) for href, label in NAV)
    probatio_link = f'<a href="{PROBATIO_URL}" rel="noopener">Probatio</a>' if PROBATIO_URL else 'Probatio'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{'' if path == 'index.html' else path}">
<meta property="og:image" content="{SITE}img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0f16">
<link rel="icon" href="{root}img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{root}img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="{root}img/apple-touch-icon.png">
<link rel="stylesheet" href="{root}css/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{root}index.html" aria-label="{NAME}, home">
      <span class="brand__glyph" aria-hidden="true"></span>
      <span class="brand__code" aria-hidden="true">{CODE}</span>
      <span class="brand__name">{NAME}</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Site">
{nav}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div>
      <a class="brand" href="{root}index.html" aria-label="{NAME}, home">
        <span class="brand__glyph" aria-hidden="true"></span>
        <span class="brand__code" aria-hidden="true">{CODE}</span>
        <span class="brand__name">{NAME}</span>
      </a>
      <p>An independent, non-profit research institute studying how artificial intelligence changes financial risk, and how the authorities responsible for stability can validate the tools and rules meant to contain it.</p>
      <p>A 501(c)(3) non-profit organisation. {CITY}.</p>
    </div>
    <div>
      <h4>Pages</h4>
      <ul>
        <li><a href="{root}research.html">Research</a></li>
        <li><a href="{root}probatio.html">Probatio</a></li>
        <li><a href="{root}people.html">People</a></li>
        <li><a href="{root}about.html">About</a></li>
        <li><a href="{root}support.html">Support</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{CITY}</li>
      </ul>
      <p class="small" style="margin-top:18px">{probatio_link} is a separate platform. The Institute&rsquo;s research informs its method; the Institute does not develop, licence or operate it.</p>
    </div>
  </div>
  <div class="legal">
    <div class="wrap">
      <span>&copy; {YEAR} {NAME}.</span>
      <span>Set in IBM Plex Sans and JetBrains Mono, both under the SIL Open Font Licence.</span>
    </div>
  </div>
</footer>
<script src="{root}js/site.js"></script>
</body>
</html>
'''


# ----------------------------------------------------------------- figures --
SENTINELS_FIDELITY = [('Volatility trigger', 1.00), ('Absorption ratio', 0.22), ('Endogeneity (Hawkes)', 0.21),
                      ('Correlation clustering', 0.21), ('Buy sell imbalance', 0.20), ('Tail dependence', 0.19),
                      ('Network community', 0.15), ('Lead lag ignition', 0.10)]
SENTINELS_DECISION = [('Tail dependence', 0.68), ('Absorption ratio', 0.57), ('Buy sell imbalance', 0.42),
                      ('Lead lag ignition', 0.41), ('Network community', 0.41), ('Correlation clustering', 0.34),
                      ('Endogeneity (Hawkes)', 0.30), ('Volatility trigger', 0.25)]
CERTIFIED = 'Tail dependence'

RULES = [('Market wide breaker', 0.32, 0.40), ('LULD band (US)', 0.22, 0.37), ('Dynamic throttle', 0.21, 0.39),
         ('Venue halt (EU)', 0.19, 0.41), ('Responsive ladder', 0.15, 0.30), ('Kill switch', 0.07, 0.08),
         ('MWCB (US levels)', 0.04, 0.13), ('Learned policy', 0.02, 0.06)]

DOSE = [(10, 0.073), (15, 0.080), (20, 0.088), (25, 0.099), (30, 0.115), (35, 0.138), (40, 0.168), (45, 0.193), (50, 0.212)]
DOSE_THRESHOLD = 0.10

AMBER_DEEP, BLUE_DEEP, GREY, INK = '#b5821a', '#2f6fb3', '#c9d0db', '#14181f'


def bump_svg():
    W, H, top, pitch = 540, 330, 50, 36
    xl_val, xr_name, xr_val = 200, 268, 540
    left_y = {n: top + i * pitch for i, (n, _) in enumerate(SENTINELS_FIDELITY)}
    right_y = {n: top + i * pitch for i, (n, _) in enumerate(SENTINELS_DECISION)}
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="bump-t" xmlns="http://www.w3.org/2000/svg">',
           '<title id="bump-t">Eight surveillance sentinels ranked by fidelity and by decision accuracy</title>',
           f'<text x="0" y="18" class="lbl" font-weight="600">Ranked by fidelity (conventional)</text>',
           f'<text x="{xr_name}" y="18" class="lbl" font-weight="600">Ranked by decision accuracy</text>']
    # connectors first, so that the text sits above them
    for n in left_y:
        cert = n == CERTIFIED
        out.append(f'<line x1="{xl_val + 8}" y1="{left_y[n] - 4}" x2="{xr_name - 8}" y2="{right_y[n] - 4}" '
                   f'stroke="{AMBER_DEEP if cert else GREY}" stroke-width="{2.5 if cert else 1.25}" />')
    for i, (n, v) in enumerate(SENTINELS_FIDELITY):
        y = top + i * pitch
        out.append(f'<text x="0" y="{y}" class="num">{i + 1}</text>')
        out.append(f'<text x="18" y="{y}" class="lbl">{n}</text>')
        out.append(f'<text x="{xl_val}" y="{y}" class="num" text-anchor="end">{v:.2f}</text>')
    for i, (n, v) in enumerate(SENTINELS_DECISION):
        y = top + i * pitch
        cert = n == CERTIFIED
        out.append(f'<text x="{xr_name}" y="{y}" class="num">{i + 1}</text>')
        weight = ' font-weight="600"' if cert else ''
        mark = '<tspan class="num" dx="8">certified</tspan>' if cert else ''
        out.append(f'<text x="{xr_name + 18}" y="{y}" class="lbl"{weight}>{n}{mark}</text>')
        out.append(f'<text x="{xr_val}" y="{y}" class="num" text-anchor="end">{v:.2f}</text>')
    out.append('</svg>')
    rows = ''.join(f'<tr><td>{i + 1}</td><td>{a}</td><td class="num">{va:.2f}</td><td>{b}</td><td class="num">{vb:.2f}</td></tr>'
                   for i, ((a, va), (b, vb)) in enumerate(zip(SENTINELS_FIDELITY, SENTINELS_DECISION)))
    table = ('<details><summary>Data table</summary><table><thead><tr><th>Rank</th><th>By fidelity</th><th class="num">Fidelity</th>'
             f'<th>By decision accuracy</th><th class="num">Decision F1</th></tr></thead><tbody>{rows}</tbody></table></details>')
    return '\n'.join(out), table


def bars_svg():
    W, left, right, top, pitch, bh = 540, 150, 500, 22, 40, 10
    H = top + pitch * len(RULES) + 30
    span = right - left
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="bars-t" xmlns="http://www.w3.org/2000/svg">',
           '<title id="bars-t">Containment and expected shortfall reduction by intervention rule</title>']
    for g in range(0, 6):
        x = left + span * g / 5
        out.append(f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{H - 24}" class="grid" />')
        out.append(f'<text x="{x:.1f}" y="{H - 6}" class="axis" text-anchor="middle">{g / 10:.1f}</text>')
    for i, (name, cont, es) in enumerate(RULES):
        y = top + i * pitch
        out.append(f'<text x="{left - 12}" y="{y + 12}" class="lbl" text-anchor="end">{name}</text>')
        for j, (v, col, lab) in enumerate(((cont, AMBER_DEEP, 'containment'), (es, BLUE_DEEP, 'expected shortfall reduction'))):
            yy = y + j * (bh + 2)
            w = span * v / 0.5
            out.append(f'<rect x="{left}" y="{yy}" width="{w:.1f}" height="{bh}" fill="{col}"><title>{name}: {lab} {v:.2f}</title></rect>')
            out.append(f'<text x="{left + w + 7:.1f}" y="{yy + bh - 1.5}" class="num">{v:.2f}</text>')
    out.append(f'<line x1="{left}" y1="{top - 8}" x2="{left}" y2="{H - 24}" stroke="{INK}" stroke-width="1" />')
    out.append('</svg>')
    rows = ''.join(f'<tr><td>{n}</td><td class="num">{c:.2f}</td><td class="num">{e:.2f}</td></tr>' for n, c, e in RULES)
    table = ('<details><summary>Data table</summary><table><thead><tr><th>Rule</th><th class="num">Containment</th>'
             f'<th class="num">Expected shortfall reduction</th></tr></thead><tbody>{rows}</tbody></table></details>')
    return '\n'.join(out), table


def dose_svg():
    W, H, left, right, top, bottom = 540, 300, 48, 528, 22, 254
    x0, x1, y0, y1 = 10, 50, 0.05, 0.23

    def X(p): return left + (right - left) * (p - x0) / (x1 - x0)

    def Y(v): return bottom - (bottom - top) * (v - y0) / (y1 - y0)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="dose-t" xmlns="http://www.w3.org/2000/svg">',
           '<title id="dose-t">Drawdown as the share of agents on one model vendor rises</title>']
    for v in (0.05, 0.10, 0.15, 0.20):
        out.append(f'<line x1="{left}" y1="{Y(v):.1f}" x2="{right}" y2="{Y(v):.1f}" class="grid" />')
        out.append(f'<text x="{left - 10}" y="{Y(v) + 4:.1f}" class="axis" text-anchor="end">{v:.2f}</text>')
    for p, _ in DOSE:
        out.append(f'<text x="{X(p):.1f}" y="{bottom + 22}" class="axis" text-anchor="middle">{p}%</text>')
    out.append(f'<text x="{(left + right) / 2:.1f}" y="{H - 2}" class="axis" text-anchor="middle">share of agents on one vendor</text>')
    out.append(f'<line x1="{left}" y1="{Y(DOSE_THRESHOLD):.1f}" x2="{right}" y2="{Y(DOSE_THRESHOLD):.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 4" />')
    out.append(f'<text x="{right}" y="{Y(DOSE_THRESHOLD) + 15:.1f}" class="num" text-anchor="end">dislocation threshold, drawdown 0.10</text>')
    pts = ' '.join(f'{X(p):.1f},{Y(v):.1f}' for p, v in DOSE)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{AMBER_DEEP}" stroke-width="2" stroke-linejoin="round" />')
    for p, v in DOSE:
        out.append(f'<circle cx="{X(p):.1f}" cy="{Y(v):.1f}" r="4.5" fill="{AMBER_DEEP}" stroke="#fff" stroke-width="2"><title>{p}% on one vendor: drawdown {v:.3f}</title></circle>')
    for p, v in ((10, 0.073), (30, 0.115), (50, 0.212)):
        anchor = 'end' if p == 50 else 'start'
        dx = -10 if p == 50 else 10
        out.append(f'<text x="{X(p) + dx:.1f}" y="{Y(v) - 10:.1f}" class="num" text-anchor="{anchor}">{v:.3f}</text>')
    out.append('</svg>')
    rows = ''.join(f'<tr><td class="num">{p}%</td><td class="num">{v:.3f}</td></tr>' for p, v in DOSE)
    table = ('<details><summary>Data table</summary><table><thead><tr><th class="num">Share on one vendor</th>'
             f'<th class="num">Drawdown</th></tr></thead><tbody>{rows}</tbody></table></details>')
    return '\n'.join(out), table


def figure(svg, table, title, caption, legend=''):
    return f'''<figure class="fig">
  <div class="fig__title"><h4>{title}</h4>{legend}</div>
  {svg}
  <figcaption>{caption}</figcaption>
  {table}
</figure>'''


# ------------------------------------------------------------------- pages --
FRONT_ROWS = [('MKT', 'market tape: every simulated price step, live, one scenario at a time', '1'),
              ('NET', 'agent correlation network of the live run, before and after the shock', '2'),
              ('GAP', 'the decision gap with its bootstrap: fidelity against decision rankings', '3'),
              ('SEN', 'sentinel telemetry with intervals, held out results and the alert feed', '4'),
              ('INT', 'intervention monitor: containment, dislocation probability, burden by class', '5'),
              ('CSF', 'case file: pivot the per scenario evidence', '6'),
              ('LDG', 'rationale ledger: the signed hash chain, entry by entry, with replay', '7'),
              ('RUN', 'run control: identities, gates with refusal, emergency stop, briefing', '8'),
              ('ASK', 'run oracle: grounded answers computed from the artefacts', '9'),
              ('AUT', 'autonomy gate: backed execution, in sample and leave one out', '0'),
              ('RSK', 'assurance: conformal guarantee, cost frontier, attribution, truth audit, dose response, red team', 'RSK'),
              ('REG', 'run registry: every past run, its status and its evidence pack', 'REG')]


FRONT_SHORT = {'MKT': 'every simulated price step, live, one scenario at a time',
               'NET': 'the agent correlation network, before and after the shock',
               'GAP': 'the decision gap with its bootstrap',
               'SEN': 'sentinel telemetry, held out results and the alert feed',
               'INT': 'containment, dislocation probability, burden by class',
               'CSF': 'the per scenario evidence, pivoted',
               'LDG': 'the signed hash chain, entry by entry, with replay',
               'RUN': 'identities, gates with refusal, emergency stop, briefing',
               'ASK': 'grounded answers computed from the artefacts',
               'AUT': 'the autonomy gate, in sample and leave one out',
               'RSK': 'guarantee, cost frontier, attribution, truth audit, red team',
               'REG': 'every past run, its status and its evidence pack'}


def front_panel(with_actions=True, short=False):
    rows = '\n'.join(f'      <div class="front__row"><span class="fcode">{c}</span><span>{FRONT_SHORT[c] if short else d}</span><span class="kbd">{k}</span></div>'
                     for c, d, k in FRONT_ROWS)
    grid_class = 'front__grid front__grid--one' if short else 'front__grid'
    actions = ''
    if with_actions:
        ext = f'\n      <a class="btn btn--ghost-ink" href="{PROBATIO_URL}" rel="noopener">The platform&rsquo;s site</a>' if PROBATIO_URL else ''
        actions = f'''
    <div class="front__actions">
      <a class="btn btn--amber" href="probatio.html">About Probatio</a>{ext}
    </div>'''
    return f'''<div class="front">
    <div class="front__code">PRB</div>
    <div class="front__name">Probatio, an agentic scenario lab</div>
    <p>A public authority stress tests surveillance sentinels and intervention rules on synthetic AI agent markets calibrated from its own data, and certifies on decision accuracy rather than aggregate fidelity. Every run passes two human gates and a critic, and leaves a signed, replayable ledger.</p>
    <div class="{grid_class}">
{rows}
    </div>{actions}
    <div class="front__build">8 sentinels, 8 rules and 18 scenario families built in, extensible by the authority. 31 critic checks. 17 security controls. Runs on the authority&rsquo;s own infrastructure; no data leaves it.</div>
  </div>'''


INDEX = f'''
<section class="hero" aria-label="Introduction">
  <div class="term">
    <div class="term__bar">
      <span class="fcode">MKT</span>
      <span class="title">Market tape</span>
      <span class="sub">the same shock, three worlds</span>
      <span class="right"><span class="chip chip--amber">demonstration</span></span>
    </div>
    <div class="term__body">
      <canvas id="tape" aria-hidden="true"></canvas>
      <div class="hero__card">
        <div class="kicker">A non-profit research institute</div>
        <h1>Research for a financial system in which the traders are machines.</h1>
        <p>The Institute studies how artificial intelligence changes financial risk, and how the authorities responsible for stability can validate, on the decisions that matter, the surveillance tools and intervention rules meant to contain it.</p>
        <div class="hero__actions">
          <a class="btn btn--amber" href="research.html">Read the research programme</a>
          <a class="btn btn--ghost-ink" href="support.html">Support the Institute</a>
        </div>
      </div>
    </div>
    <div class="term__foot">
      <div class="legend" aria-hidden="true"><span class="key key--quiet">quiet</span><span class="key key--herd">herd</span><span class="key key--throttle">throttle</span></div>
      <div class="caption">Three synthetic markets receive the same shock at step 280: one in which the trading agents are independent, one in which agents on a shared foundation model herd, and one in which a dynamic throttle engages 25 steps later. Drawn from a seeded simulation, not from market data.</div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="problem-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('H', 'HRD')}<h2 id="problem-h">Why the question is open</h2></div>
      <p class="lede">Supervisors are building surveillance tools and circuit breakers for a market in which AI agents trade. The way those tools are validated can certify the one that fails at the decision it exists to inform.</p>
    </div>
    <div class="cols">
      <div>
        <h3>Herding is plausible, and flagged</h3>
        <p>Trading agents built on shared foundation models can react in correlated ways, so that a routine shock becomes a dislocation. The Financial Stability Board, IOSCO, the Bank of England and the IMF have each raised the concern, and algorithmic trading already accounts for around 70 per cent of United States equity trading.</p>
      </div>
      <div>
        <h3>The yardstick is wrong</h3>
        <p>Surveillance tools and intervention rules are validated on aggregate fidelity: how well a synthetic market reproduces volatility, spreads and correlation. A tool can match those statistics and still fail at the supervisory decision, which agents are destabilising and when to act.</p>
      </div>
      <div>
        <h3>The record is empty</h3>
        <p>Historical back tests contain almost no episodes of machine herding, so a tool can only be scored on the decision in a generated market with a known truth. Public agent based studies describe behaviour; they benchmark no tools or rules and leave no audit trail on which a certification could rest.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--ink" aria-labelledby="evidence-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('R', 'RES')}<h2 id="evidence-h">What the evidence shows</h2></div>
      <p class="lede">The decision gap is real, a certification can carry a guarantee, and the guarantee can be stress tested.</p>
    </div>
    <div class="tiles">
      <div class="tile"><div class="tile__n">0.68</div><div class="tile__l">Decision gap</div><div class="tile__t">Tools ranked by how well they mimic market statistics are close to the reverse of tools ranked by whether they catch the destabilising agents (0 is the same order, 1 the exact reverse).</div></div>
      <div class="tile"><div class="tile__n">90%</div><div class="tile__l">Rankings still invert</div><div class="tile__t">In 90 per cent of 400 resampled batteries the two orders disagree, so the gap is not one lucky draw.</div></div>
      <div class="tile"><div class="tile__n">1.00 &rarr; 0.25</div><div class="tile__l">The volatility trigger</div><div class="tile__t">First by fidelity, last on the decision: the conventional yardstick certifies the tool that fails at the decision it exists to inform.</div></div>
      <div class="tile"><div class="tile__n">1 in 4</div><div class="tile__l">Guaranteed false alert bound</div><div class="tile__t">Tail dependence is certified by a conformal threshold set on eight calibration scenarios, and tops the decision ranking in 98 per cent of resamples.</div></div>
    </div>
    <div class="counts"><span><b>8</b> sentinels</span><span><b>8</b> rules</span><span><b>51</b> synthetic markets in <b>18</b> families</span><span><b>400</b> scenario bootstrap</span><span><b>48</b> reinforcement learning traders</span><span><b>31</b> critic checks</span><span><b>2</b> human gates</span></div>
    <div class="after-tiles">
      <p>The figures come from a demonstration battery produced with Probatio. The central finding, that ranking tools by fidelity nearly reverses ranking them by decision accuracy, is the subject of a paper accepted at ICAIF 2026.</p>
      <a class="btn btn--ghost-ink" href="research.html">How the results are read</a>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="prog-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('P', 'PRG')}<h2 id="prog-h">Programmes</h2></div>
      <p class="lede">Five lines of work, one question: when the traders are machines, how should a supervisor decide which tools and rules to trust, and how can that decision be certified?</p>
    </div>
    <div class="prog">
      <article style="background:var(--paper)">
        {tag('C', 'CRT')}
        <h3>Decision first certification</h3>
        <p>Scoring surveillance tools on the supervisory decision rather than on resemblance to market statistics, with finite sample guarantees: conformal false alert bounds, winner stability and walk forward regret, so that the procedure, not one tool, is what is certified.</p>
      </article>
      <article style="background:var(--paper)">
        {tag('H', 'HRD')}
        <h3>Agentic markets and herding</h3>
        <p>Synthetic markets with a known truth: noise traders, fundamentalists, vendor clusters, reinforcement learning traders that learn to herd, distilled language model personas and colluding manipulators, and the dose response of concentration on a single model vendor.</p>
      </article>
      <article style="background:var(--paper)">
        {tag('I', 'INT')}
        <h3>Intervention rules</h3>
        <p>Circuit breakers, price bands, venue halts, dynamic throttles and kill switches across EU, UK and US style instruments, each scored on containment, false halts, tail risk, time to dislocation and proportionality against the untreated market.</p>
      </article>
      <article style="background:var(--paper)">
        {tag('G', 'GOV')}
        <h3>Governance, audit and assurance</h3>
        <p>The controls that let a supervisory system rest on generated evidence: human gates whose approver is checked against a register, signed replayable ledgers, critics that recompute every figure, transparency records and a red team that attacks the certified tool.</p>
      </article>
      <article class="wide" style="background:var(--paper)">
        <div>
          {tag('O', 'OPN')}
          <h3>An open benchmark</h3>
          <span class="status">in preparation</span>
        </div>
        <p>A public library of scenario families and agent templates, written in a bounded declarative language and hashed into every battery that uses them, so that any authority can calibrate the markets to its own data, add its own families and compare its tools against the same truth as everyone else.</p>
      </article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="prb-h">
  <div class="wrap">
    <div class="split">
      <div class="sticky">
        <div class="head" style="margin-bottom:24px">
          <div class="head__row">{tag('P', 'PRB')}<h2 id="prb-h">The platform</h2></div>
        </div>
        <p class="lede" style="margin-bottom:20px">The Institute&rsquo;s method is implemented in Probatio, an agentic scenario lab in which an authority stress tests candidate tools and rules on synthetic markets calibrated from its own data.</p>
        <p class="muted">Probatio is a separate platform with its own governance. The Institute&rsquo;s research informs its method, and the Institute uses it to produce the evidence published here; it does not develop, licence or operate it.</p>
      </div>
      {front_panel(short=True)}
    </div>
  </div>
</section>

<section class="band" aria-labelledby="give-h">
  <div class="wrap">
    <div>
      <h2 id="give-h">Independent evidence needs independent support.</h2>
      <p>Gifts and grants fund the open benchmark, independent audits of the certification procedure and the researchers&rsquo; time. Authorities can partner with the Institute to run a pilot on their own data.</p>
    </div>
    <div class="band__actions">
      <a class="btn btn--amber" href="support.html">Support the Institute</a>
      <a class="btn btn--ghost-ink" href="mailto:{EMAIL}">Write to us</a>
    </div>
  </div>
</section>
'''


def research_page():
    bump, bump_t = bump_svg()
    bars, bars_t = bars_svg()
    dose, dose_t = dose_svg()
    legend_bars = '<div class="fig__legend"><span><i style="--k:#b5821a"></i>containment</span><span><i style="--k:#2f6fb3"></i>expected shortfall reduction</span></div>'
    return f'''
<div class="page-head">
  <div class="wrap">
    <h1>Research programme</h1>
    <p class="lede">The Institute&rsquo;s work asks one question in several forms: when the traders are machines, how should a supervisor decide which tools and rules to trust, and how can that decision be certified and audited?</p>
  </div>
</div>

<section class="section" aria-labelledby="crt-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('C', 'CRT')}<h2 id="crt-h">How a surveillance tool is certified</h2></div>
    </div>
    <div class="two">
      <div class="prose">
        <p><strong>Every sentinel is ranked twice.</strong> By fidelity: how closely its stress signal tracks the market&rsquo;s aggregate statistics, the conventional validation yardstick. By decision accuracy: whether the agents it flags are the ones that were in fact destabilising, which only a generated market can reveal. The decision gap (0 for the same order, 1 for the exact reverse) is 0.68 on the demonstration battery; in 90 per cent of 400 resampled batteries the two orders still disagree. The volatility trigger is first by fidelity and last on the decision.</p>
        <p><strong>Certification.</strong> Tail dependence is the most accurate tool whose false alert probability on a new quiet market is bounded at 0.25 by a conformal threshold set on eight calibration scenarios. It tops the decision ranking in 98 per cent of resamples. The walk forward test, which certifies on earlier folds and scores on the next, shows a mean regret of 0.27, so the procedure, not the tool, is what is certified.</p>
        <p><strong>The science behind the metrics.</strong> Precision, recall and F1 against the generator&rsquo;s truth; a 400 scenario bootstrap for intervals, evidence grades, the probability of inversion and winner stability; Kendall&rsquo;s tau turned into the gap (1 minus tau over 2); and a split conformal threshold on exchangeable quiet scenarios, which gives a finite sample bound on the false alert probability at level alpha.</p>
      </div>
      {figure(bump, bump_t, 'Eight sentinels, ranked twice on the demonstration battery',
              'Fidelity on the left, decision accuracy (F1 against the generator&rsquo;s truth) on the right; the certified tool in amber. Tools near the top of the conventional ranking fall to the bottom of the decision ranking and the reverse.')}
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="int-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('I', 'INT')}<h2 id="int-h">How an intervention rule is scored</h2></div>
    </div>
    <div class="two">
      <div class="prose">
        <p><strong>Each rule is applied to every herding scenario and to the quiet ones.</strong> Containment is the share of the dislocation it removes. The hazard ratio, from a Cox model against the untreated market, is the chance of a crash beginning at any moment relative to doing nothing, so 0.27 means the breaker prevents crashes rather than delaying them. The expected shortfall reduction is the cut to the worst tenth of crashes, and false halts are how often a rule stops a calm market.</p>
        <p><strong>The appraisal then asks three regulator&rsquo;s questions,</strong> containment, false halts and proportionality: only the market wide breaker passes all three. Hazard ratios on the battery: breaker 0.27, throttle 0.50, LULD band 0.61, kill switch 0.63, ladder 0.72, venue halt 0.80. No rule halted a quiet market.</p>
        <p>Rules are drawn from EU, UK and US style instruments, each carrying its human oversight class; the learned policy, a model based reinforcement learning supervisor solved by value iteration under declared halt and throttle costs, is advisory only.</p>
      </div>
      {figure(bars, bars_t, 'Containment and expected shortfall reduction by rule', 'Share of the dislocation removed, and the cut to the worst tenth of crashes, for eight intervention rules on the demonstration battery.', legend_bars)}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="net-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('N', 'NET')}<h2 id="net-h">Where the risk comes from</h2></div>
    </div>
    <div class="two">
      <div class="prose">
        <p><strong>Concentration.</strong> The share of agents on one model vendor is raised step by step at a fixed correlation and the crash measured each time. Below 30 per cent no run dislocates; from 30 per cent every run does, and the curve is convex (curvature 0.63), so each extra percentage point does more damage than the last. The concentration risk that the FSB and Bank of England reports describe gets a number.</p>
        <p><strong>Attribution.</strong> Shapley values share the crash among agent groups by silencing each combination and re running the same shock; in the strong herd, vendor A carries 0.106 of the drawdown and vendor B 0.013.</p>
        <p><strong>Learned herding.</strong> 48 reinforcement learning traders, trained separately on quiet markets by double Q learning, SARSA(&lambda;) and advantage actor critic, converge on the same strategy (0.74) without any shared signal: herding is learned, not imposed, and measured by policy convergence and the momentum slope.</p>
      </div>
      {figure(dose, dose_t, 'Drawdown as one vendor&rsquo;s share of agents rises', 'Dose response at correlation 0.85. The dislocation threshold, a drawdown above 0.10, is crossed at a 30 per cent share.')}
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="rsk-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('K', 'RSK')}<h2 id="rsk-h">Can the answer be gamed, and does it transfer?</h2></div>
    </div>
    <div class="cols">
      <div>
        <h3>The red team and the game</h3>
        <p>A bandit search for the evasion that hurts the certified tool most while the market still dislocates finds one that drives it to an F1 of 0.00, and the same holds for every other single sentinel. Treated as a game, in which the supervisor picks a tool and the adversary picks an evasion, a fixed choice loses outright, but drawing the armed sentinel at random from a mix (endogeneity 41 per cent, lead lag 30 per cent, volatility trigger 29 per cent) guarantees 0.16. Unpredictability is worth measurable detection.</p>
      </div>
      <div>
        <h3>Truth dependence</h3>
        <p>Regenerating the battery under four different herding mechanisms leaves tail dependence first every time, so the certification is not an artefact of one model of herding. Even so, the certified tool can be gamed, which is why certification is of the procedure, restated on every calibrated battery, and never of one tool for all time.</p>
      </div>
      <div>
        <h3>Off policy audit</h3>
        <p>From ten logged runs, an estimate of a rule&rsquo;s value built on the fitted model lands within 0.01 of the simulated truth; the doubly robust estimator is 0.16 off. A live pilot has only the log and could not tell the difference, which is the case for a generated market with a known truth.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="dat-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('D', 'DAT')}<h2 id="dat-h">What an authority&rsquo;s own data changes</h2></div>
    </div>
    <div class="cols cols--2">
      <div>
        <h3>Calibration shift</h3>
        <p>Refitting the simulator to an authority&rsquo;s data, its volatility, impact, who trades with whom and the vendor split observed from a vendor column or inferred from flows, and re running gives a rank correlation of 0.47 with the demonstration ranking, and a different winner. A certification must be re run on calibrated markets; the demonstration battery shows the method, not the answer.</p>
      </div>
      <div>
        <h3>Backtest</h3>
        <p>On a labelled real tape the volatility trigger alerts 18 steps before the marked episode but fires 3.5 times per 100 quiet steps; the absorption ratio finds all four labelled participants, 54 steps late. Timing and workload are measurable on real data; precision is not, because nobody knows who the innocent were.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="mth-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('M', 'MTH')}<h2 id="mth-h">Method</h2></div>
      <p class="lede">Synthetic markets with a known truth; sentinels that live over the stream and rules that act on it; an evaluation on the decision, and then an audit of the evaluation.</p>
    </div>
    <div class="cols block">
      <div>
        <h3>Synthetic markets with a known truth</h3>
        <p>Noise traders, fundamentalists, vendor clusters, reinforcement learning traders, distilled language model personas, manipulators and the templates an authority defines, under five generators. The truth is a property of how the market was made.</p>
      </div>
      <div>
        <h3>Sentinels live over the stream, rules act on it</h3>
        <p>Eight sentinels from the herding and risk literature and eight rules by jurisdiction, each reading only the flags as they stood at that step, so that no rule sees the future.</p>
      </div>
      <div>
        <h3>Evaluate on the decision, then audit the evaluation</h3>
        <p>A decision evaluator, a critic that re verifies every number, a red team, and a walk forward test of the certification procedure itself.</p>
      </div>
    </div>
    <div class="panel-ink">
      <div class="panel-ink__bar">{tag('A', 'AUT')}<span>Reinforcement learning and the science behind the metrics</span></div>
      <div class="panel-ink__body">
        <div>
          <p><strong>Reinforcement learning traders.</strong> 48 agents trained once on quiet markets by double Q learning, SARSA(&lambda;) and advantage actor critic, acting on discretised momentum and volatility; herding is learned, not imposed, and measured by policy convergence and the momentum slope.</p>
          <p><strong>Learned supervisor.</strong> Model based reinforcement learning: a tabular Markov decision process fitted from trajectories logged under an epsilon soft policy, solved by value iteration under declared halt and throttle costs. Advisory only.</p>
          <p><strong>Off policy evaluation.</strong> Per decision importance sampling, a clipped doubly robust estimator and the fitted model, each checked against the simulated truth. The red team is a UCB1 bandit, and the game is solved by linear programme.</p>
        </div>
        <div>
          <p><strong>Decision metrics.</strong> Precision, recall and F1 against the generator&rsquo;s truth; a 400 scenario bootstrap for intervals, evidence grades, the probability of inversion and winner stability; Kendall&rsquo;s tau turned into the gap (1 minus tau over 2).</p>
          <p><strong>Guarantee.</strong> A split conformal threshold on exchangeable quiet scenarios gives a finite sample bound on the false alert probability at level alpha.</p>
          <p><strong>Attribution and risk.</strong> Shapley values over agent groups under common random numbers; Kaplan Meier and ridge Cox hazards for time to dislocation; value at risk, expected shortfall and a generalised Pareto tail; sentinels from LSV imbalance, Hawkes branching, PCA absorption, Louvain communities and tail dependence.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="lim-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('L', 'LIM')}<h2 id="lim-h">Limits and risks</h2></div>
      <p class="lede">Every figure the Institute publishes carries an interval, an evidence grade and its limitations. These are the ones that matter most.</p>
    </div>
    <div class="rows">
      <div><h3>Simulation to reality</h3><p>The simulator is calibrated from an authority&rsquo;s data and hybrid markets are run on the observed path; the calibration shift (0.47, rank one not preserved) and the rankings are reported, never forecasts.</p></div>
      <div><h3>Goodharting and overreliance</h3><p>Held out scenario families, a truth dependence audit under four generators, walk forward regret of 0.27, and evidence grades and limitations on every figure.</p></div>
      <div><h3>Fabricated figures</h3><p>No generated figure reaches a supervisor: every number is computed from artefacts and recomputed by a critic; a model, when one is used, plans within hard bounds, and an injection suite of eleven cases must be contained on every run.</p></div>
      <div><h3>Data sensitivity</h3><p>The demonstration battery is synthetic. Observed data enters only through a quarantine, with size, type, formula and personal identifier checks and classification with no write down; a pilot would use delayed, pseudonymised venue data under the authority&rsquo;s own statutory powers.</p></div>
      <div><h3>Residual risk</h3><p>Even the certified tool can be gamed, so certification is of the procedure, restated on every calibrated battery, never of one tool for all time.</p></div>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="out-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('O', 'OUT')}<h2 id="out-h">Outputs</h2></div>
    </div>
    <ul class="pubs">
      <li>
        <span class="when">2026</span>
        <div>
          <div class="title">Reconstructing Systemic Risk: How Synthetic Network Generators Shape Banking Stress Tests</div>
          <div class="with">D. Godorozha, S. Inman Altass and N. Hashish</div>
          <div class="where">ACM International Conference on AI in Finance (ICAIF 2026), accepted</div>
        </div>
      </li>
      <li>
        <span class="when">2026</span>
        <div>
          <div class="title">An open benchmark of scenario families for agentic markets</div>
          <div class="with">The Institute</div>
          <div class="where">In preparation: eighteen families and their agent templates in a bounded declarative language, with calibration to historical episodes</div>
        </div>
      </li>
    </ul>
  </div>
</section>
'''


PROBATIO = f'''
<div class="page-head">
  <div class="wrap">
    <div class="head__row" style="margin-bottom:18px">{tag('P', 'PRB')}<span class="fcode" style="letter-spacing:.1em">Probatio</span></div>
    <h1>An agentic scenario lab for financial stability supervisors</h1>
    <p class="lede">Probatio is a decision first sandbox that stress tests AI market surveillance tools and intervention rules against synthetic AI agent markets, calibrated from an authority&rsquo;s own data and extended with its own scenarios and agents.</p>
  </div>
</div>

<section class="section" aria-labelledby="sep-h">
  <div class="wrap">
    <div class="two">
      <div class="prose">
        <h2 id="sep-h" style="margin-bottom:16px">A separate platform</h2>
        <p>Probatio is separate from the Institute, with its own governance{' and its own site' if PROBATIO_URL else ''}. The Institute&rsquo;s research informs the platform&rsquo;s method, and the Institute uses the platform to produce the evidence it publishes; it does not develop, licence or operate it, and it does not benefit from its sale.</p>
        <p>The description on this page is of the platform as the Institute uses it. Authorities wishing to run Probatio on their own infrastructure should approach the platform directly{f', at <a href="{PROBATIO_URL}" rel="noopener">{PROBATIO_URL}</a>' if PROBATIO_URL else ''}; the Institute is glad to make an introduction and to help design a battery.</p>
      </div>
      <div class="prose">
        <h2 style="margin-bottom:16px">What it does</h2>
        <p>It certifies tools on the decision that matters, with a conformal false alert guarantee, a winner stability figure and a walk forward test of the certification itself, and it shows that even the certified tool can be gamed. Every run passes two human gates, whose approver is checked against a register of regulated persons, and 31 critic checks; it leaves a signed, replayable ledger, a transparency record and an evidence pack, and answers the needs that the FSB, IOSCO, the Bank of England and the IMF have flagged.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="run-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('R', 'RUN')}<h2 id="run-h">How a run proceeds</h2></div>
      <p class="lede">Seven stages, two of them gates at which a named human can refuse.</p>
    </div>
    <ol class="steps">
      <li><b>Policy question</b>Read deterministically, or planned by a model within hard bounds.</li>
      <li><b>Plan</b>The battery is hashed: demonstration, question, own and calibrated families.</li>
      <li class="gate"><b>Gate 1</b>The approver, checked against the register, signs off the battery by hash or refuses with a recorded reason.</li>
      <li><b>Battery, rules, assurance</b>Sentinels, rules, guarantee, attribution, audits, red team, backtests.</li>
      <li><b>Critic</b>31 checks recompute every number from the raw rows and replay the ledger.</li>
      <li class="gate"><b>Gate 2</b>The approver releases the briefing, or refuses.</li>
      <li><b>Briefing and evidence pack</b>Graded, vetted and replayable, with the transparency record.</li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="gov-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('G', 'GOV')}<h2 id="gov-h">The controls</h2></div>
      <p class="lede">Governed like a supervisory system, not a research artefact.</p>
    </div>
    <div class="cols cols--2">
      <div>
        <h3>Human in the loop</h3>
        <p>Two mandatory gates: the approver signs off the battery by hash, then releases the briefing, or refuses with a recorded reason. The approver must be on the authority&rsquo;s register of regulated persons (an active senior management or certified function, matched by reference number and written into the ledger), must differ from the preparer, and can stop a run at any moment. Every rule carries its human oversight class; the learned policy is advisory only.</p>
      </div>
      <div>
        <h3>Auditability and traceability</h3>
        <p>An HMAC signed, hash chained ledger of every step, replayable by a third party; the battery, persona, agent and family definitions hashed and bound at Gate 1; 31 critic checks that recompute every number from the raw rows; an evidence pack with a manifest, a transparency record in the UK algorithmic transparency recording standard structure, and an exchange record.</p>
      </div>
      <div>
        <h3>Safety and governance</h3>
        <p>No generated figure reaches a supervisor: the critic vets every number in the briefing and the transparency record, and the model, when used, only plans within hard bounds, distils personas and phrases text. Conformal certification bounds false alerts; the autonomy gate defaults to no execution; an injection suite of eleven cases must be contained on every run; roles (viewer, preparer, approver, admin) gate every action.</p>
      </div>
      <div>
        <h3>Cyber risk</h3>
        <p>A security framework of seventeen controls that block release on a failure: keys from the environment only, security headers, request and rate limits, a SHA-256 manifest over every vendored asset, HTTPS and an egress allowlist for connectors and models, a quarantine for every dataset, classification with no write down, and identity from an authenticating proxy.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--well" aria-labelledby="front-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('T', 'TRM')}<h2 id="front-h">The terminal</h2></div>
      <p class="lede">Twelve pages, each reached by a three letter code or a key, with the command line that runs them.</p>
    </div>
    {front_panel(with_actions=False)}
  </div>
</section>
'''


PEOPLE_LIST = [
    ('daria-godorozha', 'D', 'LEAD', 'Daria Godorozha', 'Founder and Director',
     ['Daria is completing an MSc in Statistics by Research (Finance) at the London School of Economics, with a dissertation on construct validity in language model evaluation, and holds an LLM in international financial law from King&rsquo;s College London and an MSc in AI and Data Science.',
      'She co leads research teams at the Oxford Computational Political Science Group and ETH Zurich, carried out a Bank of England research project on whether banks that lobby are riskier, and has taken four hackathon prizes since 2024, including the CIUK Cluster Challenge as LSE team captain.']),
    ('prithika-narayanan', 'P', 'STAT', 'Prithika Narayanan', 'Statistics',
     ['Prithika is a statistician with an MSc in Statistics from LSE, after a triple major in mathematics, computer science and statistics at Christ University, Bangalore. As a Pathway Developer at Impact Advantage she builds social return on investment models and measurement frameworks.',
      'She won the 2026 LSE Postgraduate Statistics Practitioners&rsquo; Challenge with an SROI model of wage equality initiatives and has published on Bayesian optimisation with Springer Nature. With Daria she presented a taxonomy of geometric space for diffusion models at the Oxford Erlangen conference on the Mathematical Foundations of AI.']),
    ('sara-gabrielli-salis', 'S', 'LAW', 'Sara Gabrielli Salis', 'Law and policy',
     ['Sara is completing an LLM in public international law and human rights law at LSE, after an LLB in transnational law at the University of Luxembourg. She has drafted legal analysis and reports on draft laws in three Luxembourg ministries, at the Conseil d&rsquo;&Eacute;tat and in the European Parliament.',
      'She is Luxembourg&rsquo;s United Nations Youth Delegate, after two years as its Youth Delegate to the EU, and represented the United Kingdom at the UN Commission on the Status of Women in 2026. With Daria she co leads a research project at the Oxford Computational Political Science Group.']),
    ('rajib-ahmed', 'R', 'ML', 'Rajib Ahmed', 'Machine learning',
     ['Rajib is a statistician at the Department for Business, Innovation, Science and Trade, on a Government Statistical Service placement, and a final year medical student at Cardiff University with an MSc in Health Data Science from LSE.',
      'At Oxford&rsquo;s Radcliffe Department of Medicine he has spent three years building machine learning models for cardiac MRI, and in 2020 he built an agent based model of COVID-19 spread as a Nuffield Future Researcher. He is a Research Associate at the Oxford Computational Political Science Group and completed the Principles of Intelligence Iliad intensive on AI safety in 2026.']),
]


def people_page():
    cards = []
    for slug, letter, code, name, role, paras in PEOPLE_LIST:
        ps = '\n'.join(f'        <p>{p}</p>' for p in paras)
        cards.append(f'''      <article class="person">
        <div class="person__photo"><img src="img/people/{slug}.jpg" alt="{name}" width="422" height="422" loading="lazy"></div>
        <div>
          <div class="person__name"><h3>{name}</h3>{tag(letter, code)}</div>
          <div class="person__role">{role}</div>
{ps}
        </div>
      </article>''')
    return f'''
<div class="page-head">
  <div class="wrap">
    <h1>People</h1>
    <p class="lede">Statisticians, a lawyer and a machine learning researcher, who have built and audited the method together since the first concept note.</p>
  </div>
</div>
<section class="section" aria-label="The people of the Institute">
  <div class="wrap">
    <div class="people">
{chr(10).join(cards)}
    </div>
  </div>
</section>
'''


ABOUT = f'''
<div class="page-head">
  <div class="wrap">
    <h1>About the Institute</h1>
    <p class="lede">An independent, non-profit research institute for artificial intelligence, financial risk and stability, constituted in the United States and based in {CITY}.</p>
  </div>
</div>

<section class="section" aria-labelledby="mission-h">
  <div class="wrap">
    <div class="two">
      <div class="prose">
        <h2 id="mission-h" style="margin-bottom:16px">Mission</h2>
        <p>Artificial intelligence is changing who trades, how they react and how quickly a routine shock can become a dislocation. The authorities responsible for financial stability are building surveillance tools and intervention rules for that market, and need a way to know which of them to trust before an episode, not after.</p>
        <p>The Institute exists to produce that evidence: to validate tools and rules on the supervisory decisions they inform, with guarantees where guarantees are possible, with every number computed and recomputed, and with a trail a third party can replay. Its work is published for any authority to use.</p>
      </div>
      <div class="prose">
        <h2 style="margin-bottom:16px">What we do</h2>
        <h3 style="margin-top:0">Research</h3>
        <p>Decision first certification, agentic markets and herding, intervention rules, and the governance of generated evidence. The programme is set out under <a href="research.html">Research</a>.</p>
        <h3>Evidence for supervisors</h3>
        <p>Calibrated batteries run with authorities on their own data, read with them, and reported with intervals, evidence grades and limitations.</p>
        <h3>Open methods</h3>
        <p>An open benchmark of scenario families and agent templates, so that results can be compared against the same truth and reproduced.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="princ-h">
  <div class="wrap">
    <div class="head">
      <div class="head__row">{tag('P', 'PRN')}<h2 id="princ-h">Principles</h2></div>
    </div>
    <div class="rows">
      <div><h3>Decide on the decision</h3><p>A tool is judged by whether it identifies the destabilising agents and the moment to act, not by how well a synthetic market resembles a real one.</p></div>
      <div><h3>Compute, never generate</h3><p>No figure reaches a reader that was not computed from artefacts and recomputed by an independent check. A language model, when one is used, plans within hard bounds and phrases text; it does not produce numbers.</p></div>
      <div><h3>Guarantee what can be guaranteed</h3><p>Where a finite sample bound exists, as for the false alert rate under a conformal threshold, it is stated; where it does not, an interval and an evidence grade are.</p></div>
      <div><h3>Keep a human at the gate</h3><p>Named people, checked against a register and distinct from the preparer, approve a battery and release a briefing, and can refuse or stop at any moment.</p></div>
      <div><h3>Leave a trail</h3><p>Every step is written to a signed, hash chained ledger that a third party can replay; every battery and every definition it used is hashed and bound before it runs.</p></div>
      <div><h3>Say what it cannot show</h3><p>Limitations are reported beside results: the calibration shift on an authority&rsquo;s data, the regret of the certification procedure, the evasions a red team found.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="struct-h">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3 id="struct-h">Structure</h3>
        <p>The Institute is a 501(c)(3) non-profit organisation based in {CITY}. It is led by its founder and director, <a href="people.html">Daria Godorozha</a>, with a research team in statistics, law and machine learning.</p>
      </div>
      <div>
        <h3>Independence</h3>
        <p>The Institute is separate from <a href="probatio.html">Probatio</a>, the platform that implements its method. It does not develop, licence or operate the platform, and it publishes what the evidence shows about any tool or rule, including the certified ones.</p>
      </div>
      <div>
        <h3>Funding</h3>
        <p>The Institute is funded by gifts and grants. It does not accept funding on terms that would restrict what it publishes, and it names its supporters. See <a href="support.html">Support</a>.</p>
      </div>
    </div>
  </div>
</section>
'''


SUPPORT = f'''
<div class="page-head">
  <div class="wrap">
    <h1>Support the Institute</h1>
    <p class="lede">Independent evidence about AI in markets needs independent support. There are three ways to give it.</p>
  </div>
</div>

<section class="section" aria-label="Ways to support">
  <div class="wrap">
    <div class="ways">
      <article>
        {tag('G', 'GIV')}
        <h3>Give</h3>
        <p>Gifts and grants fund the open benchmark, independent audits of the certification procedure and the researchers&rsquo; time. The Institute is a 501(c)(3) non-profit organisation, so gifts from United States taxpayers are deductible to the extent the law allows.</p>
        <a class="btn btn--amber" href="mailto:{EMAIL}?subject=Giving%20to%20the%20Institute">Write to us about a gift</a>
      </article>
      <article>
        {tag('P', 'PRT')}
        <h3>Partner</h3>
        <p>Central banks and market regulators can run a pilot on their own data and their own scenarios, on their own infrastructure. The Institute helps design the battery, reads the evidence with the authority and reports it with its intervals, grades and limitations.</p>
        <a class="btn btn--ghost" href="mailto:{EMAIL}?subject=A%20pilot%20with%20the%20Institute">Propose a pilot</a>
      </article>
      <article>
        {tag('C', 'CLB')}
        <h3>Collaborate</h3>
        <p>Researchers in statistics, market microstructure, reinforcement learning and financial regulation are welcome to work with the Institute on the benchmark, on new scenario families and on the certification procedure itself.</p>
        <a class="btn btn--ghost" href="mailto:{EMAIL}?subject=Research%20collaboration">Get in touch</a>
      </article>
    </div>
  </div>
</section>

<section class="section section--panel" aria-labelledby="contact-h">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3 id="contact-h">Contact</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a><br>{CITY}</p>
      </div>
      <div>
        <h3>Press</h3>
        <p>Journalists may write to the same address. The Institute&rsquo;s people speak to the evidence they have published and to the method, and will say when a question lies outside it.</p>
      </div>
      <div>
        <h3>The platform</h3>
        <p>Questions about running Probatio belong with the platform, which is separate from the Institute. The Institute is glad to make an introduction.</p>
      </div>
    </div>
  </div>
</section>
'''


NOT_FOUND = f'''
<div class="page-head">
  <div class="wrap">
    <div class="head__row" style="margin-bottom:18px"><span class="tag"><b>4</b><span>404</span></span></div>
    <h1>There is no page at this address.</h1>
    <p class="lede">The page may have moved, or the address may have been mistyped. The site&rsquo;s pages are listed below.</p>
  </div>
</div>
<section class="section">
  <div class="wrap">
    <div class="hero__actions">
      <a class="btn btn--amber" href="{BASE}index.html">Front page</a>
      <a class="btn btn--ghost" href="{BASE}research.html">Research</a>
      <a class="btn btn--ghost" href="{BASE}probatio.html">Probatio</a>
      <a class="btn btn--ghost" href="{BASE}people.html">People</a>
      <a class="btn btn--ghost" href="{BASE}about.html">About</a>
      <a class="btn btn--ghost" href="{BASE}support.html">Support</a>
    </div>
  </div>
</section>
'''


PAGES = [
    ('index.html', 'Home', 'An independent, non-profit research institute studying how artificial intelligence changes financial risk, and how supervisors can validate the tools and rules meant to contain it.', INDEX, True),
    ('research.html', 'Research', 'Decision first certification of surveillance tools, agentic markets and herding, intervention rules, and the governance of generated evidence.', research_page(), False),
    ('probatio.html', 'Probatio', 'Probatio, an agentic scenario lab for financial stability supervisors, is a separate platform that implements the Institute’s method.', PROBATIO, False),
    ('people.html', 'People', 'The people of the Institute for AI, Financial Risk and Stability.', people_page(), False),
    ('about.html', 'About', 'Mission, principles, structure and funding of the Institute for AI, Financial Risk and Stability.', ABOUT, False),
    ('support.html', 'Support', 'Give, partner on a pilot or collaborate with the Institute for AI, Financial Risk and Stability.', SUPPORT, False),
    ('404.html', 'Page not found', 'There is no page at this address.', NOT_FOUND, False),
]

if __name__ == '__main__':
    for path, title, desc, body, home in PAGES:
        html = shell(path, title, desc, body, home)
        with open(os.path.join(ROOT, path), 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', path, len(html), 'characters')
