"""
Gera o desenho da capa do site-hvac: planta baixa de climatização (rede de dutos),
no padrão de prancha de instalações: arquitetura em meio-tom, sistema em destaque.

Escala: 36 px = 1 m. Valores de exemplo (9 difusores x 600 m³/h = 5.400 m³/h).
Uso:  python3 gerar_hvac.py caminho/para/index.html
"""
import sys
from desenho import Desenho, inserir, n

d = Desenho(1400, 700)
X0, X1, Y0, Y1 = 60, 1040, 60, 600           # faces externas do pavimento
EIXOS_X = (60, 400, 680, 1040)               # eixos A, B, C, D
EIXOS_Y = (60, 350, 600)                     # eixos 1, 2, 3

# =========================================================================== ARQUITETURA (meio-tom)
PAREDES = [(X0, Y0, X1, Y0), (X0, Y0, X0, Y1), (X1, Y0, X1, Y1), (X0, Y1, 820, Y1), (900, Y1, X1, Y1),
           (400, 60, 400, 250), (400, 300, 400, 350),            # escritório | área aberta (porta)
           (60, 350, 612, 350), (660, 350, 680, 350),            # divisa norte/sul (porta da reunião)
           (680, 350, 680, 600),
           (290, 350, 290, 370), (290, 420, 290, 600)]           # casa de máquinas (porta)
for x1, y1, x2, y2 in PAREDES:
    d.linha(x1, y1, x2, y2, "parede")
# portas: folha + arco de abertura
d.caminho("M400 250 H350 M350 250 A50 50 0 0 0 400 300", "fino")
d.caminho("M612 350 V398 M612 398 A48 48 0 0 0 660 350", "fino")
d.caminho("M290 370 H240 M240 370 A50 50 0 0 0 290 420", "fino")
d.caminho("M820 600 V560 M820 560 A40 40 0 0 1 860 600 M900 600 V560 M900 560 A40 40 0 0 0 860 600", "fino")
# janelas (vão com três linhas)
for jx in (110, 240, 450, 560, 740, 870):
    d.ret(jx, Y0 - 4, 100, 8, "corpo fino"); d.linha(jx, Y0, jx + 100, Y0, "fino")
for jy in (120, 240, 420):
    d.ret(X1 - 4, jy, 8, 90, "corpo fino"); d.linha(X1, jy, X1, jy + 90, "fino")
# pilares
for px in EIXOS_X:
    for py in EIXOS_Y:
        d.ret(px - 7, py - 7, 14, 14, "pilar")
# mobiliário (bem leve, só para dar escala)
def estacao(x, y):
    """Ilha de 4 mesas com cadeiras."""
    for i in (0, 1):
        for j in (0, 1):
            d.ret(x + 42 * i, y + 22 * j, 40, 20, "mob")
            d.circ(x + 20 + 42 * i, y - 8 + 60 * j, 6, "mob")
for ex, ey in ((455, 262), (700, 262), (876, 262), (712, 512), (876, 512)):
    estacao(ex, ey)
d.ret(96, 96, 90, 34, "mob"); d.circ(141, 142, 7, "mob"); d.ret(84, 276, 80, 30, "mob"); d.circ(124, 262, 7, "mob")
d.ret(410, 500, 200, 46, "mob", r=20)                                              # mesa de reunião
for k in range(5):
    d.circ(434 + 38 * k, 488, 6, "mob"); d.circ(434 + 38 * k, 558, 6, "mob")

# eixos e bolhas
for k, ex in enumerate(EIXOS_X):
    d.linha(ex, 42, ex, 54, "fino"); d.circ(ex, 28, 14, "fino"); d.texto(ex, 33, "ABCD"[k], "t p", "middle")
for k, ey in enumerate(EIXOS_Y):
    d.linha(42, ey, 54, ey, "fino"); d.circ(28, ey, 14, "fino"); d.texto(28, ey + 5, str(k + 1), "t p", "middle")

# =========================================================================== RETORNO E AR EXTERNO (tracejados, atrás)
d.caminho("M640 553 H117 V540 M640 567 H103 V540", "fino", d.fundo, 'stroke-dasharray="9 6" fill="none"')
d.caminho("M60 472 H90 M60 488 H90", "azulclaro", d.fundo, 'fill="none"')

# =========================================================================== UNIDADE DE TRATAMENTO DE AR
d.ret(90, 430, 140, 110, "corpo grosso")
d.caminho("M128 430 V540 M146 430 V540 M172 430 V540")                              # caixa de mistura | filtro | serpentina | ventilador
d.caminho("M128 436 L146 449 L128 462 L146 475 L128 488 L146 501 L128 514 L146 527 L128 540", "fino")   # filtro plissado
for k in range(9):
    d.linha(148, 440 + 11 * k, 170, 434 + 11 * k, "fino")                           # aletas da serpentina
d.circ(204, 492, 24); d.circ(204, 492, 7, "fino")                                   # ventilador centrífugo
d.caminho("M180 492 V444 H228 V480", "fino")
d.caminho("M100 444 L118 456 M100 500 L118 512", "fino")                            # dampers da caixa de mistura
d.caminho("M152 540 V584 M162 540 V584", "azulclaro")                               # água gelada
d.caminho("M149 562 l6 8 l0 -8 l-6 8 z M159 562 l6 8 l0 -8 l-6 8 z", "fino")        # válvulas
# veneziana de ar externo na fachada
for k in range(4):
    d.linha(48, 468 + 6 * k, 60, 474 + 6 * k, "fino")

# =========================================================================== REDE DE INSUFLAMENTO
RX0, RX1 = 186, 222                          # prumada que sai do ventilador
MY0, MY1 = 187, 223                          # duto principal (trecho 700x350)
NY0, NY1 = 192, 218                          # depois da redução (500x300)
XR, XF = 700, 986                            # início da redução e fim da rede
CONTORNO = ("M%d 422 V%d A30 30 0 0 1 %d %d H%d L%d %d H%d V%d H%d L%d %d H%d A6 6 0 0 0 %d %d V422"
            % (RX0, MY0 + 30, RX0 + 30, MY0, XR, XR + 26, NY0, XF, NY1, XR + 26, XR, MY1, RX1 + 6, RX1, MY1 + 6))
d.caminho(CONTORNO + " Z", "corpo azul")
d.caminho("M%d 430 l6 -4 l-6 -4 M%d 430 l-6 -4 l6 -4" % (RX0, RX1), "azul")         # junta flexível na descarga
d.caminho("M196 233 A24 24 0 0 1 220 209 M204 240 A18 18 0 0 1 222 222", "fino")    # veios direcionais da curva
for jx in (250, 340, 500, 660, 760, 890):                                           # juntas flangeadas
    y0, y1 = (MY0, MY1) if jx < XR else (NY0, NY1)
    d.linha(jx, y0, jx, y1, "fino")
for jy in (290, 380):
    d.linha(RX0, jy, RX1, jy, "fino")

DIFUSORES = []                               # (x, y) para as etiquetas


def difusor(x, y):
    d.ret(x - 18, y - 18, 36, 36, "corpo")
    for m in (13, 8, 3):
        d.ret(x - m, y - m, 2 * m, 2 * m, "fino")
    d.caminho("M%d %d L%d %d M%d %d L%d %d M%d %d L%d %d M%d %d L%d %d" % (
        x - 18, y - 18, x - 3, y - 3, x + 18, y - 18, x + 3, y - 3, x - 18, y + 18, x - 3, y + 3, x + 18, y + 18, x + 3, y + 3), "fino")
    DIFUSORES.append((x, y))


def ramal(x, y_dif, sobe):
    """Ramal de 300x200 saindo do principal até o difusor, com registro e trecho flexível."""
    reduz = x > XR
    borda = (NY0 if reduz else MY0) if sobe else (NY1 if reduz else MY1)
    s = -1 if sobe else 1
    fim = y_dif - s * 36                                                             # onde começa o flexível
    d.caminho("M%d %d L%d %d V%d M%d %d V%d" % (x - 16, borda, x - 8, borda + s * 8, fim, x + 8, borda, fim), "azul")
    yr = borda + s * 24                                                              # registro de regulagem
    d.linha(x - 8, yr + 5, x + 8, yr - 5, "fino"); d.circ(x + 12, yr - 5, 2.4, "fino")
    zig = "M%d %d" % (x - 7, fim) + "".join(" l14 %d l-14 %d" % (s * 3, s * 3) for _ in range(3))
    d.caminho(zig, "azul")
    difusor(x, y_dif)


ramal(280, 118, True); ramal(280, 292, False)        # escritório
ramal(600, 118, True)                                 # área aberta (norte)
ramal(820, 118, True); ramal(960, 118, True)
ramal(820, 468, False); ramal(960, 468, False)        # área aberta (sul)
ramal(440, 440, False); ramal(600, 440, False)        # reunião

# grelhas de retorno
for gx, gy in ((640, 546), (340, 300), (990, 300)):
    d.ret(gx, gy, 44, 28 if gx == 640 else 18, "corpo")
    for k in range(1, 6):
        d.linha(gx + 7.3 * k, gy, gx + 7.3 * k, gy + (28 if gx == 640 else 18), "fino")

# tonalidade do duto e ar em movimento
d.caminho(CONTORNO + " Z", camada=d.frente, extra='fill="rgba(36,91,219,.30)" stroke="none"')
EIXO_DUTO = "M204 430 V205 H980"
PERCURSOS = ((EIXO_DUTO, 8, 0), (EIXO_DUTO, 8, -2.7), (EIXO_DUTO, 8, -5.4), ("M204 430 V205 H600 V420", 6, -1), ("M204 430 V205 H820 V136", 6.5, -3),
             ("M204 430 V205 H280 V274", 4, -2), ("M204 430 V205 H960 V450", 8, -6))
d.frente.append('<g fill="#C9D7FB">' + "".join(
    '<circle r="%s"><animateMotion dur="%ss" begin="%ss" repeatCount="indefinite" path="%s"/></circle>' % (4 if i < 3 else 3, dur, ini, cam)
    for i, (cam, dur, ini) in enumerate(PERCURSOS)) + "</g>")

# =========================================================================== TEXTOS
def ambiente(x, y, nome, area):
    d.texto(x, y, nome, "t"); d.texto(x, y + 16, area, "t p")


ambiente(80, 222, "ESCRITÓRIO", "76 m²"); ambiente(420, 92, "ÁREA ABERTA", "213 m²")
ambiente(80, 384, "CASA DE MÁQUINAS", "44 m²"); ambiente(310, 384, "REUNIÃO", "75 m²")
d.texto(236, 468, "UTA-01"); d.texto(236, 484, "18 TR", "t p")
d.texto(172, 598, "AG", "t p"); d.texto(66, 462, "AE", "t p")
d.texto(360, 180, "700 × 350", "t c", "middle"); d.texto(890, 184, "500 × 300", "t c", "middle")
for k, (x, y) in enumerate(DIFUSORES):
    d.texto(x + 24, y - 3, "DI-%02d" % (k + 1), "t p"); d.texto(x + 24, y + 11, "600", "t p")
d.texto(640, 590, "GR-01", "t p"); d.texto(340, 334, "GR-02", "t p"); d.texto(990, 334, "GR-03", "t p")
# cotas entre eixos
for a, b in zip(EIXOS_X, EIXOS_X[1:]):
    d.cota(a, 632, b, 632, ("%.2f" % ((b - a) / 36.0)).replace(".", ","), tam_texto="t p")
# norte
d.circ(1010, 660, 13, "fino"); d.caminho("M1010 649 L1016 668 L1010 664 L1004 668 Z", "cheio", d.frente); d.texto(1010, 643, "N", "t p", "middle")

# =========================================================================== COLUNA DA DIREITA
QX, QW = 1070, 300
d.ret(QX, 34, QW, 164, "fino", d.frente, 'fill="none"'); d.linha(QX, 64, QX + QW, 64, "fino", d.frente)
d.texto(QX + 14, 55, "QUADRO DE VAZÕES"); d.texto(QX + QW - 86, 55, "m²", "t p", "end"); d.texto(QX + QW - 14, 55, "m³/h", "t p", "end")
for k, (amb, area, vaz) in enumerate((("Escritório", "76", "1.200"), ("Área aberta", "213", "3.000"), ("Reunião", "75", "1.200"))):
    y = 86 + 22 * k
    d.texto(QX + 14, y, amb, "t p"); d.texto(QX + QW - 86, y, area, "t p", "end"); d.texto(QX + QW - 14, y, vaz, "t", "end")
d.linha(QX, 152, QX + QW, 152, "fino", d.frente)
d.texto(QX + 14, 180, "Total insuflado"); d.texto(QX + QW - 14, 180, "5.400", "t c", "end")

d.texto(QX, 240, "LEGENDA")
LY = 268
d.ret(QX, LY - 9, 44, 14, camada=d.frente, extra='fill="rgba(36,91,219,.30)" stroke="#245BDB" stroke-width="2"'); d.texto(QX + 60, LY + 3, "Duto de insuflamento", "t p")
d.caminho("M%d %d h44 M%d %d h44" % (QX, LY + 22, QX, LY + 34), "fino", d.frente, 'stroke-dasharray="9 6" fill="none"'); d.texto(QX + 60, LY + 33, "Duto de retorno", "t p")
d.ret(QX + 10, LY + 50, 24, 24, "fino", d.frente, 'fill="none"'); d.ret(QX + 16, LY + 56, 12, 12, "fino", d.frente, 'fill="none"'); d.texto(QX + 60, LY + 67, "Difusor de 4 vias (DI)", "t p")
d.ret(QX + 4, LY + 90, 36, 14, "fino", d.frente, 'fill="none"'); d.caminho("M%d %d v14 M%d %d v14 M%d %d v14" % (QX + 13, LY + 90, QX + 22, LY + 90, QX + 31, LY + 90), "fino", d.frente); d.texto(QX + 60, LY + 101, "Grelha de retorno (GR)", "t p")
d.caminho("M%d %d l28 -10" % (QX + 6, LY + 128), "fino", d.frente); d.circ(QX + 38, LY + 118, 2.4, "fino", d.frente, 'fill="none"'); d.texto(QX + 60, LY + 127, "Registro de regulagem", "t p")
d.caminho("M%d %d h44 M%d %d h44" % (QX, LY + 146, QX, LY + 154), "azulclaro", d.frente, 'fill="none"'); d.texto(QX + 60, LY + 155, "Água gelada (AG) e ar externo (AE)", "t p")

d.ret(QX, 590, QW, 76, "fino", d.frente, 'fill="none"'); d.linha(QX, 622, QX + QW, 622, "fino", d.frente); d.linha(QX + 136, 622, QX + 136, 666, "fino", d.frente)
d.texto(QX + 14, 612, "CLIMATIZAÇÃO · PLANTA BAIXA")
d.texto(QX + 14, 640, "REDE DE DUTOS", "t p"); d.texto(QX + 14, 657, "ESC. 1:75", "t p")
d.texto(QX + 148, 640, "ILUSTRAÇÃO", "t p"); d.texto(QX + 148, 657, "VALORES DE EXEMPLO", "t p")

if __name__ == "__main__":
    inserir(sys.argv[1], "capa", d.svg("", oculto=True))
    print("hvac ok:", len(DIFUSORES), "difusores")
