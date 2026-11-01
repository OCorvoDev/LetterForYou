"""
Script to simulate and render keyframes of the letter-to-rose-to-rounded-photo animation.
Generates all stage previews as high-resolution PNG images.
"""
import os
import math
import random
import pygame
from portrait_data import PORTRAIT_COLS, PORTRAIT_ROWS, PORTRAIT_CELLS

# Headless mode for testing and frame generation
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

WIDTH, HEIGHT = 720, 780
CW, CH = 9, 16
COLS = WIDTH // CW
ROWS = HEIGHT // CH

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('consolas', 16, bold=True)

PORTRAIT_FONT_SIZE = 12
portrait_font = pygame.font.SysFont('consolas', PORTRAIT_FONT_SIZE, bold=True)
PCW, PCH = portrait_font.size('A')

title_font = pygame.font.SysFont('consolas', 16, bold=True)
subtitle_font = pygame.font.SysFont('consolas', 13, bold=True)

DIR = os.path.dirname(__file__)

# Load real rounded photo
photo_path = os.path.join(DIR, "photo_rounded.png")
photo_real_surf = pygame.image.load(photo_path).convert_alpha()
photo_orig_w, photo_orig_h = photo_real_surf.get_size()
PHOTO_CX = WIDTH // 2
PHOTO_CY = HEIGHT // 2 - 12
PHOTO_RADIUS = photo_orig_w // 2

# ---------------------------------------------------------------------------
# COLOR PALETTES & UTILS
# ---------------------------------------------------------------------------
BG_COLOR = (7, 8, 12)

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

FIRE_PALETTE = [
    (255, 255, 245),
    (255, 235, 60),
    (255, 130, 20),
    (225, 40, 15),
    (90, 25, 20),
    (35, 22, 28),
]

def get_fire_color(progress):
    p = max(0.0, min(0.999, progress)) * (len(FIRE_PALETTE) - 1)
    idx = int(p)
    frac = p - idx
    return lerp_color(FIRE_PALETTE[idx], FIRE_PALETTE[idx + 1], frac)

GLYPH_CACHE = {}
PORTRAIT_GLYPH_CACHE = {}

def get_glyph(char, color):
    qr = (color[0] // 8) * 8
    qg = (color[1] // 8) * 8
    qb = (color[2] // 8) * 8
    key = (char, (qr, qg, qb))
    if key not in GLYPH_CACHE:
        try:
            surf = font.render(char, True, (qr, qg, qb))
        except Exception:
            surf = font.render('?', True, (qr, qg, qb))
        GLYPH_CACHE[key] = surf
    return GLYPH_CACHE[key]

def get_portrait_glyph(char, color):
    qr = (color[0] // 8) * 8
    qg = (color[1] // 8) * 8
    qb = (color[2] // 8) * 8
    key = (char, (qr, qg, qb))
    if key not in PORTRAIT_GLYPH_CACHE:
        try:
            surf = portrait_font.render(char, True, (qr, qg, qb))
        except Exception:
            surf = portrait_font.render('?', True, (qr, qg, qb))
        PORTRAIT_GLYPH_CACHE[key] = surf
    return PORTRAIT_GLYPH_CACHE[key]

# ---------------------------------------------------------------------------
# ASCII MODELS
# ---------------------------------------------------------------------------
ENVELOPE_RAW = [
    r"  /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\  ",
    r" // \                                                     / \\ ",
    r"//   \                                                   /   \\",
    r'||    \                                                 /    ||',
    r"||     \                      .:::. .:::.              /     ||",
    r"||      \                    :::::::::::::            /      ||",
    r"||       \                   ':::::::::::'           /       ||",
    r"||        \                    ':::::::'            /        ||",
    r"||         \                     ':::'             /         ||",
    r"||          \_____________________________________/          ||",
    r"||                                                           ||",
    r"||   De: Seu Amor                                     ♥      ||",
    r"||   Para: A Pessoa Mais Especial Deste Mundo                ||",
    r"||   -----------------------------------------------------   ||",
    r"||   Mesmo que as palavras se queimem com o tempo, o meu     ||",
    r"||   sentimento por você floresce como a mais bela rosa.     ||",
    r"||   -----------------------------------------------------   ||",
    r"||                                                           ||",
    r"||   Com todo o meu amor e carinho sempre...                 ||",
    r"||                                                           ||",
    r" \\_________________________________________________________// ",
    r"  \~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/  ",
]

ENV_START_ROW = 12
ENV_START_COL = (COLS - len(ENVELOPE_RAW[0])) // 2

ENVELOPE_CELLS = []
for r_idx, line in enumerate(ENVELOPE_RAW):
    r = ENV_START_ROW + r_idx
    for c_idx, ch in enumerate(line):
        if ch == ' ':
            continue
        c = ENV_START_COL + c_idx
        if ch == '♥':
            col = (255, 35, 95)
            c_type = 'heart'
        elif ch in ('.', ':', "'") and r_idx < 10 and 20 < c_idx < 45:
            col = (245, 50, 110)
            c_type = 'seal'
        elif r_idx in (11, 12):
            col = (255, 230, 190)
            c_type = 'text_hi'
        elif r_idx in (14, 15, 18):
            col = (225, 205, 175)
            c_type = 'text'
        elif ch in ('/', '\\', '_', '~', '|', '-'):
            col = (195, 180, 155)
            c_type = 'border'
        else:
            col = (175, 160, 135)
            c_type = 'paper'
        ENVELOPE_CELLS.append((r, c, ch, col, c_type))

IG_ROW = ENV_START_ROW + len(ENVELOPE_RAW) - 3
IG_COL = ENV_START_COL + len(ENVELOPE_RAW[0]) - 8

T_IGNITE = 2.0
T_FIRE_END = 5.8
ENV_BURN_TIMES = []
for cell in ENVELOPE_CELLS:
    r, c = cell[0], cell[1]
    dr = (IG_ROW - r) * 1.0
    dc = (IG_COL - c) * 0.8
    dist = math.sqrt(dr * dr + dc * dc)
    jitter = math.sin(r * 0.8 + c * 0.5) * 2.8 + math.cos(r * 1.4 - c * 0.9) * 2.0
    tot_dist = max(0.0, dist + jitter)
    max_d = 68.0
    t_offset = (tot_dist / max_d) * (T_FIRE_END - T_IGNITE)
    ENV_BURN_TIMES.append(T_IGNITE + t_offset)

BURN_DURATION = 0.65

# Rose
ROSE_RAW = [
    (r"                 ####888888888####                  ", "petal_edge"),
    (r"             888 \  - %%%%%%%% 88888888 %%%         ", "petal"),
    (r"          888% %88% %8888888888888888888 %%% %888   ", "petal"),
    (r"        8888 888% 8888 888888 88 8888 88888 8888    ", "petal_hi"),
    (r"       888 %88 888 888 8888888 8888 888888 88888    ", "petal_hi"),
    (r"       %888 888 888 888 8888888 8888 8888 888888    ", "petal_hi"),
    (r"       %%8888 8888 8888 8888888 8888 8888 888888    ", "petal"),
    (r"       %%%88888 8888 88888888888 88888 888888888    ", "petal"),
    (r"       %8888888888888888888888888888888888888888    ", "petal"),
    (r"        %88888888888888888888888888888888888888     ", "petal"),
    (r"         %888888888888888888888888888888888888      ", "petal"),
    (r"           %888888888888888888888888888888888       ", "petal"),
    (r"             %88888888888888888888888888888         ", "petal"),
    (r"                %88888888888888888888888            ", "petal"),
    (r"                    %88888888888888                 ", "petal_edge"),
    (r"                %#%   .   ||   .   %#%              ", "leaf"),
    (r"             \ %%%%%% /   ||   \ %%%%%% /           ", "leaf"),
    (r"            \\ %%%%%%%    ||    %%%%%%% //          ", "leaf"),
    (r"             \\ %%%%%%    ||    %%%%%% //           ", "leaf"),
    (r"               %#% %%%    ||    %%% %#%             ", "leaf"),
    (r"                   %#%    ||    %#%                 ", "leaf"),
    (r"                          ||                        ", "stem"),
    (r"                         //                         ", "stem"),
    (r"                 \ %%%%%%//                         ", "leaf"),
    (r"                \\ %%%%%%%||                        ", "leaf"),
    (r"                 \\ %%%%%%||                        ", "leaf"),
    (r"                   %%%%%% ||                        ", "leaf"),
    (r"                          || %%%%%% /               ", "leaf"),
    (r"                          ||%%%%%%% //              ", "leaf"),
    (r"                         // %%%%%% //               ", "leaf"),
    (r"                        //    %#%                   ", "leaf"),
    (r"                        ||                          ", "stem"),
    (r"                        ||                          ", "stem"),
    (r"                       //                           ", "stem"),
    (r"                      //                            ", "stem"),
    (r"                      ||                            ", "stem"),
]

ROSE_START_ROW = 6
ROSE_START_COL = (COLS - len(ROSE_RAW[0][0])) // 2

ROSE_CELLS = []
ROSE_CELL_POSITIONS = set()
for r_idx, (line, ptype) in enumerate(ROSE_RAW):
    r = ROSE_START_ROW + r_idx
    for c_idx, ch in enumerate(line):
        if ch == ' ':
            continue
        c = ROSE_START_COL + c_idx
        ROSE_CELLS.append((r, c, ch, ptype, r_idx, c_idx))
        ROSE_CELL_POSITIONS.add((r, c))

T_ROSE_START = 4.2
T_ROSE_FULL = 7.0
T_PORTRAIT_START = 8.8
T_PORTRAIT_FULL = 11.2

PORTRAIT_OX = (WIDTH - PORTRAIT_COLS * PCW) // 2
PORTRAIT_OY = (HEIGHT - PORTRAIT_ROWS * PCH) // 2


def render_state_at_time(t, theme_mode="gold", force_portrait=False):
    screen.fill(BG_COLOR)

    # 1. Background stars
    for i in range(45):
        sr = int((math.sin(i * 17.3 + t * 0.15) * 0.5 + 0.5) * ROWS)
        sc = int((math.cos(i * 31.7 + t * 0.12) * 0.5 + 0.5) * COLS)
        twinkle = math.sin(t * 2.8 + i) * 0.5 + 0.5
        if twinkle > 0.35:
            s_char = '.' if twinkle < 0.75 else '*'
            s_col = lerp_color((18, 22, 36), (110, 150, 210), twinkle)
            glyph = get_glyph(s_char, s_col)
            screen.blit(glyph, (sc * CW, sr * CH))

    # 2. Raios Anamórficos
    if t > T_ROSE_START and not force_portrait:
        rose_progress = min(1.0, max(0.0, (t - T_ROSE_START) / (T_ROSE_FULL - T_ROSE_START)))
        if rose_progress > 0.40:
            flare_alpha = min(1.0, (rose_progress - 0.40) / 0.60)
            if t >= T_PORTRAIT_START:
                flare_alpha = 0.55 + 0.25 * math.sin(t * 2.0)
            beam_rows = [ROSE_START_ROW + 3, ROSE_START_ROW + 5, ROSE_START_ROW + 7, ROSE_START_ROW + 9]
            center_c = ROSE_START_COL + 25
            for b_idx, br in enumerate(beam_rows):
                wobble = math.sin(t * 3.8 + b_idx * 1.4) * 0.2 + 0.8
                for bc in range(COLS):
                    if (br, bc) not in ROSE_CELL_POSITIONS:
                        dc = abs(bc - center_c)
                        intensity = math.exp(-dc * 0.055) * flare_alpha * wobble
                        if intensity > 0.08:
                            if intensity > 0.45:
                                b_char = '='
                                b_col = lerp_color((50, 150, 255), (210, 240, 255), (intensity - 0.45) / 0.55)
                            elif intensity > 0.2:
                                b_char = '-'
                                b_col = lerp_color((20, 60, 180), (50, 150, 255), (intensity - 0.2) / 0.25)
                            else:
                                b_char = '.'
                                b_col = lerp_color((12, 30, 90), (20, 60, 180), intensity / 0.2)
                            glyph = get_glyph(b_char, b_col)
                            screen.blit(glyph, (bc * CW, br * CH))

    # 3. Rose
    rose_fade = 1.0
    if t >= T_PORTRAIT_START and not force_portrait:
        rose_fade = max(0.0, 1.0 - (t - T_PORTRAIT_START) / 1.4)

    if t > T_ROSE_START and rose_fade > 0.01 and not force_portrait:
        pulse = 1.0 + 0.08 * math.sin(t * 3.2)
        for (r, c, ch, ptype, r_idx, c_idx) in ROSE_CELLS:
            dist_center = math.sqrt((r_idx - 10)**2 + (c_idx - 25)**2)
            cell_rev_t = T_ROSE_START + (dist_center / 34.0) * (T_ROSE_FULL - T_ROSE_START)
            if t >= cell_rev_t:
                local_p = min(1.0, (t - cell_rev_t) / 1.1)
                if ptype == "petal_hi":
                    base_col = (255, 65, 105)
                elif ptype == "petal":
                    base_col = (225, 25, 60)
                elif ptype == "petal_edge":
                    base_col = (165, 15, 45)
                elif ptype == "stem":
                    base_col = (40, 185, 75)
                elif ptype == "leaf":
                    base_col = (30, 150, 65) if ch in ('\\', '/') else (50, 225, 105)
                else:
                    base_col = (200, 200, 200)

                if local_p < 0.4:
                    col = lerp_color((255, 235, 110), (255, 95, 30), local_p / 0.4)
                else:
                    col = lerp_color((255, 95, 30), base_col, (local_p - 0.4) / 0.6)

                if "petal" in ptype:
                    col = (min(255, int(col[0] * pulse)), min(255, int(col[1] * pulse)), min(255, int(col[2] * pulse)))
                if rose_fade < 1.0:
                    col = (int(col[0] * rose_fade), int(col[1] * rose_fade), int(col[2] * rose_fade))

                glyph = get_glyph(ch, col)
                screen.blit(glyph, (c * CW, r * CH))

    # 4. Envelope
    if not force_portrait and t < T_FIRE_END + BURN_DURATION:
        for idx, (r, c, ch, default_col, ctype) in enumerate(ENVELOPE_CELLS):
            b_t = ENV_BURN_TIMES[idx]
            if t < b_t:
                glyph = get_glyph(ch, default_col)
                screen.blit(glyph, (c * CW, r * CH))
            elif t < b_t + BURN_DURATION:
                burn_p = (t - b_t) / BURN_DURATION
                f_col = get_fire_color(burn_p)
                f_chars = ['#', '*', '&', '%', '^', '!', '+']
                f_ch = f_chars[int((r * 5 + c * 11 + t * 30)) % len(f_chars)]
                glyph = get_glyph(f_ch, f_col)
                screen.blit(glyph, (c * CW, r * CH))

    # 5. FOTO REAL ARREDONDADA
    if t >= T_PORTRAIT_START or force_portrait:
        prog = 1.0 if force_portrait else min(1.0, max(0.0, (t - T_PORTRAIT_START) / 1.5))
        alpha = int(255 * prog)

        pulse = 1.0 + 0.018 * math.sin(t * 2.5)
        cur_w = int(photo_orig_w * pulse)
        cur_h = int(photo_orig_h * pulse)
        cur_radius = int(PHOTO_RADIUS * pulse)

        if theme_mode == "ruby":
            ring_core = (255, 200, 220)
            ring_mid = (255, 60, 110)
            ring_edge = (160, 20, 65)
            halo_color = (255, 50, 100)
            title_col = (255, 185, 215)
        elif theme_mode == "cyan":
            ring_core = (220, 250, 255)
            ring_mid = (0, 210, 255)
            ring_edge = (20, 80, 200)
            halo_color = (0, 160, 255)
            title_col = (160, 240, 255)
        else:  # gold
            ring_core = (255, 235, 175)
            ring_mid = (255, 160, 60)
            ring_edge = (180, 40, 70)
            halo_color = (255, 130, 80)
            title_col = (255, 215, 160)

        # Halo
        halo_surf = pygame.Surface((cur_w + 90, cur_h + 90), pygame.SRCALPHA)
        hcx, hcy = (cur_w + 90) // 2, (cur_h + 90) // 2
        halo_intensity = int(alpha * (0.35 + 0.15 * math.sin(t * 2.5)))
        for r_off in range(40, 0, -2):
            a = int(halo_intensity * (1.0 - r_off / 40.0) ** 1.5)
            if a > 0:
                pygame.draw.circle(halo_surf, (*halo_color, a), (hcx, hcy), cur_radius + r_off)
        screen.blit(halo_surf, (PHOTO_CX - hcx, PHOTO_CY - hcy))

        # Photo
        photo_scaled = pygame.transform.smoothscale(photo_real_surf, (cur_w, cur_h))
        if alpha < 255:
            photo_scaled.set_alpha(alpha)
        screen.blit(photo_scaled, (PHOTO_CX - cur_w // 2, PHOTO_CY - cur_h // 2))

        # Rings
        pygame.draw.circle(screen, ring_core, (PHOTO_CX, PHOTO_CY), cur_radius, width=2)
        pygame.draw.circle(screen, ring_mid, (PHOTO_CX, PHOTO_CY), cur_radius + 1, width=1)
        pygame.draw.circle(screen, ring_edge, (PHOTO_CX, PHOTO_CY), cur_radius + 2, width=1)

        # Captions
        caption1 = title_font.render("♥  Para Sempre a Razão do Meu Sorriso  ♥", True, title_col)
        screen.blit(caption1, (WIDTH // 2 - caption1.get_width() // 2, PHOTO_CY - cur_radius - 42))

        caption2 = subtitle_font.render("♥  Com todo o meu amor e carinho  ♥", True, (245, 200, 150))
        screen.blit(caption2, (WIDTH // 2 - caption2.get_width() // 2, PHOTO_CY + cur_radius + 24))

    # Hint footer
    hint_surf = font.render("[H] Ajuda  |  [V] Rosa/Foto  |  [T] Moldura  |  [1/2/3] Fases  |  [S] Salvar PNG", True, (80, 90, 120))
    screen.blit(hint_surf, (WIDTH // 2 - hint_surf.get_width() // 2, HEIGHT - 24))

    return screen


# Gerar e salvar frames finais
renders = [
    (1.0, "final_1.0s_envelope.png", "gold", False),
    (2.2, "final_2.2s_ignition.png", "gold", False),
    (3.8, "final_3.8s_combustion.png", "gold", False),
    (5.4, "final_5.4s_emergence.png", "gold", False),
    (8.0, "final_8.0s_rose_bloom.png", "gold", False),
    (9.8, "final_9.8s_portrait_emergence.png", "gold", False),
    (12.0, "final_12.0s_portrait_complete.png", "gold", False),
    (12.0, "final_portrait_ruby.png", "ruby", True),
    (12.0, "final_portrait_cyberpunk.png", "cyan", True),
]

for ts, filename, mode, force in renders:
    out_surf = render_state_at_time(ts, theme_mode=mode, force_portrait=force)
    out_path = os.path.join(DIR, filename)
    pygame.image.save(out_surf, out_path)
    print(f"Saved: {filename}")

pygame.quit()
print("All preview keyframes generated successfully.")
