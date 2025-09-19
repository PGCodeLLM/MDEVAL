import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import httpx
from openai import OpenAI

from .utils import load_dataset, save_results, create_metadata, create_progress_file, update_progress


def create_client(base_url, api_key, timeout=300):
    """Create OpenAI client for vLLM API"""
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=httpx.Client(verify=True, timeout=timeout)
    )


def generate_response(client, model, instruction, generation_params):
    """Generate response for a single instruction"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": instruction}
            ],
            **generation_params
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return ""


def prepare_generation_params(temperature=0.0, max_completion_tokens=4096,
                             top_p=None, top_k=None, presence_penalty=None,
                             repetition_penalty=None):
    """Prepare generation parameters for API calls"""
    params = {
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
        "stream": False,
    }

    if top_p is not None:
        params["top_p"] = top_p
    if presence_penalty is not None:
        params["presence_penalty"] = presence_penalty

    extra_body = {}
    if top_k is not None:
        extra_body["top_k"] = top_k
    if repetition_penalty is not None:
        extra_body["repetition_penalty"] = repetition_penalty

    if extra_body:
        params["extra_body"] = extra_body

    return params


def process_language(language, task, experiment_id, client, model, generation_params, meta_dir=None, global_progress=None):
    """Process a single language"""
    print(f"Processing {language} for task {task}...")

    dataset = load_dataset(task, language)
    if not dataset:
        return {"language": language, "completed": 0, "total": 0}

    results = []
    completed = 0

    for item in dataset:
        llm_response = generate_response(client, model, item['instruction'], generation_params)

        result_item = item.copy()
        result_item['llm_response'] = llm_response
        results.append(result_item)
        completed += 1

        # Update global progress every 5 tasks for better real-time tracking
        if meta_dir and global_progress is not None and completed % 5 == 0:
            with global_progress['lock']:
                global_progress['completed'] += 5
                update_progress(meta_dir, global_progress['completed'], global_progress['total'])

        if completed % 10 == 0:
            print(f"{language}: {completed}/{len(dataset)} completed")

    output_file = f'mdeval/eval_results/{experiment_id}/{task}/{language}.jsonl'
    save_results(results, output_file)

    print(f"Completed {language}: {completed}/{len(dataset)}")
    return {"language": language, "completed": completed, "total": len(dataset)}


def run_generation(args):
    """Run generation for all languages"""
    output_dir = Path(f"mdeval/eval_results/{args.experiment_id}/{args.task}")
    meta_dir = output_dir / "meta"
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    client = create_client(args.base_url, args.api_key, args.timeout)
    generation_params = prepare_generation_params(
        temperature=args.temperature,
        max_completion_tokens=args.max_completion_tokens,
        top_p=args.top_p,
        top_k=args.top_k,
        presence_penalty=args.presence_penalty,
        repetition_penalty=args.repetition_penalty
    )

    total_tasks = 0
    language_counts = {}
    for language in args.languages:
        dataset = load_dataset(args.task, language)
        language_count = len(dataset)
        language_counts[language] = language_count
        total_tasks += language_count

    print(f"Total tasks to process: {total_tasks} across {len(args.languages)} languages")
    print("Tasks per language:")
    for language, count in language_counts.items():
        print(f"  {language}: {count} tasks")

    create_metadata(args, total_tasks, meta_dir)
    create_progress_file(total_tasks, meta_dir)

    # Set up shared progress tracking for parallel processing
    import threading
    global_progress = {
        'completed': 0,
        'total': total_tasks,
        'lock': threading.Lock()
    }

    completed_total = 0

    if args.parallel_workers > 1:
        with ThreadPoolExecutor(max_workers=args.parallel_workers) as executor:
            futures = []
            for language in args.languages:
                future = executor.submit(
                    process_language, language, args.task, args.experiment_id,
                    client, args.model, generation_params, meta_dir, global_progress
                )
                futures.append((future, language))

            for future, language in futures:
                try:
                    result = future.result()
                    completed_total += result["completed"]
                    # Final update for this language
                    with global_progress['lock']:
                        # Adjust for any remaining tasks not updated in the 5-task increments
                        remaining = result["completed"] % 5
                        if remaining > 0:
                            global_progress['completed'] += remaining
                            update_progress(meta_dir, global_progress['completed'], total_tasks)
                    print(f"{language}: {result['completed']}/{result['total']} tasks completed")
                except Exception as e:
                    print(f"{language} failed: {e}")
    else:
        for language in args.languages:
            try:
                result = process_language(language, args.task, args.experiment_id, client, args.model, generation_params, meta_dir, global_progress)
                completed_total += result["completed"]
                update_progress(meta_dir, completed_total, total_tasks)
                print(f"{language}: {result['completed']}/{result['total']} tasks completed")
            except Exception as e:
                print(f"{language} failed: {e}")

    print(f"\nGeneration completed!")
    print(f"Total completed: {completed_total}/{total_tasks}")
    print(f"Results saved to: {output_dir}")

    return True


def run_evaluation(task, experiment_id):
    """Run evaluation using original apr.py"""
    print(f"Running evaluation for task '{task}', experiment '{experiment_id}'")

    eval_cmd = [
        sys.executable, "excute/apr.py",
        task,
        experiment_id
    ]

    try:
        result = subprocess.run(eval_cmd, check=True, capture_output=True, text=True)
        print("Evaluation completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Evaluation failed!")
        print(f"Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def show_results(task, experiment_id):
    """Show evaluation results"""
    results_file = Path(f"mdeval/eval_results/{experiment_id}/{task}/evaluation_results.jsonl")

    if not results_file.exists():
        print(f"Results file not found: {results_file}")
        return

    print(f"Results saved to: {results_file}")

    try:
        total_problems = 0
        total_failed = 0

        print("\nPer-Language Results:")
        print("-" * 40)

        with open(results_file, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    language = result.get('language', 'Unknown')
                    failed = result.get('fail_num', 0)
                    total = result.get('total', 0)
                    passed = total - failed
                    pass_rate = (passed / total * 100) if total > 0 else 0

                    print(f"{language:12} | {passed:3}/{total:3} | {pass_rate:5.1f}%")

                    total_problems += total
                    total_failed += failed

        if total_problems > 0:
            overall_pass_rate = (total_problems - total_failed) / total_problems * 100
            print("-" * 40)
            print(f"{'OVERALL':12} | {total_problems - total_failed:3}/{total_problems:3} | {overall_pass_rate:5.1f}%")

    except Exception as e:
        print(f"Error reading results: {e}")
        print("Please check the results file manually.")
