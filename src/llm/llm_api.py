import os

from openai import OpenAI



def llm_deepseek(input):

    client = OpenAI(api_key="sk-5fc5bf25dd484c308fba84483081e858", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=input,
        stream=False
    )
    return response.choices[0].message.content


def llm_qwen_vl(input):
    client = OpenAI(api_key="sk-3ca2b792e48f4422bc8ff8bd3ea53da9",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "user", "content": [
            {"type": "text", "text": input},
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
        ]}]
    )
    #print(completion.model_dump_json())
    return completion.choices[0].message.content

if __name__ == '__main__':
    an = llm_qwen_vl('图里是什么，用最最简单的词汇描述这张图')
    print(an)