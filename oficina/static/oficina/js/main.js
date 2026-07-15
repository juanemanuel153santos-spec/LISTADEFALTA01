// Filtra as linhas de uma tabela conforme o usuário digita na caixa de busca.
// Uso: <input oninput="filtrarTabela(this, 'id-da-tabela')">
function filtrarTabela(input, idTabela) {
    const termo = input.value.toLowerCase();
    const tabela = document.getElementById(idTabela);
    const linhas = tabela.querySelectorAll('tbody tr');

    linhas.forEach((linha) => {
        const texto = linha.textContent.toLowerCase();
        linha.style.display = texto.includes(termo) ? '' : 'none';
    });
}

// Pede confirmação antes de seguir um link (ex: marcar como comprado).
// Uso: <a href="..." onclick="return confirmar('Marcar como comprado?')">
function confirmar(mensagem) {
    return window.confirm(mensagem);
}

// Validação simples no navegador antes de enviar formulários de cadastro:
// evita mandar campos numéricos com valor zero ou negativo.
document.addEventListener('DOMContentLoaded', () => {
    const formularios = document.querySelectorAll('form[data-validar]');

    formularios.forEach((form) => {
        form.addEventListener('submit', (evento) => {
            const camposNumericos = form.querySelectorAll('input[type="number"]');
            let valido = true;

            camposNumericos.forEach((campo) => {
                if (campo.value !== '' && Number(campo.value) <= 0) {
                    valido = false;
                    campo.style.border = '2px solid #cc0000';
                } else {
                    campo.style.border = '';
                }
            });

            if (!valido) {
                evento.preventDefault();
                alert('Verifique os campos destacados em vermelho: os valores precisam ser maiores que zero.');
            }
        });
    });
});
