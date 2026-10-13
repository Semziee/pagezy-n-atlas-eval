"""Pagezy x N-ATLAS inference engine."""
import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

DEFAULT_MODEL_ID = "NCAIR1/N-ATLaS"

def clear_vram():
    gc.collect()
    torch.cuda.empty_cache()

def load_model_4bit(model_id=DEFAULT_MODEL_ID):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
    return model, tokenizer

def generate(model, tokenizer, prompt, max_tokens=200, temperature=0.3, do_sample=True):
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=max_tokens, temperature=temperature, do_sample=do_sample)
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()
    return response