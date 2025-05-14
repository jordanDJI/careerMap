import json
from utils import image_to_base64, pdf_to_image
from mistralai.client import Mistral
from config import Api_key

def extract_from_cv(pdf_path):
    # Convertir la première page du PDF en image
    image_path = pdf_to_image(pdf_path)

    client = Mistral(api_key=Api_key)
    base64_image = image_to_base64(image_path)

    model = "pixtral-12b-2409"
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Tu es un expert RH. Ton objectif est d'extraire les informations essentielles d'un CV fourni sous forme d'image. "
                        "Les informations doivent être retournées en JSON structuré. Tous les champs manquants doivent être à null. "
                        "Langue : français. N'invente rien si l'information n'existe pas. Format :\n"
                        "- full_name\n- email\n- phone\n- experiences (liste de postes avec titre, entreprise, dates, description)\n"
                        "- education (liste de diplômes avec école, diplôme, date)\n"
                        "- skills (liste)\n- certifications (liste)\n- languages (liste avec niveau si disponible)"
                    )
                }
            ],
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Merci d'extraire toutes les informations pertinentes de ce CV selon le format demandé ci-dessus."
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    response = client.chat.complete(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    try:
        json_data = json.loads(content)
        return json.dumps(json_data, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON response", "raw_response": content})
