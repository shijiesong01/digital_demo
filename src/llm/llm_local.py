###
# 本文件旨在实现所有本地大模型的调用
###

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 模型路径
model_path = "F:/llm/DeepSeek-R1-Distill-Qwen-1.5B/download"

# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
print('ok')
# 输入文本
input_text = "你好，世界！"
inputs = tokenizer(input_text, return_tensors="pt")

# 推理
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=50,
    )

# 解码输出
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)