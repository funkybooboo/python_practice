#!/usr/bin/env python3
import os
import sys
import re
import shutil
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

def main():
    VAULT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    THRESHOLD = 0.4

    model = SentenceTransformer('all-MiniLM-L6-v2')

    docs = load_files(VAULT)
    file_paths = list(docs.keys())
    file_texts = list(docs.values())

    print("🔎 Embedding documents...")
    embeddings = model.encode(file_texts, convert_to_tensor=True)

    print("🔗 Finding semantic links...")
    sims = util.pytorch_cos_sim(embeddings, embeddings)

    for i, path_a in enumerate(file_paths):
        related = []
        for j, path_b in enumerate(file_paths):
            if i == j:
                continue
            sim = sims[i][j].item()
            if sim >= THRESHOLD:
                related.append(get_title(path_b))

        if related:
            with open(path_a, 'r', encoding='utf-8') as f:
                content = f.read()

            content = re.sub(r'## Related\b.*$', '', content, flags=re.DOTALL)

            content = content.rstrip() + '\n\n## Related\n'
            for link in sorted(set(related)):
                if f'[[{link}]]' not in content:
                    content += f'- [[{link}]]\n'

            with open(path_a, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Updated: {path_a.relative_to(VAULT)}")

    print("🎉 Semantic linking complete.")

if __name__ == "__main__":
    main()

