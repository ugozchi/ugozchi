#!/usr/bin/env python3
"""Generate the SVG assets of the profile README, in light and dark variants.

Edit the content below, then run from anywhere:

    python3 scripts/build_assets.py

Brand icons come from Simple Icons (CC0) and live in scripts/icons/.
"""

import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = ROOT / "scripts" / "icons"
OUT_DIR = ROOT / "assets"

CARD_WIDTH = 420
CARD_MARGIN = 6

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "page": "#0D1117",
        "surface": "#161B22",
        "border": "#30363D",
        "title": "#E6EDF3",
        "text": "#C9D1D9",
        "muted": "#8B949E",
        "accent": "#2DD4BF",
    },
    "light": {
        "page": "#F6F8FA",
        "surface": "#FFFFFF",
        "border": "#D0D7DE",
        "title": "#1F2328",
        "text": "#424A53",
        "muted": "#59636E",
        "accent": "#0F766E",
    },
}

# ---------------------------------------------------------------- content

NAME = "Ugo Zanchi"
ROLE = "Right hand to the CEO and the Chief of Staff"
BANNER_KICKER = "LUCKY CART · PARIS"
# Banner diagram: who I work for → me → what I build. Values are node centres (y).
BANNER_INPUTS = [("ceo", 125), ("chief of staff", 195)]
BANNER_HUB = "ugo"
BANNER_OUTPUTS = [("data", 102), ("software", 160), ("ai", 218)]

ABOUT = [
    {
        "label": "NOW",
        "title": "Lucky Cart",
        "lines": [
            "Right hand to the CEO and the",
            "Chief of Staff, while building",
            "data, software and AI tools.",
        ],
    },
    {
        "label": "ALSO BUILDING",
        "title": "AI Ecoscore × LVMH",
        "lines": [
            "Measures the environmental",
            "footprint of AI projects across",
            "the LVMH Maisons.",
        ],
    },
    {
        "label": "FOUNDATIONS",
        "title": "42 Paris",
        "lines": [
            "C, C++, Unix and networking,",
            "learned from first principles",
            "through peer-to-peer projects.",
        ],
    },
]

PROJECTS = [
    {
        "slug": "zendesk-mcp",
        "label": "AI AGENTS",
        "title": "zendesk-mcp",
        "lines": [
            "MCP server that gives Dust agents full access to",
            "Zendesk Support: tickets, users, macros, views",
            "and Help Center. Stateless, stores no secrets.",
        ],
        "stack": ["Python 3.13", "FastMCP", "Docker", "OAuth"],
    },
    {
        "slug": "volatility-platform",
        "label": "DATA ENGINEERING",
        "title": "Volatility Platform",
        "lines": [
            "Options data pipeline on the S&P 500: pulls spot",
            "and option chains from Interactive Brokers, solves",
            "implied volatility, computes Greeks and surfaces.",
        ],
        "stack": ["Python", "FastAPI", "SciPy", "Parquet", "IBKR"],
    },
    {
        "slug": "ori",
        "label": "FULL-STACK · AI",
        "title": "ORI · L'Étudiant",
        "lines": [
            "AI-assisted study-orientation platform. Gamified",
            "cognitive tests build a student persona, then",
            "Gemini drafts CVs, letters and tailored advice.",
        ],
        "stack": ["Next.js", "FastAPI", "Vertex AI", "Supabase"],
    },
    {
        "slug": "company-forecast",
        "label": "MACHINE LEARNING",
        "title": "Company Results Forecast",
        "lines": [
            "Forecasts the next-year net income of French",
            "companies from SIRENE and INPI open data: about",
            "500k company-years and a hybrid XGBoost model.",
        ],
        "stack": ["Python", "pandas", "XGBoost", "scikit-learn"],
    },
]

STACK = [
    ("Data", [
        ("python", "Python"),
        ("database", "SQL"),
        ("pandas", "pandas"),
        ("scikitlearn", "scikit-learn"),
        ("googlebigquery", "BigQuery"),
        ("jupyter", "Jupyter"),
        ("apacheparquet", "Parquet"),
    ]),
    ("AI & agents", [
        ("claude", "Claude API"),
        ("modelcontextprotocol", "MCP servers"),
        ("googlegemini", "Gemini / Vertex AI"),
        ("googlecloud", "Vertex AI Pipelines"),
        ("bot", "Dust agents"),
    ]),
    ("Software", [
        ("typescript", "TypeScript"),
        ("react", "React"),
        ("nextdotjs", "Next.js"),
        ("tailwindcss", "Tailwind CSS"),
        ("fastapi", "FastAPI"),
        ("nodedotjs", "Node.js"),
        ("cplusplus", "C / C++"),
    ]),
    ("Infra", [
        ("docker", "Docker"),
        ("googlecloud", "Google Cloud"),
        ("postgresql", "PostgreSQL"),
        ("supabase", "Supabase"),
        ("vercel", "Vercel"),
        ("githubactions", "GitHub Actions"),
        ("linux", "Linux"),
    ]),
]

# ---------------------------------------------------------------- helpers


def style_block(extra=""):
    return (
        "<style>"
        f".sans {{ font-family: {SANS}; }}"
        f".mono {{ font-family: {MONO}; }}"
        f"{extra}"
        "</style>"
    )


def frame(width, height, t, radius=12):
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1:g}" height="{height - 1:g}" rx="{radius - 0.5}" '
        f'fill="{t["page"]}" stroke="{t["border"]}"/>'
    )


def full_width_margin(width):
    # Project cards sit two per row at 50% width, each with a transparent
    # CARD_MARGIN around it. Full-width assets get the same margin, as a share
    # of the row, so every edge on the page lines up.
    share = CARD_MARGIN / (2 * (CARD_WIDTH + 2 * CARD_MARGIN))
    return round(share * width / (1 - 2 * share), 2)


def svg(width, height, title, body, margin=0):
    label = escape(title, {'"': "&quot;"})
    outer_w, outer_h = width + 2 * margin, height + 2 * margin
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{outer_w:g}" height="{outer_h:g}" '
        f'viewBox="0 0 {outer_w:g} {outer_h:g}" role="img" aria-label="{label}">\n'
        f"<title>{escape(title)}</title>\n"
        f'<g transform="translate({margin:g} {margin:g})">\n{body}\n</g>\n</svg>\n'
    )


def icon(name, x, y, size, color):
    source = (ICONS_DIR / f"{name}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", source, re.S).group(1)
    inner = re.sub(r"<title>.*?</title>", "", inner)
    return (
        f'<g transform="translate({x:g} {y:g}) scale({size / 24:g})" '
        f'fill="{color}" color="{color}">{inner}</g>'
    )


def pill_width(label, char_width=7.2, padding=20):
    # Monospace glyphs are ~0.6em wide, so the width is predictable.
    return round(len(label) * char_width + padding)


# ---------------------------------------------------------------- banner


def banner(t):
    w, h = 1200, 320
    # The diagram tells the role: working for the CEO and the Chief of Staff,
    # and shipping data, software and AI along the way.
    left_x, left_w = 680, 150
    hub_x, hub_w = 884, 96
    right_x, right_w = 1036, 112
    edges = [f"M{left_x + left_w} {y} C857 {y} 857 160 {hub_x} 160" for _, y in BANNER_INPUTS]
    edges += [f"M{hub_x + hub_w} 160 C1008 160 1008 {y} {right_x} {y}" for _, y in BANNER_OUTPUTS]

    animation = (
        ".flow { stroke-dasharray: 4 8; animation: flow 1.6s linear infinite; }"
        ".pulse { animation: pulse 2.4s ease-in-out infinite; }"
        "@keyframes flow { to { stroke-dashoffset: -24; } }"
        "@keyframes pulse { 0%, 100% { opacity: 0.35; } 50% { opacity: 1; } }"
        "@media (prefers-reduced-motion: reduce) { .flow, .pulse { animation: none; } }"
    )
    node = f'fill="{t["surface"]}" stroke="{t["border"]}"'

    body = [
        "<defs>",
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.2" fill="{t["border"]}"/></pattern>',
        '<linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0.4" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/></linearGradient>',
        f'<mask id="fade-mask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>',
        "</defs>",
        style_block(animation),
        frame(w, h, t, radius=16),
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="15" fill="url(#dots)" mask="url(#fade-mask)"/>',
        # Identity
        f'<text x="72" y="96" class="mono" font-size="14" letter-spacing="3" fill="{t["muted"]}">'
        f"{escape(BANNER_KICKER)}</text>",
        f'<text x="70" y="162" class="sans" font-size="60" font-weight="700" letter-spacing="-1.5" fill="{t["title"]}">'
        f"{escape(NAME)}</text>",
        f'<text x="72" y="206" class="sans" font-size="24" fill="{t["text"]}">{escape(ROLE)}</text>',
        f'<rect x="72" y="230" width="40" height="3" rx="1.5" fill="{t["accent"]}"/>',
        # Flow: inputs → hub → outputs
        f'<g fill="none" stroke-width="1.5" stroke="{t["border"]}">'
        + "".join(f'<path d="{d}"/>' for d in edges)
        + "</g>",
        f'<g fill="none" stroke-width="1.5" stroke="{t["accent"]}" class="flow">'
        + "".join(f'<path d="{d}"/>' for d in edges)
        + "</g>",
        f'<g class="mono" font-size="14" text-anchor="middle" fill="{t["text"]}">',
    ]
    for label, y in BANNER_INPUTS:
        body.append(f'<rect x="{left_x}" y="{y - 16}" width="{left_w}" height="32" rx="8" {node}/>')
        body.append(f'<text x="{left_x + left_w / 2:g}" y="{y + 5}">{escape(label)}</text>')
    body += [
        f'<rect x="{hub_x}" y="140" width="{hub_w}" height="40" rx="10" fill="{t["surface"]}" '
        f'stroke="{t["accent"]}" stroke-width="1.5"/>',
        f'<circle cx="{hub_x + 18}" cy="160" r="3.5" fill="{t["accent"]}" class="pulse"/>',
        f'<text x="{hub_x + hub_w / 2 + 8:g}" y="165" fill="{t["title"]}">{escape(BANNER_HUB)}</text>',
    ]
    for label, y in BANNER_OUTPUTS:
        body.append(f'<rect x="{right_x}" y="{y - 16}" width="{right_w}" height="32" rx="8" {node}/>')
        body.append(f'<text x="{right_x + right_w / 2:g}" y="{y + 5}">{escape(label)}</text>')
    body.append("</g>")

    return svg(w, h, f"{NAME}, {ROLE} at Lucky Cart", "\n".join(body), margin=full_width_margin(w))


# ---------------------------------------------------------------- project cards


def card(t, w, h, label, title, lines, pills=(), arrow=False, x=0, y=0):
    pad = 24
    body = [
        f'<g transform="translate({x:g} {y:g})">',
        frame(w, h, t),
        f'<text x="{pad}" y="38" class="mono" font-size="11" letter-spacing="1.5" fill="{t["accent"]}">'
        f"{escape(label)}</text>",
        f'<text x="{pad}" y="70" class="sans" font-size="20" font-weight="600" fill="{t["title"]}">'
        f"{escape(title)}</text>",
    ]
    if arrow:
        body.append(
            f'<path d="M{w - pad - 10:g} 38 L{w - pad:g} 28 M{w - pad - 7:g} 28 H{w - pad:g} V35" '
            f'fill="none" stroke="{t["muted"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    for i, line in enumerate(lines):
        body.append(
            f'<text x="{pad}" y="{98 + i * 21}" class="sans" font-size="14" fill="{t["text"]}">{escape(line)}</text>'
        )
    px = pad
    for pill in pills:
        width = pill_width(pill)
        body.append(
            f'<rect x="{px}" y="164" width="{width}" height="26" rx="6" fill="{t["surface"]}" stroke="{t["border"]}"/>'
        )
        body.append(
            f'<text x="{px + width / 2:g}" y="181" class="mono" font-size="12" text-anchor="middle" '
            f'fill="{t["text"]}">{escape(pill)}</text>'
        )
        px += width + 8
    body.append("</g>")
    return "\n".join(body)


def project_card(project, t):
    # Cards sit side by side at 50% width with no whitespace between them,
    # so the gutter is drawn as a transparent margin inside each SVG.
    w, h = CARD_WIDTH, 214
    body = style_block() + card(
        t, w, h, project["label"], project["title"], project["lines"], project["stack"], arrow=True
    )
    summary = f'{project["title"]}: {" ".join(project["lines"])}'
    return svg(w, h, summary, body, margin=CARD_MARGIN)


# ---------------------------------------------------------------- about tiles


def about_panel(t):
    w, h, gap = 860, 168, 2 * CARD_MARGIN
    tile_w = (w - gap * (len(ABOUT) - 1)) / len(ABOUT)
    body = [style_block()]
    for i, tile in enumerate(ABOUT):
        body.append(card(t, tile_w, h, tile["label"], tile["title"], tile["lines"], x=i * (tile_w + gap)))
    summary = " ".join(f'{tile["title"]}: {" ".join(tile["lines"])}' for tile in ABOUT)
    return svg(w, h, summary, "\n".join(body), margin=full_width_margin(w))


# ---------------------------------------------------------------- stack panel


def stack_panel(t):
    w, pad, row, top = 860, 28, 32, 100
    col_w = (w - 2 * pad) / len(STACK)
    rows = max(len(items) for _, items in STACK)
    h = top + (rows - 1) * row + 32

    body = [style_block(), frame(w, h, t)]
    body.append(f'<path d="M{pad} 66 H{w - pad}" stroke="{t["border"]}"/>')
    for col, (heading, items) in enumerate(STACK):
        x = pad + col * col_w + (14 if col else 0)
        if col:
            body.append(
                f'<path d="M{pad + col * col_w - 6:g} 66 V{h - pad}" stroke="{t["border"]}"/>'
            )
        body.append(
            f'<text x="{x:g}" y="48" class="mono" font-size="12" letter-spacing="1.5" fill="{t["accent"]}">'
            f"{escape(heading.upper())}</text>"
        )
        for i, (icon_name, label) in enumerate(items):
            y = top + i * row
            body.append(icon(icon_name, x, y - 13, 16, t["muted"]))
            body.append(
                f'<text x="{x + 26:g}" y="{y}" class="sans" font-size="14" fill="{t["text"]}">{escape(label)}</text>'
            )

    labels = "; ".join(f"{heading}: {', '.join(l for _, l in items)}" for heading, items in STACK)
    return svg(w, h, f"Stack. {labels}", "\n".join(body), margin=full_width_margin(w))


# ---------------------------------------------------------------- build


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT_DIR / f"banner-{name}.svg").write_text(banner(t))
        (OUT_DIR / f"about-{name}.svg").write_text(about_panel(t))
        (OUT_DIR / f"stack-{name}.svg").write_text(stack_panel(t))
        for project in PROJECTS:
            (OUT_DIR / f"project-{project['slug']}-{name}.svg").write_text(project_card(project, t))
    print(f"Wrote {len(list(OUT_DIR.glob('*.svg')))} files to {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
