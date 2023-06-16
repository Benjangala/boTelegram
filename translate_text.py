
from deep_translator import GoogleTranslator

def translator(lang1:str= "auto", lang2:str= "fr", texte:str= "")->str:
	translator = GoogleTranslator(source=lang1, target=lang2)
	new_text = translator.translate(texte)
	return new_text


if __name__ == "__main__":
	pass






