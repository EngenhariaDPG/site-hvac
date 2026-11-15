/* ==========================================================================
   DPG Engenharia Mecânica — script compartilhado (idêntico nos dois sites)
   --------------------------------------------------------------------------
   Sem dependências e sem etapa de build. Blocos:
     1. Configuração (número do WhatsApp)
     2. Menu do celular
     3. Sombra do cabeçalho ao rolar
     4. Traçado dos desenhos técnicos (SVG)
     5. Revelação dos títulos ao rolar
     6. Formulário -> mensagem no WhatsApp
   ========================================================================== */
(function () {
  "use strict";

  /* 1. Configuração ------------------------------------------------------- */
  // Para trocar o número de atendimento, altere SOMENTE esta linha
  // (e os links wa.me escritos direto no HTML).
  var WHATSAPP = "5532999042269";

  // Respeita quem pediu menos movimento no sistema operacional.
  var menosMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 2. Menu do celular ---------------------------------------------------- */
  var botaoMenu = document.querySelector(".abre-menu");
  var menu = document.querySelector(".menu");

  function alternarMenu(abrir) {
    if (!botaoMenu || !menu) return;
    botaoMenu.setAttribute("aria-expanded", String(abrir));
    botaoMenu.setAttribute("aria-label", abrir ? "Fechar menu" : "Abrir menu");
    menu.classList.toggle("aberto", abrir);
    document.body.classList.toggle("menu-aberto", abrir);
  }

  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () {
      alternarMenu(botaoMenu.getAttribute("aria-expanded") !== "true");
    });
    // Fecha ao escolher um item ou apertar Esc.
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { alternarMenu(false); });
    });
    document.addEventListener("keydown", function (evento) {
      if (evento.key === "Escape") alternarMenu(false);
    });
  }

  /* 3. Sombra do cabeçalho ao rolar --------------------------------------- */
  var cabecalho = document.querySelector(".cabecalho");
  function marcarRolagem() {
    if (cabecalho) cabecalho.classList.toggle("rolou", window.scrollY > 8);
  }
  window.addEventListener("scroll", marcarRolagem, { passive: true });
  marcarRolagem();

  /* 4. Traçado dos desenhos técnicos -------------------------------------- */
  // Cada <figure class="desenho"> contém um SVG. Tudo o que estiver dentro de
  // um grupo .tinta é "desenhado" linha a linha (técnica do stroke-dashoffset).
  // Elementos dentro de .tarde aparecem depois, por CSS (textos, preenchimentos).
  var GEOMETRIAS = "path, line, polyline, polygon, rect, circle, ellipse";
  var DURACAO_TOTAL = 2200; // ms para o desenho inteiro começar a aparecer
  var DURACAO_LINHA = 900;  // ms que cada linha leva para ser traçada

  function prepararDesenho(figura) {
    var linhas = figura.querySelectorAll(".tinta " + GEOMETRIAS);
    var passo = Math.min(45, DURACAO_TOTAL / Math.max(linhas.length, 1));
    // As linhas usam vector-effect: non-scaling-stroke (espessura constante na tela),
    // e nesse modo o tracejado é medido em pixels de tela. Por isso o comprimento
    // é corrigido pela escala em que o SVG está sendo exibido (+10% de folga).
    var svg = figura.querySelector("svg");
    var escala = svg && svg.viewBox.baseVal.width ? svg.getBoundingClientRect().width / svg.viewBox.baseVal.width : 1;
    var fator = Math.max(1, escala) * 1.1;
    linhas.forEach(function (linha, indice) {
      // Linhas tracejadas (eixos, retornos) não podem usar esta técnica: ficam em .tarde.
      if (linha.closest(".tarde") || typeof linha.getTotalLength !== "function") return;
      var comprimento = Math.ceil(linha.getTotalLength() * fator);
      linha.style.strokeDasharray = comprimento;
      linha.style.strokeDashoffset = comprimento;
      linha.style.transition = "stroke-dashoffset " + DURACAO_LINHA + "ms cubic-bezier(.6,0,.2,1) " + Math.round(indice * passo) + "ms";
    });
  }

  function tracarDesenho(figura) {
    figura.classList.add("tracado");
    var linhas = figura.querySelectorAll(".tinta " + GEOMETRIAS);
    linhas.forEach(function (linha) {
      if (!linha.closest(".tarde")) linha.style.strokeDashoffset = "0";
    });
    // Terminado o traçado, remove o tracejado para o desenho não abrir falhas
    // se a janela for redimensionada (ex.: girar o celular).
    setTimeout(function () {
      linhas.forEach(function (linha) {
        linha.style.transition = "none";
        linha.style.strokeDasharray = "";
        linha.style.strokeDashoffset = "";
      });
    }, DURACAO_TOTAL + DURACAO_LINHA + 300);
  }

  var desenhos = document.querySelectorAll(".desenho");
  if (menosMovimento || !("IntersectionObserver" in window)) {
    // Sem animação: mostra tudo pronto.
    desenhos.forEach(function (figura) { figura.classList.add("tracado"); });
  } else {
    desenhos.forEach(prepararDesenho);
    var observadorDesenho = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        tracarDesenho(entrada.target);
        observadorDesenho.unobserve(entrada.target);
      });
    }, { threshold: 0.25 });
    desenhos.forEach(function (figura) { observadorDesenho.observe(figura); });
  }

  /* 5. Revelação dos títulos ao rolar ------------------------------------- */
  var revelar = document.querySelectorAll(".revela");
  if (menosMovimento || !("IntersectionObserver" in window)) {
    revelar.forEach(function (item) { item.classList.add("visivel"); });
  } else {
    var observadorTitulo = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("visivel");
        observadorTitulo.unobserve(entrada.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    revelar.forEach(function (item) { observadorTitulo.observe(item); });
  }

  /* 6. Formulário -> WhatsApp --------------------------------------------- */
  // O site não tem servidor: o formulário apenas monta uma mensagem e abre o
  // WhatsApp. Nenhum dado é armazenado. A saudação vem do atributo
  // data-saudacao do <form>, para cada site ter a sua.
  var formulario = document.getElementById("formulario-contato");
  if (formulario) {
    formulario.addEventListener("submit", function (evento) {
      evento.preventDefault();
      if (!formulario.reportValidity()) return;

      var dados = new FormData(formulario);
      var mensagem = [
        formulario.dataset.saudacao || "Olá! Gostaria de falar com a DPG Engenharia Mecânica.",
        "",
        "Nome: " + dados.get("nome"),
        "Empresa: " + (dados.get("empresa") || "não informada"),
        "Cidade/UF: " + dados.get("cidade"),
        "Serviço: " + dados.get("servico"),
        "",
        "Descrição:",
        dados.get("mensagem")
      ].join("\n");

      var endereco = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(mensagem);
      var janela = window.open(endereco, "_blank");
      if (janela) janela.opener = null; // segurança: a nova aba não acessa esta página

      // Se o navegador bloquear a nova aba, oferece o link para o visitante clicar.
      var retorno = document.getElementById("retorno");
      if (retorno) {
        retorno.textContent = janela ? "Mensagem pronta no WhatsApp. " : "Seu navegador bloqueou a nova aba. ";
        var link = document.createElement("a");
        link.href = endereco;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = "Abrir o WhatsApp com a mensagem";
        retorno.appendChild(link);
      }
    });
  }

  /* Ano corrente no rodapé */
  var ano = document.getElementById("ano");
  if (ano) ano.textContent = String(new Date().getFullYear());
})();
