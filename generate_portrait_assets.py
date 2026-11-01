import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

pygame.init()

DIR = r"C:\Users\HenriqueRF\Desktop\LetterForYou"
src_img_path = os.path.join(DIR, "portrait_centered.jpg")

if not os.path.exists(src_img_path):
    raise FileNotFoundError(f"Source image not found: {src_img_path}")

img = Image.open(src_img_path)

# Subtle enhancement for rich tones and clarity
enh_col = ImageEnhance.Color(img)
img = enh_col.enhance(1.24)
enh_con = ImageEnhance.Contrast(img)
img = enh_con.enhance(1.28)

FONT_SIZE = 12
font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
char_w, char_h = font.size("A")  # Consolas 12: char_w=7, char_h=12

WIDTH, HEIGHT = 720, 780
avail_w = WIDTH - 40
avail_h = HEIGHT - 70

char_aspect = char_h / char_w
img_aspect = img.width / img.height
grid_aspect = img_aspect * char_aspect

rows = min(avail_h // char_h, int((avail_w // char_w) / grid_aspect))  # 51
cols = int(rows * grid_aspect)  # 96

print(f"Generating Portrait Data: {cols} columns x {rows} rows (cw={char_w}, ch={char_h})")

img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
arr_rgb = np.array(img_resized)
arr_gray = np.array(img_resized.convert("L"))

# Edge detection
edges = np.array(img_resized.convert("L").filter(ImageFilter.FIND_EDGES))

# Soft elliptical vignette focused on her face and hair
y_grid, x_grid = np.ogrid[:rows, :cols]
cx, cy = cols * 0.45, rows * 0.44
rx, ry = cols * 0.48, rows * 0.50
dist = ((x_grid - cx) / rx) ** 2 + ((y_grid - cy) / ry) ** 2
vig = np.clip(1.0 - (dist - 0.60) / 0.40, 0.0, 1.0)
vig = vig * vig * (3 - 2 * vig)

CODE_SYMBOLS = ["{", "}", "(", ")", "[", "]", ";", ":", "=", "+", "-", "*", "&", "|", "^", "%", "#", "@", "$", "!", "?", "<", ">"]
LOVE_CHARS = ["♥", "l", "o", "v", "e", "a", "m", "o", "r", "y", "o", "u", "1", "0", "∞"]

cells = []
text_lines = []

for r in range(rows):
    line_chars = []
    for c in range(cols):
        rgb = arr_rgb[r, c]
        lum = arr_gray[r, c]
        ed = edges[r, c]
        v = vig[r, c]

        if v < 0.06:
            line_chars.append(" ")
            continue

        # Character selection based on geometry and luminance
        if ed > 42:
            ch_c = "/" if (r + c) % 2 == 0 else "\\"
        elif lum > 218:
            ch_c = "♥" if (r * c) % 5 == 0 else ("*" if (r + c) % 2 == 0 else "+")
        elif lum > 160:
            ch_c = LOVE_CHARS[(r * 7 + c * 3) % len(LOVE_CHARS)]
        elif lum > 90:
            ch_c = CODE_SYMBOLS[(r * 5 + c * 11) % len(CODE_SYMBOLS)]
        elif lum > 40:
            ch_c = "#" if (r + c) % 2 == 0 else "%"
        else:
            ch_c = "." if (r + c) % 2 == 0 else " "

        line_chars.append(ch_c)

        if ch_c != " ":
            # Modulate RGB by vignette for smooth cosmic edge blending
            final_r = min(255, max(0, int(rgb[0] * v)))
            final_g = min(255, max(0, int(rgb[1] * v)))
            final_b = min(255, max(0, int(rgb[2] * v)))
            cells.append((r, c, ch_c, (final_r, final_g, final_b)))

    text_lines.append("".join(line_chars))

print(f"Total active cells: {len(cells)}")

# 1. Save portrait_data.py
data_path = os.path.join(DIR, "portrait_data.py")
with open(data_path, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""\nPrecomputed Code Portrait Data for LetterForYou.\n"""\n\n')
    f.write(f"PORTRAIT_COLS = {cols}\n")
    f.write(f"PORTRAIT_ROWS = {rows}\n")
    f.write(f"PORTRAIT_FONT_SIZE = {FONT_SIZE}\n\n")
    f.write("# Format: (row, col, char, (R, G, B))\n")
    f.write("PORTRAIT_CELLS = [\n")
    for r, c, ch, col in cells:
        # Escape backslash
        ch_esc = ch.replace("\\", "\\\\").replace("'", "\\'")
        f.write(f"    ({r}, {c}, '{ch_esc}', {col}),\n")
    f.write("]\n")

print(f"Saved {data_path}")

# 2. Save portrait_ascii.txt
ascii_txt_path = os.path.join(DIR, "portrait_ascii.txt")
with open(ascii_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(text_lines))
print(f"Saved {ascii_txt_path}")

# 3. Save high-res preview image
surf = pygame.Surface((WIDTH, HEIGHT))
surf.fill((7, 8, 12))
ox = (WIDTH - cols * char_w) // 2
oy = (HEIGHT - rows * char_h) // 2

for r, c, ch_c, col in cells:
    glyph = font.render(ch_c, True, col)
    surf.blit(glyph, (ox + c * char_w, oy + r * char_h))

# Title header and footer
title_font = pygame.font.SysFont("consolas", 14, bold=True)
title_surf = title_font.render("♥  Eternamente em Meus Pensamentos  ♥", True, (255, 180, 200))
surf.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 12))

preview_png = os.path.join(DIR, "portrait_render_full.png")
pygame.image.save(surf, preview_png)
print(f"Saved {preview_png}")

# 4. Save interactive HTML preview
html_path = os.path.join(DIR, "portrait_interactive.html")
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Letter For You ♥ - Retrato em Códigos</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #07080c;
            color: #fff;
            font-family: 'Consolas', 'Courier New', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow-x: hidden;
            padding: 20px;
        }}
        h1 {{
            font-size: 22px;
            color: #ff8cb2;
            text-shadow: 0 0 15px rgba(255, 60, 120, 0.6);
            margin-bottom: 8px;
            letter-spacing: 2px;
        }}
        .subtitle {{
            font-size: 13px;
            color: #8899bb;
            margin-bottom: 20px;
        }}
        .canvas-container {{
            position: relative;
            background: #07080c;
            border: 1px solid rgba(255, 100, 150, 0.25);
            border-radius: 12px;
            box-shadow: 0 0 40px rgba(255, 40, 100, 0.2), inset 0 0 20px rgba(0,0,0,0.8);
            padding: 15px;
        }}
        canvas {{
            display: block;
        }}
        .controls {{
            margin-top: 18px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        button {{
            background: rgba(30, 35, 55, 0.8);
            border: 1px solid rgba(255, 120, 170, 0.4);
            color: #ffb8d0;
            padding: 8px 16px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        button:hover {{
            background: rgba(255, 60, 120, 0.3);
            border-color: #ff3c78;
            box-shadow: 0 0 12px rgba(255, 60, 120, 0.5);
            color: #fff;
        }}
    </style>
</head>
<body>
    <h1>♥ LETTER FOR YOU ♥</h1>
    <div class="subtitle">Retrato Gerado Proceduralmente em Código Monoespaçado</div>
    <div class="canvas-container">
        <canvas id="codeCanvas" width="{cols * char_w}" height="{rows * char_h}"></canvas>
    </div>
    <div class="controls">
        <button onclick="setTheme(0)">Cores Reais</button>
        <button onclick="setTheme(1)">Brasa Dourada</button>
        <button onclick="setTheme(2)">Ciano Cyberpunk</button>
        <button onclick="setTheme(3)">Matrix Esmeralda</button>
        <button onclick="toggleGlow()">Pulsação / Brilho</button>
    </div>

    <script>
        const cells = {[[r, c, ch_c, list(col)] for r, c, ch_c, col in cells]};
        const cw = {char_w}, ch = {char_h};
        const canvas = document.getElementById('codeCanvas');
        const ctx = canvas.getContext('2d');
        ctx.font = 'bold 12px Consolas, monospace';
        ctx.textBaseline = 'top';

        let currentTheme = 0;
        let glowEnabled = true;
        let time = 0;

        function setTheme(theme) {{
            currentTheme = theme;
        }}

        function toggleGlow() {{
            glowEnabled = !glowEnabled;
        }}

        function render() {{
            time += 0.03;
            ctx.fillStyle = '#07080c';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const pulse = glowEnabled ? (1.0 + 0.08 * Math.sin(time * 2.5)) : 1.0;

            for (const [r, c, chChar, rgb] of cells) {{
                let [red, green, blue] = rgb;

                if (currentTheme === 1) {{
                    // Golden Flame
                    const lum = (red * 0.299 + green * 0.587 + blue * 0.114) / 255.0;
                    red = Math.min(255, lum * 255 * 1.1);
                    green = Math.min(255, lum * 190);
                    blue = Math.min(255, lum * 50);
                }} else if (currentTheme === 2) {{
                    // Cyberpunk Cyan / Violet
                    const lum = (red * 0.299 + green * 0.587 + blue * 0.114) / 255.0;
                    red = Math.min(255, lum * 80 + 30);
                    green = Math.min(255, lum * 230);
                    blue = Math.min(255, lum * 255);
                }} else if (currentTheme === 3) {{
                    // Matrix Emerald
                    const lum = (red * 0.299 + green * 0.587 + blue * 0.114) / 255.0;
                    red = Math.min(255, lum * 40);
                    green = Math.min(255, lum * 255);
                    blue = Math.min(255, lum * 70);
                }}

                red = Math.min(255, Math.floor(red * pulse));
                green = Math.min(255, Math.floor(green * pulse));
                blue = Math.min(255, Math.floor(blue * pulse));

                ctx.fillStyle = `rgb(${{red}}, ${{green}}, ${{blue}})`;
                ctx.fillText(chChar, c * cw, r * ch);
            }}

            requestAnimationFrame(render);
        }}

        render();
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved {html_path}")
print("All portrait assets generated successfully.")
