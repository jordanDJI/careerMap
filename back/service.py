import smtplib
from fpdf import FPDF
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def envoyer_email(destinataire, sujet, corps, fichier_pdf):
    expediteur = "ton.email@exemple.com"
    mot_de_passe = "TON_MOT_DE_PASSE_EMAIL"

    msg = MIMEMultipart()
    msg["From"] = expediteur
    msg["To"] = destinataire
    msg["Subject"] = sujet

    msg.attach(MIMEText(corps, "plain"))

    with open(fichier_pdf, "rb") as f:
        pdf_part = MIMEApplication(f.read(), _subtype="pdf")
        pdf_part.add_header('Content-Disposition', 'attachment', filename=fichier_pdf)
        msg.attach(pdf_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(expediteur, mot_de_passe)
        server.send_message(msg)


def nettoyer_texte_unicode(texte):
    # Remplacement des caractères unicode non compatibles
    return texte.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")

def creer_pdf(resultat, filename="ecoles_recommandees.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Utilisation de la police Arial par défaut
    pdf.set_font("Arial", size=12)

    # Nettoyage du texte avant l'ajout (remplacement des caractères non encodables)
    resultat = nettoyer_texte_unicode(resultat)
    
    for ligne in resultat.split("\n"):
        pdf.multi_cell(0, 10, ligne)

    pdf.output(filename)
    return filename




    

 # Création du PDF avec les résultats
    nom_pdf = creer_pdf(resultat)
    print(f"\n📄 Résultat enregistré dans le fichier : {nom_pdf}")

    # Envoi par email (optionnel)
    envoyer = input("✉ Veux-tu recevoir le résultat par email ? (o/n) : ").lower()
    if envoyer == "o":
        email_dest = input("📧 Ton adresse email : ")
        envoyer_email(email_dest, "Tes écoles recommandées", "Voici le PDF avec les écoles.", nom_pdf)
        print("✅ Email envoyé !")