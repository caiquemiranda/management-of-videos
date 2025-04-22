from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import glob
import re

if not os.path.exists("prontosCompilar"):
    print("A pasta 'prontosCompilar' não foi encontrada")
    exit()

if not os.path.exists("videoFinal"):
    os.makedirs("videoFinal")

videos_path = glob.glob("prontosCompilar/*.*")

if not videos_path:
    print("Nenhum vídeo encontrado na pasta 'prontosCompilar'")
    exit()

# Função para extrair o número do nome do arquivo para ordenação
def get_video_number(filename):
    # Extrai números do nome do arquivo
    match = re.search(r'(\d+)', os.path.basename(filename))
    if match:
        return int(match.group(1))
    return 0

videos_path.sort(key=get_video_number)

print(f"Encontrados {len(videos_path)} vídeos para compilar")

video_clips = []
for video_path in videos_path:
    print(f"Carregando: {video_path}")
    clip = VideoFileClip(video_path)
    video_clips.append(clip)

video_final = concatenate_videoclips(video_clips)

output_path = "videoFinal/video_completo.mp4"
print("Compilando vídeo final. Isso pode levar alguns minutos...")
video_final.write_videofile(output_path, codec="libx264")

for clip in video_clips:
    clip.close()
video_final.close()

print(f"Compilação concluída! O vídeo final está em '{output_path}'.")