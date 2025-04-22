from moviepy.editor import VideoFileClip
import os
import glob
import math

# Cria a pasta de saída se não existir
if not os.path.exists("videosCortes"):
    os.makedirs("videosCortes")

# Encontra o vídeo na pasta 'videoAntes'
videos = glob.glob("videoAntes/*.*")
if not videos:
    print("Nenhum vídeo encontrado na pasta 'videoAntes'")
    exit()

input_video = videos[0]  # Pega o primeiro vídeo encontrado

# Carrega o vídeo
video = VideoFileClip(input_video)
duracao_total = video.duration
duracao_parte = 14.5

# Calcula o número total de cortes que serão feitos
num_cortes = math.ceil(duracao_total / duracao_parte)

# Mostra informações e pergunta se deseja continuar
print(f"Informações do vídeo:")
print(f"- Duração total: {duracao_total:.2f} segundos")
print(f"- Tamanho de cada parte: {duracao_parte:.1f} segundos")
print(f"- Número total de cortes a serem feitos: {num_cortes}")

# Pergunta ao usuário se deseja continuar
resposta = input("\nDeseja continuar com os cortes? (s/n): ").lower()
if resposta != 's' and resposta != 'sim':
    print("Operação cancelada pelo usuário.")
    video.close()
    exit()

# Corta o vídeo em partes de 14,5 segundos
num_parte = 1
for inicio in range(0, int(duracao_total), int(duracao_parte)):
    fim = min(inicio + duracao_parte, duracao_total)
    
    # Pega a parte do vídeo
    parte = video.subclip(inicio, fim)
    
    # Nome de saída formatado (vid001, vid002, etc.)
    nome_saida = f"videosCortes/vid{num_parte:03d}.mp4"
    
    # Salva a parte
    print(f"Cortando parte {num_parte}/{num_cortes}...")
    parte.write_videofile(nome_saida, codec="libx264")
    
    print(f"Parte {num_parte} salva como {nome_saida}")
    num_parte += 1

# Fecha o vídeo para liberar recursos
video.close()

print("Corte concluído! Os vídeos estão na pasta 'videosCortes'.") 