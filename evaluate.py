#!/usr/bin/env python3
import json
import subprocess
import sys
import shutil
from pathlib import Path


def run_evaluation(experiment_id, task, inference_file=None, evaluation_dir=None):
    print(f"Running evaluation for experiment '{experiment_id}', task '{task}'")

    # Use provided paths or default paths
    if inference_file is None:
        inference_file = Path(f"data/eval_result/{experiment_id}/{task}/inference_results.jsonl")
    else:
        inference_file = Path(inference_file)

    if evaluation_dir is None:
        evaluation_dir = Path(f"data/eval_result/{experiment_id}/{task}")
    else:
        evaluation_dir = Path(evaluation_dir)

    evaluation_file = evaluation_dir / "evaluation_results.jsonl"

    if not inference_file.exists():
        print(f"Inference results file not found: {inference_file}")
        return False

    # Create evaluation output directory
    evaluation_dir.mkdir(parents=True, exist_ok=True)

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

        # Create expected directory structure that apr.py expects
        apr_input_dir = Path("data/chat_result") / experiment_id / task
        apr_output_dir = Path("data/eval_result") / experiment_id / task

        # Create directories
        apr_input_dir.mkdir(parents=True, exist_ok=True)
        apr_output_dir.mkdir(parents=True, exist_ok=True)

        for language, items in language_results.items():
            print(f"Evaluating {language}...")

            # Save language results in the directory structure apr.py expects
            language_file = apr_input_dir / f"{language}.jsonl"
            print(f"Creating language file: {language_file}")

            with open(language_file, 'w') as f:
                for item in items:
                    # Convert CLI framework 'response' field to 'llm_response' for apr.py compatibility
                    if 'response' in item:
                        item['llm_response'] = item['response']
                        del item['response']
                    f.write(json.dumps(item) + '\n')

            print(f"Created {language_file} with {len(items)} items")

        # Run evaluation using apr.py
        eval_cmd = [
            sys.executable, "excute/apr.py",
            task,
            experiment_id
        ]

        try:
            result = subprocess.run(eval_cmd, check=True, capture_output=True, text=True, cwd=".")
            print("Evaluation completed successfully!")
            print("Results:", result.stdout.strip())

            # Copy results from apr.py output location to our desired location
            apr_results_file = apr_output_dir / "evaluation_results.jsonl"
            if apr_results_file.exists():
                shutil.copy2(apr_results_file, evaluation_file)
                print(f"Copied evaluation results to: {evaluation_file}")

                # Clean up temporary directories
                try:
                    shutil.rmtree(Path("data"))
                    print("Cleaned up temporary data directory")
                except Exception as cleanup_e:
                    print(f"Warning: Failed to cleanup temporary directory: {cleanup_e}")

                return True
            else:
                print(f"Warning: apr.py results file not found at {apr_results_file}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"Evaluation failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False

        finally:
            # Always try to clean up temporary directory
            try:
                if Path("data").exists():
                    shutil.rmtree(Path("data"))
            except Exception:
                pass

    except Exception as e:
        print(f"Error during evaluation: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MDEVAL Evaluation")
    parser.add_argument("--experiment_id", required=True, help="Experiment ID")
    parser.add_argument("--task", required=True, help="Task name")
    parser.add_argument("--inference_file", help="Inference results file path")
    parser.add_argument("--evaluation_dir", help="Evaluation output directory")

    args = parser.parse_args()

    success = run_evaluation(args.experiment_id, args.task, args.inference_file, args.evaluation_dir)
    sys.exit(0 if success else 1)
