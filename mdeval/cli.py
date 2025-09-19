import argparse
import sys

from .main import run_generation, run_evaluation, show_results


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="MDEVAL Complete Evaluation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Complete evaluation with vLLM
  python evaluate.py --experiment_id qwen-doc --base_url http://localhost:8000/v1 \\
                     --model Qwen/Qwen3-8B --task doc
        """
    )

    # Required parameters
    parser.add_argument("--experiment_id", type=str, required=True,
                       help="Unique experiment identifier")
    parser.add_argument("--task", type=str, required=True,
                       choices=["bug", "doc", "example", "ident", "loc", "loc_apr", "review"],
                       help="MDEVAL task type")


    # Inference parameters
    parser.add_argument("--base_url", type=str, required=True,
                       help="vLLM API base URL")
    parser.add_argument("--model", type=str, required=True,
                       help="Model name")
    parser.add_argument("--api_key", type=str, default="my-vllm-api-key",
                       help="API key for authentication")


    # Generation parameters
    parser.add_argument("--temperature", type=float, default=0.0,
                       help="Generation temperature")
    parser.add_argument("--max_completion_tokens", type=int, default=4096,
                       help="Maximum completion tokens")
    parser.add_argument("--top_p", type=float,
                       help="Top-p sampling parameter")
    parser.add_argument("--top_k", type=int,
                       help="Top-k sampling parameter")
    parser.add_argument("--presence_penalty", type=float,
                       help="Presence penalty parameter")
    parser.add_argument("--repetition_penalty", type=float,
                       help="Repetition penalty parameter")

    # Execution parameters
    parser.add_argument("--parallel_workers", type=int, default=8,
                       help="Number of parallel workers for inference")
    parser.add_argument("--timeout", type=int, default=300,
                       help="Request timeout in seconds")

    return parser.parse_args()



def run_inference(args):
    """Run inference step"""
    print("=" * 60)
    print("STEP 1: Running Inference (Generation)")
    print("=" * 60)

    return run_generation(args)


def run_evaluation_step(args):
    """Run evaluation step"""
    print("\n" + "=" * 60)
    print("STEP 2: Running Evaluation (Code Execution)")
    print("=" * 60)

    return run_evaluation(args.task, args.experiment_id)


def show_results_step(args):
    """Show evaluation results"""
    print("\n" + "=" * 60)
    print("STEP 3: Results Summary")
    print("=" * 60)

    show_results(args.task, args.experiment_id)


def main():
    """Main entry point"""
    args = parse_arguments()

    # Add all languages
    args.languages = [
        'C', 'C#', 'Clisp', 'CPP', 'F#', 'Go', 'HTML', 'JavaScript',
        'Java', 'JSON', 'Julia', 'Markdown', 'PHP', 'Pascal', 'Python',
        'R', 'Ruby', 'Rust', 'Scala', 'Swift'
    ]

    print(f"Starting MDEVAL evaluation for '{args.task}' task")
    print(f"Experiment ID: {args.experiment_id}")

    # Run inference step
    success = run_inference(args)
    if not success:
        print("Pipeline failed at inference step")
        sys.exit(1)

    # Run evaluation step
    success = run_evaluation_step(args)
    if not success:
        print("Pipeline failed at evaluation step")
        sys.exit(1)

    # Show results
    show_results_step(args)

    print(f"\nMDEVAL evaluation completed successfully!")
    print(f"Results location: mdeval/eval_results/{args.task}/{args.experiment_id}/")
    print(f"Metadata location: mdeval/eval_results/{args.task}/{args.experiment_id}/meta/")
