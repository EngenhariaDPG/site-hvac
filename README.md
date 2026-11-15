# DPG Engenharia Mecânica — Projetos HVAC

Site institucional estático da DPG Engenharia Mecânica. Apresenta exclusivamente serviços de projetos HVAC e documentação técnica.

**Site público:** https://muitozika12.github.io/site-hvac/

## Escopo e informações confirmadas

- A atuação apresentada é de desenvolvimento de projetos HVAC e documentação técnica.
- Não são oferecidos instalação, execução, fornecimento de equipamentos ou manutenção.
- Contato por WhatsApp: `(32) 99904-2269` (`5532999042269`).
- Responsável técnico informado: Denys Pinto Gonçalves — CREA-MG `142398574-5`.
- A página de contato não envia nem armazena dados em servidor. O briefing monta uma mensagem e abre o WhatsApp.
- O blog contém três artigos informativos. Eles distinguem desenvolvimento de projeto das etapas de execução e não prometem conformidade, certificações ou resultados.

## Melhorias desta versão

- Redesign editorial/cinematográfico com grafite, azul técnico, tipografia expressiva e imagem original local.
- Layout responsivo com prioridade para telas móveis, menu acessível e navegação entre páginas estáticas.
- Scroll reveal com alternativa para `prefers-reduced-motion`.
- Formulário de briefing com validação nativa e encaminhamento ao WhatsApp.
- Blog navegável com índice e três artigos próprios em HTML.
- Links internos relativos, URLs canônicas, metadados Open Graph, sitemap XML e robots.txt alinhados ao domínio publicado.

## Estrutura

```text
.
├── index.html                         # Landing page da DPG
├── styles.css                         # Estilos compartilhados e responsivos
├── script.js                          # Menu, reveal e formulário para WhatsApp
├── favicon.svg                        # Ícone do site
├── logo.svg                           # Logotipo vetorial existente
├── assets/
│   ├── hvac-hero-optimized.jpg        # Imagem ilustrativa otimizada para o hero
├── sitemap.xml                        # Endereços públicos indexáveis
├── robots.txt                         # Regras de rastreamento e sitemap
└── blog/
    ├── index.html                     # Índice do caderno técnico
    ├── projeto-hvac.html              # Artigo sobre escopo de projeto HVAC
    ├── ventilacao-renovacao-ar.html   # Artigo sobre ventilação e renovação do ar
    └── coordenacao-interdisciplinar.html # Artigo sobre coordenação entre disciplinas
```

As páginas do blog reutilizam `../styles.css` e `../script.js`. A implementação não exige build nem dependências locais.

## Publicação no GitHub Pages

O site é publicado pela branch `main`, pasta `/(root)`, no endereço `https://muitozika12.github.io/site-hvac/`. O campo homepage do repositório, os canônicos, os metadados sociais, o sitemap e o robots.txt devem permanecer alinhados se o domínio ou a configuração de publicação mudar.

## Avisos antes da divulgação

- Revisar se o escopo, as entregas e as atribuições descritas correspondem ao serviço efetivamente contratado e ofertado.
- Não adicionar alegações de clientes, cases, depoimentos, economias, ROI, preços, certificações, garantias de conformidade ou capacidades sem confirmação documental.
- A imagem hero incluída é ilustrativa e não representa obra, instalação ou case da DPG. Substituições devem ter direitos e adequação confirmados.
- O formulário depende da abertura do WhatsApp no navegador do visitante.
