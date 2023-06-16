
from gtts import gTTS
import os
import langdetect
from datetime import datetime

def getAudio(texte):
    language = langdetect.detect(texte)
    tts = gTTS(text=texte, lang=language)

    name_audio = "audio"
    change_name = str(datetime.now()).replace(" ", "")[0:-4].replace(":", "_")
    print(type(change_name))
    format_audio = ".opus"

    name_audio = name_audio + change_name + format_audio
    tts.save(name_audio)
    path_file_audio = os.path.abspath(name_audio)
    return path_file_audio
         
        
texte = """
Salut à toi


"""
if __name__ == "__main__":
    getAudio(texte)



