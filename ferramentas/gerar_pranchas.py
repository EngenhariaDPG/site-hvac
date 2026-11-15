"""
Gera as figuras técnicas da seção "Entregas" dos dois sites (três por site).
Todas são ilustrações originais com valores de exemplo.

Uso:  python3 gerar_pranchas.py consultoria caminho/index.html
      python3 gerar_pranchas.py hvac        caminho/index.html
"""
import math
import sys
from desenho import Desenho, inserir, n

# ----------------------------------------------------------------------------- utilidades
PALETA = ((29, 78, 216), (6, 182, 212), (34, 197, 94), (250, 204, 21), (239, 68, 68))   # azul > ciano > verde > amarelo > vermelho


def cor(t):
    """Cor da escala de resultados (0 = mínimo, 1 = máximo), como em pós-processamento de simulação."""
    t = max(0.0, min(0.9999, t)) * (len(PALETA) - 1)
    i = int(t); f = t - i
    a, b = PALETA[i], PALETA[i + 1]
    return "#%02X%02X%02X" % tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))


def escala_cores(d, x, y, alt, valores, titulo, faixas=9):
    """Barra de legenda vertical com faixas de cor e valores."""
    h = alt / faixas
    for k in range(faixas):
        d.ret(x, y + alt - (k + 1) * h, 13, h + 0.4, camada=d.frente, extra='fill="%s"' % cor((k + 0.5) / faixas))
    d.ret(x, y, 13, alt, "fino", d.frente, 'fill="none"')
    for k, v in enumerate(valores):
        yy = y + alt - alt * k / (len(valores) - 1)
        d.linha(x + 13, yy, x + 18, yy, "fino", d.frente); d.texto(x + 22, yy + 4, v, "t p")
    d.texto(x, y - 12, titulo, "t p")


def carimbo(d, x, y, w, titulo, linha2):
    d.ret(x, y, w, 60, "fino", d.frente, 'fill="none"'); d.linha(x, y + 30, x + w, y + 30, "fino", d.frente)
    d.texto(x + 12, y + 21, titulo); d.texto(x + 12, y + 49, linha2, "t p")


# ============================================================================= CONSULTORIA 1: elementos finitos
def balancim():
    d = Desenho(640, 420)
    X0, X1, YC, ALT = 70, 490, 196, 56                 # viga: início, fim, eixo e altura
    XM, MEIO = (X0 + X1) / 2, (X1 - X0) / 2
    NX, NY = 42, 6

    def flecha(x):                                     # deformada ampliada: as pontas descem
        return 24 * ((x - XM) / MEIO) ** 2

    def ponto(i, j):
        x = X0 + (X1 - X0) * i / NX
        return x, YC - ALT / 2 + ALT * j / NY + flecha(x)

    # contorno indeformado (tracejado) e malha colorida pela tensão
    d.ret(X0, YC - ALT / 2, X1 - X0, ALT, "fino", d.fundo, 'fill="none" stroke-dasharray="5 5"')
    for i in range(NX):
        for j in range(NY):
            xm = X0 + (X1 - X0) * (i + 0.5) / NX
            eta = abs((j + 0.5) / NY * 2 - 1)                                        # distância à linha neutra
            momento = 1 - abs(xm - XM) / MEIO                                        # momento fletor (máximo no centro)
            conc = 0.35 * math.exp(-((xm - XM) / 26) ** 2) * (1 if j < 2 else 0.2)   # concentração junto ao olhal
            t = min(1, momento * (0.12 + 0.88 * eta) * 0.92 + conc)
            p = [ponto(i, j), ponto(i + 1, j), ponto(i + 1, j + 1), ponto(i, j + 1)]
            d.fundo.append('<path d="M%s Z" fill="%s" stroke="#0B1118" stroke-width=".5" stroke-opacity=".55"/>'
                           % (" L".join("%s %s" % (n(a), n(b)) for a, b in p), cor(t)))
    # contorno deformado, mesas do perfil e enrijecedores
    topo = " L".join("%s %s" % (n(a), n(b)) for a, b in (ponto(i, 0) for i in range(NX + 1)))
    base = " L".join("%s %s" % (n(a), n(b)) for a, b in (ponto(i, NY) for i in range(NX, -1, -1)))
    d.caminho("M%s L%s Z" % (topo, base), "grosso")
    # olhal central (içamento) e olhais das pontas (carga)
    yt = YC - ALT / 2
    d.caminho("M%s %s L%s %s H%s L%s %s" % (n(XM - 26), n(yt), n(XM - 14), n(yt - 40), n(XM + 14), n(XM + 26), n(yt)), "corpo")
    d.circ(XM, yt - 24, 7); d.circ(XM, yt - 24, 12, "fino")
    for xo in (X0 + 22, X1 - 22):
        yb = YC + ALT / 2 + flecha(xo)
        d.caminho("M%s %s L%s %s H%s L%s %s" % (n(xo - 16), n(yb), n(xo - 9), n(yb + 28), n(xo + 9), n(xo + 16), n(yb)), "corpo")
        d.circ(xo, yb + 17, 5)
        d.caminho("M%s %s V%s" % (n(xo), n(yb + 34), n(yb + 78)), "cota"); d.seta(xo, yb + 78, 90)
        d.texto(xo, yb + 96, "35,8 kN", "t c", "middle")
    d.caminho("M%s %s V%s" % (n(XM), n(yt - 44), n(yt - 92)), "cota"); d.seta(XM, yt - 92, -90)
    d.texto(XM + 12, yt - 80, "F = 71,6 kN", "t c")
    # chamada do ponto de máxima tensão
    d.linha(XM - 16, YC + ALT / 2 - 3, XM - 44, YC + 76, "fino"); d.circ(XM - 16, YC + ALT / 2 - 3, 2.2, "ponto", d.frente)
    d.texto(XM - 40, YC + 92, "MÁX 118 MPa", "t", "middle"); d.texto(XM - 40, YC + 108, "mesa inferior, meio do vão", "t p", "middle")
    d.texto(X0, YC - ALT / 2 - 10, "indeformada", "t p")
    # eixos, legenda e dados
    d.caminho("M40 384 H74 M40 384 V350", "fino"); d.seta(74, 384, 0, 7, "ponto"); d.seta(40, 350, -90, 7, "ponto")
    d.texto(80, 388, "x", "t p"); d.texto(36, 342, "y", "t p")
    escala_cores(d, 548, 96, 216, ("0", "30", "59", "89", "118"), "von Mises, MPa")
    d.texto(110, 372, "Balancim de 4,0 m em perfil W 250, aço ASTM A36", "t p")
    d.texto(110, 390, "Deformada ampliada 50×. Fator de segurança 2,1 ao escoamento", "t p")
    return d.svg("Mapa de tensões de um balancim de içamento calculado por elementos finitos, com malha, cargas e legenda de cores")


# ============================================================================= CONSULTORIA 2: NR-12
def prensa():
    d = Desenho(640, 420)
    PISO = 384
    d.defs.append('<pattern id="tela" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                  '<path d="M0 0H9M0 0V9" stroke="#7F8A98" stroke-width=".8" fill="none"/></pattern>')
    # proteções fixas (grades) dos dois lados
    for gx in (118, 446):
        d.ret(gx, 110, 76, PISO - 110, camada=d.fundo, extra='fill="url(#tela)"')
        d.ret(gx, 110, 76, PISO - 110); d.linha(gx, 240, gx + 76, 240, "fino")
        for pe in (gx, gx + 76):
            d.caminho("M%d %d h-6 v6 h12 v-6 z" % (pe, PISO - 6), "fino")
    # estrutura da prensa: cabeçote, colunas, mesa e base
    d.ret(288, 26, 64, 26, "corpo"); d.caminho("M300 26 V16 H340 V26", "fino")                 # cilindro hidráulico
    d.ret(216, 52, 208, 52, "corpo grosso"); d.linha(216, 92, 424, 92, "fino")
    for k in range(6):
        d.circ(232 + 35.2 * k, 98, 1.6, "fino")
    d.ret(226, 104, 34, 204, "corpo"); d.ret(380, 104, 34, 204, "corpo")                       # colunas
    d.linha(236, 104, 236, 308, "fino"); d.linha(404, 104, 404, 308, "fino")
    d.ret(311, 104, 18, 54, "corpo")                                                           # haste
    d.ret(264, 158, 112, 40, "corpo grosso"); d.linha(264, 168, 376, 168, "fino")              # martelo
    d.ret(260, 162, 6, 32, "fino"); d.ret(374, 162, 6, 32, "fino")                             # guias
    d.ret(288, 198, 64, 16, "corpo"); d.caminho("M296 214 L304 226 H336 L344 214", "corpo")    # ferramenta superior
    d.ret(284, 262, 72, 18, "corpo"); d.linha(300, 262, 300, 280, "fino"); d.linha(340, 262, 340, 280, "fino")
    d.ret(240, 280, 160, 28, "corpo grosso")                                                   # mesa
    for k in range(4):
        d.linha(262 + 39 * k, 284, 262 + 39 * k, 304, "fino")                                  # rasgos em T
    d.ret(210, 308, 220, 50, "corpo grosso"); d.ret(300, 318, 40, 28, "fino")
    d.ret(222, 358, 196, PISO - 358, "corpo")
    # cortina de luz: emissor e receptor em colunas
    for cx in (198, 428):
        d.ret(cx, 150, 14, 138, "corpo azul"); d.ret(cx + 4, PISO - 96, 6, 96, "corpo")
        d.caminho("M%d %d h30" % (cx - 8, PISO), "fino")
        for k in range(11):
            d.circ(cx + 7, 158 + 12.2 * k, 1.3, "fino")
    d.frente.append('<path class="fluxo" stroke="#245BDB" stroke-width="1.2" stroke-opacity=".6" d="%s"/>' % "".join("M212 %sH428" % n(158 + 12.2 * k) for k in range(11)))
    # painel elétrico com relé de segurança
    d.ret(132, 150, 48, 78, "corpo"); d.ret(138, 158, 36, 20, "fino"); d.circ(146, 196, 4.5); d.circ(166, 196, 4.5, "fino")
    d.circ(156, 214, 6); d.circ(156, 214, 9.5, "fino")
    # comando bimanual em pedestal
    d.ret(460, 290, 62, 22, "corpo"); d.ret(486, 312, 10, PISO - 312, "corpo"); d.caminho("M476 %d h30" % PISO, "fino")
    d.circ(472, 301, 5.5); d.circ(510, 301, 5.5); d.circ(491, 301, 4, "azul")
    d.caminho("M462 290 a10 9 0 0 1 20 0 M500 290 a10 9 0 0 1 20 0", "fino")                   # abas contra acionamento acidental
    d.linha(90, PISO, 550, PISO, "grosso")
    # chamadas
    d.linha(442, 172, 532, 150, "fino"); d.texto(536, 148, "Cortina de luz"); d.texto(536, 164, "tipo 4", "t p")
    d.linha(522, 301, 536, 292, "fino"); d.texto(540, 290, "Bimanual"); d.texto(540, 306, "tipo III C", "t p")
    d.linha(500, 124, 532, 100, "fino"); d.texto(536, 98, "Proteção fixa"); d.texto(536, 114, "grade com travas", "t p")
    d.linha(132, 180, 108, 170, "fino"); d.texto(104, 168, "Painel", "t", "end"); d.texto(104, 184, "relé de segurança", "t p", "end"); d.texto(104, 198, "categoria 4", "t p", "end")
    d.linha(147, 214, 108, 250, "fino"); d.texto(104, 254, "Emergência", "t", "end"); d.texto(104, 270, "com retenção", "t p", "end")
    d.texto(320, 408, "Distância de segurança da cortina: S = K × T + C (ABNT NBR ISO 13855)", "t p", "middle")
    return d.svg("Vista frontal de uma prensa hidráulica adequada à NR-12: cortina de luz, proteções fixas, comando bimanual, painel com relé de segurança e parada de emergência")


# ============================================================================= CONSULTORIA 3: desenho de fabricação
def flange():
    d = Desenho(1280, 420)
    d.defs.append('<pattern id="corte" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                  '<line x1="0" y1="0" x2="0" y2="7" stroke="#111820" stroke-width="1"/></pattern>')
    CX, CY = 220, 206
    # ---- vista frontal
    d.linha(CX - 150, CY, CX + 150, CY, "fino", d.fundo, 'stroke-dasharray="18 5 3 5"')
    d.linha(CX, CY - 150, CX, CY + 150, "fino", d.fundo, 'stroke-dasharray="18 5 3 5"')
    d.circ(CX, CY, 88, "fino", d.fundo, 'fill="none" stroke-dasharray="18 5 3 5"')
    d.circ(CX, CY, 126, "grosso"); d.circ(CX, CY, 70); d.circ(CX, CY, 42, "grosso"); d.circ(CX, CY, 46, "fino")
    d.ret(CX - 7, CY - 49, 14, 9, "corpo")                                                    # rasgo de chaveta
    for k in range(6):
        a = math.radians(60 * k)
        d.circ(CX + 88 * math.cos(a), CY + 88 * math.sin(a), 11)
        d.linha(CX + 70 * math.cos(a), CY + 70 * math.sin(a), CX + 106 * math.cos(a), CY + 106 * math.sin(a), "fino", d.fundo, 'stroke-dasharray="8 4 2 4"')
    d.linha(CX + 88 * math.cos(math.radians(-60)) + 8, CY + 88 * math.sin(math.radians(-60)) - 8, CX + 150, CY - 150, "fino")
    d.texto(CX + 154, CY - 152, "6 × Ø22"); d.texto(CX + 154, CY - 136, "igualmente espaçados", "t p")
    d.caminho("M%d %d V%d M%d %d V%d" % (CX, CY - 160, CY - 176, CX, CY + 160, CY + 176), "grosso")   # plano de corte A-A
    d.seta(CX + 22, CY - 172, 0, 9, "cheio"); d.seta(CX + 22, CY + 172, 0, 9, "cheio")
    d.linha(CX, CY - 172, CX + 22, CY - 172); d.linha(CX, CY + 172, CX + 22, CY + 172)
    d.texto(CX - 14, CY - 166, "A", "t", "end"); d.texto(CX - 14, CY + 178, "A", "t", "end")
    # ---- corte A-A
    SX = 520                                                                                   # face esquerda do flange no corte
    PERFIL = [(SX, CY - 126), (SX + 36, CY - 126), (SX + 36, CY - 70), (SX + 120, CY - 70), (SX + 120, CY + 70), (SX + 36, CY + 70), (SX + 36, CY + 126), (SX, CY + 126)]
    d.caminho("M%d %d H%d V%d H%d V%d H%d Z M%d %d H%d V%d H%d V%d H%d Z" % (
        SX, CY - 126, SX + 36, CY - 70, SX + 120, CY - 42, SX,
        SX, CY + 42, SX + 120, CY + 70, SX + 36, CY + 126, SX), camada=d.fundo, extra='fill="url(#corte)"')
    for s in (-1, 1):                                                                          # furos passantes vistos em corte
        d.ret(SX, CY + s * 88 - 11, 36, 22, "papel", d.fundo)
    d.poli(PERFIL, "grosso")
    d.caminho("M%d %d H%d M%d %d H%d" % (SX, CY - 42, SX + 120, SX, CY + 42, SX + 120))
    for s in (-1, 1):
        d.caminho("M%d %d H%d M%d %d H%d" % (SX, CY + s * 88 - 11, SX + 36, SX, CY + s * 88 + 11, SX + 36))
        d.linha(SX - 10, CY + s * 88, SX + 46, CY + s * 88, "fino", d.fundo, 'stroke-dasharray="8 4 2 4"')
    d.linha(SX - 24, CY, SX + 144, CY, "fino", d.fundo, 'stroke-dasharray="18 5 3 5"')
    d.texto(SX + 60, CY - 150, "CORTE A-A", "t", "middle")
    # cotas
    d.cota(SX + 176, CY + 126, SX + 176, CY - 126, "Ø252"); d.linha(SX + 36, CY - 126, SX + 184, CY - 126, "fino"); d.linha(SX + 36, CY + 126, SX + 184, CY + 126, "fino")
    d.cota(SX + 148, CY + 70, SX + 148, CY - 70, "Ø140")
    d.cota(SX - 34, CY + 42, SX - 34, CY - 42, "Ø84 H7"); d.linha(SX - 42, CY - 42, SX, CY - 42, "fino"); d.linha(SX - 42, CY + 42, SX, CY + 42, "fino")
    d.cota(SX, CY + 156, SX + 36, CY + 156, "36", lado=1, afast=8); d.cota(SX, CY + 186, SX + 120, CY + 186, "120", lado=1, afast=8)
    d.linha(SX, CY + 126, SX, CY + 194, "fino"); d.linha(SX + 36, CY + 126, SX + 36, CY + 164, "fino"); d.linha(SX + 120, CY + 70, SX + 120, CY + 194, "fino")
    # acabamento superficial e tolerância geométrica
    d.caminho("M%d %d l7 12 l14 -24 h16" % (SX + 62, CY - 84), "fino"); d.texto(SX + 84, CY - 102, "Ra 1,6", "t p")
    d.ret(SX + 150, CY - 186, 116, 24, "fino"); d.linha(SX + 180, CY - 186, SX + 180, CY - 162, "fino"); d.linha(SX + 238, CY - 186, SX + 238, CY - 162, "fino")
    d.caminho("M%d %d h14 M%d %d v-12" % (SX + 158, CY - 168, SX + 165, CY - 168), "fino")    # símbolo de perpendicularidade
    d.texto(SX + 209, CY - 169, "0,05", "t p", "middle"); d.texto(SX + 252, CY - 169, "B", "t p", "middle")
    d.linha(SX + 150, CY - 174, SX + 120, CY - 100, "fino")
    d.ret(SX - 78, CY + 60, 22, 22, "fino"); d.texto(SX - 67, CY + 76, "B", "t p", "middle"); d.linha(SX - 56, CY + 60, SX - 34, CY + 42, "fino")
    # notas e carimbo
    NX = 860
    d.texto(NX, 70, "NOTAS")
    NOTAS = ("1. Material: aço SAE 1045, normalizado", "2. Tolerâncias gerais conforme ISO 2768-mK", "3. Quebrar cantos vivos 0,5 × 45°",
             "4. Rugosidade geral Ra 3,2 µm, exceto onde indicado", "5. Rasgo de chaveta conforme DIN 6885", "6. Proteção: oxidação negra após usinagem")
    for k, t in enumerate(NOTAS):
        d.texto(NX, 96 + 22 * k, t, "t p")
    d.ret(NX, 262, 360, 108, "fino", d.frente, 'fill="none"')
    d.caminho("M%d 298 H%d M%d 334 H%d M%d 298 V370 M%d 298 V370" % (NX, NX + 360, NX, NX + 360, NX + 120, NX + 240), "fino", d.frente)
    d.texto(NX + 14, 286, "FLANGE DE ACOPLAMENTO")
    for k, (a, b) in enumerate((("Escala", "1:2"), ("Massa", "14,2 kg"), ("Folha", "1 / 1"))):
        d.texto(NX + 14 + 120 * k, 320, a, "t p"); d.texto(NX + 14 + 120 * k, 357, b, "t")
    return d.svg("Desenho de fabricação de um flange: vista frontal, corte A-A hachurado, cotas, tolerâncias, acabamento superficial, notas e carimbo")


# ============================================================================= HVAC 1: CFD
def cfd():
    d = Desenho(640, 420)
    X0, Y0, W, H = 56, 64, 456, 252                    # sala em corte
    XD = X0 + W / 2                                    # difusor no centro do forro
    FONTES = ((X0 + 118, Y0 + H - 60), (X0 + 338, Y0 + H - 60))   # ocupantes (fontes de calor)

    def temperatura(x, y):
        prof = y - Y0
        jato = 4.6 * math.exp(-(prof / 30.0) ** 2) * math.exp(-abs(x - XD) / 190.0)
        queda = 1.6 * math.exp(-((x - X0) / 34.0) ** 2) * math.exp(-(prof / 190.0))
        janela = 3.4 * math.exp(-(X0 + W - x) / 52.0) * (0.55 + 0.45 * (1 - prof / H))
        pluma = sum(2.3 * math.exp(-((x - fx) / 30.0) ** 2) * math.exp(-max(0, fy - y) / 110.0) * (1 if y < fy + 40 else 0.4) for fx, fy in FONTES)
        return 21.8 - jato - queda + janela + pluma + 0.9 * (1 - prof / H)

    # campo de temperatura em faixas (isotermas), fundindo células vizinhas de mesma cor
    PASSO, NIVEIS = 6, 18
    for j in range(H // PASSO):
        y = Y0 + j * PASSO
        inicio, atual = 0, None
        for i in range(W // PASSO + 1):
            if i < W // PASSO:
                t = (temperatura(X0 + (i + 0.5) * PASSO, y + PASSO / 2) - 18) / 8
                nivel = max(0, min(NIVEIS - 1, int(t * NIVEIS)))
            else:
                nivel = None
            if nivel != atual:
                if atual is not None:
                    d.fundo.append('<rect shape-rendering="crispEdges" x="%d" y="%d" width="%s" height="%s" fill="%s"/>' % (X0 + inicio * PASSO, y, n((i - inicio) * PASSO), n(PASSO), cor((atual + 0.5) / NIVEIS)))
                inicio, atual = i, nivel

    # vetores de velocidade: duas células de recirculação (jato pelo forro, descida nas paredes, retorno pelo piso)
    def velocidade(x, y):
        lado = -1 if x < XD else 1
        a = math.pi * abs(x - XD) / (W / 2); b = math.pi * (y - Y0) / H
        u = lado * math.sin(a) * math.cos(b) * 1.25
        v = -math.cos(a) * math.sin(b)          # sobe no centro, desce junto às paredes (y da tela cresce para baixo)
        return u, v

    setas = []
    for i in range(15):
        for j in range(8):
            x, y = X0 + 16 + i * 30.3, Y0 + 18 + j * 31
            u, v = velocidade(x, y)
            m = math.hypot(u, v)
            if m < 0.12:
                continue
            c = 5 + 9 * min(1, m)
            ex, ey = x + u / m * c, y + v / m * c
            ang = math.atan2(v, u)
            setas.append("M%s %s L%s %s M%s %s L%s %s L%s %s" % (n(x), n(y), n(ex), n(ey),
                         n(ex - 4 * math.cos(ang - 0.5)), n(ey - 4 * math.sin(ang - 0.5)), n(ex), n(ey),
                         n(ex - 4 * math.cos(ang + 0.5)), n(ey - 4 * math.sin(ang + 0.5))))
    d.frente.append('<path d="%s" fill="none" stroke="#0B1118" stroke-opacity=".7" stroke-width="1.1"/>' % "".join(setas))

    # sala, difusor, grelha de retorno, janela, mesas e ocupantes (blocos)
    d.ret(X0, Y0, W, H, "grosso")
    d.ret(XD - 24, Y0 - 10, 48, 10, "corpo"); d.caminho("M%s %s l-8 8 M%s %s l8 8" % (n(XD - 10), Y0, n(XD + 10), Y0), "fino")
    d.ret(X0 + W - 96, Y0 - 8, 44, 8, "corpo")
    d.frente.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#7FA2F2" stroke-width="5"/>' % (X0 + W, Y0 + 36, X0 + W, Y0 + 176))
    for fx, fy in FONTES:
        d.ret(fx - 12, fy - 34, 24, 34, "corpo"); d.circ(fx, fy - 44, 9, "corpo"); d.ret(fx - 12, fy, 30, 12, "corpo"); d.ret(fx + 8, fy + 12, 10, 48, "corpo")
        d.caminho("M%s %s H%s M%s %s V%s" % (n(fx + 26), n(fy - 12), n(fx + 92), n(fx + 84), n(fy - 12), n(Y0 + H)))
        d.ret(fx + 44, fy - 44, 34, 24, "corpo"); d.linha(fx + 61, fy - 20, fx + 61, fy - 12)
    d.texto(XD, Y0 - 18, "difusor · 14 °C", "t p", "middle"); d.texto(X0 + W - 74, Y0 - 16, "retorno", "t p", "middle")
    d.texto(X0 + W, Y0 + H + 16, "janela com carga solar", "t p", "end")
    escala_cores(d, 556, 96, 190, ("18", "20", "22", "24", "26"), "°C")
    d.texto(X0, 362, "Campo de temperatura e vetores de velocidade, regime permanente", "t p")
    d.texto(X0, 380, "Zona ocupada: 22 a 24 °C, velocidade abaixo de 0,25 m/s", "t p")
    return d.svg("Simulação CFD de uma sala em corte: campo de temperatura em faixas de cor e vetores de velocidade do ar a partir do difusor de forro")


# ============================================================================= HVAC 2: isométrico de água gelada
def isometrico():
    d = Desenho(640, 420)
    K, OX, OY = 30.0, 112, 124

    def iso(x, y, z):
        return OX + (x - y) * 0.866 * K, OY + (x + y) * 0.5 * K - z * K

    def caixa(x0, y0, z0, x1, y1, z1, cls="corpo"):
        """Prisma isométrico: desenha as três faces visíveis (topo, frente x e frente y)."""
        d.poli([iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)], cls)
        d.poli([iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)], cls)
        d.poli([iso(x0, y1, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x0, y1, z1)], cls)

    def tubo(pontos, cls="azul", extra=""):
        d.caminho("M" + " L".join("%s %s" % (n(a), n(b)) for a, b in (iso(*p) for p in pontos)), cls, extra=extra)

    def valvula(p, eixo):
        """Válvula (gravata) sobre o tubo, alinhada ao eixo 'x' ou 'y'."""
        a = iso(*p)
        dx, dy = (0.866 * 7, 0.5 * 7) if eixo == "x" else (-0.866 * 7, 0.5 * 7)
        d.caminho("M%s %s L%s %s L%s %s L%s %s Z" % (n(a[0] - dx), n(a[1] - dy - 4), n(a[0] + dx), n(a[1] + dy + 4), n(a[0] + dx), n(a[1] + dy - 4), n(a[0] - dx), n(a[1] - dy + 4)), "corpo")

    # ---- chiller a ar sobre base
    caixa(-0.2, -0.2, 0, 4.0, 2.2, 0.15)
    caixa(0, 0, 0.15, 3.8, 2.0, 2.2, "corpo grosso")
    for fx in (0.75, 1.9, 3.05):                                                               # ventiladores no topo
        c = iso(fx, 1.0, 2.2)
        d.bruto('<ellipse class="fino" cx="%s" cy="%s" rx="15" ry="8.6"/>' % (n(c[0]), n(c[1])))
        d.bruto('<ellipse class="fino" cx="%s" cy="%s" rx="4" ry="2.3"/>' % (n(c[0]), n(c[1])))
    for k in range(1, 14):                                                                     # serpentina na face frontal
        a, b = iso(0.2 + 0.26 * k, 2.0, 0.4), iso(0.2 + 0.26 * k, 2.0, 2.0)
        d.linha(a[0], a[1], b[0], b[1], "fino")
    p = [iso(3.8, 0.3, 0.5), iso(3.8, 0.9, 0.5), iso(3.8, 0.9, 1.7), iso(3.8, 0.3, 1.7)]; d.poli(p, "fino")   # quadro elétrico

    # ---- tubulação: alimentação (cheia) e retorno (tracejado)
    ZA, ZR = 3.6, 3.1                                                                           # níveis dos barriletes
    ALIM = [(3.8, 1.5, 0.9), (6.2, 1.5, 0.9), (6.2, 1.5, ZA), (14.9, 1.5, ZA)]
    RET = [(14.9, 0.6, ZR), (7.2, 0.6, ZR), (7.2, 0.6, 0.5), (3.8, 0.6, 0.5)]
    tubo(RET, "azul", 'stroke-dasharray="7 5"')
    tubo(ALIM)
    FCS = (9.4, 11.7, 14.0)
    for fx in FCS:
        tubo([(fx, 1.5, ZA), (fx, 3.1, ZA), (fx, 3.1, 3.0)])
        tubo([(fx + 0.5, 0.6, ZR), (fx + 0.5, 3.1, ZR), (fx + 0.5, 3.1, 3.0)], "azul", 'stroke-dasharray="7 5"')
        valvula((fx, 2.3, ZA), "y"); valvula((fx + 0.5, 2.1, ZR), "y")
        caixa(fx - 0.5, 2.7, 2.3, fx + 1.0, 3.7, 3.0)                                           # fan-coil
        a, b = iso(fx - 0.3, 3.7, 2.45), iso(fx + 0.8, 3.7, 2.45); d.linha(a[0], a[1], b[0], b[1], "fino")
        a, b = iso(fx - 0.3, 3.7, 2.6), iso(fx + 0.8, 3.7, 2.6); d.linha(a[0], a[1], b[0], b[1], "fino")
    # bombas (uma em operação, uma reserva) na alimentação
    for py in (1.5, 2.7):
        caixa(4.5, py - 0.3, 0, 5.6, py + 0.3, 0.25)
        caixa(4.6, py - 0.22, 0.25, 5.1, py + 0.22, 0.75); caixa(5.1, py - 0.3, 0.25, 5.55, py + 0.3, 0.9)
    tubo([(4.2, 1.5, 0.9), (4.2, 2.7, 0.9), (6.2, 2.7, 0.9), (6.2, 1.5, 0.9)], "fino")
    valvula((5.9, 1.5, 0.9), "x"); valvula((6.2, 1.5, 2.3), "x")
    # tanque de expansão no retorno
    tubo([(7.2, 0.6, 1.5), (7.2, -0.6, 1.5)], "fino")
    t = iso(7.2, -0.6, 1.5)
    d.ret(t[0] - 9, t[1] - 30, 18, 30, "corpo", r=8)
    # setas de fluxo
    for p0, p1 in (((9.6, 1.5, ZA), (10.2, 1.5, ZA)), ((10.4, 0.6, ZR), (9.8, 0.6, ZR))):
        a, b = iso(*p0), iso(*p1)
        d.seta(b[0], b[1], math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), 9)
    # etiquetas
    a = iso(3.8, 0, 2.2); d.texto(a[0] + 10, a[1] - 34, "CH-01"); d.texto(a[0] + 10, a[1] - 18, "chiller a ar, 60 TR", "t p")
    a = iso(4.5, 3.0, 0); d.texto(a[0] - 6, a[1] + 26, "BAG-01/02", "t", "end"); d.texto(a[0] - 6, a[1] + 42, "1 operação + 1 reserva", "t p", "end")
    for k, fx in enumerate(FCS):
        a = iso(fx - 0.5, 3.7, 2.3); d.texto(a[0] - 6, a[1] + 16, "FC-%02d" % (k + 1), "t p", "end")
    d.texto(t[0], t[1] - 38, "TE-01", "t p", "middle")
    d.linha(40, 356, 84, 356, "azul", d.frente, 'stroke="#245BDB" stroke-width="2"'); d.texto(96, 360, "Alimentação, AG 7 °C, Ø 4″", "t p")
    d.linha(40, 378, 84, 378, "azul", d.frente, 'stroke="#245BDB" stroke-width="2" stroke-dasharray="7 5"'); d.texto(96, 382, "Retorno, AG 12 °C, Ø 4″", "t p")
    d.texto(40, 406, "ISOMÉTRICO SEM ESCALA · VALORES DE EXEMPLO", "t p")
    return d.svg("Isométrico de uma central de água gelada: chiller a ar, bombas, tanque de expansão, barriletes de alimentação e retorno e três fan-coils com válvulas")


# ============================================================================= HVAC 3: pressurização de escada
def escada():
    d = Desenho(1280, 420)
    TERREO, PE = 372, 62                                # nível do térreo e pé-direito (px)
    NIVEIS = [TERREO - PE * k for k in range(6)]         # térreo, 1º a 4º e cobertura
    EX0, EX1 = 480, 620                                  # caixa da escada
    DX0 = 430                                            # duto vertical (430 a 480)
    FX1 = 900                                            # fachada direita

    # fumaça no pavimento sinistrado (2º) e ar limpo na escada
    y2 = NIVEIS[2]
    d.caminho("M%d %d H%d V%d q-22 12 -44 0 t-44 0 t-44 0 t-44 0 t-44 0 t-44 0 Z" % (EX1 + 6, y2 - PE + 6, FX1 - 4, y2 - 28),
              camada=d.fundo, extra='fill="rgba(190,198,208,.20)"')
    d.ret(EX0, NIVEIS[5], EX1 - EX0, TERREO - NIVEIS[5], camada=d.fundo, extra='fill="rgba(36,91,219,.20)"')
    d.ret(DX0, NIVEIS[5], 50, TERREO - NIVEIS[5], camada=d.fundo, extra='fill="rgba(36,91,219,.10)"')

    # lajes, fachada e pavimentos
    for k, y in enumerate(NIVEIS):
        d.caminho("M%d %d H%d M%d %d H%d" % (EX1, y, FX1, EX1, y + 6, FX1), "fino" if 0 < k < 5 else "")
    d.caminho("M%d %d V%d" % (FX1, NIVEIS[5], TERREO)); d.linha(FX1 - 8, NIVEIS[5], FX1 - 8, TERREO, "fino")
    for k in range(5):
        d.ret(FX1 - 8, NIVEIS[k] - 44, 8, 30, "corpo fino")                                    # janelas
    # caixa da escada com degraus e patamares
    d.ret(EX0, NIVEIS[5], EX1 - EX0, TERREO - NIVEIS[5], "grosso")
    for k in range(5):
        y = NIVEIS[k]
        p = "M%d %d" % (EX0 + 14, y)
        for s in range(8):                                                                     # lance de ida
            p += " v-3.9 h13"
        p += " H%d" % (EX1 - 6)
        d.caminho(p, "fino")
        p = "M%d %s" % (EX1 - 22, n(y - 31.2))
        for s in range(8):                                                                     # lance de volta
            p += " v-3.85 h-13"
        d.caminho(p, "fino")
        d.caminho("M%d %s l104 -31" % (EX0 + 14, n(y - 14)), "fino")                                        # corrimãos
        if k < 4:
            d.caminho("M%d %s l-104 -31" % (EX1 - 22, n(y - 45)), "fino")
    # portas corta-fogo (uma por pavimento)
    for k in range(5):
        d.ret(EX1 - 3, NIVEIS[k] - 42, 6, 42, "corpo azul")
    # duto vertical com grelhas de insuflamento
    d.ret(DX0, NIVEIS[5], 50, TERREO - NIVEIS[5])
    for k in range(5):
        y = NIVEIS[k] - 40
        d.ret(EX0 - 4, y, 8, 20, "corpo")
        for s in range(4):
            d.linha(EX0 - 4, y + 4 + 4 * s, EX0 + 4, y + 2 + 4 * s, "fino")
    # casa dos ventiladores no térreo
    d.ret(232, TERREO - PE, DX0 - 232, PE, "grosso")
    for k, vx in enumerate((300, 372)):
        d.circ(vx, TERREO - 28, 19, "corpo"); d.caminho("M%d %d L%d %d H%d Z" % (vx, TERREO - 47, vx + 16, TERREO - 19, vx - 16), "fino")
        d.ret(vx - 14, TERREO - 9, 28, 9, "corpo")
    d.caminho("M391 %d H%d" % (TERREO - 28, DX0), "fino")
    for s in range(5):                                                                          # veneziana e filtro da tomada de ar
        d.linha(220, TERREO - 50 + 9 * s, 232, TERREO - 44 + 9 * s, "fino")
    d.caminho("M244 %d l8 8 l-8 8 l8 8 l-8 8 l8 8" % (TERREO - 50), "fino")
    # damper de alívio no topo da escada
    d.ret(532, NIVEIS[5] - 16, 44, 16, "corpo"); d.caminho("M540 %d l8 -12 M552 %d l8 -12 M564 %d l8 -12" % (NIVEIS[5] - 2, NIVEIS[5] - 2, NIVEIS[5] - 2), "fino")
    d.linha(180, TERREO, 940, TERREO, "grosso")

    # ar em movimento
    fluxo = "M170 %d H%d M%d %d V%d" % (TERREO - 28, 280, DX0 + 25, TERREO - 12, NIVEIS[5] + 12)
    fluxo += "".join("M%d %d H%d" % (EX0 + 6, NIVEIS[k] - 30, EX0 + 44) for k in range(5))
    fluxo += "M554 %d V%d" % (NIVEIS[5] - 18, NIVEIS[5] - 44)
    d.frente.append('<path class="fluxo" stroke="#C9D7FB" stroke-width="2" d="%s"/>' % fluxo)

    # textos
    NOMES = ("TÉRREO", "1º PAV.", "2º PAV.", "3º PAV.", "4º PAV.")
    for k, nome in enumerate(NOMES):
        d.texto(FX1 - 20, NIVEIS[k] - 12, nome, "t p", "end"); d.texto(EX1 + 12, NIVEIS[k] - 12, "PCF", "t p")
    d.texto(760, y2 - 34, "pavimento em incêndio", "t", "middle"); d.texto(760, y2 - 18, "fumaça não entra na escada", "t p", "middle")
    d.texto((EX0 + EX1) / 2, NIVEIS[2] - 26, "+50 Pa", "t c", "middle")
    d.texto(232, TERREO - PE - 26, "Ventiladores"); d.texto(232, TERREO - PE - 10, "principal e reserva", "t p")
    d.texto(160, TERREO - 40, "ar externo", "t p", "end"); d.texto(160, TERREO - 24, "filtrado", "t p", "end")
    d.texto(584, NIVEIS[5] - 24, "damper de alívio", "t p")
    d.texto(DX0 + 25, 400, "duto", "t p", "middle"); d.texto((EX0 + EX1) / 2, 400, "ESCADA PRESSURIZADA", "t p", "middle")
    d.cota(930, NIVEIS[0], 930, NIVEIS[1], "3,00", tam_texto="t p")
    d.cota(956, NIVEIS[0], 956, NIVEIS[5], "15,00", tam_texto="t p")

    # o que o projeto define + carimbo
    NX = 1010
    d.texto(NX, 64, "O QUE O PROJETO DEFINE")
    for k, t in enumerate(("1. Diferencial de pressão escada / pavimento", "2. Velocidade do ar pela porta aberta", "3. Vazão e pressão dos ventiladores",
                           "4. Alimentação elétrica de emergência", "5. Tomada de ar protegida da fumaça", "6. Acionamento pela central de alarme")):
        d.texto(NX, 92 + 21 * k, t, "t p")
    carimbo(d, NX, 300, 250, "PRESSURIZAÇÃO · CORTE", "NBR 14880 · VALORES DE EXEMPLO")
    return d.svg("Corte esquemático de uma escada pressurizada de cinco pavimentos: ventiladores, duto vertical com grelhas, portas corta-fogo, damper de alívio e pavimento em incêndio")


FIGURAS = {"consultoria": (balancim, prensa, flange), "hvac": (cfd, isometrico, escada)}

if __name__ == "__main__":
    site, arquivo = sys.argv[1], sys.argv[2]
    for k, figura in enumerate(FIGURAS[site]):
        inserir(arquivo, "p%d" % (k + 1), figura())
    print("pranchas ok:", site)
