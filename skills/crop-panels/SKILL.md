---
name: crop-panels
description: Crops individual panels from a manga page using a segmentation JSON file.
---

# Crop Panels

This skill takes an original manga page image and a JSON file containing panel coordinates (produced by the `segment-page` skill) and generates individual image files for each panel.

## Dependencies

This skill requires the `Pillow` library.
```bash
pip install Pillow
```

## Workflow

1.  **Prerequisites**:
    *   You must have the original image file.
    *   You must have a JSON file containing the panel rectangles (e.g., from `segment-page`).

2.  **Execute**: Run the `crop_tool.py` script.
    ```bash
    python3 .agent/skills/crop-panels/crop_tool.py --image "<path_to_image>" --json "<path_to_json>" --output "<output_directory>"
    ```
    *   `--image`: Absolute or relative path to the original image file.
    *   `--json`: Absolute or relative path to the JSON segmentation file in `[[x,y,w,h], ...]` format.
    *   `--output`: Directory where the cropped panel images will be saved.

## Example

Assuming you have:
*   Image: `raw/chapter1/01.jpg`
*   JSON: `processed/segment/chapter1_01.json`

Run:
```bash
python3 .agent/skills/crop-panels/crop_tool.py \
  --image "raw/chapter1/01.jpg" \
  --json "processed/segment/chapter1_01.json" \
  --output "processed/panels/chapter1_01"
```

## Output

The script will generate images named `panel_001.jpg`, `panel_002.jpg`, etc., in the specified output directory.
