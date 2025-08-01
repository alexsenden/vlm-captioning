import os

from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

DEFAULT_MODEL = "Qwen/Qwen2.5-VL-32B-Instruct"


def init_model(model_name=None):
    if model_name is None:
        model_name = DEFAULT_MODEL
        print(f"INFO: No model name provided. Using default model {model_name}.")

    print(f"INFO: Initializing model {model_name}.", flush=True)

    # Load the model on the available device(s)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_name, torch_dtype="auto", device_map="auto"
    )

    print(f"INFO: Model {model_name} loaded successfully.", flush=True)
    print(f"INFO: Loading processor for model {model_name}.", flush=True)

    # Load the default processor
    processor = AutoProcessor.from_pretrained(model_name)

    print(f"INFO: Processor for model {model_name} loaded successfully.", flush=True)

    return model, processor


def get_prompt_for_directory(directory_path):
    prompt = ""
    prompt_file_path = os.path.join(directory_path, "prompt.txt")
    try:
        with open(prompt_file_path) as prompt_file:
            prompt = prompt_file.read()
    except FileNotFoundError:
        print(
            f"WARN: Prompt file not found for directory {prompt_file_path}. Using default prompt.",
            flush=True,
        )
        prompt = "Describe the image in detail."

    print(f"INFO: Using prompt: '{prompt}'", flush=True)

    return prompt


def is_image_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif")):
            return True
    return False


def get_messages(prompt, image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        }
    ]


def caption_image(prompt, image, model, processor):
    messages = get_messages(prompt, image)

    # Prepare inputs for the model
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # Generate caption
    generated_ids = model.generate(**inputs, max_new_tokens=128, do_sample=True, top_p = 1.0, temperature=0.7, top_k=50)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    return output_text[0]


def write_caption_to_file(image_file, caption, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    caption_file = os.path.join(
        output_directory, f"{os.path.splitext(image_file)[0]}.txt"
    )
    with open(caption_file, "w") as f:
        f.write(caption)


def caption_entire_directory(directory_path, output_directory, model, processor):
    print(
        f"INFO: Processing directory {directory_path} for image captions.", flush=True
    )

    if not is_image_directory(directory_path):
        for subdir in os.listdir(directory_path):
            subdir_path = os.path.join(directory_path, subdir)
            if os.path.isdir(subdir_path):
                caption_entire_directory(
                    subdir_path,
                    os.path.join(output_directory, subdir),
                    model,
                    processor,
                )
    else:
        prompt = get_prompt_for_directory(directory_path)
        for image_file in os.listdir(directory_path):
            if image_file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif")
            ):
                try:
                    caption = caption_image(
                        prompt,
                        os.path.join(directory_path, image_file),
                        model,
                        processor,
                    )
                    write_caption_to_file(image_file, caption, output_directory)
                except Exception as e:
                    print(
                        f"WARN: Error processing image {image_file} in {directory_path}: {e}",
                        flush=True,
                    )
