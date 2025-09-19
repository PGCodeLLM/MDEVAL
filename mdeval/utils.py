"""Utilities for MDEVAL"""

import json
import os
from datetime import datetime


def load_dataset(task, language):
    """Load dataset for specific task and language"""
    input_file = f'data/raw_data/{task}/{language}.jsonl'

    if not os.path.exists(input_file):
        print(f"Warning: Dataset file not found: {input_file}")
        return []

    dataset = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    dataset.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return dataset


def save_results(results, output_file):
    """Save results to JSONL file"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def create_metadata(args, total_tasks, output_dir):
    """Create experiment metadata"""
    metadata = {
        "created_at": datetime.now().isoformat(),
        "experiment_id": args.experiment_id,
        "total_tasks": total_tasks,
        "model_name": args.model,
        "base_url": args.base_url,
        "task": args.task,
        "languages": args.languages,
        "temperature": args.temperature,
        "max_completion_tokens": args.max_completion_tokens,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "presence_penalty": args.presence_penalty,
        "repetition_penalty": args.repetition_penalty,
        "parallel_workers": args.parallel_workers,
        "timeout": args.timeout,
    }

    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    return metadata


def create_progress_file(total_tasks, output_dir):
    """Create initial progress file"""
    progress = {
        "completed_problems": 0,
        "total_problems": total_tasks,
        "current_problem": 0,
        "last_updated": datetime.now().isoformat()
    }
    with open(output_dir / "progress.json", "w") as f:
        json.dump(progress, f, indent=2)


def update_progress(output_dir, completed_problems, total_problems):
    """Update progress file"""
    try:
        progress_file = output_dir / "progress.json"
        if progress_file.exists():
            with open(progress_file, "r") as f:
                progress = json.load(f)
        else:
            progress = {"completed_problems": 0, "total_problems": total_problems, "current_problem": 0}

        progress["completed_problems"] = completed_problems
        progress["total_problems"] = total_problems
        progress["current_problem"] = completed_problems
        progress["last_updated"] = datetime.now().isoformat()

        with open(progress_file, "w") as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        print(f"Error updating progress: {e}")