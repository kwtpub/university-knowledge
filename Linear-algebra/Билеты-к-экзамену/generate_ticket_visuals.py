#!/usr/bin/env python3
from __future__ import annotations

import glob
import os
import re
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path('.')
VIS_DIR = ROOT / 'visuals'
VIS_DIR.mkdir(exist_ok=True)


def extract_ticket_number(path: Path) -> int:
    m = re.search(r"(\d+)", path.stem)
    if not m:
        raise ValueError(f"Cannot parse ticket number: {path}")
    return int(m.group(1))


def first_heading(lines: list[str]) -> str:
    for line in lines:
        if line.startswith('#'):
            return line.lstrip('#').strip()
    return 'Ticket'


def extract_subheadings(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        if line.startswith('## '):
            out.append(line[3:].strip())
    return out


def extract_terms(lines: list[str]) -> list[str]:
    terms: list[str] = []
    for line in lines:
        line = line.strip()
        if not line.startswith('**'):
            continue

        # Match **term** -- ... OR **term**: ...
        m = re.match(r"\*\*(.+?)\*\*\s*[—:-]?\s*(.*)$", line)
        if not m:
            continue
        term = m.group(1).strip()
        desc = m.group(2).strip()

        if desc:
            clean = f"{term}: {desc}"
        else:
            clean = term

        clean = re.sub(r"\$+", "", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean and clean not in terms:
            terms.append(clean)

        if len(terms) >= 8:
            break
    return terms


def extract_formulas(lines: list[str]) -> list[str]:
    formulas: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('#') or s.startswith('- ') or s.startswith('|'):
            continue
        if s.startswith('**') and s.endswith('**'):
            continue
        if any(tok in s for tok in ['=', '⇔', '→', 'det', 'rank', 'dim', 'cos', 'sin', 'proj', 'Ker', 'Im']):
            cleaned = re.sub(r"\$+", "", s)
            cleaned = re.sub(r"\\[A-Za-z]+", "", cleaned)
            cleaned = re.sub(r"\{[^}]*\}", "", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned and cleaned not in formulas:
                formulas.append(cleaned)
        if len(formulas) >= 6:
            break
    return formulas


def infer_application_text(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ['гаусс', 'крамер', 'слау', 'кронекера', 'капелли']):
        return 'Pipeline: set up system -> transform matrix -> classify solutions.'
    if any(k in t for k in ['собствен', 'характерист', 'диагонализ']):
        return 'Pipeline: build characteristic equation -> find eigenvalues -> eigenvectors.'
    if any(k in t for k in ['грам', 'шмидт', 'ортогон', 'парсевал']):
        return 'Pipeline: project vectors -> orthogonalize basis -> compute coordinates.'
    if any(k in t for k in ['плоск', 'прямая', 'угол', 'расстояни', 'координат']):
        return 'Geometry workflow: vector form <-> equation form <-> angle/distance formulas.'
    if any(k in t for k in ['эллипс', 'гипербол', 'парабол', 'кривая', 'поверхност', 'цилиндр']):
        return 'Conic/quadric workflow: canonical equation -> parameters -> geometric interpretation.'
    if any(k in t for k in ['форма', 'билинейн', 'квадратич', 'сильвестр']):
        return 'Forms workflow: matrix representation -> basis change -> definiteness criteria.'
    return 'Core workflow: definitions -> theorem/criterion -> algorithm -> interpretation.'


def wrap_text(s: str, width: int = 52) -> str:
    return textwrap.fill(s, width=width)


def draw_card(ticket_no: int, title: str, subheads: list[str], terms: list[str], formulas: list[str], app_text: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 8), dpi=160)

    # Soft gradient background
    bg = np.linspace(0, 1, 256)
    bg = np.vstack([bg] * 256)
    ax.imshow(bg, extent=[0, 100, 0, 100], origin='lower', cmap='Blues', alpha=0.12, aspect='auto')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(
        4,
        95,
        f"Ticket {ticket_no:02d}: {title}",
        fontsize=18,
        fontweight='bold',
        color='#0f172a',
        va='top',
    )

    # Helper to draw a rounded box
    def box(x: float, y: float, w: float, h: float, title_txt: str, body_txt: str, fc: str) -> None:
        p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.8,rounding_size=3.2', linewidth=1.3, edgecolor='#1e293b', facecolor=fc)
        ax.add_patch(p)
        ax.text(x + 1.8, y + h - 3.2, title_txt, fontsize=12.5, fontweight='bold', color='#0b2545', va='top')
        ax.text(x + 1.8, y + h - 8.0, body_txt, fontsize=10.6, color='#111827', va='top')

    # Content extraction for sections
    sub_txt = '\n'.join(f"- {s}" for s in subheads[:4]) if subheads else '- Main section(s) not found'
    term_txt = '\n'.join(f"- {wrap_text(t, 46)}" for t in terms[:4]) if terms else '- Key terms not detected'
    formula_txt = '\n'.join(f"- {wrap_text(f, 46)}" for f in formulas[:3]) if formulas else '- Formula line not detected'
    app_txt = wrap_text(app_text, 54)

    box(4, 54, 43, 36, '1) Sections', sub_txt, '#eef6ff')
    box(53, 54, 43, 36, '2) Key Concepts', term_txt, '#f2fbf3')
    box(4, 8, 43, 38, '3) Core Formula/Criterion', formula_txt, '#fff8e8')
    box(53, 8, 43, 38, '4) Visual Learning Path', app_txt, '#fef2f2')

    # Arrows for flow
    arrows = [
        ((47.5, 72), (53, 72)),
        ((25.5, 54), (25.5, 46)),
        ((74.5, 54), (74.5, 46)),
        ((47, 27), (53, 27)),
    ]
    for (x1, y1), (x2, y2) in arrows:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=16, linewidth=1.2, color='#334155'))

    ax.text(4, 2.5, 'Auto-generated visual summary for exam revision', fontsize=9.8, color='#475569')

    fig.tight_layout(pad=0.6)
    fig.savefig(out_path, bbox_inches='tight')
    plt.close(fig)


def inject_image_reference(md_path: Path, image_rel: str, ticket_no: int) -> bool:
    text = md_path.read_text(encoding='utf-8')
    marker_title = '## Наглядное представление'
    marker_img = f'![Наглядная схема билета {ticket_no:02d}]({image_rel})'

    if marker_img in text:
        return False

    block = f"\n\n{marker_title}\n\n{marker_img}\n"

    if marker_title in text:
        # Replace existing visual block image line if section already exists
        lines = text.splitlines()
        out: list[str] = []
        i = 0
        replaced = False
        while i < len(lines):
            line = lines[i]
            out.append(line)
            if line.strip() == marker_title:
                j = i + 1
                # Skip blank lines
                while j < len(lines) and not lines[j].strip():
                    out.append(lines[j])
                    j += 1
                # Replace first image markdown if present
                if j < len(lines) and lines[j].strip().startswith('!['):
                    out.append(marker_img)
                    replaced = True
                    i = j + 1
                    continue
            i += 1
        if replaced:
            md_path.write_text('\n'.join(out) + ('\n' if text.endswith('\n') else ''), encoding='utf-8')
            return True

    md_path.write_text(text.rstrip() + block + '\n', encoding='utf-8')
    return True


def main() -> None:
    files = sorted(Path('.').glob('Билет-*.md'), key=extract_ticket_number)
    generated = 0
    updated = 0

    for md in files:
        no = extract_ticket_number(md)
        raw = md.read_text(encoding='utf-8')
        lines = raw.splitlines()

        title = first_heading(lines)
        subheads = extract_subheadings(lines)
        terms = extract_terms(lines)
        formulas = extract_formulas(lines)
        app = infer_application_text(raw)

        out_name = f'bilet-{no:02d}.png'
        out_path = VIS_DIR / out_name

        draw_card(no, title, subheads, terms, formulas, app, out_path)
        generated += 1

        rel = f'visuals/{out_name}'
        if inject_image_reference(md, rel, no):
            updated += 1

    print(f'Generated images: {generated}')
    print(f'Updated markdown files: {updated}')


if __name__ == '__main__':
    main()
