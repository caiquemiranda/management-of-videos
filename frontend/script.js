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