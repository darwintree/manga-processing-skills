import argparse
import json
import os
import sys
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is not installed. Please install it using 'pip install Pillow'")
    sys.exit(1)

def crop_panels(image_path, json_path, output_dir):
    """
    Crops panels from an image based on a JSON file containing rectangles.
    
    Args:
        image_path: Path to the source image file.
        json_path: Path to the JSON file with segmentation data.
        output_dir: Directory to save the cropped images.
    """
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found: {json_path}")
        return

    try:
        with open(json_path, 'r') as f:
            rects = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON file: {json_path}")
        return

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error: Failed to open image: {e}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing {len(rects)} panels...")
    
    for i, rect in enumerate(rects):
        # Format: [x, y, w, h]
        if len(rect) != 4:
            print(f"Warning: Skipping invalid rectangle format at index {i}: {rect}")
            continue
            
        x, y, w, h = rect
        
        # Validate coordinates
        if w <= 0 or h <= 0:
             print(f"Warning: Skipping invalid dimensions at index {i}: {w}x{h}")
             continue

        # Crop
        # PIL crop takes (left, top, right, bottom)
        left = x
        top = y
        right = x + w
        bottom = y + h
        
        try:
            panel = img.crop((left, top, right, bottom))
            
            # Save
            output_filename = f"panel_{i+1:03d}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            # Convert to RGB if necessary (e.g. for PNGs with alpha) before saving as JPG
            if panel.mode in ('RGBA', 'P'):
                panel = panel.convert('RGB')
                
            panel.save(output_path, "JPEG", quality=95)
            print(f"Saved {output_path}")
            
        except Exception as e:
            print(f"Error processing panel {i+1}: {e}")

    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop panels from a manga page based on segmentation JSON.")
    parser.add_argument("--image", required=True, help="Path to the original image file")
    parser.add_argument("--json", required=True, help="Path to the segmentation JSON file")
    parser.add_argument("--output", required=True, help="Directory to output cropped panels")
    
    args = parser.parse_args()
    
    crop_panels(args.image, args.json, args.output)
