import asyncio
import tempfile

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

class Crofty:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2:1b")
        self.prompt = prompt
        pygame.mixer.init()

    def cleanup(self):
        pygame.mixer.quit()

    def chat(self, data):
        self.prompt = prompt + "\n" + data
        return self.llm.invoke(self.prompt).lower()

    async def speak(self, data):
        myobj = gTTS(text=data[1:-1], lang='en', slow=False, tld='co.uk')

        temp_file = tempfile.TemporaryFile(suffix='.mp3')
        myobj.write_to_fp(temp_file)
        temp_file.flush()

        temp_file.seek(0)
        pygame.mixer.music.load(temp_file, namehint = ".mp3")
        # Play the loaded mp3 file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.5)
        pygame.mixer.music.unload()

    @staticmethod
    async def test():
        this = Crofty()

        response = this.chat(f"""### INSTRUCTION ###
                             The Durhack Grand Prix in Durham is beginning soon! Tell us about it, and our two drivers: {DRIVERA} and {DRIVERB}""")
        print(response)
        await this.speak(response)

        response = this.chat("""### Event ###
                             The lights are out, and the race is underway!""")
        print(response)
        await this.speak(response)

        print("\n")
        response = this.chat(f"""### Event ###
                             {DRIVERA} almost comes off the track as the back left wheel locks up!""")
        print(response)
        await this.speak(response)

        print("\n")
        response = this.chat(f"""### Event ###
                             {DRIVERA} isn't happy at {DRIVERB}! He's just cut him off""")
        print(response)
        await this.speak(response)

        this.cleanup()