import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from trl import setup_chat_format

#path_to_finetuned_model = "C:\\Users\\USER_ELISEY\\hakaton\\russia_chad_1.5\\final"
path_to_finetuned_model = "C:\\Users\\USER_ELISEY\\hakaton\\russia_chad_1.5\\final"

# QLoRA config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    path_to_finetuned_model,
    #quantization_config=bnb_config,
#     device_map="auto",
    attn_implementation="eager"
)

tokenizer = tokenizer = AutoTokenizer.from_pretrained(path_to_finetuned_model)
tokenizer.padding_side = 'right'
tokenizer.padding_token = '<|pad_token|>'

model, tokenizer = setup_chat_format(model, tokenizer)

def generate_answer(prompt):
    chat = [
        { "role": "user", "content": prompt },
    ]
    prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    outputs = model.generate(input_ids=inputs.to(model.device), max_new_tokens=150)

    return(tokenizer.decode(outputs[0]))

