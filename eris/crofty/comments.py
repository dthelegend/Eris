from langchain_ollama import OllamaLLM
from gtts import gTTS
import pygame
from time import sleep as zzz
import os
from datetime import datetime

DRIVERB = "Dingle"
DRIVERA = "Quandale"

prompt = f"""
### Instruction ###
You are the commentator for a 1v1 motorsport race. 
There are two drivers, {DRIVERA} and {DRIVERB}.
Commentate it live like Crofty from Formula 1.
Respond in one fast sentence.
Reacting to each moment as it happens.
Stay in character and wait for data.
"""

class Crofty():
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2:1b")
        self.prompt = prompt
        pygame.mixer.init()
        self.names = []

    def cleanup(self):
        pygame.mixer.quit()
        for i in self.names:
            os.remove(i)

    def chat(self, data):
        self.prompt = prompt + "\n" + data
        return self.llm.invoke(self.prompt).lower()

    def speak(self, data):
        myobj = gTTS(text=data[1:-1], lang='en', slow=False, tld='co.uk')
        
        date_string = datetime.now().strftime("%d%m%Y%H%M%S")

        myobj.save(f"{date_string}.mp3")
        self.names.append(f"{date_string}.mp3")
        pygame.mixer.music.load(f"{date_string}.mp3")
        # Play the loaded mp3 file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    @staticmethod
    def test():
        this = Crofty()

        response = this.chat(f"""### INSTRUCTION ###
                             The Durhack Grand Prix in Durham is beginning soon! Tell us about it, and our two drivers: {DRIVERA} and {DRIVERB}""")
        print(response)
        this.speak(response)

        response = this.chat("""### Event ###
                             The lights are out, and the race is underway!""")
        print(response)
        this.speak(response)

        print("\n")
        response = this.chat("""### Event ###
                             f{DRIVERA} almost comes off the track as the back left wheel locks up!""")
        print(response)
        this.speak(response)

        print("\n")
        response = this.chat("""### Event ###
                             f{DRIVERA} isn't happy at {DRIVERB}! He's just cut him off""")
        print(response)
        this.speak(response)

        this.cleanup()