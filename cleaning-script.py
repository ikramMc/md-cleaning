import os
import re
import argparse
from pathlib import Path

def load_regexes_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

def remove_non_ascii(text):
    return ''.join([c for c in text if ord(c) < 128])

def basic_cleanup(text):
    # Nettoyage standard
    text = re.sub(r'\n{3,}', '\n\n', text)  # lignes vides multiples
    text = re.sub(r'\n[-–—_]{3,}\n', '\n', text)  # séparateurs
    text = re.sub(r' {2,}', ' ', text)  # espaces multiples
    return text.strip()

def clean_markdown(content, regex_patterns, remove_ascii=False):
    for pattern in regex_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)

    if remove_ascii:
        content = remove_non_ascii(content)

    return basic_cleanup(content)

def process_folder(input_dir, output_dir, regex_file, remove_ascii):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    regex_patterns = load_regexes_from_file(regex_file)
    md_files = list(input_dir.glob("*.md"))
    print(f"📂 {len(md_files)} fichiers trouvés dans {input_dir}")

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = clean_markdown(content, regex_patterns, remove_ascii)

        out_path = output_dir / file_path.name
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"✅ {file_path.name} nettoyé → {out_path.name}")

def main():
    parser = argparse.ArgumentParser(description="Nettoyage CLI de fichiers Markdown avec des regex")
    parser.add_argument("--input", required=True, help="Répertoire contenant les fichiers .md")
    parser.add_argument("--regex-file", required=True, help="Fichier texte avec une regex par ligne")
    parser.add_argument("--remove-non-ascii", choices=["true", "false"], default="false", help="Supprimer les caractères non-ASCII")
    parser.add_argument("--output", default=None, help="Répertoire de sortie (par défaut: écrasement)")

    args = parser.parse_args()
    remove_ascii = args.remove_non_ascii.lower() == "true"
    output_dir = args.output or args.input

    process_folder(args.input, output_dir, args.regex_file, remove_ascii)

if __name__ == "__main__":
    main()
