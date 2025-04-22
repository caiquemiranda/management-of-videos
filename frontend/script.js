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

document.getElementById('form-corte').addEventListener('submit', async function (e) {
    e.preventDefault();
    const status = document.getElementById('status-corte');
    const fileInput = document.getElementById('video-corte');
    if (!fileInput.files.length) {
        status.textContent = 'Selecione um vídeo para cortar.';
        status.style.color = '#c00';
        return;
    }
    status.textContent = 'Enviando vídeo e cortando...';
    status.style.color = '#444';
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    try {
        const response = await fetch('/cortar', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        status.textContent = data.message;
        status.style.color = data.success ? '#1976d2' : '#c00';
        if (data.success) {
            atualizarListaCortes();
        }
    } catch (err) {
        status.textContent = 'Erro ao enviar vídeo.';
        status.style.color = '#c00';
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

// Atualiza a lista ao carregar a página
atualizarListaCortes(); 