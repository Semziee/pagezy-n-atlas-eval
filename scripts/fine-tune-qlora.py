## Dependencies: pip install peft bitsandbytes accelerate (see requirements.txt)

import torch
import gc
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

# Clear memory
gc.collect()
torch.cuda.empty_cache()

MODEL_ID = "NCAIR1/N-ATLaS"
OUTPUT_DIR = "./pagezy-n-atlas-qlora-500"

# 2. Load Data
print("📂 Loading training data...")
dataset = load_dataset("json", data_files="data/train_400.jsonl", split="train")

def format_prompt(example):
    prompt = f"Passage: {example['read_text']}\nQuestion: {example['quiz'][0]['question']}\nCorrect Answer: {example['quiz'][0]['correct']}\n\nProvide a 1-sentence explanation of why this is correct based on the text."
    response = example['quiz'][0]['explanation']
    return {"text": f"<|user|>\n{prompt}\n<|assistant|>\n{response}<|end|>"}

dataset = dataset.map(format_prompt)

# 3. Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

# 4. TOKENIZATION STEP 
def tokenize_function(examples):
    outputs = tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length",  
        return_tensors="pt"    
    )
    outputs["labels"] = outputs["input_ids"].clone()
    return outputs

print("🔢 Tokenizing dataset...")
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names
)

# 5. Load Model in 4-bit
print("⏳ Loading N-ATLAS model in 4-bit... (Takes ~1-2 mins)")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map={"": 0}
)
model = prepare_model_for_kbit_training(model)

# 6. LoRA Config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
)
model = get_peft_model(model, peft_config)

# 7. Training Args
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=2,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    bf16=True,
    optim="paged_adamw_8bit",
    logging_steps=10,
    report_to="none",
    save_strategy="epoch"
)

# 8. Data Collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 9. Run Native Trainer
print("🚀 Starting QLoRA Fine-Tune... (This will take ~15-20 mins)")
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

trainer.train()

# 10. Save Model
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("✅ Fine-tune complete! Model saved locally.")