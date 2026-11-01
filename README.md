# Letter For You ♥ (Burning Letter to Rose & Real Rounded Photo)

Projeto de arte computacional e animação procedimental em **Python + Pygame**, recriado e aperfeiçoado a partir do vídeo viral de animação ASCII.

Uma carta de amor em arte ASCII com selo de cera que pega fogo de forma orgânica e realista, liberando fagulhas físicas e fumaça dinâmica, revelando uma rosa radiante em chamas com feixes de luz anamórficos e culminando na revelação da **foto real arredondada com moldura luminosa radiante**, feixes de luz anamórficos e trilha sonora sincronizada.

---

## 🌹 Demonstração das Fases

1. **Fase 0 (0.0s - 2.0s) — A Carta Intacta**:
   - Envelope em estilo pergaminho com linhas de dobra e selo de coração em cera carmesim.
   - Mensagem personalizada de dedicação e amor.
   - Poeira estelar e cintilações suaves ao fundo.
   - Sutil efeito de tremulação à luz de velas.

2. **Fase 1 (2.0s) — A Ignição**:
   - Explosão inicial de 160 fagulhas incandescentes no canto inferior direito, sincronizada com o início da música.

3. **Fase 2 (2.0s - 5.8s) — Combustão Celular Orgânica**:
   - Propagação física com perturbação senoidal orgânica que simula o papel queimando.
   - Transição térmica de cores: Branco Incandescente $\to$ Amarelo $\to$ Laranja $\to$ Brasa Vermelha $\to$ Cinza.
   - Emissão contínua de fagulhas balísticas ascendentes e plumas de fumaça com oscilação de vento.

4. **Fase 3 (4.2s - 8.5s) — A Rosa Radiante & Feixes Anamórficos**:
   - Rosa em arte ASCII detalhada com pétalas em camadas e caule curvado natural.
   - Resfriamento térmico das pétalas saindo da brasa viva para as cores escolhidas.
   - Feixes anamórficos horizontais (*cinematic lens flares*) em azul ciano elétrico pulsando com respiração rítmica.

5. **Fase 4 (8.8s - 11.2s+) — A Foto Real Arredondada (Grand Finale)**:
   - A Rosa se transforma em uma chuva mágica de partículas douradas ascendentes.
   - A **foto real arredondada** surge suavemente do centro em fade-in com expansão suave e aura luminosa (*halo ring*).
   - Moldura circular com anéis de luz concêntricos em degradê e brilho pulsante.
   - Efeito de respiração sutil (pulsação rítmica suave da imagem).
   - Feixes anamórficos e pirilampos orbitando ao redor do medalhão.
   - Dedicações em tipografia romântica:
     - Topo: *"♥ Para Sempre a Razão do Meu Sorriso ♥"*
     - Base: *"♥ Com todo o meu amor e carinho ♥"*.

---

## ⌨️ Controles Interativos

| Tecla | Ação |
|---|---|
| `ESPAÇO` ou `R` | Reiniciar a animação do início |
| `1` | Saltar diretamente para a **Carta (Envelope)** |
| `2` | Saltar diretamente para a **Rosa em Chamas** |
| `3` | Saltar diretamente para a **Foto Real Arredondada** |
| `V` ou `TAB` | Alternar modo de visualização fixa (`Carta` $\to$ `Rosa` $\to$ `Foto` $\to$ `Automático`) |
| `T` | Alternar tema da Moldura da Foto (Ouro & Carmesim, Rubi Escarlate, Ciano Cyberpunk, Modo Código) |
| `C` | Alternar entre 4 temas de cores da Rosa |
| `S` | Salvar captura de tela em PNG de alta resolução |
| `P` | Pausar / Continuar a simulação |
| `M` | Ativar / Desativar áudio (Mute) |
| `F` | Alternar Tela Cheia / Janela |
| `H` | Abrir / Fechar menu de ajuda HUD |
| `ESC` ou `Q` | Sair |

---

## 🎨 Temas da Moldura da Foto (Tecla `T`)

1. **Ouro Imperial & Carmesim (Padrão)**: Borda com anel em ouro nobre, núcleo âmbar e halo suave carmesim.
2. **Rubi Escarlate**: Borda e halo em tons profundos de rubi e carmesim apaixonado.
3. **Ciano Neon Cyberpunk**: Estética futurista em ciano neon com halo azul elétrico.
4. **Modo Arte em Códigos**: Modo alternativo que exibe a foto gerada em glifos monoespaçados e código ASCII.

---

## 🎨 Temas da Rosa (Tecla `C`)

1. **Rubi Carmesim (Clássico)**: Pétalas carmesim escarlate, folhas esmeralda e feixes azul-ciano.
2. **Ouro Imperial (Golden Sun)**: Pétalas douradas incandescentes e feixes ambarinos.
3. **Ciano Neon (Cyberpunk)**: Pétalas neon ciano, caule violeta e raios elétricos.
4. **Ametista Real (Violet Bloom)**: Pétalas em tons de lilás e ametista, com aura mágica.

---

## 📁 Arquivos Criados

- `letter.py`: Aplicação principal em Python + Pygame com a Foto Real Arredondada.
- `photo_rounded.png`: Imagem da foto real tratada com corte circular perfeitamente antialiased (420x420).
- `portrait_interactive.html`: Visualizador web interativo em HTML5/Canvas com pulsação suave e controles de moldura.
- `portrait_data.py`: Matriz dos 3.106 glifos monoespaçados (para o modo código opcional).
- `render_preview.py`: Gerador de quadros-chave em PNG.
- `run.bat`: Inicializador rápido para Windows (duplo clique).
- `audio.wav`: Trilha sonora sincronizada.

---

## 🌐 Acesso via Web / Navegador (Novo!)

O projeto na sua Área de Trabalho agora possui uma **versão Web completa e responsiva** em **HTML5 + Canvas 2D + Áudio sincronizado**, compatível com computadores e celulares (iPhone/Android).

- **No seu Computador**: [http://localhost:8088](http://localhost:8088)
- **No Celular (mesma rede Wi-Fi)**: `http://192.168.3.190:8088`
- **Link Online na Internet**: [https://little-hats-shop.loca.lt](https://little-hats-shop.loca.lt) *(IP de confirmação: `143.255.252.195`)*
- **Arquivo direto**: [index.html](index.html) ou execute `start_web.bat`.

---

## 🚀 Como Executar

Execute diretamente no terminal:
```bash
cd "C:\Users\HenriqueRF\Desktop\LetterForYou"
python letter.py
```
Ou dê um duplo clique no arquivo:
`run.bat`
