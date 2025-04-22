from flask import Flask, request, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'videoAntes'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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