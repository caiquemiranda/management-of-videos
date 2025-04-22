let arquivoSelecionado = null;
let infoVideo = null;

const fileInput = document.getElementById('video-corte');
const infoDiv = document.getElementById('info-video');
const btnConfirmar = document.getElementById('btn-confirmar-corte');
const btnEnviar = document.getElementById('btn-enviar-corte');
const statusCorte = document.getElementById('status-corte');
const progressCorte = document.getElementById('progress-corte');

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
    progressCorte.style.display = 'block';
    progressCorte.innerHTML = '<div class="progress-bar-inner" id="progress-corte-inner"></div>';
    let progressInner = document.getElementById('progress-corte-inner');
    let fakeProgress = 0;
    let interval = setInterval(() => {
        fakeProgress = Math.min(fakeProgress + Math.random() * 10, 95);
        progressInner.style.width = fakeProgress + '%';
    }, 300);
    const formData = new FormData();
    formData.append('file', arquivoSelecionado);
    try {
        const response = await fetch('/cortar', {
            method: 'POST',
            body: formData
        });
        clearInterval(interval);
        progressInner.style.width = '100%';
        setTimeout(() => { progressCorte.style.display = 'none'; }, 800);
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
        clearInterval(interval);
        progressCorte.style.display = 'none';
        statusCorte.textContent = 'Erro ao enviar vídeo.';
        statusCorte.style.color = '#c00';
    }
});

// --- Upload para compilação ---
const formUploadCompilar = document.getElementById('form-upload-compilar');
const inputCompilar = document.getElementById('videos-compilar');
const statusUploadCompilar = document.getElementById('status-upload-compilar');
const listaCompilar = document.getElementById('arquivos-compilar-lista');
const progressUploadCompilar = document.getElementById('progress-upload-compilar');

formUploadCompilar.addEventListener('submit', async function (e) {
    e.preventDefault();
    statusUploadCompilar.textContent = '';
    progressUploadCompilar.style.display = 'block';
    progressUploadCompilar.innerHTML = '<div class="progress-bar-inner" id="progress-upload-compilar-inner"></div>';
    let progressInner = document.getElementById('progress-upload-compilar-inner');
    let fakeProgress = 0;
    let interval = setInterval(() => {
        fakeProgress = Math.min(fakeProgress + Math.random() * 15, 95);
        progressInner.style.width = fakeProgress + '%';
    }, 200);
    const files = inputCompilar.files;
    if (!files.length) return;
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    try {
        const response = await fetch('/upload_compilar', {
            method: 'POST',
            body: formData
        });
        clearInterval(interval);
        progressInner.style.width = '100%';
        setTimeout(() => { progressUploadCompilar.style.display = 'none'; }, 800);
        const data = await response.json();
        statusUploadCompilar.textContent = data.success ? 'Vídeos enviados com sucesso!' : (data.message || 'Erro ao enviar vídeos.');
        statusUploadCompilar.style.color = data.success ? '#1976d2' : '#c00';
        if (data.success) {
            inputCompilar.value = '';
            atualizarListaCompilar();
        }
    } catch (err) {
        clearInterval(interval);
        progressUploadCompilar.style.display = 'none';
        statusUploadCompilar.textContent = 'Erro ao enviar vídeos.';
        statusUploadCompilar.style.color = '#c00';
    }
});

async function atualizarListaCompilar() {
    listaCompilar.innerHTML = '';
    try {
        const resp = await fetch('/arquivos_compilar');
        const data = await resp.json();
        if (data.success && data.arquivos.length > 0) {
            let html = '<b>Vídeos enviados para compilar:</b><ul>';
            data.arquivos.forEach(nome => {
                html += `<li>${nome}</li>`;
            });
            html += '</ul>';
            listaCompilar.innerHTML = html;
        } else {
            listaCompilar.innerHTML = '<em>Nenhum vídeo enviado para compilação.</em>';
        }
    } catch (err) {
        listaCompilar.innerHTML = '<em>Erro ao buscar vídeos enviados.</em>';
    }
}

// --- Compilar vídeos enviados ---
const btnCompilar = document.getElementById('btn-compilar');
const statusCompilar = document.getElementById('status-compilar');
const progressCompilar = document.getElementById('progress-compilar');

btnCompilar.addEventListener('click', async function () {
    statusCompilar.textContent = 'Compilando vídeos...';
    statusCompilar.style.color = '#444';
    progressCompilar.style.display = 'block';
    progressCompilar.innerHTML = '<div class="progress-bar-inner" id="progress-compilar-inner"></div>';
    let progressInner = document.getElementById('progress-compilar-inner');
    let fakeProgress = 0;
    let interval = setInterval(() => {
        fakeProgress = Math.min(fakeProgress + Math.random() * 10, 95);
        progressInner.style.width = fakeProgress + '%';
    }, 300);
    try {
        const response = await fetch('/compilar', {
            method: 'POST'
        });
        clearInterval(interval);
        progressInner.style.width = '100%';
        setTimeout(() => { progressCompilar.style.display = 'none'; }, 800);
        const data = await response.json();
        statusCompilar.textContent = data.message;
        statusCompilar.style.color = data.success ? '#1976d2' : '#c00';
        if (data.success) {
            atualizarListaCompilar();
        }
    } catch (err) {
        clearInterval(interval);
        progressCompilar.style.display = 'none';
        statusCompilar.textContent = 'Erro ao compilar vídeos.';
        statusCompilar.style.color = '#c00';
    }
});

// --- Lista cortes ao carregar ---
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

// Atualiza listas ao carregar a página
atualizarListaCortes();
atualizarListaCompilar(); 