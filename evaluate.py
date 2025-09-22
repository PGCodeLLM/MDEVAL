#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def run_evaluation(experiment_id, task):
    print(f"Running evaluation for experiment '{experiment_id}', task '{task}'")

    inference_file = Path(f"data/eval_result/{experiment_id}/{task}/inference_results.jsonl")
    evaluation_file = Path(f"data/eval_result/{experiment_id}/{task}/evaluation_results.jsonl")

    if not inference_file.exists():
        print(f"Inference results file not found: {inference_file}")
        return False

    print(f"Processing inference results from: {inference_file}")

    # Group results by language for evaluation
    language_results = {}

    try:
        with open(inference_file, 'r') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    language = item.get('language', 'Unknown')
                    if language not in language_results:
                        language_results[language] = []
                    language_results[language].append(item)

        print(f"Found results for {len(language_results)} languages")

        for language, items in language_results.items():
            print(f"Evaluating {language}...")

            # Save language results in the format expected by evaluation
            language_file = Path(f"data/chat_result/{experiment_id}/{task}/{language}.jsonl")
            language_file.parent.mkdir(parents=True, exist_ok=True)

            with open(language_file, 'w') as f:
                for item in items:
                    # Convert CLI framework 'response' field to 'llm_response' for apr.py compatibility
                    if 'response' in item:
                        item['llm_response'] = item['response']
                        del item['response']
                    f.write(json.dumps(item) + '\n')

        # Run evaluation using original evaluation logic
        eval_cmd = [
            sys.executable, "excute/apr.py",
            task,
            experiment_id
        ]

        try:
            result = subprocess.run(eval_cmd, check=True, capture_output=True, text=True, cwd=".")
            print("Evaluation completed successfully!")
            print("Results:", result.stdout.strip())

            # Verify that the evaluation results file was created
            if evaluation_file.exists():
                print(f"Evaluation results file created: {evaluation_file}")
                return True
            else:
                print(f"Warning: Evaluation results file not found at {evaluation_file}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"Evaluation failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False

    except Exception as e:
        print(f"Error during evaluation: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MDEVAL Evaluation")
    parser.add_argument("--experiment_id", required=True, help="Experiment ID")
    parser.add_argument("--task", required=True, help="Task name")

    args = parser.parse_args()

    success = run_evaluation(args.experiment_id, args.task)
    sys.exit(0 if success else 1)
