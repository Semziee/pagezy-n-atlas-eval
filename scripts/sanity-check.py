""" N-ATLAS sanity check."""
import os, json, torch, datetime
from transformers import AutoTokenizer, AutoModelForCausalLM

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_ID = "NCAIR1/N-ATLaS"
RESULTS_DIR = os.path.join(REPO_ROOT, "results")

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"🔍 Loading {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    prompt = [{"role": "user", "content": "Explain the concept of 'Ajo' (traditional savings) in Yoruba culture in two sentences."}]
    input_text = tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    print("⚙️ Generating response...")
    outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.5, do_sample=True)
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": MODEL_ID,
        "prompt": prompt[0]["content"],
        "response": response,
        "status": "SUCCESS"
    }

    log_file = os.path.join(RESULTS_DIR, "n_atlas_sanity_check.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2, ensure_ascii=False)

    print(f"✅ Sanity check passed. Log saved to {log_file}")
    print(f"👉 Response: {response}")

if __name__ == "__main__":
    main()