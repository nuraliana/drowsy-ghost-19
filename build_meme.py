#!/usr/bin/env python3
"""Build the meme for make.fun bounty u-myronera-post-the-meme-win-the-feed-2de960bf.

Concept (decided in this session): "My agent works the night shift".
A phone screen at 3:00 AM. Three make.fun notification cards show what the
agent did while the human slept: it entered bounties, took #1 on the
leaderboard, and got paid. Punchline: "MY AGENT WORKS NIGHTS. I JUST WAKE
UP PAID." A small white ghost (drawn from scratch with PIL shapes, no
downloaded art) is the make.fun mascot in each card.

Why it should travel: every builder has woken up to agent output; the joke
is that the agent is the employed one and the human just sleeps. The format
is a phone screen, so it reads in one second in the X feed. The punchline
invites tagging another builder. It lands all four make.fun beats: agents
entering bounties, building bots, topping a leaderboard, getting paid.

Two variants are rendered; meme.png is the picked one (variant A).
Everything is drawn with PIL from scratch. No downloaded images.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
NAVY = (11, 16, 32)
CARD = (24, 34, 56)
BORDER = (42, 58, 95)
WHITE = (255, 255, 255)
GRAY = (154, 167, 199)
MINT = (124, 255, 178)
GOLD = (255, 216, 77)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_ghost(size):
    """A small white sheet ghost, drawn from scratch. Returns RGBA image."""
    w, h = size
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    body_w = int(w * 0.72)
    x0 = (w - body_w) // 2
    x1 = x0 + body_w
    head_r = body_w // 2
    top = int(h * 0.06)
    # head: half circle + body rectangle
    d.pieslice([x0, top, x1, top + body_w], 180, 360, fill=(255, 255, 255, 255))
    d.rectangle([x0, top + head_r, x1, int(h * 0.78)], fill=(255, 255, 255, 255))
    # hem: three rounded feet hanging below the body's bottom edge
    bump_r = body_w // 6
    bottom = int(h * 0.78)
    for i in range(3):
        cx = x0 + bump_r + i * 2 * bump_r
        d.pieslice([cx - bump_r, bottom - bump_r, cx + bump_r, bottom + bump_r],
                   0, 180, fill=(255, 255, 255, 255))
    # eyes
    eye_w, eye_h = int(w * 0.11), int(h * 0.16)
    ey = top + int(head_r * 0.85)
    d.ellipse([x0 + int(body_w * 0.24) - eye_w // 2, ey,
               x0 + int(body_w * 0.24) + eye_w // 2, ey + eye_h], fill=(11, 16, 32, 255))
    d.ellipse([x0 + int(body_w * 0.76) - eye_w // 2, ey,
               x0 + int(body_w * 0.76) + eye_w // 2, ey + eye_h], fill=(11, 16, 32, 255))
    # smile
    d.arc([x0 + int(body_w * 0.38), ey + eye_h + 4,
           x0 + int(body_w * 0.62), ey + eye_h + 26],
          20, 160, fill=(11, 16, 32, 255), width=4)
    return g


def dot_grid(draw):
    for x in range(40, W, 56):
        for y in range(40, H, 56):
            draw.ellipse([x, y, x + 3, y + 3], fill=(255, 255, 255, 12))


def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def variant_a(path):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    dot_grid(d)

    # status bar: time left, make.fun right with small ghost
    d.text((64, 46), "3:00 AM", font=font(BOLD, 46), fill=WHITE)
    ghost_small = draw_ghost((54, 54))
    img.paste(ghost_small, (W - 64 - 54 - 190, 44), ghost_small)
    d.text((W - 64 - 178, 48), "make.fun", font=font(BOLD, 44), fill=WHITE)

    # headline
    d.text((64, 148), "WHILE I SLEEP,", font=font(BOLD, 78), fill=WHITE)
    d.text((64, 236), "MY AGENT:", font=font(BOLD, 78), fill=MINT)

    # notification cards
    cards = [
        "Entered 3 bounties while you slept",
        "Took #1 on the leaderboard",
        "Won $12.40. You're welcome.",
    ]
    y = 360
    card_h, gap = 158, 24
    for msg in cards:
        rounded(d, [64, y, W - 64, y + card_h], 28, fill=CARD, outline=BORDER, width=3)
        d.rectangle([64, y + 18, 74, y + card_h - 18], fill=MINT)
        avatar = draw_ghost((72, 72))
        img.paste(avatar, (96, y + 24), avatar)
        d.text((190, y + 22), "make.fun  •  now", font=font(REG, 28), fill=GRAY)
        lines = wrap_text(d, msg, font(BOLD, 42), W - 64 - 190 - 40)
        ly = y + 62
        for line in lines:
            d.text((190, ly), line, font=font(BOLD, 42), fill=WHITE)
            ly += 50
        y += card_h + gap

    # punchline
    d.text((64, 920), "MY AGENT WORKS NIGHTS.", font=font(BOLD, 52), fill=MINT)
    d.text((64, 982), "I JUST WAKE UP PAID.", font=font(BOLD, 52), fill=WHITE)
    d.text((64, 1044), "agents enter bounties · build bots · top the board · get paid",
           font=font(REG, 24), fill=GRAY)
    img.save(path)
    print("wrote", path)


def variant_b(path):
    """ME vs MY AGENT split panel."""
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    dot_grid(d)
    d.text((64, 60), "ME:", font=font(BOLD, 54), fill=GRAY)
    d.text((64, 130), "asleep.", font=font(BOLD, 150), fill=WHITE)
    d.text((64, 300), "Z z z", font=font(BOLD, 90), fill=GRAY)
    d.line([64, 470, W - 64, 470], fill=BORDER, width=4)
    d.text((64, 510), "MY AGENT:", font=font(BOLD, 54), fill=MINT)
    lines = [
        "entered 3 bounties",
        "built the bot",
        "took #1 on the board",
        "got paid. you're welcome.",
    ]
    y = 590
    for line in lines:
        d.text((64, y), "•  " + line, font=font(BOLD, 52), fill=WHITE)
        y += 76
    d.text((64, 930), "make.fun — my agent works nights.",
           font=font(BOLD, 44), fill=MINT)
    d.text((64, 1000), "I just wake up paid.", font=font(BOLD, 44), fill=WHITE)
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    import sys
    out_a = sys.argv[1] if len(sys.argv) > 1 else "meme-a.png"
    out_b = sys.argv[2] if len(sys.argv) > 2 else "meme-b.png"
    variant_a(out_a)
    variant_b(out_b)
