import aiohttp
import asyncio
import json

class Model:
    def __init__(self):
        self.url = "https://ava-alpha-api.codelink.io/api/chat"
        self.headers = {
            "content-type": "application/json"
        }
        self.payload = {
            "model": "gpt-4",
            "temperature": 0.6,
            "stream": True
        }
        self.accumulated_content = ""

    async def _process_line(self, line):
        line_text = line.decode("utf-8").strip()
        if line_text.startswith("data:"):
            data = line_text[len("data:"):]
            try:
                data_json = json.loads(data)
                if "choices" in data_json:
                    choices = data_json["choices"]
                    for choice in choices:
                        if "finish_reason" in choice and choice["finish_reason"] == "stop":
                            break
                        if "delta" in choice and "content" in choice["delta"]:
                            content = choice["delta"]["content"]
                            self.accumulated_content += content
            except json.JSONDecodeError as e:
                return

    async def ChatCompletion(self, messages):
        self.payload["messages"] = messages

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(self.payload)) as response:
                print(response)
                async for line in response.content:
                    await self._process_line(line)

        return self.accumulated_content

class QuestionAnswerer:
    def __init__(self):
        self.model = Model()

    async def ask_question(self, question):
        with open("instructions1.txt", "r") as file_instru:
            system_prompt = file_instru.read()
        prompt = question
        messages = [
            {"role": "system", "content": system_prompt}, # Le message du système qui indique le mode ou le plugin
            {"role": "user", "content": prompt} # Le message de l'utilisateur qui contient la question
        ]
        response = await self.model.ChatCompletion(messages)
        return response

async def main(question):
    question_answerer = QuestionAnswerer()
    question = question
    response = await question_answerer.ask_question(question)
    return response

if __name__ == "__main__":
    response = asyncio.run(main("What is the capital of France?"))
    print(response)



