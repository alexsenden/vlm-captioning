# VLM Captioner

Uses a VLM (initially configured to use `Qwen2.5-VL-32B-Instruct`) to caption images from a dataset.

### Dataset Structure

One VLM prompt will be used for each entire image directory.
For each image directory, a mirror file structure is created with the suffix `_caption`. This structure contains individual `.txt` caption files with filenames matching that of their image counterparts.

```
dataset/
└── top_level_folder_1/
    ├── image_folder_1 (contains prompt for entire folder)/
    │   ├── prompt.txt
    │   ├── image_1.png
    │   ├── image_2.png
    │   └── ...
    └── ...
```

### Running

First, install the required packages:

```
pip install -r requirements.txt
```

Then, run the script:

```
python vlm_caption_cli.py --input_dir=<input_dir> [--model=<vlm_model>]
```

### Command Line Args

##### Required Args:

```
--input_dir=<input_dir> || The path of the input directory containing images to be captioned.
```

##### Optional Args:

```
--model=<vlm_model> || VLM to use to generate captions
--max_length=<max_new_tokens> || Maximum number of new tokens before truncation
--ignore_substring=<ignore_substring> || Ignore files/directories containing this substring
--num_captions=<number_of_captions> || Number of captions to generate per image
--overwrite=<True/False> || If true, overwrites captions that already exist
--output_dir=<output_dir> || The directory to act as the root of the caption file structure. Defaults to `<input_dir>_caption`.
```
