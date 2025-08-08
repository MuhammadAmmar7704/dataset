#!/usr/bin/env python3

import os
import shutil
from generator import GeometricShapes

def generate_colored_shapes():
    """Generate shape images with new color palette and organize them into folders"""
    
    # Create main output directory
    output_dir = "colored_shapes"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Number of images per shape
    images_per_shape = 50
    
    print("Generating colored shape images...")
    print(f"Generating {images_per_shape} images of each shape type...")
    
    # Generate all images in the output directory
    generator = GeometricShapes(destination=output_dir, size=images_per_shape)
    generator.generate()
    
    print(f"✓ Generated all shape images in {output_dir}")
    
    # Now organize images by shape into subfolders
    print("Organizing images into shape-specific folders...")
    
    # Create subfolders for each shape
    shape_folders = {}
    image_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.png')]
    
    for image_file in image_files:
        # Extract shape name from filename (format: ShapeName_uuid.png)
        shape_name = image_file.split('_')[0].lower()
        
        if shape_name not in shape_folders:
            shape_folder = os.path.join(output_dir, shape_name)
            os.makedirs(shape_folder, exist_ok=True)
            shape_folders[shape_name] = shape_folder
        
        # Move image to appropriate subfolder
        src_path = os.path.join(output_dir, image_file)
        dst_path = os.path.join(shape_folders[shape_name], image_file)
        shutil.move(src_path, dst_path)
    
    for shape_name, folder_path in shape_folders.items():
        count = len([f for f in os.listdir(folder_path) if f.lower().endswith('.png')])
        print(f"✓ Organized {count} {shape_name} images in {folder_path}")
    
    print(f"\n🎉 All shapes generated and organized successfully in '{output_dir}' folder!")
    print(f"📁 Each shape type has its own subfolder")

if __name__ == "__main__":
    generate_colored_shapes()
