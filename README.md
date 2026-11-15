# DPG Engenharia Mecânica — HVAC

Site estático da frente de **projetos de climatização, ventilação, exaustão, água gelada, refrigeração, gases e proteção contra incêndio** da DPG Engenharia Mecânica (Eng. Denys Pinto Gonçalves, CREA-MG 142398574-5, Juiz de Fora/MG).

Sem framework e sem etapa de build: HTML, CSS e JavaScript puros. Basta publicar a pasta (GitHub Pages, por exemplo).

## Estrutura

| Arquivo | O que é |
| --- | --- |
| `index.html` | Página inicial: capa com desenho técnico animado, serviços, entregas, normas, processo, responsável técnico, caderno e contato |
| `styles.css` | Folha de estilos, comentada e dividida em seções numeradas. **Idêntica nos dois sites** (site-consultoria e site-hvac) |
| `script.js` | Menu do celular, animação de traçado dos desenhos, formulário que abre o WhatsApp. **Idêntico nos dois sites** |
| `assets/` | Logo oficial (`dpg-monograma.svg`, `dpg-assinatura.svg`), foto e imagem de compartilhamento (`capa-social.png`) |
| `blog/` | Caderno técnico: índice e artigos |
| `ferramentas/` | Scripts Python que geram os desenhos técnicos (SVG) embutidos no `index.html` |

## Identidade visual

Segue o Manual de Marca DPG (out/2026): preto `#000000`, grafite `#111820`, azul técnico `#245BDB`, branco e cinzas de apoio `#F2F4F7` / `#5B6470`; tipografia Arial; grafismo diagonal azul. As cores ficam em variáveis no topo do `styles.css` (`:root`). O logo é sempre o arquivo oficial, nunca redigitado.

O atributo `data-site` no `<body>` define o tema: `consultoria` (capa clara) ou `hvac` (capa escura).

## Como alterar

- **Textos, serviços e normas:** direto no `index.html`. Cada seção tem um comentário de abertura.
- **Número do WhatsApp:** variável `WHATSAPP` no topo do `script.js` e links `wa.me` no HTML.
- **Cores e espaçamentos:** variáveis em `:root`, no início do `styles.css`.
- **Desenhos técnicos:** são SVG gerados por código. No `index.html` cada um fica entre os marcadores `<!-- DESENHO:nome -->` e `<!-- /DESENHO:nome -->`. Para mudar um desenho, edite o script e rode de novo na raiz do repositório:

```
python3 ferramentas/gerar_hvac.py index.html              # desenho da capa
python3 ferramentas/gerar_pranchas.py hvac index.html        # figuras da seção "Entregas"
```

  `ferramentas/desenho.py` é a pequena biblioteca comum (linhas, cotas com setas, balões, sólidos).
- **Novo artigo:** copie um arquivo de `blog/`, troque título, descrição e texto, e acrescente o link em `blog/index.html`, no `index.html` (seção "Caderno técnico") e no `sitemap.xml`.

Ao mudar `styles.css` ou `script.js`, copie o arquivo para o outro site para manter os dois iguais.

## Cuidados de conteúdo

- Os desenhos e valores são ilustrativos; não representam cliente ou obra específica.
- Não publicar prazos, quantidade de projetos, certificações ou depoimentos que não possam ser comprovados.
- As normas citadas devem ser conferidas na edição vigente antes de cada revisão do site.
- A DPG projeta e documenta; instalação e fornecimento de equipamentos não são oferecidos neste site.

## Testar no computador

```
python3 -m http.server 8000
```

Depois abra `http://localhost:8000`.
