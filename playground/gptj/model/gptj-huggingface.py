import requests
from dotenv import load_dotenv
import os

load_dotenv()

HUGGING_FACE_API_KEY = os.environ["HUGGING_FACE_API_KEY"]


API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}


class GPTJ():

    def generate(payload):

        try:
            URL = requests.post(
                API_URL, headers=headers, json=payload)

            text = URL.json()
            print(text)
            return str(text[0]['generated_text'].split("Human")[0])

        except:
            return "GPT-J-6b is currently offline, please try again later"


if __name__ == "__main__":
    res = GPTJ.generate(payload="""Human: Hello There Bot! Bot:""")

    # res = generate(context="""English: Hello! Spanish:""",
    #                token_max_length=128, temperature=1.0, top_probability=0.9)
    print(res)
