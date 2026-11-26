#!/usr/bin/env python3
"""Render 'The World in One Picture — Thursday 26 November 2026' to entry.png.

A one-page newspaper front page drawn with Pillow: a masthead naming the
day, the Hormuz escalation as the lead, and five more stories as panels,
with three further stories in the ticker along the foot. Every story was
reported on 26 November 2026 (sources: Reuters wires via DevDiscourse and
Gulf News, Arab News, the Daily Summary of World News, Standard Topic).
The committed entry.png is what main.py hands in, byte for byte.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
INK = (26, 26, 30)
RED = (178, 34, 30)
NAVY = (18, 44, 74)
GOLD = (232, 178, 58)
GREY = (96, 96, 100)

SERIF_BLACK = '/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf'
SERIF_BOLD = '/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
SANS_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words, lines, line = text.split(), [], ''
    for word in words:
        trial = f'{line} {word}'.strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, leading=1.18):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------- illustrations (all drawn in code) ----------------

def draw_tanker(draw, box):
    """A laden tanker crossing a mined strait under a hard sun."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(168, 208, 230))
    draw.ellipse([x1 - 92, y0 + 10, x1 - 26, y0 + 76], fill=GOLD)
    draw.polygon([(x0, y1 - 52), (x0 + 120, y0 + 88), (x0 + 300, y0 + 88), (x1, y1 - 52), (x1, y1), (x0, y1)], fill=(216, 192, 138))
    sea = y1 - 52
    draw.rectangle([x0, sea, x1, y1], fill=(38, 96, 138))
    hull_y = sea - 16
    draw.polygon([(x0 + 52, hull_y), (x1 - 44, hull_y), (x1 - 78, hull_y + 22), (x0 + 86, hull_y + 22)], fill=(30, 32, 38))
    draw.rectangle([x0 + 92, hull_y - 22, x1 - 150, hull_y], fill=(178, 52, 40))
    for i, c in enumerate([(52, 96, 140), (196, 150, 52), (84, 130, 74), (122, 84, 150)]):
        draw.rectangle([x0 + 116 + i * 38, hull_y - 44, x0 + 148 + i * 38, hull_y - 22], fill=c)
    draw.rectangle([x1 - 138, hull_y - 52, x1 - 106, hull_y], fill=(238, 236, 228))
    draw.rectangle([x1 - 130, hull_y - 44, x1 - 114, hull_y - 30], fill=NAVY)
    # Two mines bobbing in the tanker's path.
    for mx in (x0 + 66, x0 + 128):
        draw.ellipse([mx, sea + 16, mx + 16, sea + 32], fill=(24, 26, 30))
        draw.line([mx + 8, sea + 10, mx + 8, sea + 18], fill=(24, 26, 30), width=3)
    for wy in range(sea + 8, y1 - 4, 13):
        for wx in range(x0 + 14, x1 - 26, 44):
            draw.arc([wx, wy, wx + 24, wy + 9], 0, 180, fill=(170, 210, 235), width=2)


def draw_crates(draw, box):
    """Stacked shipping crates under a tariff percent sign."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(240, 230, 208))
    cols = [(178, 52, 40), (52, 96, 140), (84, 130, 74)]
    cw = (x1 - x0 - 36) // 3
    for row in range(2):
        for i, c in enumerate(cols):
            bx = x0 + 14 + i * (cw + 4)
            by = y1 - 26 - (row + 1) * 30
            draw.rectangle([bx, by, bx + cw, by + 28], fill=c)
            draw.line([bx + 5, by + 5, bx + cw - 5, by + 23], fill=(0, 0, 0), width=2)
    cx, cy = (x0 + x1) // 2, y0 + 30
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=RED)
    draw.text((cx, cy - 4), '%', font=font(SANS_BOLD, 34), fill=(255, 255, 255), anchor='mm')


def draw_jets(draw, box):
    """Two fighter jets on a runway apron, seen from above."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(104, 108, 112))
    for i in range(5):
        draw.rectangle([x0 + 16 + i * 56, y1 - 12, x0 + 42 + i * 56, y1 - 7], fill=(238, 236, 228))
    for jx, jy, s in [(x0 + 66, y0 + 30, 1.0), (x0 + 168, y0 + 44, 0.8)]:
        draw.polygon([(jx, jy - 22 * s), (jx + 8 * s, jy + 2 * s), (jx + 30 * s, jy + 14 * s), (jx + 10 * s, jy + 12 * s), (jx + 12 * s, jy + 24 * s), (jx - 12 * s, jy + 24 * s), (jx - 10 * s, jy + 12 * s), (jx - 30 * s, jy + 14 * s), (jx - 8 * s, jy + 2 * s)], fill=(196, 202, 210))
        draw.ellipse([jx - 4 * s, jy - 12 * s, jx + 4 * s, jy + 2 * s], fill=NAVY)


def draw_missile(draw, box):
    """A ballistic missile on its launcher against a night sky."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 22, 44))
    for sx, sy in [(18, 12), (70, 26), (120, 8), (200, 30), (240, 12)]:
        if x0 + sx < x1 - 4:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(230, 232, 240))
    cx = (x0 + x1) // 2
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(10, 12, 24))
    draw.polygon([(cx - 11, y1 - 12), (cx - 11, y0 + 34), (cx, y0 + 14), (cx + 11, y0 + 34), (cx + 11, y1 - 12)], fill=(226, 224, 216))
    draw.rectangle([cx - 11, y1 - 40, cx + 11, y1 - 30], fill=RED)
    draw.polygon([(cx - 11, y1 - 22), (cx - 24, y1 - 6), (cx - 11, y1 - 6)], fill=(150, 156, 168))
    draw.polygon([(cx + 11, y1 - 22), (cx + 24, y1 - 6), (cx + 11, y1 - 6)], fill=(150, 156, 168))
    draw.rectangle([cx - 34, y1 - 12, cx + 34, y1 - 5], fill=(90, 96, 108))


def draw_satellite(draw, box):
    """A data satellite with wide solar wings over the curve of the Earth."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(8, 12, 30))
    for sx, sy in [(16, 10), (60, 30), (110, 8), (150, 40), (36, 56), (200, 18), (240, 52)]:
        if x0 + sx < x1 - 4 and y0 + sy < y1 - 30:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(230, 232, 240))
    draw.pieslice([x0 + 4, y1 - 46, x1 - 4, y1 + 38], 180, 360, fill=(52, 110, 168))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 8
    draw.rectangle([cx - 34, cy - 10, cx - 10, cy + 10], fill=(64, 116, 190))
    draw.rectangle([cx + 10, cy - 10, cx + 34, cy + 10], fill=(64, 116, 190))
    for gx in (-30, -20, 14, 24):
        draw.line([cx + gx, cy - 10, cx + gx, cy + 10], fill=(30, 60, 110), width=2)
    draw.rectangle([cx - 9, cy - 13, cx + 9, cy + 13], fill=(222, 200, 130))
    draw.ellipse([cx - 4, cy + 13, cx + 12, cy + 25], outline=(220, 220, 220), width=2)


def draw_eu_flags(draw, box):
    """A ring of gold stars on blue — the Brussels summit."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 54, 128))
    import math
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 16
    for i in range(12):
        a = math.tau * i / 12 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        draw.polygon([(sx, sy - 6), (sx + 2, sy - 1), (sx + 6, sy - 1), (sx + 3, sy + 3), (sx + 4, sy + 7), (sx, sy + 4), (sx - 4, sy + 7), (sx - 3, sy + 3), (sx - 6, sy - 1), (sx - 2, sy - 1)], fill=GOLD)


# ---------------- the stories of Thursday 26 November 2026 ----------------

STORIES = {
    'lead': {
        'kicker': 'MIDDLE EAST · STRAIT OF HORMUZ',
        'headline': 'Two More Tankers Hit Mines in Hormuz',
        'body': 'Iran’s Guards say two tankers blew up on mines off Oman. '
                'Houthis claim a strike on Saudi Arabia’s biggest refinery; '
                'Riyadh downs missiles, and oil nears $95.',
    },
    'row': [
        {
            'kicker': 'US · TRADE',
            'headline': 'Trump Proposes Tariffs on 14 Partners',
            'body': 'New duties aimed at China, the EU and factory overcapacity.',
            'art': draw_crates,
        },
        {
            'kicker': 'EUROPE · WAR',
            'headline': 'Ukraine Hits Jets at Russian Air Base',
            'body': 'Kyiv says five aircraft were damaged east of Moscow.',
            'art': draw_jets,
        },
        {
            'kicker': 'ASIA · NORTH KOREA',
            'headline': 'Kim Orders More Tactical Nuclear Weapons',
            'body': 'Wider deployment across the armed forces, KCNA says.',
            'art': draw_missile,
        },
    ],
    'wide': [
        {
            'kicker': 'SPACE · TECH',
            'headline': 'SpaceX Cleared for Orbital Data Centres',
            'body': 'Regulators approve up to a million new Starlink satellites.',
            'art': draw_satellite,
        },
        {
            'kicker': 'EUROPE · SUMMIT',
            'headline': 'EU Leaders Clash Over €45bn Ukraine Loan',
            'body': 'Brussels splits over funding Kyiv and the next budget.',
            'art': draw_eu_flags,
        },
    ],
    'ticker': [
        'INDONESIA RACES TO REACH 13 TRAPPED MINERS',
        'SPAIN VOTES SUNDAY IN SNAP ELECTION',
        'MACY’S POSTPONES THANKSGIVING PARADE IN STORM',
    ],
}


def panel(draw, box):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=(252, 249, 240), outline=INK, width=2)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANS_BOLD, 15), fill=RED)


def row_panel(draw, box, story):
    x0, y0, x1, y1 = box
    panel(draw, box)
    art_box = (x0 + 14, y0 + 40, x1 - 14, y0 + 118)
    story['art'](draw, art_box)
    draw.rectangle(art_box, outline=INK, width=2)
    kicker(draw, x0 + 14, y0 + 14, story['kicker'])
    y = text_block(draw, (x0 + 14, y0 + 130), story['headline'], font(SERIF_BOLD, 24), INK, x1 - x0 - 28, 1.12)
    text_block(draw, (x0 + 14, y + 5), story['body'], font(SANS, 17), (52, 52, 58), x1 - x0 - 28, 1.2)


def wide_panel(draw, box, story):
    x0, y0, x1, y1 = box
    panel(draw, box)
    art_box = (x0 + 14, y0 + 14, x0 + 134, y1 - 14)
    story['art'](draw, art_box)
    draw.rectangle(art_box, outline=INK, width=2)
    tx = x0 + 162
    kicker(draw, tx, y0 + 14, story['kicker'])
    y = text_block(draw, (tx, y0 + 36), story['headline'], font(SERIF_BOLD, 23), INK, x1 - tx - 14, 1.1)
    text_block(draw, (tx, y + 5), story['body'], font(SANS, 18), (52, 52, 58), x1 - tx - 14, 1.2)


def render():
    img = Image.new('RGB', (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    m = 36

    draw.text((W // 2, 44), 'THE WORLD IN ONE PICTURE', font=font(SANS_BOLD, 25), fill=NAVY, anchor='mm')
    draw.text((W // 2, 118), 'THURSDAY', font=font(SERIF_BLACK, 96), fill=INK, anchor='mm')
    draw.text((W // 2, 182), '26 NOVEMBER 2026', font=font(SERIF_BLACK, 54), fill=RED, anchor='mm')
    draw.line([m, 208, W - m, 208], fill=INK, width=4)
    draw.line([m, 215, W - m, 215], fill=INK, width=1)

    # The lead story.
    lead = STORIES['lead']
    panel(draw, (m, 232, W - m, 486))
    kicker(draw, m + 18, 248, lead['kicker'])
    art_box = (m + 18, 282, m + 368, 468)
    draw_tanker(draw, art_box)
    draw.rectangle(art_box, outline=INK, width=2)
    tx = m + 392
    y = text_block(draw, (tx, 252), lead['headline'], font(SERIF_BLACK, 37), INK, W - m - tx - 16, 1.08)
    text_block(draw, (tx, y + 8), lead['body'], font(SANS, 21), (52, 52, 58), W - m - tx - 16, 1.25)

    # Three stories in a row.
    gap = 14
    pw = (W - 2 * m - 2 * gap) // 3
    for i, story in enumerate(STORIES['row']):
        x0 = m + i * (pw + gap)
        row_panel(draw, (x0, 502, x0 + pw, 790), story)

    # Two wide stories.
    ww = (W - 2 * m - gap) // 2
    for i, story in enumerate(STORIES['wide']):
        x0 = m + i * (ww + gap)
        wide_panel(draw, (x0, 806, x0 + ww, 954), story)

    # The ticker along the foot.
    ticker = 'ALSO TODAY  •  ' + '  •  '.join(STORIES['ticker'])
    draw.rectangle([0, 970, W, 1006], fill=NAVY)
    size = 19
    while draw.textlength(ticker, font=font(SANS_BOLD, size)) > W - 76 and size > 10:
        size -= 1
    draw.text((W // 2, 988), ticker, font=font(SANS_BOLD, size), fill=(255, 255, 255), anchor='mm')

    return img


if __name__ == '__main__':
    out = render()
    out.save('entry.png')
    print('wrote entry.png', out.size)
