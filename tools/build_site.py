#!/usr/bin/env python3
"""Render the Korean reading site from the Markdown manuscripts in text/."""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs"
COVERS = "https://ny83427.github.io/jing/img"
CONTENTS = json.loads((ROOT / "tools/contents.json").read_text(encoding="utf-8"))
CHAPTERS = CONTENTS["chapters"]

def page(title, body):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | 경(景)</title>
<link rel="stylesheet" href="style.css">
<script src="reader.js" defer></script>
</head>
<body>
<header class="bar">
<a class="brand" href="index.html">경 <span>景</span></a>
<nav aria-label="읽기 설정"><a href="index.html#contents">목차</a>
<button id="theme" aria-label="야간 모드" aria-pressed="false">◐</button>
<button data-size="-1" aria-label="글자 작게">가−</button>
<button data-size="1" aria-label="글자 크게">가+</button></nav>
</header>
{body}
</body>
</html>
"""

def write(name, title, body):
    (OUTPUT / name).write_text(page(title, body), encoding="utf-8")

def title_link(chapter, available):
    title = html.escape(chapter["title"])
    number = chapter["id"]
    if number in available:
        return f'<a href="{number}.html">{title}</a>'
    return f'<span class="pending">{title} <small>번역 준비 중</small></span>'

def rows(chapters, available):
    return "".join(f"<li>{title_link(chapter, available)}</li>" for chapter in chapters)

def render_index(available):
    sections = []
    for number, name in enumerate(CONTENTS["volumes"], 1):
        if number in (1, 7, 10):
            part = (1, 7, 10).index(number) + 1
            sections.append(f'<h3 id="p{part}">제{part}부　{CONTENTS["parts"][part - 1]}</h3>')
        entries = [chapter for chapter in CHAPTERS if chapter["volume"] == number]
        sections.append(f"<details><summary>제{number}권　{name}</summary>"
                        f"<ol>{rows(entries, available)}</ol></details>")
    covers = "".join(f'<a href="#p{i}"><img src="{COVERS}/Vol{i}.jpg" '
                     f'alt="제{i}부 표지" loading="lazy"><span>제{i}부　{name}</span></a>'
                     for i, name in enumerate(CONTENTS["parts"], 1))
    count = sum(chapter["id"] in available for chapter in CHAPTERS if chapter["volume"])
    write("index.html", "한국어판", f"""
<main class="home">
<section class="hero">
<img class="cover" src="{COVERS}/Main.jpg" alt="원작 《경》의 중국어판 표지">
<div><h1>경 <span>景</span></h1>
<p class="author">라오톄(老铁) · Claude</p>
<p>명나라 때 서안성 밖에서 당나라 비석이 나왔다. 비석 밑에는 모래가 깔려 있었고, 위에는 삭은 털깔개가 덮여 있었다. 누군가 깨진 받침돌까지 맞춰 놓고 비석을 조심스레 땅에 뉘었다.</p>
<p>비문 뒤에는 세 세대의 이야기가 있다. 곽자의의 길을 살피던 이사, 경전을 번역하고 비를 세운 경정, 그리고 그들이 남긴 믿음을 품고 장안을 떠난 사람들.</p>
<p class="edition">한국어판 · 본편 {count} / 85장 공개</p>
<div class="actions"><a class="primary" href="000.html">서장 읽기</a> <a id="resume" hidden>이어서 읽기</a></div>
</div>
</section>
<section class="volumes" aria-label="부별 표지">{covers}</section>
<section id="contents"><h2>목차</h2>
<ul class="standalone">{rows(CHAPTERS[:1], available)}</ul>
{"".join(sections)}
<ul class="standalone">{rows(CHAPTERS[-2:], available)}</ul></section>
<footer><a href="https://ny83427.github.io/jing/" lang="zh-CN">中文版</a></footer>
</main>
""")

def render_chapter(chapter, source, index):
    number = chapter["id"]
    title = html.escape(chapter["title"])
    lines = source.read_text(encoding="utf-8").splitlines()
    while lines and (not lines[0].strip() or re.match(r"^#{1,3} ", lines[0])):
        lines.pop(0)
    body = "\n".join(lines)
    body = re.sub(r"\n---\s*\n\s*\*\*중국어 원고 판본\*\*[^\n]*\s*$", "", body)
    body = markdown.markdown(body, extensions=["extra", "sane_lists"])
    previous = CHAPTERS[index - 1] if index else None
    following = CHAPTERS[index + 1] if index + 1 < len(CHAPTERS) else None

    def nav_link(item, label):
        if item and item["id"] in available:
            return f'<a href="{item["id"]}.html">{label}</a>'
        return ""

    part = chapter["volume"]
    section = f'<p class="edition">제{part}권　{CONTENTS["volumes"][part - 1]}</p>' if part else ""
    write(f"{number}.html", chapter["title"], f"""
<main class="reader">
<article data-chapter="{number}" data-title="{title}">
<header>{section}<h1>{title}</h1></header>
{body}
</article>
<nav class="chapter-nav" aria-label="장 이동">
{nav_link(previous, '이전 장')}<a href="index.html#contents">목차</a>{nav_link(following, '다음 장')}
</nav>
</main>
""")

if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / ".nojekyll").touch()
    available = {}
    for source in sorted((ROOT / "text").glob("*.md")):
        number = source.name.split("-", 1)[0]
        if number in available:
            raise ValueError(f"Duplicate manuscript number: {number}")
        available[number] = source
    render_index(available)
    for index, chapter in enumerate(CHAPTERS):
        number = chapter["id"]
        if number in available:
            render_chapter(chapter, available[number], index)
