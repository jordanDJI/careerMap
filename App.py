from flask import Flask, request, jsonify
from extractor import extract_from_cv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/extract_cv', methods=['POST'])
def handle_cv_extraction():
    if 'cv' not in request.files:
        return jsonify({'error': 'Aucun fichier CV fourni'}), 400

    file = request.files['cv']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    result = extract_from_cv(filepath)
    return jsonify(json.loads(result))

if __name__ == '__main__':
    app.run(debug=True)
