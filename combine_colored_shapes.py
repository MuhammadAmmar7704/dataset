#!/usr/bin/env python3

import os
import random
from PIL import Image
import math

def combine_colored_shapes(source_dir="colored_shapes", output_file="combined_colored_shapes.png", num_combinations=10):
    """
    Combine 2-5 shapes from the colored shapes directory into grid layouts
    
    Args:
        source_dir: Directory containing shape folders
        output_file: Name of the output combined image
        num_combinations: Number of different combinations to generate
    """
    
    # Find all shape folders
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' not found. Please run generate_colored_shapes.py first.")
        return
    
    shape_dirs = [
        os.path.join(source_dir, d)
        for d in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, d))
    ]
    
    if len(shape_dirs) < 2:
        print("Need at least 2 shape folders to combine images.")
        return
    
    print(f"Found {len(shape_dirs)} shape types: {[os.path.basename(d) for d in shape_dirs]}")
    
    for combination in range(num_combinations):
        # Randomly select between 2-5 shapes (allows duplicates)
        num_shapes = random.randint(2, 5)
        selected_shape_dirs = random.choices(shape_dirs, k=num_shapes)
        
        # Pick one random image from each selected shape folder
        selected_images = []
        for shape_dir in selected_shape_dirs:
            images = [
                os.path.join(shape_dir, f)
                for f in os.listdir(shape_dir)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
            ]
            if images:
                selected_images.append(random.choice(images))
        
        if not selected_images:
            print(f"No images found for combination {combination + 1}")
            continue
        
        # Open images
        images = [Image.open(img).convert("RGBA") for img in selected_images]
        width, height = images[0].size
        
        # Calculate grid dimensions for better layout
        cols = math.ceil(math.sqrt(len(images)))
        rows = math.ceil(len(images) / cols)
        
        # Create blank canvas with white background
        canvas = Image.new('RGBA', (width * cols, height * rows), (255, 255, 255, 255))
        
        # Paste images into the canvas
        for idx, img in enumerate(images):
            x = (idx % cols) * width
            y = (idx // cols) * height
            canvas.paste(img, (x, y), img)
        
        # Save final image
        if num_combinations == 1:
            output_path = output_file
        else:
            base, ext = os.path.splitext(output_file)
            output_path = f"{base}_{combination + 1:03d}{ext}"
        
        canvas.save(output_path)
        print(f"✓ Saved combination {combination + 1}: {len(images)} shapes -> {output_path}")
    
    print(f"\n🎉 Generated {num_combinations} combined images!")

if __name__ == "__main__":
    # Generate one combined image
    combine_colored_shapes(num_combinations=1)
    
    # Uncomment the line below to generate multiple combinations
    # combine_colored_shapes(num_combinations=10)
