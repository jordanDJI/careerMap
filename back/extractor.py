import json
from untiles import image_to_base64, pdf_to_image
from mistralai import Mistral
from config import Api_key

    
def extract_from_cv(pdf_path):
    # Convertir la première page du PDF en image
    image_path = pdf_to_image(pdf_path)
    base64_image = image_to_base64(image_path)

    client = Mistral(api_key=Api_key)

    prompt = """
Tu es un assistant RH expert en lecture de CV. À partir d’une image d’un CV, tu dois extraire les informations suivantes dans un JSON structuré.

Voici le format EXACT que tu dois renvoyer (toutes les clés doivent être présentes, avec null si non trouvé) :

{
    "full_name": "Nom complet",
    "email": "Adresse email",
    "experiences": [{"title": "Poste", "company": "Entreprise", "start_date": "AAAA-MM", "end_date": "AAAA-MM"}],
    "education": [{"school": "Nom de l'école", "degree": "Diplôme", "year": "AAAA"}],
    "skills": ["Liste", "de", "compétences"],
    "certifications": ["Nom de certification"],
    "languages": ["Langue (niveau)"]
}

Respecte les formats de date (AAAA-MM). Si une information n’est pas disponible, utilise `null`.
    """

    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "Tu es un expert en extraction de données à partir de CV. Tu dois structurer la sortie pour qu’elle soit facilement exploitable par un système de recommandation."}
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ]
        }
    ]

    response = client.chat.complete(
        model="pixtral-12b-2409",
        messages=messages,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        json_data = json.loads(content)
        JsonData= json.dumps(json_data, indent=2)
        return JsonData
    except json.JSONDecodeError:
        return json.dumps({"error": "Réponse invalide", "raw_response": content})

if __name__ == "__main__":
    # Example usage
    pdf_path = r"C:\Users\jorda\OneDrive\Documents\Moi\CV JD\Alternance\V1_Djilla Jordan Data Analyst (curriculum vitae).pdf_.pdf"
    result = extract_from_cv(pdf_path)
    print(result)
    with open("result_extra.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Extraction completed. Result saved to result.json.")

