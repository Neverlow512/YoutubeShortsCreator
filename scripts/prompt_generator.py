# scripts/prompt_generator.py

import yaml
import subprocess
import logging

def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def generate_prompts(key_points, config):
    prompts = []
    for point in key_points:
        try:
            # Use LLM to generate image prompt for the key point
            prompt_text = f"Generate a detailed image prompt for the following key point: {point}"
            command = ["ollama", "run", "hf.co/ArliAI/Mistral-Small-22B-ArliAI-RPMax-v1.1-GGUF:latest", prompt_text]
            logging.info(f"Running LLM command for prompt generation: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')  # Updated line
            if result.returncode != 0:
                logging.error(f"LLM command failed for key point '{point}': {result.stderr}")
                prompts.append(f"Image for: {point}")
                continue
            output = result.stdout.strip()
            prompts.append(output)
            logging.info(f"Generated prompt: {output}")
        except Exception as e:
            logging.error(f"Error generating prompt for key point '{point}': {e}")
            prompts.append(f"Image for: {point}")
    return prompts

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python prompt_generator.py <config_path> <script_path> <output_prompts_file>")
        sys.exit(1)
    config_path = sys.argv[1]
    script_path = sys.argv[2]
    output_prompts_file = sys.argv[3]
    from script_processor import process_script
    config = load_config(config_path)
    key_points, _ = process_script(script_path, config)
    prompts = generate_prompts(key_points, config)
    with open(output_prompts_file, 'w', encoding='utf-8') as f:
        for prompt in prompts:
            f.write(f"{prompt}\n")
    print(prompts)
