# scripts/image_generator.py

import yaml
import requests
import os
import logging
import base64

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def list_available_models(models_directory):
    try:
        models = [f for f in os.listdir(models_directory) if f.endswith('.ckpt') or f.endswith('.safetensors')]
        return models
    except Exception as e:
        logging.error(f"Error listing models: {e}")
        return []

def list_available_loras(loras_directory):
    try:
        loras = [f for f in os.listdir(loras_directory) if f.endswith('.ckpt') or f.endswith('.safetensors')]
        return loras
    except Exception as e:
        logging.error(f"Error listing LoRAs: {e}")
        return []

def generate_image(prompt, config, output_path, model=None, lora=None, style=None):
    try:
        payload = {
            "prompt": prompt,
            "steps": 20,  # Example steps
            "cfg_scale": 7.0,  # Example cfg scale
            "width": 512,
            "height": 512,
            "sampler_index": "Euler a",  # Example sampler
            "seed": -1,  # Random seed
            "negative_prompt": "",
        }
        if model:
            payload["model"] = model
        if lora:
            payload["lora"] = lora
        # Include style in the prompt if necessary
        if style:
            payload["prompt"] += f", style of {style}"
        
        logging.info(f"Sending request to Stable Diffusion API with prompt: {prompt}")
        response = requests.post(
            f"{config['automatic1111_api']}/sdapi/v1/txt2img",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        # Assuming the API returns images as base64-encoded strings
        image_data = data['images'][0]
        image_bytes = base64.b64decode(image_data)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        logging.info(f"Image generated and saved to {output_path}.")
        return True
    except Exception as e:
        logging.error(f"Failed to generate image for prompt '{prompt}': {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6:
        print("Usage: python image_generator.py <config_path> <prompt> <output_path> <model> <lora>")
        sys.exit(1)
    config_path = sys.argv[1]
    prompt = sys.argv[2]
    output_path = sys.argv[3]
    model = sys.argv[4]
    lora = sys.argv[5]
    config = load_config(config_path)
    success = generate_image(prompt, config, output_path, model=model, lora=lora)
    if success:
        print(f"Image saved to {output_path}")
    else:
        print("Image generation failed.")
