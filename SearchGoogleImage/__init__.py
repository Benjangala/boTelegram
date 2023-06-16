# Importer les modules nécessaires
import requests
from bs4 import BeautifulSoup

# Définir une fonction qui prend un texte en entrée et renvoie les urls des images correspondantes
def searchImagesGoogle(texte):
  # Construire l'url de la requête à Google Images
  url = "https://www.google.com/search"
  # Spécifier les paramètres de la requête
  params = {
    "q": texte, # Le texte à rechercher
    "tbm": "isch" # Le mode de recherche d'images
  }
  # Envoyer la requête et récupérer la réponse
  response = requests.get(url, params=params)
  # Convertir la réponse en objet BeautifulSoup
  soup = BeautifulSoup(response.text, "html.parser")
  # Extraire la liste des éléments img de la réponse
  imgs = soup.find_all("img")
  # Créer une liste vide pour stocker les urls des images
  urls = []
  # Parcourir les éléments img et ajouter les urls des images à la liste
  for img in imgs:
    urls.append(img.get("src", ""))
  # Retourner la liste des urls des images
  return urls

# Tester la fonction avec un texte d'exemple
if __name__ == "__main__":
    texte = "chats mignons"
    urls = searchImages(texte)
    # Afficher les urls des images trouvées
    print(urls)