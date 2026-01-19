---
name: remove-bubble
description: Removes speech bubbles and text from manga pages.
---

# Remove Speech Bubbles

This skill removes speech bubbles and text from manga pages using image generation (inpainting).

## Workflow

1. **Generate**: Use the `generate_image` tool with the prompt below to remove bubbles.
2. **Verify**: Use the `view_file` tool to inspect the generated image for any remaining text, artifacts, or poor inpainting. **Crucially, compare the generated image with the *original* image.** Ensure that **only** the speech bubble areas were modified. The rest of the artwork (background, characters outside bubbles, borders) must remain **exactly** the same.
3. **Retry**: If defects are found, re-run `generate_image` on the *new* image (or the original if appropriate) with a refined prompt or masked area to fix the specific issues. Repeat until clean.

## Usage

Use the `generate_image` tool with the following prompt:

"Remove all speech bubbles and text from this manga page. Inpaint the area behind the bubbles to match the background artwork seamlessly. Keep the rest of the image unchanged."

## Example

```json
{
  "prompt": "Remove all speech bubbles and text from this manga page. Inpaint the area behind the bubbles to match the background artwork seamlessly. Keep the rest of the image unchanged.",
  "image_paths": ["/path/to/manga_page.png"]
}
```
