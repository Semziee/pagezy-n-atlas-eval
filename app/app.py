import gradio as gr
import json
import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# ==========================================
# 1. CONFIG & DATA LOADING
# ==========================================
DATA_PATH = "data/passages.jsonl"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("Please ensure data/passages.jsonl exists in your root folder.")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    PASSAGES = [json.loads(line) for line in f]

# Model IDs
BASE_ID = "NCAIR1/N-ATLaS"
ADAPTER_ID = "Semziee/pagezy-n-atlas-qlora-500"
QWEN_ID = "Qwen/Qwen2.5-3B-Instruct"
LLAMA_ID = "meta-llama/Llama-3.2-3B-Instruct"

# ==========================================
# 2. DIAGNOSTIC LOGIC (Tab 1)
# ==========================================
def diagnose(read_score, listen_score):
    read_score = float(read_score)
    listen_score = float(listen_score)
    
    if listen_score >= 0.7 and read_score < 0.7:
        return "🔤 **Decoding Gap:** You understand the story when you hear it, but struggle to read the words. Pagezy will help you practice listening while reading."
    elif listen_score < 0.7 and read_score < 0.7:
        return "🧠 **Comprehension Gap:** The story is hard to understand in both modes. Pagezy will help break down the vocabulary and context."
    else:
        return "✅ **On Track:** Great job! You are comprehending the text well."

def load_passage(passage_id):
    p = next((x for x in PASSAGES if x["id"] == passage_id), PASSAGES[0])
    q = p["quiz"][0]
    return (p["read_text"], f"**Question:** {q['question']}", gr.Radio(choices=q["options"], label="Your Answer", value=None))

# ==========================================
# 3. MODEL LOADING & GENERATION (Tab 2)
# ==========================================
MODELS = {}

def _bnb():
    return BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)

def load_all_models():
    if MODELS:
        return
    print("⏳ Loading models (this takes ~2 mins)...")
    
    # 1. Load Base + Pagezy Adapter (They share the same base weights in VRAM!)
    tok = AutoTokenizer.from_pretrained(BASE_ID)
    base_model = AutoModelForCausalLM.from_pretrained(BASE_ID, quantization_config=_bnb(), device_map={"": 0})
    ft_model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
    
    MODELS["Pagezy (Fine-Tuned)"] = {"model": ft_model, "tokenizer": tok, "adapter": True}
    MODELS["Base N-ATLAS"] = {"model": ft_model, "tokenizer": tok, "adapter": False} # Uses disable_adapter()
    
    # 2. Load Qwen & Llama
    for name, mid in [("Qwen-2.5-3B", QWEN_ID), ("Llama-3.2-3B", LLAMA_ID)]:
        t = AutoTokenizer.from_pretrained(mid)
        m = AutoModelForCausalLM.from_pretrained(mid, quantization_config=_bnb(), device_map={"": 0})
        MODELS[name] = {"model": m, "tokenizer": t, "adapter": False}
    print("✅ All models loaded.")

def generate_hint(cfg, prompt):
    model, tok = cfg["model"], cfg["tokenizer"]
    text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt").to(model.device)
    
    if cfg["adapter"]:
        out = model.generate(**inputs, max_new_tokens=100, temperature=0.3, do_sample=True)
    elif hasattr(model, "disable_adapter"):
        with model.disable_adapter():
            out = model.generate(**inputs, max_new_tokens=100, temperature=0.3, do_sample=True)
    else:
        out = model.generate(**inputs, max_new_tokens=100, temperature=0.3, do_sample=True)

    return tok.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()

def run_arena(passage_id):
    load_all_models()
    p = next((x for x in PASSAGES if x["id"] == passage_id), PASSAGES[0])
    q = p["quiz"][0]
    wrong_opt = next((o for o in q["options"] if o != q["correct"]), q["options"][0])
    
    prompt = (f"Passage: {p['read_text']}\nQuestion: {q['question']}\n"
              f"Student incorrectly answered: {wrong_opt}\n\n"
              f"Provide a 1-sentence, culturally relevant hint to guide them to the correct answer without giving it away.")
    
    results = []
    outputs = {}
    for name, cfg in MODELS.items():
        t0 = time.time()
        resp = generate_hint(cfg, prompt)
        elapsed = round(time.time() - t0, 1)
        words = len(resp.split())
        grounded = "YES" if q["correct"].lower() in resp.lower() else "NO"
        
        outputs[name] = resp
        results.append([name, words, grounded, elapsed])
        
    return outputs["Pagezy (Fine-Tuned)"], outputs["Base N-ATLAS"], outputs["Qwen-2.5-3B"], outputs["Llama-3.2-3B"], results

# ==========================================
# 4. BUILD GRADIO UI
# ==========================================
with gr.Blocks() as demo:
    gr.Markdown("# 📖 Pagezy — Read. Assess. Learn.")
    gr.Markdown("An accessibility-first reading tutor for Nigerian classrooms.")

    with gr.Tabs():
        
        # TAB 1: THE PRODUCT
        with gr.TabItem("📖 Learn with Pagezy"):
            gr.Markdown("### For the Student & Parent")
            pid = gr.Dropdown(choices=[p["id"] for p in PASSAGES], value=PASSAGES[0]["id"], label="1. Choose a story")
            
            with gr.Row():
                with gr.Column(scale=2):
                    read_text = gr.Textbox(label="2. Read the story", lines=6, interactive=False)
                    gr.Markdown("### 3. How well did you understand it?")
                    with gr.Row():
                        read_slider = gr.Slider(0, 1, step=0.1, value=0.4, label="By READING it")
                        listen_slider = gr.Slider(0, 1, step=0.1, value=0.8, label="If SOMEONE READ it to you")
                with gr.Column(scale=1):
                    question_box = gr.Markdown(label="4. Quick Quiz")
                    answer_radio = gr.Radio(label="Your Answer", choices=[])
                    submit_btn = gr.Button("Check Answer", variant="primary")
            
            feedback_box = gr.Markdown(label="Feedback / Hint")
            diagnosis_box = gr.Markdown(label="Pagezy Diagnosis")

            def check_answer(pid, choice, r_s, l_s):
                if not choice: return "⚠️ Please select an answer first.", ""
                p = next((x for x in PASSAGES if x["id"] == pid), PASSAGES[0])
                q = p["quiz"][0]
                diag = diagnose(r_s, l_s)
                if choice == q["correct"]:
                    return f"🎉 **Correct!** {q['explanation']}", diag
                else:
                    hint = "💡 **Tutor Hint:** Look closely at the passage and think about what the text actually says."
                    return f"🤔 **Not quite.** {hint}\n\n(Try again!)", diag

            pid.change(load_passage, inputs=[pid], outputs=[read_text, question_box, answer_radio])
            submit_btn.click(check_answer, inputs=[pid, answer_radio, read_slider, listen_slider], outputs=[feedback_box, diagnosis_box])

        # TAB 2: THE EVIDENCE (MODEL ARENA)
        with gr.TabItem("⚔️ Model Arena (For Judges)"):
            gr.Markdown("### The Engineering Proof")
            gr.Markdown("See how our fine-tuned Pagezy model compares to the base model and global baselines on the exact same prompt.")
            
            arena_pid = gr.Dropdown(choices=[p["id"] for p in PASSAGES], value=PASSAGES[0]["id"], label="Select Passage")
            arena_btn = gr.Button("⚔️ Run 4-Model Comparison", variant="primary")
            
            with gr.Row():
                out_pagezy = gr.Textbox(label="Pagezy (Fine-Tuned)", lines=3)
                out_base = gr.Textbox(label="Base N-ATLAS", lines=3)
            with gr.Row():
                out_qwen = gr.Textbox(label="Qwen-2.5-3B", lines=3)
                out_llama = gr.Textbox(label="Llama-3.2-3B", lines=3)
                
            stats_df = gr.Dataframe(
                headers=["Model", "Words", "Grounded in Text", "Time (s)"],
                datatype=["str", "number", "str", "number"],
                interactive=False
            )
            
            arena_btn.click(run_arena, inputs=[arena_pid], outputs=[out_pagezy, out_base, out_qwen, out_llama, stats_df])

    gr.Markdown("*Powered by Awarri N-ATLAS • N-ATLAS Research License (non-commercial, ≤1,000 users, attribution).*")

if __name__ == "__main__":
    demo.launch(share=True)