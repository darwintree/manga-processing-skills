---
name: segment-page
description: Allows the user to manually segment a manga page by drawing rectangles.
---

# Segment Page

This skill launches a local web interface for the user to manually draw segmentation rectangles on a manga page.

## Workflow

1.  **Execute**: Run the `segment_tool.py` script.
    ```bash
    python3 .agent/skills/segment-page/segment_tool.py --image "<relative_path_to_image>" --chapter "<chapter_number>" --page "<page_number>"
    ```
    *   `--image`: Path to the image file (relative to project root).
    *   `--chapter`: Chapter number (used for output filename).
    *   `--page`: Page number (used for output filename).

2.  **Interact**:
    - The default browser should open automatically. If not, open `http://localhost:8000`.
    - Draw rectangles over the panels.
    - Click "Save" when finished.

3.  **Result**:
    - The backend saves the segmentation data to `processed/segment/chapter<chapter>_<page>.json`.
    - The server shuts down automatically after saving.

## Example

```bash
python3 .agent/skills/segment-page/segment_tool.py --image "25.jpg" --chapter "1" --page "25"
```
