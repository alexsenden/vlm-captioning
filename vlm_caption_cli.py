import argparse

from vlm_caption import caption_entire_directory, init_model


def parse_args():
    parser = argparse.ArgumentParser(
        description="Caption images from a dataset using a VLM."
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="The path of the input directory containing images to be captioned.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="The HuggingFace model used to generate captions.",
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=None,
        help="The maximum number of tokens to be generated in any given caption.",
    )
    parser.add_argument(
        "--ignore_substring",
        type=str,
        default=None,
        help="Ignore files and subdirectories that contain this substring in their names.",
    )
    parser.add_argument(
        "--num_captions",
        type=str,
        default=None,
        help="Number of captions to be generated.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    model, processor = init_model(args.model)
    output_dir = f"{args.input_dir}_caption"

    if args.model is not None:
        print(f"INFO: Using model {args.model} for captioning.", flush=True)
    if args.max_length is not None:
        print(f"INFO: Setting max length to {args.max_length} tokens.", flush=True)
    if args.ignore_substring is not None:
        print(
            f"INFO: Ignoring files/directories containing substring '{args.ignore_substring}'.",
            flush=True,
        )

    caption_entire_directory(
        args.input_dir,
        output_dir,
        model,
        processor,
        max_new_tokens=args.max_length,
        ignore_substring=args.ignore_substring,
        num_captions=args.num_captions,
    )


main()
