from moviepy.editor import VideoFileClip
import os
import glob
import math

if not os.path.exists("videosCortes"):
    os.makedirs("videosCortes")

videos = glob.glob("videoAntes/*.*")
if not videos:
    print("Nenhum vídeo encontrado na pasta 'videoAntes'")
    exit()

input_video = videos[0]

video = VideoFileClip(input_video)
duracao_total = video.duration
duracao_parte = 14.5

num_cortes = math.ceil(duracao_total / duracao_parte)

print(f"Informações do vídeo:")
print(f"- Duração total: {duracao_total:.2f} segundos")
print(f"- Tamanho de cada parte: {duracao_parte:.1f} segundos")
print(f"- Número total de cortes a serem feitos: {num_cortes}")

resposta = input("\nDeseja continuar com os cortes? (s/n): ").lower()
if resposta != 's' and resposta != 'sim':
    print("Operação cancelada pelo usuário.")
    video.close()
    exit()

num_parte = 1
for inicio in range(0, int(duracao_total), int(duracao_parte)):
    fim = min(inicio + duracao_parte, duracao_total)
    
    parte = video.subclip(inicio, fim)
    
    nome_saida = f"videosCortes/vid{num_parte:03d}.mp4"
    
    print(f"Cortando parte {num_parte}/{num_cortes}...")
    parte.write_videofile(nome_saida, codec="libx264")
    
    print(f"Parte {num_parte} salva como {nome_saida}")
    num_parte += 1

video.close()

print("Corte concluído! Os vídeos estão na pasta 'videosCortes'.")