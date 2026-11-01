#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
             LETTER FOR YOU  ♥  (Letter -> Rose -> Real Rounded Photo)
=============================================================================
Projeto de arte computacional e animação procedimental em Python + Pygame.
Simula uma carta de amor com selo de cera que pega fogo organicamente,
liberando fagulhas físicas e fumaça, se transforma em uma rosa radiante
com feixes de luz anamórficos e culmina na revelação da foto real arredondada
com moldura luminosa, feixes de luz, partículas estelares e trilha sonora.

Comandos Interativos:
  [ESPAÇO] ou [R] : Reiniciar animação do início
  [1]             : Exibir Carta (Envelope)
  [2]             : Exibir Rosa em Chamas
  [3]             : Exibir Foto Real Arredondada
  [V] ou [TAB]    : Alternar visualização fixa (Carta <-> Rosa <-> Foto)
  [T]             : Mudar estilo da Moldura da Foto (Ouro, Rubi, Ciano, Modo Código)
  [C]             : Mudar tema de cores da Rosa (Carmesim, Dourado, Ciano, Ametista)
  [S]             : Salvar captura de tela em PNG de alta resolução
  [P]             : Pausar / Continuar
  [M]             : Ativar / Desativar áudio (Mute)
  [F]             : Alternar Tela Cheia / Janela
  [H]             : Mostrar / Ocultar menu de ajuda HUD
  [ESC] ou [Q]    : Sair
=============================================================================
"""

import os
import sys
import math
import random
import time
import pygame

# Importação dos dados pré-computados do retrato em códigos (para o modo código opcional)
try:
    from portrait_data import PORTRAIT_COLS, PORTRAIT_ROWS, PORTRAIT_CELLS
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from portrait_data import PORTRAIT_COLS, PORTRAIT_ROWS, PORTRAIT_CELLS

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES DE PERSONALIZAÇÃO
# ---------------------------------------------------------------------------
TITLE = "For You ♥"
SENDER_NAME = "Seu Amor"
RECIPIENT_NAME = "A Pessoa Mais Especial Deste Mundo"
LOVE_MESSAGE_1 = "Mesmo que as palavras se queimem com o tempo, o meu"
LOVE_MESSAGE_2 = "sentimento por você floresce como a mais bela rosa."
PORTRAIT_CAPTION = "♥  Para Sempre a Razão do Meu Sorriso  ♥"
PORTRAIT_SUBTITLE = "♥  Com todo o meu amor e carinho  ♥"

# ---------------------------------------------------------------------------
# CONSTANTES DE DIMENSÃO E GRADE MONOESPAÇADA
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 720, 780
FONT_SIZE = 16
PORTRAIT_FONT_SIZE = 12
FPS = 60

D2R = math.pi / 180.0

# Linha do tempo da animação (em segundos)
T_IDLE_END       = 2.0   # Fim do estado de repouso da carta
T_IGNITE         = 2.0   # Momento exato da ignição
T_FIRE_END       = 5.8   # Fim da combustão do papel
T_ROSE_START     = 4.2   # Início do surgimento da Rosa sob as cinzas
T_ROSE_FULL      = 7.0   # Rosa totalmente desabrochada com raios de luz
T_PORTRAIT_START = 8.8   # Início da revelação da Foto Real Arredondada
T_PORTRAIT_FULL  = 11.2  # Foto totalmente revelada e radiante

# ---------------------------------------------------------------------------
# PALETAS DE CORES E TEMAS
# ---------------------------------------------------------------------------
COLOR_BG = (7, 8, 12)

FIRE_PALETTE = [
    (255, 255, 245),  # 0.00: Núcleo incandescente (Branco-quente)
    (255, 235, 60),   # 0.20: Amarelo vivo
    (255, 130, 20),   # 0.45: Laranja chama
    (225, 40, 15),    # 0.70: Vermelho brasa viva
    (90, 25, 20),     # 0.88: Brasa escura / Carvão
    (35, 22, 28),     # 1.00: Fuligem / Cinza apagada
]

THEMES = [
    {
        "name": "Rubi Carmesim (Clássico)",
        "petal_hi": (255, 65, 105),
        "petal": (225, 25, 60),
        "petal_edge": (165, 15, 45),
        "stem": (40, 185, 75),
        "leaf": (50, 225, 105),
        "leaf_dark": (30, 150, 65),
        "flare_core": (210, 240, 255),
        "flare_beam": (50, 150, 255),
        "flare_edge": (20, 60, 180),
        "embers": (255, 180, 120),
    },
    {
        "name": "Ouro Imperial (Golden Sun)",
        "petal_hi": (255, 230, 120),
        "petal": (245, 180, 40),
        "petal_edge": (190, 120, 20),
        "stem": (160, 180, 60),
        "leaf": (190, 215, 80),
        "leaf_dark": (120, 140, 40),
        "flare_core": (255, 250, 210),
        "flare_beam": (255, 200, 70),
        "flare_edge": (180, 110, 20),
        "embers": (255, 235, 150),
    },
    {
        "name": "Ciano Neon (Cyberpunk)",
        "petal_hi": (140, 255, 255),
        "petal": (0, 215, 235),
        "petal_edge": (0, 145, 185),
        "stem": (120, 70, 220),
        "leaf": (160, 110, 255),
        "leaf_dark": (90, 45, 175),
        "flare_core": (230, 245, 255),
        "flare_beam": (0, 190, 255),
        "flare_edge": (0, 80, 190),
        "embers": (150, 240, 255),
    },
    {
        "name": "Ametista Real (Violet Bloom)",
        "petal_hi": (240, 160, 255),
        "petal": (195, 70, 235),
        "petal_edge": (135, 30, 175),
        "stem": (45, 175, 120),
        "leaf": (65, 220, 155),
        "leaf_dark": (30, 130, 85),
        "flare_core": (250, 220, 255),
        "flare_beam": (190, 100, 255),
        "flare_edge": (110, 40, 190),
        "embers": (230, 180, 255),
    },
]

PORTRAIT_THEMES = [
    {
        "name": "Foto Real (Ouro Imperial & Carmesim)",
        "mode": "gold",
        "ring_core": (255, 235, 175),
        "ring_mid": (255, 160, 60),
        "ring_edge": (180, 40, 70),
        "halo": (255, 130, 80),
        "title_color": (255, 215, 160),
    },
    {
        "name": "Foto Real (Rubi Escarlate)",
        "mode": "ruby",
        "ring_core": (255, 200, 220),
        "ring_mid": (255, 60, 110),
        "ring_edge": (160, 20, 65),
        "halo": (255, 50, 100),
        "title_color": (255, 185, 215),
    },
    {
        "name": "Foto Real (Ciano Neon Cyberpunk)",
        "mode": "cyan",
        "ring_core": (220, 250, 255),
        "ring_mid": (0, 210, 255),
        "ring_edge": (20, 80, 200),
        "halo": (0, 160, 255),
        "title_color": (160, 240, 255),
    },
    {
        "name": "Modo Arte em Códigos (ASCII / Code Matrix)",
        "mode": "code",
    },
]

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def get_fire_color(progress):
    p = max(0.0, min(0.999, progress)) * (len(FIRE_PALETTE) - 1)
    idx = int(p)
    frac = p - idx
    return lerp_color(FIRE_PALETTE[idx], FIRE_PALETTE[idx + 1], frac)

# ---------------------------------------------------------------------------
# MODELAGEM ASCII DA CARTA (ENVELOPE)
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
    "||   De: " + SENDER_NAME.ljust(48) + "♥   ||",
    "||   Para: " + RECIPIENT_NAME.ljust(50) + "||",
    r"||   -----------------------------------------------------   ||",
    "||   " + LOVE_MESSAGE_1.ljust(53) + "   ||",
    "||   " + LOVE_MESSAGE_2.ljust(53) + "   ||",
    r"||   -----------------------------------------------------   ||",
    r"||                                                           ||",
    r"||   Com todo o meu amor e carinho sempre...                 ||",
    r"||                                                           ||",
    r" \\_________________________________________________________// ",
    r"  \~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/  ",
]

# ---------------------------------------------------------------------------
# MODELAGEM ASCII DA ROSA
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# APLICAÇÃO PRINCIPAL
# ---------------------------------------------------------------------------
class LetterToRoseApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        # Ícone de coração para a barra de tarefas
        icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon_surf, (255, 30, 80), (11, 11), 8)
        pygame.draw.circle(icon_surf, (255, 30, 80), (21, 11), 8)
        pts = [(3, 14), (29, 14), (16, 29)]
        pygame.draw.polygon(icon_surf, (255, 30, 80), pts)
        try:
            pygame.display.set_icon(icon_surf)
        except Exception:
            pass

        self.width = WIDTH
        self.height = HEIGHT
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Fontes
        self.font = self.load_monospace_font(FONT_SIZE)
        self.cw, self.ch = self.font.size('A')
        self.cols = self.width // self.cw
        self.rows = self.height // self.ch

        self.portrait_font = self.load_monospace_font(PORTRAIT_FONT_SIZE)
        self.pcw, self.pch = self.portrait_font.size('A')

        self.title_font = self.load_monospace_font(16)
        self.subtitle_font = self.load_monospace_font(13)

        self.glyph_cache = {}
        self.portrait_glyph_cache = {}

        # Carregar Foto Real Arredondada
        self.load_real_photo()

        self.soundtrack = None
        self.audio_muted = False
        self.init_audio()

        self.current_theme_idx = 0
        self.theme = THEMES[self.current_theme_idx]

        self.portrait_theme_idx = 0
        self.portrait_theme = PORTRAIT_THEMES[self.portrait_theme_idx]

        self.force_view = None  # None (automático), 'letter', 'rose', 'portrait'
        self.show_help = False
        self.screenshot_toast = 0.0

        self.setup_cells()
        self.reset_animation()

    def load_real_photo(self):
        photo_path = os.path.join(os.path.dirname(__file__), "photo_rounded.png")
        if not os.path.exists(photo_path):
            photo_path = os.path.join(os.path.dirname(__file__), "photo_circle.png")
        try:
            self.photo_real_surf = pygame.image.load(photo_path).convert_alpha()
            self.photo_orig_w, self.photo_orig_h = self.photo_real_surf.get_size()
        except Exception:
            # Fallback seguro caso imagem falhe
            self.photo_real_surf = pygame.Surface((400, 400), pygame.SRCALPHA)
            pygame.draw.circle(self.photo_real_surf, (255, 120, 160), (200, 200), 200)
            self.photo_orig_w, self.photo_orig_h = 400, 400

    def load_monospace_font(self, size):
        candidates = ['consolas', 'cascadia code', 'courier new', 'dejavu sans mono', 'monospace']
        for name in candidates:
            try:
                f = pygame.font.SysFont(name, size, bold=True)
                if f:
                    return f
            except Exception:
                continue
        return pygame.font.Font(None, size)

    def init_audio(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            audio_path = os.path.join(os.path.dirname(__file__), "audio.wav")
            if os.path.exists(audio_path):
                self.soundtrack = pygame.mixer.Sound(audio_path)
                self.soundtrack.play(loops=-1)
                self.soundtrack.set_volume(0.85)
        except Exception:
            self.soundtrack = None

    def get_glyph(self, char, color):
        qr = (max(0, min(255, color[0])) // 8) * 8
        qg = (max(0, min(255, color[1])) // 8) * 8
        qb = (max(0, min(255, color[2])) // 8) * 8
        key = (char, (qr, qg, qb))
        if key not in self.glyph_cache:
            try:
                surf = self.font.render(char, True, (qr, qg, qb))
            except Exception:
                surf = self.font.render('?', True, (qr, qg, qb))
            self.glyph_cache[key] = surf
        return self.glyph_cache[key]

    def get_portrait_glyph(self, char, color):
        qr = (max(0, min(255, color[0])) // 8) * 8
        qg = (max(0, min(255, color[1])) // 8) * 8
        qb = (max(0, min(255, color[2])) // 8) * 8
        key = (char, (qr, qg, qb))
        if key not in self.portrait_glyph_cache:
            try:
                surf = self.portrait_font.render(char, True, (qr, qg, qb))
            except Exception:
                surf = self.portrait_font.render('?', True, (qr, qg, qb))
            self.portrait_glyph_cache[key] = surf
        return self.portrait_glyph_cache[key]

    def setup_cells(self):
        # 1. ENVELOPE
        self.env_start_row = 12
        self.env_start_col = (self.cols - len(ENVELOPE_RAW[0])) // 2

        self.envelope_cells = []
        for r_idx, line in enumerate(ENVELOPE_RAW):
            r = self.env_start_row + r_idx
            for c_idx, ch in enumerate(line):
                if ch == ' ':
                    continue
                c = self.env_start_col + c_idx
                if ch == '♥':
                    color = (255, 35, 95)
                    ctype = 'heart'
                elif ch in ('.', ':', "'") and r_idx < 10 and 20 < c_idx < 45:
                    color = (245, 50, 110)
                    ctype = 'seal'
                elif r_idx in (11, 12):
                    color = (255, 230, 190)
                    ctype = 'text_hi'
                elif r_idx in (14, 15, 18):
                    color = (225, 205, 175)
                    ctype = 'text'
                elif ch in ('/', '\\', '_', '~', '|', '-'):
                    color = (195, 180, 155)
                    ctype = 'border'
                else:
                    color = (175, 160, 135)
                    ctype = 'paper'
                self.envelope_cells.append((r, c, ch, color, ctype))

        self.ig_row = self.env_start_row + len(ENVELOPE_RAW) - 3
        self.ig_col = self.env_start_col + len(ENVELOPE_RAW[0]) - 8

        self.env_burn_times = []
        for cell in self.envelope_cells:
            r, c = cell[0], cell[1]
            dr = (self.ig_row - r) * 1.0
            dc = (self.ig_col - c) * 0.8
            dist = math.sqrt(dr * dr + dc * dc)
            jitter = math.sin(r * 0.8 + c * 0.5) * 2.8 + math.cos(r * 1.4 - c * 0.9) * 2.0
            tot_dist = max(0.0, dist + jitter)
            max_d = 68.0
            t_offset = (tot_dist / max_d) * (T_FIRE_END - T_IGNITE)
            self.env_burn_times.append(T_IGNITE + t_offset)

        self.burn_duration = 0.65

        # 2. ROSA
        self.rose_start_row = 6
        self.rose_start_col = (self.cols - len(ROSE_RAW[0][0])) // 2

        self.rose_cells = []
        self.rose_cell_positions = set()
        for r_idx, (line, ptype) in enumerate(ROSE_RAW):
            r = self.rose_start_row + r_idx
            for c_idx, ch in enumerate(line):
                if ch == ' ':
                    continue
                c = self.rose_start_col + c_idx
                self.rose_cells.append((r, c, ch, ptype, r_idx, c_idx))
                self.rose_cell_positions.add((r, c))

        # 3. POSIÇÃO DA FOTO REAL ARREDONDADA
        self.photo_cx = self.width // 2
        self.photo_cy = self.height // 2 - 12
        self.photo_radius = self.photo_orig_w // 2

        # 4. RETRATO EM CÓDIGOS (MODO ALTERNATIVO)
        self.portrait_ox = (self.width - PORTRAIT_COLS * self.pcw) // 2
        self.portrait_oy = (self.height - PORTRAIT_ROWS * self.pch) // 2
        self.portrait_center_r = 23
        self.portrait_center_c = 43

        self.portrait_reveal_times = []
        for (r, c, ch, rgb) in PORTRAIT_CELLS:
            dr = (r - self.portrait_center_r) * 1.5
            dc = (c - self.portrait_center_c) * 1.0
            dist = math.sqrt(dr * dr + dc * dc)
            t_offset = (dist / 48.0) * (T_PORTRAIT_FULL - T_PORTRAIT_START - 0.7)
            self.portrait_reveal_times.append(T_PORTRAIT_START + t_offset)

    def reset_animation(self):
        self.anim_time = 0.0
        self.paused = False
        self.burst_done = False
        self.portrait_burst_done = False
        self.force_view = None
        self.sparks = []
        self.smoke = []

        if self.soundtrack and not self.audio_muted:
            self.soundtrack.stop()
            self.soundtrack.play(loops=-1)

    def update_particles(self, dt):
        live_sparks = []
        for s in self.sparks:
            s[4] += dt
            if s[4] < s[5]:
                s[0] += s[2] * dt
                s[1] += s[3] * dt
                s[3] += s[6] * dt
                s[2] *= 0.96
                s[3] *= 0.98
                live_sparks.append(s)
        self.sparks = live_sparks
        if len(self.sparks) > 1600:
            del self.sparks[:len(self.sparks) - 1600]

        live_smoke = []
        for sm in self.smoke:
            sm[4] += dt
            if sm[4] < sm[5]:
                sm[0] += sm[2] * dt
                sm[1] += sm[3] * dt
                sm[2] += math.sin(sm[4] * 4.0) * 8.0 * dt
                live_smoke.append(sm)
        self.smoke = live_smoke
        if len(self.smoke) > 300:
            del self.smoke[:len(self.smoke) - 300]

    def render(self, dt):
        t = self.anim_time
        if self.force_view == 'letter':
            t = 1.0
        elif self.force_view == 'rose':
            t = 7.5
        elif self.force_view == 'portrait':
            t = 12.0

        self.screen.fill(COLOR_BG)

        # 1. Poeira estelar / Estrelas cintilantes no fundo
        for i in range(45):
            sr = int((math.sin(i * 17.3 + t * 0.15) * 0.5 + 0.5) * self.rows)
            sc = int((math.cos(i * 31.7 + t * 0.12) * 0.5 + 0.5) * self.cols)
            twinkle = math.sin(t * 2.8 + i) * 0.5 + 0.5
            if twinkle > 0.35:
                s_char = '.' if twinkle < 0.75 else '*'
                s_col = lerp_color((18, 22, 36), (110, 150, 210), twinkle)
                glyph = self.get_glyph(s_char, s_col)
                self.screen.blit(glyph, (sc * self.cw, sr * self.ch))

        # 2. Raios Anamórficos Horizontais
        if t > T_ROSE_START:
            rose_progress = min(1.0, max(0.0, (t - T_ROSE_START) / (T_ROSE_FULL - T_ROSE_START)))
            if rose_progress > 0.40:
                in_portrait = (t >= T_PORTRAIT_START or self.force_view == 'portrait')
                flare_alpha = min(1.0, (rose_progress - 0.40) / 0.60)
                if in_portrait:
                    flare_alpha = 0.55 + 0.25 * math.sin(t * 2.0)

                beam_rows = [
                    self.rose_start_row + 3,
                    self.rose_start_row + 5,
                    self.rose_start_row + 7,
                    self.rose_start_row + 9,
                ]
                center_c = self.rose_start_col + 25
                for b_idx, br in enumerate(beam_rows):
                    wobble = math.sin(t * 3.8 + b_idx * 1.4) * 0.2 + 0.8
                    for bc in range(self.cols):
                        if (br, bc) not in self.rose_cell_positions:
                            dc = abs(bc - center_c)
                            intensity = math.exp(-dc * 0.055) * flare_alpha * wobble
                            if intensity > 0.08:
                                if intensity > 0.45:
                                    b_char = '='
                                    b_col = lerp_color(self.theme["flare_beam"], self.theme["flare_core"], (intensity - 0.45) / 0.55)
                                elif intensity > 0.2:
                                    b_char = '-'
                                    b_col = lerp_color(self.theme["flare_edge"], self.theme["flare_beam"], (intensity - 0.2) / 0.25)
                                else:
                                    b_char = '.'
                                    b_col = lerp_color((12, 30, 90), self.theme["flare_edge"], intensity / 0.2)

                                glyph = self.get_glyph(b_char, b_col)
                                self.screen.blit(glyph, (bc * self.cw, br * self.ch))

        # 3. Renderização da Rosa (com fade suave quando o Retrato emerge)
        rose_fade = 1.0
        if t >= T_PORTRAIT_START and self.force_view != 'rose':
            rose_fade = max(0.0, 1.0 - (t - T_PORTRAIT_START) / 1.4)

        if t > T_ROSE_START and rose_fade > 0.01:
            pulse = 1.0 + 0.08 * math.sin(t * 3.2)

            for (r, c, ch, ptype, r_idx, c_idx) in self.rose_cells:
                dist_center = math.sqrt((r_idx - 10)**2 + (c_idx - 25)**2)
                cell_rev_t = T_ROSE_START + (dist_center / 34.0) * (T_ROSE_FULL - T_ROSE_START)

                if t >= cell_rev_t:
                    local_p = min(1.0, (t - cell_rev_t) / 1.1)

                    if ptype == "petal_hi":
                        base_col = self.theme["petal_hi"]
                    elif ptype == "petal":
                        base_col = self.theme["petal"]
                    elif ptype == "petal_edge":
                        base_col = self.theme["petal_edge"]
                    elif ptype == "stem":
                        base_col = self.theme["stem"]
                    elif ptype == "leaf":
                        base_col = self.theme["leaf_dark"] if ch in ('\\', '/') else self.theme["leaf"]
                    else:
                        base_col = (200, 200, 200)

                    if local_p < 0.4:
                        ember_p = local_p / 0.4
                        col = lerp_color((255, 235, 110), (255, 95, 30), ember_p)
                    else:
                        cool_p = (local_p - 0.4) / 0.6
                        col = lerp_color((255, 95, 30), base_col, cool_p)

                    if "petal" in ptype:
                        col = (
                            min(255, int(col[0] * pulse)),
                            min(255, int(col[1] * pulse)),
                            min(255, int(col[2] * pulse)),
                        )

                    if rose_fade < 1.0:
                        col = (
                            int(col[0] * rose_fade),
                            int(col[1] * rose_fade),
                            int(col[2] * rose_fade),
                        )

                    glyph = self.get_glyph(ch, col)
                    self.screen.blit(glyph, (c * self.cw, r * self.ch))

        # 4. Renderização do Envelope & Combustão
        if self.force_view != 'portrait' and self.force_view != 'rose':
            active_front = []
            for idx, (r, c, ch, default_col, ctype) in enumerate(self.envelope_cells):
                b_t = self.env_burn_times[idx]
                if t < b_t:
                    flicker = 1.0 + 0.04 * math.sin(t * 5.0 + r + c)
                    col = (
                        min(255, int(default_col[0] * flicker)),
                        min(255, int(default_col[1] * flicker)),
                        min(255, int(default_col[2] * flicker)),
                    )
                    glyph = self.get_glyph(ch, col)
                    self.screen.blit(glyph, (c * self.cw, r * self.ch))
                elif t < b_t + self.burn_duration:
                    burn_p = (t - b_t) / self.burn_duration
                    f_col = get_fire_color(burn_p)
                    f_chars = ['#', '*', '&', '%', '^', '!', '+']
                    f_ch = f_chars[int((r * 5 + c * 11 + t * 30)) % len(f_chars)]
                    glyph = self.get_glyph(f_ch, f_col)
                    self.screen.blit(glyph, (c * self.cw, r * self.ch))
                    active_front.append((c * self.cw + self.cw // 2, r * self.ch + self.ch // 2))

            # Spawners de Ignição inicial
            if t >= T_IGNITE and not self.burst_done:
                self.burst_done = True
                ig_px = self.ig_col * self.cw
                ig_py = self.ig_row * self.ch
                for _ in range(160):
                    angle = random.uniform(-170, -10) * D2R
                    speed = random.uniform(120, 580)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    max_age = random.uniform(0.7, 1.8)
                    grav = random.uniform(150, 400)
                    self.sparks.append([ig_px, ig_py, vx, vy, 0.0, max_age, grav])

            if active_front and t < T_FIRE_END:
                n_sparks = int(140 * dt * min(1.0, len(active_front) / 45.0) + random.random())
                for _ in range(n_sparks):
                    fx, fy = random.choice(active_front)
                    angle = random.uniform(-135, -45) * D2R
                    speed = random.uniform(80, 420)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    max_age = random.uniform(0.6, 1.9)
                    grav = random.uniform(180, 480)
                    self.sparks.append([fx, fy, vx, vy, 0.0, max_age, grav])

                if random.random() < 24.0 * dt:
                    fx, fy = random.choice(active_front)
                    self.smoke.append([
                        fx, fy - 8,
                        random.uniform(-18, 18), -random.uniform(30, 75),
                        0.0, random.uniform(1.8, 3.2),
                        random.uniform(8, 22), (60, 50, 60)
                    ])

        # 5. Renderização da FOTO REAL ARREDONDADA (Grand Finale)
        if (t >= T_PORTRAIT_START or self.force_view == 'portrait') and self.force_view != 'rose' and self.force_view != 'letter':
            # Burst de partículas na transição
            if not self.portrait_burst_done:
                self.portrait_burst_done = True
                for _ in range(140):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(90, 420)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    max_age = random.uniform(1.2, 2.8)
                    self.sparks.append([self.photo_cx, self.photo_cy, vx, vy, 0.0, max_age, 25.0])

            theme_mode = self.portrait_theme["mode"]

            if theme_mode == "code":
                # Modo alternativo em código/ASCII
                pulse = 1.0 + 0.06 * math.sin(t * 2.8)
                for idx, (r, c, ch, rgb) in enumerate(PORTRAIT_CELLS):
                    rev_t = 0.0 if self.force_view == 'portrait' else self.portrait_reveal_times[idx]
                    if t >= rev_t:
                        col = (
                            min(255, int(rgb[0] * pulse)),
                            min(255, int(rgb[1] * pulse)),
                            min(255, int(rgb[2] * pulse)),
                        )
                        px = self.portrait_ox + c * self.pcw
                        py = self.portrait_oy + r * self.pch
                        glyph = self.get_portrait_glyph(ch, col)
                        self.screen.blit(glyph, (px, py))
            else:
                # MODO PRINCIPAL: FOTO REAL ARREDONDADA COM MOLDURA LUMINOSA
                prog = 1.0 if self.force_view == 'portrait' else min(1.0, max(0.0, (t - T_PORTRAIT_START) / 1.5))
                alpha = int(255 * prog)

                # Pulsação suave de respiração (escala 1.0 a 1.025)
                pulse = 1.0 + 0.018 * math.sin(t * 2.5)
                cur_w = int(self.photo_orig_w * pulse)
                cur_h = int(self.photo_orig_h * pulse)
                cur_radius = int(self.photo_radius * pulse)

                # 1. Halo luminoso difuso atrás da foto
                halo_color = self.portrait_theme["halo"]
                halo_surf = pygame.Surface((cur_w + 90, cur_h + 90), pygame.SRCALPHA)
                hcx, hcy = (cur_w + 90) // 2, (cur_h + 90) // 2
                halo_intensity = int(alpha * (0.35 + 0.15 * math.sin(t * 2.5)))
                for r_off in range(40, 0, -2):
                    a = int(halo_intensity * (1.0 - r_off / 40.0) ** 1.5)
                    if a > 0:
                        pygame.draw.circle(halo_surf, (*halo_color, a), (hcx, hcy), cur_radius + r_off)
                self.screen.blit(halo_surf, (self.photo_cx - hcx, self.photo_cy - hcy))

                # 2. Renderização da Foto Real Arredondada
                if cur_w == self.photo_orig_w and cur_h == self.photo_orig_h:
                    photo_to_draw = self.photo_real_surf.copy()
                else:
                    photo_to_draw = pygame.transform.smoothscale(self.photo_real_surf, (cur_w, cur_h))

                if alpha < 255:
                    photo_to_draw.set_alpha(alpha)

                draw_ox = self.photo_cx - cur_w // 2
                draw_oy = self.photo_cy - cur_h // 2
                self.screen.blit(photo_to_draw, (draw_ox, draw_oy))

                # 3. Anéis de moldura luminosa concêntricos
                ring_core = self.portrait_theme["ring_core"]
                ring_mid = self.portrait_theme["ring_mid"]
                ring_edge = self.portrait_theme["ring_edge"]

                # Desenho dos anéis suavizados
                pygame.draw.circle(self.screen, ring_core, (self.photo_cx, self.photo_cy), cur_radius, width=2)
                pygame.draw.circle(self.screen, ring_mid, (self.photo_cx, self.photo_cy), cur_radius + 1, width=1)
                pygame.draw.circle(self.screen, ring_edge, (self.photo_cx, self.photo_cy), cur_radius + 2, width=1)

                # Anel de brilho externo pulsante
                outer_pulse_r = cur_radius + 5 + int(3 * math.sin(t * 3.5))
                outer_alpha = max(0, min(255, int(80 + 40 * math.sin(t * 3.5))))
                ring_surf = pygame.Surface((outer_pulse_r * 2 + 10, outer_pulse_r * 2 + 10), pygame.SRCALPHA)
                rcx = outer_pulse_r + 5
                pygame.draw.circle(ring_surf, (*ring_mid, outer_alpha), (rcx, rcx), outer_pulse_r, width=1)
                self.screen.blit(ring_surf, (self.photo_cx - rcx, self.photo_cy - rcx))

            # Legendas Românticas
            if t > T_PORTRAIT_START + 0.4 or self.force_view == 'portrait':
                cap_alpha = min(1.0, (t - (T_PORTRAIT_START + 0.4)) / 1.0) if self.force_view != 'portrait' else 1.0
                title_col = self.portrait_theme.get("title_color", (255, 215, 160))
                c_col = lerp_color((40, 40, 50), title_col, cap_alpha)

                caption_surf = self.title_font.render(PORTRAIT_CAPTION, True, c_col)
                self.screen.blit(caption_surf, (self.width // 2 - caption_surf.get_width() // 2, self.photo_cy - self.photo_radius - 42))

                sub_col = lerp_color((30, 30, 40), (245, 200, 150), cap_alpha)
                sub_surf = self.subtitle_font.render(PORTRAIT_SUBTITLE, True, sub_col)
                self.screen.blit(sub_surf, (self.width // 2 - sub_surf.get_width() // 2, self.photo_cy + self.photo_radius + 24))

            # Fagulhas mágicas e pirilampos orbitando a foto arredondada
            if random.random() < 35.0 * dt:
                angle = random.uniform(0, 2 * math.pi)
                rad = self.photo_radius + random.uniform(10, 85)
                self.sparks.append([
                    self.photo_cx + math.cos(angle) * rad,
                    self.photo_cy + math.sin(angle) * rad * 0.9,
                    random.uniform(-14, 14), -random.uniform(20, 60),
                    0.0, random.uniform(1.2, 2.5), -12.0
                ])

        # 6. Spawners contínuos da Rosa
        if 6.0 < t < T_PORTRAIT_START + 0.5 and (self.force_view is None or self.force_view == 'rose'):
            if random.random() < 35.0 * dt:
                angle = random.uniform(0, 2 * math.pi)
                rad = random.uniform(40, 140)
                rx = (self.rose_start_col + 25) * self.cw + math.cos(angle) * rad
                ry = (self.rose_start_row + 12) * self.ch + math.sin(angle) * rad * 0.7
                self.sparks.append([
                    rx, ry,
                    random.uniform(-15, 15), -random.uniform(20, 65),
                    0.0, random.uniform(1.2, 2.5), -15.0
                ])

        # 7. Desenho de Fagulhas e Fumaça
        for sm in self.smoke:
            sm_life = sm[4] / sm[5]
            sm_alpha = math.sin(sm_life * math.pi)
            if sm_alpha > 0.05:
                sm_col = lerp_color((15, 16, 22), (90, 75, 85), sm_alpha * 0.4)
                glyph = self.get_glyph('o' if sm_life < 0.5 else '.', sm_col)
                self.screen.blit(glyph, (int(sm[0]), int(sm[1])))

        for s in self.sparks:
            sp_life = s[4] / s[5]
            if sp_life < 1.0:
                sp_col = get_fire_color(sp_life * 0.8)
                sp_char = random.choice(['*', '.', '`', '+']) if sp_life < 0.6 else '.'
                glyph = self.get_glyph(sp_char, sp_col)
                self.screen.blit(glyph, (int(s[0]), int(s[1])))

        # 8. Notificação de captura de tela (Toast)
        if self.screenshot_toast > 0:
            self.screenshot_toast -= dt
            msg = "Captura de tela salva com sucesso! (PNG)"
            t_surf = self.title_font.render(msg, True, (120, 255, 160))
            bg_rect = pygame.Rect(self.width // 2 - t_surf.get_width() // 2 - 14, 18, t_surf.get_width() + 28, 30)
            pygame.draw.rect(self.screen, (20, 40, 30), bg_rect, border_radius=6)
            pygame.draw.rect(self.screen, (80, 220, 130), bg_rect, width=1, border_radius=6)
            self.screen.blit(t_surf, (self.width // 2 - t_surf.get_width() // 2, 24))

        # 9. Overlay de Ajuda / HUD
        if self.show_help:
            self.render_hud()
        else:
            hint = "[H] Ajuda  |  [V] Rosa/Foto  |  [T] Moldura  |  [1/2/3] Fases  |  [S] Salvar PNG"
            h_glyph = self.get_glyph(hint, (80, 90, 120))
            self.screen.blit(h_glyph, (self.width // 2 - h_glyph.get_width() // 2, self.height - 24))

    def save_screenshot(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        path = os.path.join(os.path.dirname(__file__), filename)
        try:
            pygame.image.save(self.screen, path)
            self.screenshot_toast = 2.5
        except Exception:
            pass

    def render_hud(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 195))
        self.screen.blit(overlay, (0, 0))

        v_mode_name = "Automático (Carta -> Rosa -> Foto)"
        if self.force_view == 'letter':
            v_mode_name = "Carta Intacta"
        elif self.force_view == 'rose':
            v_mode_name = "Rosa em Chamas"
        elif self.force_view == 'portrait':
            v_mode_name = "Foto Real Arredondada"

        lines = [
            f"=== {TITLE} - COMANDOS INTERATIVOS ===",
            "",
            "  [ESPAÇO] ou [R]  : Reiniciar animação completa do início",
            "  [1]              : Saltar para a Carta (Envelope)",
            "  [2]              : Saltar para a Rosa em Chamas",
            "  [3]              : Saltar para a Foto Real Arredondada",
            f"  [V] ou [TAB]     : Modo de Exibição: {v_mode_name}",
            f"  [T]              : Estilo da Moldura: {self.portrait_theme['name']}",
            f"  [C]              : Tema de Cores da Rosa: {self.theme['name']}",
            "  [S]              : Salvar Captura de Tela (PNG)",
            "  [P]              : Pausar / Continuar simulação",
            "  [M]              : Ativar / Desativar trilha sonora",
            "  [F]              : Alternar Tela Cheia / Janela",
            "  [H]              : Fechar este menu de ajuda HUD",
            "  [ESC] ou [Q]     : Sair",
            "",
            f"Tempo: {self.anim_time:.2f}s  |  FPS: {int(self.clock.get_fps())}",
            "Desenvolvido com Python + Pygame  ♥",
        ]

        start_y = (self.height - len(lines) * 25) // 2
        for idx, line in enumerate(lines):
            col = (255, 230, 140) if idx == 0 else ((255, 120, 150) if "Desenvolvido" in line else (230, 235, 245))
            surf = self.font.render(line, True, col)
            self.screen.blit(surf, (self.width // 2 - surf.get_width() // 2, start_y + idx * 25))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key in (pygame.K_SPACE, pygame.K_r):
                        self.reset_animation()
                    elif event.key == pygame.K_1:
                        self.force_view = 'letter'
                    elif event.key == pygame.K_2:
                        self.force_view = 'rose'
                    elif event.key == pygame.K_3:
                        self.force_view = 'portrait'
                    elif event.key in (pygame.K_v, pygame.K_TAB):
                        if self.force_view is None:
                            self.force_view = 'rose'
                        elif self.force_view == 'rose':
                            self.force_view = 'portrait'
                        elif self.force_view == 'portrait':
                            self.force_view = 'letter'
                        else:
                            self.force_view = None
                    elif event.key == pygame.K_t:
                        self.portrait_theme_idx = (self.portrait_theme_idx + 1) % len(PORTRAIT_THEMES)
                        self.portrait_theme = PORTRAIT_THEMES[self.portrait_theme_idx]
                        self.portrait_glyph_cache.clear()
                    elif event.key == pygame.K_c:
                        self.current_theme_idx = (self.current_theme_idx + 1) % len(THEMES)
                        self.theme = THEMES[self.current_theme_idx]
                    elif event.key == pygame.K_s:
                        self.save_screenshot()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_h:
                        self.show_help = not self.show_help
                    elif event.key == pygame.K_m:
                        self.audio_muted = not self.audio_muted
                        if self.soundtrack:
                            if self.audio_muted:
                                self.soundtrack.set_volume(0.0)
                            else:
                                self.soundtrack.set_volume(0.85)
                    elif event.key == pygame.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                        w, h = self.screen.get_size()
                        self.cols = w // self.cw
                        self.rows = h // self.ch
                        self.setup_cells()
                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self.cols = self.width // self.cw
                    self.rows = self.height // self.ch
                    self.setup_cells()

            if not self.paused:
                self.anim_time += dt
                self.update_particles(dt)

            self.render(dt)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    app = LetterToRoseApp()
    app.run()
