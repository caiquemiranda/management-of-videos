let arquivoSelecionado = null;
let infoVideo = null;

const fileInput = document.getElementById('video-corte');
const infoDiv = document.getElementById('info-video');
const btnConfirmar = document.getElementById('btn-confirmar-corte');
const btnEnviar = document.getElementById('btn-enviar-corte');
const statusCorte = document.getElementById('status-corte');

fileInput.addEventListener('change', async function () {
    infoDiv.innerHTML = '';
    btnConfirmar.style.display = 'none';
    btnEnviar.style.display = 'none';
    statusCorte.textContent = '';
    arquivoSelecionado = null;
    infoVideo = null;
    if (!fileInput.files.length) return;
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    infoDiv.innerHTML = 'Analisando vídeo...';
    try {
        const resp = await fetch('/info_video', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (data.success) {
            arquivoSelecionado = file;
            infoVideo = data;
            infoDiv.innerHTML = `Duração: <b>${data.duracao.toFixed(2)}s</b><br>O vídeo será cortado em <b>${data.num_partes}</b> parte(s).`;
            btnConfirmar.style.display = 'inline-block';
        } else {
            infoDiv.innerHTML = data.message || 'Erro ao analisar vídeo.';
        }
    } catch (err) {
        infoDiv.innerHTML = 'Erro ao analisar vídeo.';
    }
});

btnConfirmar.addEventListener('click', function () {
    btnConfirmar.style.display = 'none';
    btnEnviar.style.display = 'inline-block';
});

document.getElementById('form-corte').addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!arquivoSelecionado) return;
    statusCorte.textContent = 'Enviando vídeo e cortando...';
    statusCorte.style.color = '#444';
    btnEnviar.style.display = 'none';
    const formData = new FormData();
    formData.append('file', arquivoSelecionado);
    try {
        const response = await fetch('/cortar', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        statusCorte.textContent = data.message;
        statusCorte.style.color = data.success ? '#1976d2' : '#c00';
        if (data.success) {
            atualizarListaCortes();
            fileInput.value = '';
            infoDiv.innerHTML = '';
            arquivoSelecionado = null;
            infoVideo = null;
        }
    } catch (err) {
        statusCorte.textContent = 'Erro ao enviar vídeo.';
        statusCorte.style.color = '#c00';
    }
});

document.getElementById('btn-compilar').addEventListener('click', async function () {
    const status = document.getElementById('status-compilar');
    status.textContent = 'Compilando vídeos...';
    status.style.color = '#444';
    try {
        const response = await fetch('/compilar', {
            method: 'POST'
        });
        const data = await response.json();
        status.textContent = data.message;
        status.style.color = data.success ? '#1976d2' : '#c00';
    } catch (err) {
        status.textContent = 'Erro ao compilar vídeos.';
        status.style.color = '#c00';
    }
});

async function atualizarListaCortes() {
    const listaDiv = document.getElementById('cortes-lista');
    listaDiv.innerHTML = '';
    try {
        const resp = await fetch('/cortes');
        const data = await resp.json();
        if (data.success && data.cortes.length > 0) {
            let html = '<h3>Cortes disponíveis:</h3><ul>';
            data.cortes.forEach(nome => {
                html += `<li><a href="/download/${nome}" target="_blank">${nome}</a></li>`;
            });
            html += '</ul>';
            listaDiv.innerHTML = html;
        } else {
            listaDiv.innerHTML = '<em>Nenhum corte disponível.</em>';
        }
    } catch (err) {
        listaDiv.innerHTML = '<em>Erro ao buscar cortes.</em>';
    }
}

// Atualiza a lista ao carregar a página
atualizarListaCortes(); 