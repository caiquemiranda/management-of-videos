from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import tempfile

app = Flask(__name__)

UPLOAD_FOLDER = 'videoAntes'
CORTES_FOLDER = 'videosCortes'
PRONTOS_COMPILAR_FOLDER = 'prontosCompilar'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(CORTES_FOLDER):
    os.makedirs(CORTES_FOLDER)
if not os.path.exists(PRONTOS_COMPILAR_FOLDER):
    os.makedirs(PRONTOS_COMPILAR_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/info_video', methods=['POST'])
def info_video():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nome de arquivo vazio.'}), 400
    if file and allowed_file(file.filename):
        try:
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp.close()
            file.save(temp.name)
            clip = VideoFileClip(temp.name)
            duracao = clip.duration
            duracao_parte = 14.5
            num_partes = int(-(-duracao // duracao_parte))  # ceil
            clip.close()
            os.remove(temp.name)
            return jsonify({
                'success': True,
                'duracao': duracao,
                'num_partes': num_partes
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Tipo de arquivo não permitido.'}), 400

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend', filename)

@app.route('/cortar', methods=['POST'])
def cortar_video():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nome de arquivo vazio.'}), 400
    if file and allowed_file(file.filename):
        # Limpa a pasta antes de salvar novo vídeo
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Executa o script de corte
        try:
            result = subprocess.run(['python', 'cortar_video.py'], capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                return jsonify({'success': True, 'message': 'Vídeo cortado com sucesso!'}), 200
            else:
                return jsonify({'success': False, 'message': result.stderr or result.stdout}), 500
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Tipo de arquivo não permitido.'}), 400

@app.route('/cortes', methods=['GET'])
def listar_cortes():
    try:
        arquivos = [f for f in os.listdir(CORTES_FOLDER) if f.endswith('.mp4')]
        arquivos.sort()
        return jsonify({'success': True, 'cortes': arquivos}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_corte(filename):
    return send_from_directory(CORTES_FOLDER, filename, as_attachment=True)

@app.route('/compilar', methods=['POST'])
def compilar_videos():
    try:
        result = subprocess.run(['python', 'compilar_videos.py'], capture_output=True, text=True, timeout=1200)
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Vídeo final compilado com sucesso!'}), 200
        else:
            return jsonify({'success': False, 'message': result.stderr or result.stdout}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/upload_compilar', methods=['POST'])
def upload_compilar():
    if 'files' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado.'}), 400
    files = request.files.getlist('files')
    if not files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado.'}), 400
    salvos = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(PRONTOS_COMPILAR_FOLDER, filename)
            file.save(filepath)
            salvos.append(filename)
    return jsonify({'success': True, 'arquivos': salvos}), 200

@app.route('/arquivos_compilar', methods=['GET'])
def arquivos_compilar():
    try:
        arquivos = [f for f in os.listdir(PRONTOS_COMPILAR_FOLDER) if f.endswith('.mp4')]
        arquivos.sort()
        return jsonify({'success': True, 'arquivos': arquivos}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/excluir_compilar/<filename>', methods=['DELETE'])
def excluir_compilar(filename):
    caminho = os.path.join(PRONTOS_COMPILAR_FOLDER, filename)
    if os.path.exists(caminho):
        try:
            os.remove(caminho)
            return jsonify({'success': True, 'message': f'{filename} removido com sucesso.'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Arquivo não encontrado.'}), 404

@app.route('/download_final', methods=['GET'])
def download_final():
    caminho = os.path.join('videoFinal', 'video_completo.mp4')
    if os.path.exists(caminho):
        return send_from_directory('videoFinal', 'video_completo.mp4', as_attachment=True)
    else:
        return jsonify({'success': False, 'message': 'Vídeo final não encontrado.'}), 404

if __name__ == '__main__':
    app.run(debug=True) 