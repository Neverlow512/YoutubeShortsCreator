# scripts/image_editor.py

from PIL import Image, ImageEnhance
import logging

def enhance_image(image_path, output_path):
    try:
        image = Image.open(image_path)
        # Example enhancements
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        image.save(output_path)
        logging.info(f"Enhanced image saved to {output_path}.")
        return output_path
    except Exception as e:
        logging.error(f"Error enhancing image '{image_path}': {e}")
        return image_path  # Return original if enhancement fails

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python image_editor.py <input_image_path> <output_image_path>")
        sys.exit(1)
    input_image = sys.argv[1]
    output_image = sys.argv[2]
    enhanced_image = enhance_image(input_image, output_image)
    print(f"Enhanced image saved to {enhanced_image}")
