"""
Phase 2: Dataset Cleaning & Prep
Cleans all .sona files in datasets/raw/, removes broken/partial samples, validates syntax, and saves to datasets/cleaned/.
"""
import os
import re
from glob import glob

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'raw'))
CLEAN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cleaned'))
os.makedirs(CLEAN_DIR, exist_ok=True)

# Simple Sona syntax checks
REQUIRED_KEYWORDS = [r'\bfn\b', r'\blet\b']
BRACE_PATTERN = re.compile(r'[{}\[\]()]')

for file in glob(os.path.join(RAW_DIR, '*.sona')):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    # Remove empty or tiny files
    if len(code.strip()) < 20:
        continue
    # Check for required keywords
    if not all(re.search(kw, code) for kw in REQUIRED_KEYWORDS):
        continue
    # Check for matching braces
    stack = []
    braces = {'{': '}', '(': ')', '[': ']'}
    valid = True
    for c in code:
        if c in braces:
            stack.append(braces[c])
        elif c in braces.values():
            if not stack or stack.pop() != c:
                valid = False
                break
    if not valid or stack:
        continue
    # Save cleaned file
    out_path = os.path.join(CLEAN_DIR, os.path.basename(file))
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(code)
    print(f"✅ Cleaned: {os.path.basename(file)}")
print("🎉 Dataset cleaning complete. Cleaned files in datasets/cleaned/")
