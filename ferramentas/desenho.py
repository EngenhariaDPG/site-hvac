"""
Biblioteca mínima para gerar os desenhos técnicos (SVG) dos sites da DPG.

Cada desenho é montado em três camadas, na ordem em que aparecem na tela:
  fundo  -> preenchimentos e tracejados que ficam ATRÁS das linhas (grupo .tarde)
  tinta  -> linhas que o script.js "traça" ao entrar na tela      (grupo .tinta)
  frente -> textos, setas e símbolos que aparecem depois           (grupo .tarde)

Classes CSS usadas (definidas em styles.css, seção "Desenhos técnicos"):
  grosso / fino / cota / azul  espessura e cor da linha
  corpo                        sólido preenchido (esconde o que está atrás)
  t / t p / t c                texto, texto pequeno, texto de cota
"""
import math


def n(v):
    """Formata número com no máximo 1 casa decimal (SVG mais enxuto)."""
    return ("%.1f" % v).rstrip("0").rstrip(".")


class Desenho:
    def __init__(self, largura, altura):
        self.largura, self.altura = largura, altura
        self.defs, self.fundo, self.tinta, self.frente = [], [], [], []

    # ---------- primitivas (por padrão vão para a camada "tinta") ----------
    def _attr(self, cls, extra):
        return (' class="%s"' % cls if cls else "") + ((" " + extra) if extra else "")

    def linha(self, x1, y1, x2, y2, cls="", camada=None, extra=""):
        (camada if camada is not None else self.tinta).append(
            '<line%s x1="%s" y1="%s" x2="%s" y2="%s"/>' % (self._attr(cls, extra), n(x1), n(y1), n(x2), n(y2)))

    def ret(self, x, y, w, h, cls="", camada=None, extra="", r=0):
        raio = ' rx="%s"' % n(r) if r else ""
        (camada if camada is not None else self.tinta).append(
            '<rect%s x="%s" y="%s" width="%s" height="%s"%s/>' % (self._attr(cls, extra), n(x), n(y), n(w), n(h), raio))

    def circ(self, cx, cy, r, cls="", camada=None, extra=""):
        (camada if camada is not None else self.tinta).append(
            '<circle%s cx="%s" cy="%s" r="%s"/>' % (self._attr(cls, extra), n(cx), n(cy), n(r)))

    def caminho(self, d, cls="", camada=None, extra=""):
        (camada if camada is not None else self.tinta).append('<path%s d="%s"/>' % (self._attr(cls, extra), d))

    def poli(self, pontos, cls="", camada=None, extra=""):
        d = "M" + " L".join("%s %s" % (n(x), n(y)) for x, y in pontos) + " Z"
        self.caminho(d, cls, camada, extra)

    def texto(self, x, y, s, cls="t", ancora="", extra=""):
        a = ' text-anchor="%s"' % ancora if ancora else ""
        self.frente.append('<text class="%s" x="%s" y="%s"%s%s>%s</text>' % (cls, n(x), n(y), a, (" " + extra) if extra else "", s))

    def bruto(self, s, camada=None):
        (camada if camada is not None else self.tinta).append(s)

    # ---------- elementos compostos ----------
    def barra(self, x0, y0, x1, y1, largura, cls="corpo", camada=None):
        """Retângulo inclinado entre dois pontos (lanças, cilindros, perfis)."""
        dx, dy = x1 - x0, y1 - y0
        comp = math.hypot(dx, dy)
        px, py = -dy / comp * largura / 2, dx / comp * largura / 2
        self.poli([(x0 + px, y0 + py), (x1 + px, y1 + py), (x1 - px, y1 - py), (x0 - px, y0 - py)], cls, camada)

    def seta(self, x, y, angulo, tam=9, cls="seta"):
        """Ponta de seta cheia; angulo em graus, apontando para (x, y)."""
        a = math.radians(angulo)
        p = [(x, y)]
        for lado in (-1, 1):
            b = a + math.pi + lado * math.radians(14)
            p.append((x + tam * math.cos(b), y + tam * math.sin(b)))
        d = "M" + " L".join("%s %s" % (n(px), n(py)) for px, py in p) + " Z"
        self.frente.append('<path class="%s" d="%s"/>' % (cls, d))

    def cota(self, x1, y1, x2, y2, rotulo, afast=0, lado=-1, ext=0, tam_texto="t c"):
        """Cota linear com setas nas pontas e texto centrado.
        afast: distância do texto à linha; lado: -1 texto acima/à esquerda, 1 abaixo/à direita
        ext: comprimento das linhas de chamada (perpendiculares) em cada ponta."""
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        comp = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / comp, (y2 - y1) / comp
        px, py = -uy, ux
        self.linha(x1, y1, x2, y2, "cota")
        for (x, y) in ((x1, y1), (x2, y2)):
            self.linha(x - px * 7, y - py * 7, x + px * (7 + ext), y + py * (7 + ext), "cota")
        self.seta(x1, y1, ang + 180)
        self.seta(x2, y2, ang)
        mx, my = (x1 + x2) / 2 + px * lado * (afast + 8), (y1 + y2) / 2 + py * lado * (afast + 8)
        giro = ang if -90 <= ang < 90 else ang + 180   # texto vertical lido de baixo para cima
        self.frente.append('<text class="%s" text-anchor="middle" transform="translate(%s %s) rotate(%s)">%s</text>'
                           % (tam_texto, n(mx), n(my), n(giro), rotulo))

    def balao(self, x, y, numero, ax, ay):
        """Balão numerado com linha de chamada até (ax, ay)."""
        ang = math.atan2(ay - y, ax - x)
        self.linha(x + 12 * math.cos(ang), y + 12 * math.sin(ang), ax, ay, "fino")
        self.circ(ax, ay, 2.2, "ponto", self.frente)
        self.circ(x, y, 12, "fino")
        self.texto(x, y + 4.5, str(numero), "t", "middle")

    # ---------- saída ----------
    def svg(self, rotulo, oculto=False):
        acess = 'aria-hidden="true"' if oculto else 'role="img" aria-label="%s"' % rotulo
        partes = ['<svg viewBox="0 0 %d %d" %s>' % (self.largura, self.altura, acess)]
        if self.defs:
            partes.append("<defs>" + "".join(self.defs) + "</defs>")
        if self.fundo:
            partes.append('<g class="tarde">' + "".join(self.fundo) + "</g>")
        partes.append('<g class="tinta">' + "".join(self.tinta) + "</g>")
        partes.append('<g class="tarde">' + "".join(self.frente) + "</g>")
        partes.append("</svg>")
        return "\n".join(partes)


def inserir(arquivo_html, nome, svg):
    """Troca o conteúdo entre <!-- DESENHO:nome --> e <!-- /DESENHO:nome --> pelo SVG gerado."""
    ini, fim = "<!-- DESENHO:%s -->" % nome, "<!-- /DESENHO:%s -->" % nome
    html = open(arquivo_html, encoding="utf-8").read()
    a, b = html.index(ini) + len(ini), html.index(fim)
    html = html[:a] + "\n" + svg + "\n" + html[b:]
    open(arquivo_html, "w", encoding="utf-8").write(html)
