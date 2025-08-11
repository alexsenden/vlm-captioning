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
python vlm_caption_cli.py --input=<input_dir> [--model=<vlm_model>]
```

### Command Line Args

##### Required Args:

```
--input=<input_dir>
```

##### Optional Args:

```
--model=<vlm_model>
--max_length=<max_new_tokens>
--ignore_substring=<ignore_substring>
```
