# -*- coding: utf-8 -*-
"""Build a single self-contained HTML deck from deck_content.py.

Figures are inlined as base64 data URIs so the .html file is fully portable:
open it, press F for fullscreen, advance with the arrow keys, and screen-record.
"""
import base64
import html
import os
import re

from deck_content import SLIDES, REFERENCES, TITLE, SUBTITLE, PRESENTER, COURSE, DATE

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "Clayton_spce_5065_vacuum_environment_deck.html")


def data_uri(fname):
    with open(os.path.join(FIGDIR, fname), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def data_uri_path(relpath):
    """Inline any image given a path relative to the presentation dir."""
    full = os.path.join(HERE, relpath)
    ext = os.path.splitext(full)[1].lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    with open(full, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def cite(text):
    """Escape, then style [n] citation markers."""
    esc = html.escape(text)
    return re.sub(r"\[(\d+)\]", r'<sup class="cite">[\1]</sup>', esc)


def render_slide(i, s):
    n = len(SLIDES)
    kind = s["kind"]
    counter = "" if kind == "title" else f'<div class="counter">{i + 1} / {n}</div>'

    if kind == "title":
        hero = ""
        if s.get("hero"):
            credit = (f'<div class="hero-credit">{html.escape(s["credit"])}</div>'
                      if s.get("credit") else "")
            hero = (f'<div class="hero" style="background-image:'
                    f'linear-gradient(90deg, rgba(13,13,13,0.96) 30%, rgba(13,13,13,0.55) 100%),'
                    f'url({data_uri_path(s["hero"])})"></div>{credit}')
        body = f"""
          {hero}
          <div class="title-slide">
            <div class="kicker">{html.escape(COURSE)} &nbsp;&middot;&nbsp; Current-Event Presentation</div>
            <h1>{html.escape(s['title'])}</h1>
            <p class="subtitle">{html.escape(s['subtitle'])}</p>
            <p class="meta">{html.escape(s['meta'])}</p>
          </div>"""

    elif kind == "references":
        items = "".join(
            f'<li><span class="refnum">[{k + 1}]</span> {html.escape(r)}</li>'
            for k, r in enumerate(REFERENCES)
        )
        body = f"""
          <h2>{html.escape(s['title'])}</h2>
          <ol class="refs">{items}</ol>"""

    elif kind == "figure":
        bullets = "".join(f"<li>{cite(b)}</li>" for b in s["bullets"])
        img = data_uri(s["figure"])
        body = f"""
          <h2>{html.escape(s['title'])}</h2>
          <div class="split">
            <ul class="bullets">{bullets}</ul>
            <div class="figwrap"><img src="{img}" alt="{html.escape(s['title'])}"></div>
          </div>"""

    elif kind == "bullets" and s.get("image"):
        bullets = "".join(f"<li>{cite(b)}</li>" for b in s["bullets"])
        credit = (f'<div class="credit">{html.escape(s["credit"])}</div>'
                  if s.get("credit") else "")
        img = data_uri_path(s["image"])
        body = f"""
          <h2>{html.escape(s['title'])}</h2>
          <div class="split">
            <ul class="bullets">{bullets}</ul>
            <div class="figwrap photo">
              <img src="{img}" alt="{html.escape(s['title'])}">
              {credit}
            </div>
          </div>"""

    else:  # bullets, text only
        bullets = "".join(f"<li>{cite(b)}</li>" for b in s["bullets"])
        body = f"""
          <h2>{html.escape(s['title'])}</h2>
          <ul class="bullets big">{bullets}</ul>"""

    return f'<section class="slide" data-idx="{i}">{body}{counter}</section>'


slides_html = "\n".join(render_slide(i, s) for i, s in enumerate(SLIDES))

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)}</title>
<style>
  :root {{
    --bg: #0d0d0d;
    --surface: #1a1a19;
    --ink: #ffffff;
    --ink2: #c3c2b7;
    --muted: #898781;
    --accent: #3987e5;
    --accent-l: #86b6ef;
    --amber: #fab219;
    --line: #2c2c2a;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ height: 100%; }}
  body {{
    background: var(--bg);
    color: var(--ink);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    overflow: hidden;
  }}
  .deck {{ position: fixed; inset: 0; }}
  .slide {{
    position: absolute; inset: 0;
    display: none;
    flex-direction: column;
    justify-content: center;
    padding: 5.5vh 7vw;
    background: radial-gradient(120% 120% at 15% 0%, #17171a 0%, var(--bg) 60%);
  }}
  .slide.active {{ display: flex; }}
  h1 {{ font-size: 5.2vw; line-height: 1.05; font-weight: 800; letter-spacing: -0.01em; }}
  h2 {{
    font-size: 3.2vw; font-weight: 750; letter-spacing: -0.01em;
    margin-bottom: 3vh; color: var(--ink);
    border-left: 6px solid var(--accent); padding-left: 1.1vw;
  }}
  .kicker {{
    text-transform: uppercase; letter-spacing: 0.18em;
    color: var(--accent-l); font-size: 1.15vw; font-weight: 700; margin-bottom: 2.4vh;
  }}
  .title-slide {{ max-width: 80%; }}
  .subtitle {{ font-size: 2.4vw; color: var(--ink2); margin-top: 2.4vh; font-weight: 400; }}
  .meta {{ font-size: 1.5vw; color: var(--muted); margin-top: 6vh; letter-spacing: 0.02em; }}
  ul.bullets {{ list-style: none; }}
  ul.bullets li {{
    position: relative; padding-left: 2.2vw; margin-bottom: 2.6vh;
    font-size: 1.9vw; line-height: 1.4; color: var(--ink2); max-width: 62ch;
  }}
  ul.bullets.big li {{ font-size: 2.15vw; margin-bottom: 3.2vh; }}
  ul.bullets li::before {{
    content: ""; position: absolute; left: 0; top: 0.62em;
    width: 0.9vw; height: 0.9vw; background: var(--accent);
    border-radius: 2px; transform: rotate(45deg);
  }}
  .split {{ display: flex; gap: 3vw; align-items: center; }}
  .split .bullets {{ flex: 1 1 46%; }}
  .split .figwrap {{ flex: 1 1 54%; }}
  .figwrap img {{
    width: 100%; height: auto; border-radius: 10px;
    border: 1px solid var(--line); box-shadow: 0 10px 40px rgba(0,0,0,0.5);
  }}
  .figwrap.photo img {{ max-height: 66vh; object-fit: cover; }}
  .credit {{
    color: var(--muted); font-size: 1.0vw; margin-top: 0.8vh;
    font-style: italic;
  }}
  .hero {{
    position: absolute; inset: 0; z-index: 0;
    background-size: cover; background-position: center right;
  }}
  .hero-credit {{
    position: absolute; bottom: 2.2vh; right: 3vw; z-index: 2;
    color: var(--muted); font-size: 0.95vw; font-style: italic;
  }}
  .title-slide {{ position: relative; z-index: 1; }}
  .cite {{ color: var(--accent-l); font-size: 0.62em; font-weight: 700; }}
  ol.refs {{ list-style: none; counter-reset: none; }}
  ol.refs li {{
    font-size: 1.28vw; line-height: 1.42; color: var(--ink2);
    margin-bottom: 1.5vh; padding-left: 3vw; text-indent: -3vw;
    max-width: 90ch; word-break: break-word;
  }}
  .refnum {{ color: var(--accent-l); font-weight: 700; margin-right: 0.4vw; }}
  .counter {{
    position: absolute; bottom: 3vh; right: 3vw;
    color: var(--muted); font-size: 1.1vw; font-variant-numeric: tabular-nums;
  }}
  .progress {{
    position: fixed; left: 0; bottom: 0; height: 4px;
    background: var(--accent); width: 0%; transition: width 0.25s ease; z-index: 10;
  }}
  .hint {{
    position: fixed; bottom: 3vh; left: 3vw; color: var(--muted);
    font-size: 1.0vw; opacity: 0.8;
  }}
</style>
</head>
<body>
  <div class="deck">
    {slides_html}
  </div>
  <div class="progress" id="progress"></div>
  <div class="hint">Arrow keys or space to navigate &middot; F for fullscreen</div>
<script>
  const slides = Array.from(document.querySelectorAll('.slide'));
  const progress = document.getElementById('progress');
  let idx = 0;
  function show(i) {{
    idx = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle('active', k === idx));
    progress.style.width = ((idx + 1) / slides.length * 100) + '%';
  }}
  function next() {{ show(idx + 1); }}
  function prev() {{ show(idx - 1); }}
  document.addEventListener('keydown', (e) => {{
    if (['ArrowRight', ' ', 'PageDown', 'ArrowDown'].includes(e.key)) {{ e.preventDefault(); next(); }}
    else if (['ArrowLeft', 'PageUp', 'ArrowUp'].includes(e.key)) {{ e.preventDefault(); prev(); }}
    else if (e.key === 'Home') {{ show(0); }}
    else if (e.key === 'End') {{ show(slides.length - 1); }}
    else if (e.key === 'f' || e.key === 'F') {{
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }}
  }});
  document.addEventListener('click', (e) => {{
    // click right half advances, left half goes back
    if (e.clientX > window.innerWidth * 0.35) next(); else prev();
  }});
  show(0);
</script>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT)
