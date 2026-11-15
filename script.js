const WHATSAPP_NUMBER = "5532999042269";

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".nav");

function closeMenu() {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Abrir menu");
  navigation.classList.remove("is-open");
}

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    menuButton.setAttribute("aria-label", open ? "Abrir menu" : "Fechar menu");
    navigation.classList.toggle("is-open", !open);
  });
  navigation.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu();
  });
}

const year = document.getElementById("current-year");
if (year) year.textContent = String(new Date().getFullYear());

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
    window.open(url, "_blank", "noopener,noreferrer");
  });
}