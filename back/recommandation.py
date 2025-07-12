import requests
import json
from config import Api_key 
from config import Api_Url
from config import Api_key_orient


# Mistral API Config
API_KEY = Api_key_orient
API_URL = Api_Url
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Exemple de données CV au format JSON
a = [
  {
    "full_name": "Jordan DJILLA",
    "email": "jordandjilla7@gmail.com",
    "experiences": [
      {
        "title": "Data Analyst",
        "company": "HETIC",
        "start_date": "Mars 2024",
        "end_date": "Mai 2024"
      },
      {
        "title": "Data Analyst",
        "company": "HETIC",
        "start_date": "Janvier 2024",
        "end_date": "F\u00e9vrier 2024"
      },
      {
        "title": "Product Manager - D\u00e9veloppeur",
        "company": "GAUS",
        "start_date": "Janvier 2022",
        "end_date": "Juin 2023"
      },
      {
        "title": "Stagiaire Data Analyst",
        "company": "AGC Assurance",
        "start_date": "Ao\u00fbt 2021",
        "end_date": "D\u00e9cembre 2021"
      }
    ],
    "education": [
      {
        "school": "Groupe Galil\u00e9e (HETIC)",
        "degree": "Master en Data et Intelligence Artificielle",
        "year": "2023 - 2025"
      },
      {
        "school": "IUG",
        "degree": "Licence Technologique G\u00e9nie Logiciel",
        "year": "2020 - 2021"
      },
      {
        "school": "Coll\u00e8ge Communautaire du Nouveau-Brunswick",
        "degree": "DEC Programmation et Application mobiles",
        "year": "2017 - 2020"
      }
    ],
    "skills": [
      "Azure Cloud",
      "Environment HADOOP avec NIFI, Kafka, Spark",
      "Microsoft 365 avec Power BI, SharePoint, Power Automate",
      "Google Analytics",
      "Looker Studio",
      "Python (Machine Learning et Deep Learning)",
      "Flutter",
      "SQL / NoSQL",
      "Git",
      "Base de Donn\u00e9es",
      "ETL",
      "UML",
      "Figma",
      "Adobe",
      "Marketing Mix",
      "Plan financier"
    ],
    "certifications": [],
    "languages": [
      "Fran\u00e7ais: Langue maternelle",
      "Anglais: B2 (TOEIC)",
      "Allemand: A1"
    ]
  }
]

def orientation(cv, domaine, ville):
    prompt = f"""
    Tu es un conseiller d'orientation. Voici le profil :
    {json.dumps(cv, indent=4)}

    Il souhaite se former dans le domaine : {domaine}, à {ville}.

    Fournis 5 écoles ou formations en france qui correspondent à ce profil et a les meilleurs avis:

    * Nom
    * Ville
    * Type (mastère, reconversion…)
    * Justification
    * Site officiel (lien si possible)
    """

    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]





if __name__ == "__main__":
    print("🎯 Agent IA : Écoles recommandées")
    domaine = input("👉 Quel domaine veux-tu étudier ? : ")
    ville = input("📍 Où veux-tu te former ? : ")

    print("\n🔍 Recherche en cours...\n")
    resultat = orientation(a, domaine, ville)

    print("📋 Résultats :\n")
    print(resultat)