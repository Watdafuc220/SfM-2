"""
Phase 4: SFM-2 Evaluation Script
Evaluates SFM-2 model on BLEU, syntax accuracy, and function completion rate.
- Loads model and tokenizer from models/sfm-2/
- Evaluates on datasets/cleaned/*.sona
- Saves results to eval/sfm2_eval_results.json
"""
import os
import json
from glob import glob
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/sfm-2/'))
TOKENIZER_PATH = os.path.join(MODEL_DIR, 'tokenizer.json')
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/cleaned/'))
RESULTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sfm2_eval_results.json'))

model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
model.eval()

bleu_scores = []
syntax_correct = 0
func_complete = 0
n = 0

for file in glob(os.path.join(DATA_DIR, '*.sona')):
    with open(file, 'r', encoding='utf-8') as f:
        ref = f.read().strip()
    if len(ref) < 20:
        continue
    # Generate output
    inputs = tokenizer(ref, return_tensors='pt')
    output_ids = model.generate(
        inputs['input_ids'],
        max_length=inputs['input_ids'].shape[1] + 64,
        do_sample=False
    )
    gen = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # BLEU
    bleu = sentence_bleu([ref.split()], gen.split(), smoothing_function=SmoothingFunction().method1)
    bleu_scores.append(bleu)
    # Syntax check (very basic)
    if gen.count('{') == gen.count('}') and gen.count('(') == gen.count(')'):
        syntax_correct += 1
    # Function completion (checks for 'fn' and closing brace)
    if 'fn' in gen and gen.strip().endswith('}'): 
        func_complete += 1
    n += 1

results = {
    'bleu_mean': sum(bleu_scores)/max(1, len(bleu_scores)),
    'syntax_accuracy': syntax_correct/max(1, n),
    'function_completion_rate': func_complete/max(1, n),
    'samples': n
}
with open(RESULTS_PATH, 'w') as f:
    json.dump(results, f, indent=2)
print(f"✅ SFM-2 evaluation complete. Results saved to {RESULTS_PATH}")
