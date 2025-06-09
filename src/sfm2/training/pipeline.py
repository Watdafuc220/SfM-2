"""
Phase 3–4: SFM-2 Model Training Script
Trains a GPT-2 style model for Sona code generation using the cleaned dataset and custom tokenizer.
- Uses HuggingFace Transformers
- Loads config from configs/sfm2_config.json
- Loads tokenizer from tokenizers/sona-tokenizer.json
- Trains on datasets/cleaned/*.sona
- Saves checkpoints to models/sfm-2/
- Includes TODOs for distributed training, logging, and advanced metrics
"""
import os
from glob import glob
from transformers import GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments, PreTrainedTokenizerFast, TextDataset, DataCollatorForLanguageModeling
import json

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../configs/sfm2_config.json'))
TOKENIZER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tokenizers/sona-tokenizer.json'))
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/cleaned/'))
MODEL_OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/sfm-2/'))
os.makedirs(MODEL_OUT, exist_ok=True)

# Load config and tokenizer
with open(CONFIG_PATH, 'r') as f:
    config_dict = json.load(f)
config = GPT2Config(**config_dict)
tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)

def get_dataset(tokenizer, data_dir):
    files = glob(os.path.join(data_dir, '*.sona'))
    with open('train.txt', 'w', encoding='utf-8') as out:
        for fpath in files:
            with open(fpath, 'r', encoding='utf-8') as f:
                out.write(f.read() + '\n')
    return TextDataset(
        tokenizer=tokenizer,
        file_path='train.txt',
        block_size=1024
    )

dataset = get_dataset(tokenizer, DATA_DIR)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

model = GPT2LMHeadModel(config)

training_args = TrainingArguments(
    output_dir=MODEL_OUT,
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=3,
    prediction_loss_only=True,
    logging_steps=50,
    evaluation_strategy='steps',
    eval_steps=500,
    learning_rate=5e-5,
    warmup_steps=1000,
    weight_decay=0.01,
    gradient_accumulation_steps=2,
    fp16=True,
    report_to=[],
    # TODO: Add distributed training, advanced logging, and callbacks
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=None,  # TODO: Add validation split
    data_collator=data_collator,
)

trainer.train()
model.save_pretrained(MODEL_OUT)
tokenizer.save_pretrained(MODEL_OUT)
print(f"✅ SFM-2 model trained and saved to {MODEL_OUT}")
# TODO: Add BLEU, syntax accuracy, and function completion metrics
# TODO: Add early stopping, advanced eval, and distributed support
