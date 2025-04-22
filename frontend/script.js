document.getElementById('form-corte').addEventListener('submit', function(e) {
    e.preventDefault();
    const status = document.getElementById('status-corte');
    const fileInput = document.getElementById('video-corte');
    if (!fileInput.files.length) {
        status.textContent = 'Selecione um vídeo para cortar.';
        status.style.color = '#c00';
        return;
    }
    status.textContent = 'Enviando vídeo e cortando... (simulação)';
    status.style.color = '#444';
    setTimeout(() => {
        status.textContent = 'Vídeo cortado com sucesso! (simulação)';
        status.style.color = '#1976d2';
    }, 2000);
});

document.getElementById('btn-compilar').addEventListener('click', function() {
    const status = document.getElementById('status-compilar');
    status.textContent = 'Compilando vídeos... (simulação)';
    status.style.color = '#444';
    setTimeout(() => {
        status.textContent = 'Vídeo final compilado com sucesso! (simulação)';
        status.style.color = '#1976d2';
    }, 2000);
}); 