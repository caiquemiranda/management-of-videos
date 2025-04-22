# Scripts para Processamento de Vídeos

Este projeto contém dois scripts Python para processamento de vídeos:

## 1. cortar_video.py
Script para cortar um vídeo em partes de 14,5 segundos.

### Como usar:
1. Coloque o vídeo que deseja cortar na pasta `videoAntes`.
2. Execute o script:
   ```
   python cortar_video.py
   ```
3. Os cortes serão salvos na pasta `videosCortes` com nomes sequenciais (vid001.mp4, vid002.mp4, etc.).

## 2. compilar_videos.py
Script para juntar vários vídeos editados em um único vídeo final.

### Como usar:
1. Coloque os vídeos editados na pasta `prontosCompilar`.
2. Execute o script:
   ```
   python compilar_videos.py
   ```
3. O vídeo final será salvo na pasta `videoFinal` como `video_completo.mp4`.

## Requisitos
Para usar estes scripts, você precisa ter instalado:

1. Python 3.6 ou superior
2. Biblioteca moviepy

Instale a biblioteca necessária com:
```
pip install moviepy
```

## Estrutura de pastas
- `videoAntes/`: Coloque aqui o vídeo original para cortar
- `videosCortes/`: Aqui serão salvos os cortes do vídeo original
- `prontosCompilar/`: Coloque aqui os vídeos editados prontos para compilar
- `videoFinal/`: Aqui será salvo o vídeo final compilado 