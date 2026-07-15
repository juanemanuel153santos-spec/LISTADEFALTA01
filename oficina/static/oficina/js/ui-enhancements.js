/* ============================================
   OFICINA - MELHORIAS DE INTERFACE
   Cole este arquivo em: motopecas/oficina/static/js/ui-enhancements.js
   E inclua no final do seu template com:
   <script src="{% static 'js/ui-enhancements.js' %}"></script>
   ============================================ */

document.addEventListener("DOMContentLoaded", function () {
  inicializarBusca();
  inicializarModalConfirmacao();
  inicializarValidacaoQuantidade();
  inicializarToast();
});

/* ---------------------------------------------
   1. BUSCA COM DESTAQUE (highlight) NA TABELA
   Funciona em qualquer input com [data-busca-tabela]
   apontando pro id da tabela a filtrar.
   Ex: <input data-busca-tabela="tabela-pecas" class="busca-input">
--------------------------------------------- */
function inicializarBusca() {
  const inputs = document.querySelectorAll("[data-busca-tabela]");

  inputs.forEach(function (input) {
    const tabela = document.getElementById(input.dataset.buscaTabela);
    if (!tabela) return;

    const linhas = tabela.querySelectorAll("tbody tr");

    input.addEventListener("input", function () {
      const termo = input.value.trim().toLowerCase();

      linhas.forEach(function (linha) {
        const textoOriginal = linha.dataset.textoOriginal || linha.textContent;
        // guarda o texto original só na primeira vez
        if (!linha.dataset.textoOriginal) {
          linha.dataset.textoOriginal = linha.textContent;
        }

        const textoLower = textoOriginal.toLowerCase();
        const combina = termo === "" || textoLower.includes(termo);

        linha.classList.toggle("linha-oculta", !combina);

        // destaque (highlight) simples nas células de texto
        limparDestaque(linha);
        if (combina && termo !== "") {
          destacarTermo(linha, termo);
        }
      });
    });
  });
}

function limparDestaque(linha) {
  linha.querySelectorAll("mark").forEach(function (mark) {
    const pai = mark.parentNode;
    pai.replaceChild(document.createTextNode(mark.textContent), mark);
    pai.normalize();
  });
}

function destacarTermo(linha, termo) {
  const celulas = linha.querySelectorAll("td");
  celulas.forEach(function (celula) {
    // não mexe em células que têm botões/inputs dentro
    if (celula.querySelector("button, input, select, a")) return;

    const regex = new RegExp("(" + escapeRegExp(termo) + ")", "gi");
    const textoOriginal = celula.textContent;
    if (regex.test(textoOriginal)) {
      celula.innerHTML = textoOriginal.replace(regex, "<mark>$1</mark>");
    }
  });
}

function escapeRegExp(texto) {
  return texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* ---------------------------------------------
   2. MODAL DE CONFIRMAÇÃO (substitui confirm() nativo)
   Uso: adicione [data-confirmar] no botão/link e
   [data-confirmar-titulo] / [data-confirmar-texto] opcionais.
   Ex:
   <button data-confirmar
           data-confirmar-titulo="Marcar como comprado?"
           data-confirmar-texto="Essa ação vai atualizar o estoque."
           data-form-alvo="form-comprar-3">
     Marcar como comprado
   </button>
--------------------------------------------- */
function inicializarModalConfirmacao() {
  // cria o modal uma única vez no body
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal-caixa">
      <p class="modal-titulo" id="modal-titulo">Confirmar ação</p>
      <p class="modal-texto" id="modal-texto">Tem certeza que deseja continuar?</p>
      <div class="modal-acoes">
        <button type="button" class="btn" id="modal-cancelar" style="background:#e5e7eb;color:#374151;">Cancelar</button>
        <button type="button" class="btn btn-sucesso" id="modal-confirmar">Confirmar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const tituloEl = overlay.querySelector("#modal-titulo");
  const textoEl = overlay.querySelector("#modal-texto");
  const btnConfirmar = overlay.querySelector("#modal-confirmar");
  const btnCancelar = overlay.querySelector("#modal-cancelar");

  let formPendente = null;
  let cliquePendente = null;

  function fecharModal() {
    overlay.classList.remove("aberto");
    formPendente = null;
    cliquePendente = null;
  }

  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) fecharModal();
  });
  btnCancelar.addEventListener("click", fecharModal);

  btnConfirmar.addEventListener("click", function () {
    if (formPendente) {
      formPendente.submit();
    } else if (cliquePendente) {
      cliquePendente();
    }
    fecharModal();
  });

  document.querySelectorAll("[data-confirmar]").forEach(function (elemento) {
    elemento.addEventListener("click", function (e) {
      e.preventDefault();

      tituloEl.textContent = elemento.dataset.confirmarTitulo || "Confirmar ação";
      textoEl.textContent = elemento.dataset.confirmarTexto || "Tem certeza que deseja continuar?";

      const formAlvoId = elemento.dataset.formAlvo;
      if (formAlvoId) {
        formPendente = document.getElementById(formAlvoId);
      } else if (elemento.tagName === "A" && elemento.href) {
        cliquePendente = function () {
          window.location.href = elemento.href;
        };
      } else {
        const formPai = elemento.closest("form");
        formPendente = formPai || null;
      }

      overlay.classList.add("aberto");
    });
  });
}

/* ---------------------------------------------
   3. VALIDAÇÃO VISUAL DE QUANTIDADE (zero ou negativa)
   Aplica em qualquer input com [data-validar-quantidade]
--------------------------------------------- */
function inicializarValidacaoQuantidade() {
  const campos = document.querySelectorAll("[data-validar-quantidade]");

  campos.forEach(function (campo) {
    // cria a mensagem de erro logo abaixo do campo, se não existir
    let mensagem = campo.nextElementSibling;
    if (!mensagem || !mensagem.classList.contains("mensagem-erro")) {
      mensagem = document.createElement("div");
      mensagem.className = "mensagem-erro";
      mensagem.textContent = "A quantidade precisa ser maior que zero.";
      campo.insertAdjacentElement("afterend", mensagem);
    }

    function validar() {
      const valor = parseFloat(campo.value);
      const invalido = isNaN(valor) || valor <= 0;

      campo.classList.toggle("input-erro", invalido);
      mensagem.classList.toggle("visivel", invalido);

      return !invalido;
    }

    campo.addEventListener("input", validar);

    const form = campo.closest("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        if (!validar()) {
          e.preventDefault();
          campo.focus();
        }
      });
    }
  });
}

/* ---------------------------------------------
   4. TOAST — aviso rápido no canto da tela
   Uso via JS: mostrarToast("Peça marcada como comprada!", "sucesso")
   Também lê mensagens do Django (django.contrib.messages) se existirem
   em elementos com [data-toast-mensagem] e [data-toast-tipo].
--------------------------------------------- */
function inicializarToast() {
  document.querySelectorAll("[data-toast-mensagem]").forEach(function (el) {
    mostrarToast(el.dataset.toastMensagem, el.dataset.toastTipo || "sucesso");
  });
}

function mostrarToast(mensagem, tipo) {
  const toast = document.createElement("div");
  toast.className = "toast " + (tipo || "sucesso");
  toast.textContent = mensagem;
  document.body.appendChild(toast);

  requestAnimationFrame(function () {
    toast.classList.add("visivel");
  });

  setTimeout(function () {
    toast.classList.remove("visivel");
    setTimeout(function () {
      toast.remove();
    }, 250);
  }, 3000);
}
