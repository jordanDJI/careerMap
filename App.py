from flask import Flask, render_template, request, redirect, send_from_directory, flash
import os
from rr import format_recommandation
from werkzeug.utils import secure_filename
from service import creer_pdf
from extractor import extract_from_cv
from recommandation import orientation

app = Flask(__name__)
app.secret_key = "une_clé_unique_et_secrète"

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'cv' not in request.files:
            flash('Aucun fichier CV fourni')
            return redirect(request.url)
        

        file = request.files['cv']
        domaine = request.form['domaine']
        ville = request.form['ville']

        if file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # Étape 1 : Extraire les données du CV
            cv_data = extract_from_cv(filepath)
            print(f"CV extrait : {cv_data}")

            # Étape 2 : Appeler Mistral pour les recommandations
            resulOrientation = orientation(cv_data, domaine, ville)
            print(f"Résultats de l'orientation : {resulOrientation}")

            # Étape 3 : Générer le PDF avec le résultat
            filename = secure_filename(file.filename)  
            basename = os.path.splitext(filename)[0] 
            filename = f"orientation_{basename}.pdf"
            output_pdf = os.path.join(RESULT_FOLDER, f"orientation_{filename}.pdf")
            creer_pdf(resulOrientation, output_pdf)

            # Rediriger vers la page de téléchargement  
            recommandation_html = format_recommandation(resulOrientation)
            return render_template('result.html', recommandation = recommandation_html, pdf_file=os.path.basename(output_pdf))
        except Exception as e:
            flash(f"Erreur : {str(e)}")
            return redirect(request.url)
        
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(RESULT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
