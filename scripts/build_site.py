#!/usr/bin/env python3
"""Build index.html from README.md while preserving the site shell and styling."""

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUTPUT = ROOT / "index.html"


def inline_markdown(text: str) -> str:
    """Render a small, safe subset of Markdown inline syntax."""
    rendered = escape(text, quote=False)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", rendered)
    rendered = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        r'<a href="\2">\1</a>',
        rendered,
    )
    return rendered


def render_markdown(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    title = "raven6941.github.io"
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            blocks.append("<ul>" + "".join(f"<li>{item}</li>" for item in list_items) + "</ul>")
            list_items.clear()

    for line in lines:
        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            heading_text = heading.group(2)
            if level == 1:
                title = re.sub(r"[`*_]", "", heading_text)
            blocks.append(f"<h{level}>{inline_markdown(heading_text)}</h{level}>")
            continue

        item = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if item:
            flush_paragraph()
            list_items.append(inline_markdown(item.group(1)))
            continue

        flush_list()
        paragraph.append(line.strip())

    flush_paragraph()
    flush_list()
    return title, "\n      ".join(blocks)


def main() -> None:
    title, content = render_markdown(README.read_text(encoding="utf-8"))
    safe_title = escape(title)
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(title)} — GitHub Pages site.">
  <!-- Replace the content value with the verification token provided by Google Search Console. -->
  <meta name="google-site-verification" content="REPLACE_WITH_GOOGLE_SEARCH_CONSOLE_TOKEN">
  <title>{safe_title}</title>
  <style>
    :root {{ color-scheme: light; --ink: #172326; --muted: #596a69; --accent: #176b61; --paper: #f4f6f1; --panel: #fffefa; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; padding: 2rem; display: grid; place-items: center; background: radial-gradient(ellipse at 12% 10%, #dce9dc 0, transparent 34rem), var(--paper); color: var(--ink); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width: min(100%, 760px); overflow: hidden; border: 1px solid #dce3dc; border-radius: 24px; background: var(--panel); box-shadow: 0 24px 70px rgb(28 50 43 / 9%); }}
    .accent {{ height: 8px; background: linear-gradient(90deg, #176b61, #9dbb83); }}
    .content {{ padding: clamp(2rem, 7vw, 4.5rem); }}
    .eyebrow {{ margin: 0 0 1rem; color: var(--accent); font-size: .76rem; font-weight: 750; letter-spacing: .14em; text-transform: uppercase; }}
    h1 {{ margin: 0; font-size: clamp(2.3rem, 8vw, 4.5rem); line-height: 1.02; letter-spacing: -.055em; overflow-wrap: anywhere; }}
    .readme-content {{ margin-top: 1.5rem; color: var(--muted); font-size: 1.1rem; line-height: 1.75; }}
    .readme-content h1 {{ display: none; }}
    .readme-content h2, .readme-content h3 {{ margin: 2rem 0 .6rem; color: var(--ink); line-height: 1.25; }}
    .readme-content p {{ margin: .8rem 0; }}
    .readme-content ul {{ padding-left: 1.4rem; }}
    .readme-content a {{ color: var(--accent); text-underline-offset: 3px; }}
    .readme-content code {{ padding: .12em .35em; border-radius: .35em; background: #edf1e9; font-size: .9em; }}
    .rule {{ height: 1px; margin: 2.5rem 0 1.4rem; background: #e3e8e1; }}
    footer {{ color: var(--muted); font-size: .9rem; }}
    footer a {{ color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    footer a:hover {{ text-decoration-thickness: 2px; }}
    @media (max-width: 480px) {{ body {{ padding: 1rem; }} main {{ border-radius: 18px; }} }}
  </style>
</head>
<body>
  <main>
    <div class="accent" aria-hidden="true"></div>
    <div class="content">
      <p class="eyebrow">GitHub Pages</p>
      <h1>{safe_title}</h1>
      <section class="readme-content" aria-label="README content">
      {content}
      </section>
      <div class="rule" aria-hidden="true"></div>
      <footer>Project source: <a href="https://github.com/raven6941/raven6941.github.io">GitHub</a></footer>
    </div>
  </main>
</body>
</html>
'''
    OUTPUT.write_text(page, encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(ROOT)} from {README.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
