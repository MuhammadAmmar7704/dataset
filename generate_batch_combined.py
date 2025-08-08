#!/usr/bin/env python3

import os
import random
from PIL import Image
import math

def generate_batch_combined_images(source_dir="colored_shapes", output_dir="generated_files", num_images=500):
    """
    Generate a batch of combined images from colored shapes
    
    Args:
        source_dir: Directory containing shape folders
        output_dir: Directory to save combined images
        num_images: Number of combined images to generate
    """
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
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
    print(f"Generating {num_images} combined images...")
    
    for i in range(num_images):
        # Always select exactly 5 shapes (allows duplicates)
        num_shapes = 5
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
            print(f"No images found for combination {i + 1}")
            continue
        
        # Open images
        images = [Image.open(img).convert("RGBA") for img in selected_images]
        width, height = images[0].size
        
        # Calculate grid dimensions for 5 images (ideal layout would be roughly square)
        # For 5 images, we'll use a 3x2 grid (6 slots with 1 empty)
        cols = 3
        rows = 2
        
        # Create blank canvas with white background
        canvas = Image.new('RGBA', (width * cols, height * rows), (255, 255, 255, 255))
        
        # Paste images into the canvas
        for idx, img in enumerate(images):
            x = (idx % cols) * width
            y = (idx // cols) * height
            canvas.paste(img, (x, y), img)
        
        # Save final image
        output_path = os.path.join(output_dir, f"combined_{i+1:04d}.png")
        canvas.save(output_path)
        
        if (i + 1) % 50 == 0 or i == 0:
            print(f"✓ Generated {i + 1}/{num_images} images...")
    
    print(f"\n🎉 Generated {num_images} combined images in '{output_dir}' folder!")
    print(f"📁 Each image contains exactly 5 shapes with beautiful colors from your palette")

if __name__ == "__main__":
    # Generate 500 combined images (as requested)
    generate_batch_combined_images(num_images=4500)
