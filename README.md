# Scripts para Processamento de Vídeos

Este projeto contém dois scripts Python para processamento de vídeos e uma interface web integrada com backend Flask.

## 1. cortar_video.py
Script para cortar um vídeo em partes de 14,5 segundos.

### Como usar manualmente:
1. Coloque o vídeo que deseja cortar na pasta `videoAntes`.
2. Execute o script:
   ```
   python cortar_video.py
   ```
3. Os cortes serão salvos na pasta `videosCortes` com nomes sequenciais (vid001.mp4, vid002.mp4, etc.).

## 2. compilar_videos.py
Script para juntar vários vídeos editados em um único vídeo final.

### Como usar manualmente:
1. Coloque os vídeos editados na pasta `prontosCompilar`.
2. Execute o script:
   ```
   python compilar_videos.py
   ```
3. O vídeo final será salvo na pasta `videoFinal` como `video_completo.mp4`.

---

## 3. Interface Web (Frontend + Backend Flask)

Agora você pode usar uma interface web simples para cortar e compilar vídeos sem precisar rodar scripts manualmente.

### Como usar a interface web:

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Inicie o backend Flask:
   ```
   python app.py
   ```
3. Abra o arquivo `frontend/index.html` no navegador.
   - **Dica:** Para evitar problemas de CORS, você pode servir a pasta `frontend` como estático pelo Flask, se desejar.
4. Use a interface para enviar um vídeo para corte ou compilar os vídeos já cortados.

---

## Requisitos
- Python 3.6 ou superior
- As dependências listadas em `requirements.txt`

Instale todas as dependências com:
```
pip install -r requirements.txt
```

## Estrutura de pastas
- `videoAntes/`: Coloque aqui o vídeo original para cortar (usado pelo backend)
- `videosCortes/`: Aqui serão salvos os cortes do vídeo original
- `prontosCompilar/`: Coloque aqui os vídeos editados prontos para compilar
- `videoFinal/`: Aqui será salvo o vídeo final compilado
- `frontend/`: Interface web (HTML, CSS, JS) 