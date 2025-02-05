
from openai import OpenAI



def llm_deepseek(input):

    client = OpenAI(api_key="sk-5fc5bf25dd484c308fba84483081e858", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=input,
        stream=False
    )
    return response.choices[0].message.content