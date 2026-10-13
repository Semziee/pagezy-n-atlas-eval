"""Passage generation."""
import json
import torch
import gc
import os
import re
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def clear_vram():
    gc.collect()
    torch.cuda.empty_cache()


def generate(model, tokenizer, prompt, max_tokens=200, temperature=0.3, do_sample=True):
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens, temperature=temperature, do_sample=do_sample)
    return tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()

MODEL_ID = "NCAIR1/N-ATLaS"

TOPICS = {
    "english": {
        "young": ["a short folk tale about a tortoise", "basic hygiene and washing hands",
                  "simple maths at the local market", "market day with mama", "the rainy season and our farm"],
        "teen": ["how Nigerian fintech apps work", "the history of Afrobeats music",
                 "saving your first 10,000 Naira", "family expectations and choosing a career", "street football and teamwork"],
    },
    "pidgin": {
        "young": ["football for street", "jollof rice for party", "how to wash hand well well",
                  "market day and mama", "rainy season and mosquito"],
        "teen": ["how to save small-small for ajo", "malaria no be joke", "danfo and okada for Lagos",
                 "phone time and school work", "respect for elders na power"],
    },
    "yoruba": {
        "young": ["ìtàn ìjàpá", "ìmọ́tótó àti ìwẹ̀", "ìṣirò ní ọjà", "ọjọ́ ọjà", "àkókò òjò"],
        "teen": ["àjò àti ìfowopamọ́", "orin Afrobeats àti àṣà", "iṣẹ́ agbẹ̀ àti oúnjẹ",
                 "ọwọ́ fún awọn agbalagba", "ìlera ọpọlọ awọn ọ̀dọ́"],
    },
}

TEMPLATE = """You are a strict JSON-generating machine. You do not speak, you only output valid JSON.

Generate a JSON object for a Nigerian educational passage.
Topic: {topic}
Target Age Group: {age_group}

The JSON object MUST contain exactly these keys:
"id" (string), "age_group" (string), "language" (string, use "{language}"),
"read_text" (string, 100-150 words, written as if authored by a native {language} speaker, not translated), "audio_script" (string),
"quiz" (array containing one object with keys: "question", "options" [array of 4 strings], "correct" [string matching one option], "explanation"),
"diagnostic_focus" (string, use "comprehension"), "human_verified" (boolean, set to false).

Output ONLY the JSON object. Do not write any text, rules, or markdown before or after the JSON."""

def generate_passages(lang="english", out_path=None):
    out_path = out_path or os.path.join(REPO_ROOT, "data", "draft_passages.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"🔍 Loading {MODEL_ID} in 4-bit...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
        ),
        device_map="auto"
    )

    topics_to_use = TOPICS[lang]["young"] + TOPICS[lang]["teen"]
    generated_items = []

    for i, topic in enumerate(topics_to_use):
        age_group = "8-12" if i < len(TOPICS[lang]["young"]) else "13-18"
        prompt = TEMPLATE.format(age_group=age_group, topic=topic, language=lang)

        raw_text = generate(model, tokenizer, prompt, max_tokens=400, temperature=0.2)

        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            try:
                item = json.loads(json_match.group(0))
                generated_items.append(item)
                print(f"✅ Generated {len(generated_items)}/{len(topics_to_use)}: {topic} ({age_group})")
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parse error for {topic}: {e}")
                print(f"Raw text: {raw_text[:150]}...")
        else:
            print(f"️ No JSON found for {topic}. Raw output: {raw_text[:150]}...")

    with open(out_path, "a", encoding="utf-8") as f:  # append so english + pidgin + yoruba accumulate
        for item in generated_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    clear_vram()
    print(f"\n🎉 Success! Appended {len(generated_items)} items to {out_path}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=sorted(TOPICS), default="english")
    args = ap.parse_args()
    generate_passages(lang=args.lang)