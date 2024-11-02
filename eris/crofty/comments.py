from langchain_ollama import OllamaLLM

prompt = """
### Instruction ###
You are the commentator for a motorsport race between two cars. 
Commentate it live like Crofty from Formula 1.
Respond in two sentences.
Reacting to each moment as it happens.
Stay in character and wait for data.
"""

class Crofty():
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2:1b")
        self.prompt = prompt

    def chat(self, data):
        self.prompt = prompt + "\n" + data
        return self.llm.invoke(self.prompt)

    @staticmethod
    def test():
        this = Crofty()

        response = this.chat("""### Event ###
                             Racer A has just overtook Racer B after Racer B took a corner too wide!""")
        print(response)
        print("\n")
        response = this.chat("""### Event ###
                             Racer A almost comes off the track as the back left wheel locks up!""")
        print(response)