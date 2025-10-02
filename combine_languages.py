#!/usr/bin/env python3
"""
MDEVAL Language Combination Script
Simple and clean language dataset combiner.
"""

import argparse
import json
import sys
import shutil
from pathlib import Path


def combine_languages(task: str, languages: str, output_file: Path) -> bool:
    """
    Combine language datasets for MDEVAL task

    Args:
        task: Task name (bug, doc, example, etc.)
        languages: Comma-separated language list or 'all'
        output_file: Output file path

    Returns:
        bool: Success status
    """
    base_dir = Path(__file__).parent

    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if languages == "all":
        # Copy merged data file
        merged_file = base_dir / "data" / "merged_data" / f"{task}.jsonl"
        if merged_file.exists():
            shutil.copy2(merged_file, output_file)
            line_count = sum(1 for line in open(output_file) if line.strip())
            print(f"Copied all languages: {line_count} problems")
            return True
        else:
            print(f"Merged file not found: {merged_file}")
            return False

    # Combine specific languages
    raw_data_dir = base_dir / "data" / "raw_data" / task
    if not raw_data_dir.exists():
        print(f"Task directory not found: {raw_data_dir}")
        return False

    lang_list = [lang.strip() for lang in languages.split(',')]
    total_count = 0

    print(f"Combining {len(lang_list)} language(s) for task '{task}'")

    with open(output_file, 'w') as outf:
        for lang in lang_list:
            lang_file = raw_data_dir / f"{lang}.jsonl"

            if not lang_file.exists():
                print(f"Language file not found: {lang_file}")
                continue

            lang_count = 0
            with open(lang_file, 'r') as inf:
                for line in inf:
                    line = line.strip()
                    if line:
                        # Parse and add missing fields
                        try:
                            data = json.loads(line)
                            data['language'] = lang
                            data['task'] = task
                            outf.write(json.dumps(data) + '\n')
                            lang_count += 1
                        except json.JSONDecodeError:
                            continue

            total_count += lang_count
            print(f"   - {lang}: {lang_count} problems")

    print(f"Combined dataset: {total_count} total problems")
    return total_count > 0


def main():
    parser = argparse.ArgumentParser(description="Combine MDEVAL language datasets")
    parser.add_argument('--task', required=True,
                       choices=['bug', 'doc', 'example', 'ident', 'loc', 'loc_apr', 'review'],
                       help='MDEVAL task name')
    parser.add_argument('--languages', required=True,
                       help='Comma-separated languages or "all"')
    parser.add_argument('--output', required=True, type=Path,
                       help='Output file path')

    args = parser.parse_args()

    success = combine_languages(args.task, args.languages, args.output)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
