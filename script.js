const WHATSAPP_NUMBER = "5532999042269";

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".main-nav");

function closeMenu() {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Abrir menu");
  navigation.classList.remove("is-open");
  document.body.classList.remove("menu-open");
}

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    menuButton.setAttribute("aria-label", open ? "Abrir menu" : "Fechar menu");
    navigation.classList.toggle("is-open", !open);
    document.body.classList.toggle("menu-open", !open);
  });
  navigation.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu();
  });
}

const year = document.getElementById("current-year");
if (year) year.textContent = String(new Date().getFullYear());

const revealItems = document.querySelectorAll(".reveal");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if ("IntersectionObserver" in window && !reduceMotion) {
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });
  revealItems.forEach(item => revealObserver.observe(item));
} else {
  revealItems.forEach(item => item.classList.add("is-visible"));
}

const form = document.getElementById("contact-form");
if (form) {
  form.addEventListener("submit", event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const message = [
      "Olá! Gostaria de conversar com a DPG sobre um projeto HVAC.",
      "",
      "Nome: " + data.get("nome"),
      "Empresa: " + (data.get("empresa") || "Não informada"),
      "Cidade/UF: " + data.get("cidade"),
      "Tipo de projeto: " + data.get("servico"),
      "",
      "Informações sobre o empreendimento:",
      data.get("mensagem")
    ].join("\n");
    const url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(message);
    const opened = window.open(url, "_blank", "noopener,noreferrer");
    const status = document.getElementById("form-status");
    if (!opened && status) status.textContent = "Não foi possível abrir uma nova aba. Permita pop-ups ou use o contato direto por WhatsApp ao lado.";
  });
}
