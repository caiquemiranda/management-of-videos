from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'videoAntes'
CORTES_FOLDER = 'videosCortes'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(CORTES_FOLDER):
    os.makedirs(CORTES_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

if __name__ == '__main__':
    app.run(debug=True) 