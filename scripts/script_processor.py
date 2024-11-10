# scripts/script_processor.py

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

def process_script(script_path, config):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read()
        # Use LLM to process the script
        prompt = f"Analyze the following script and list the key points and characters:\n\n{script}"
        # Command to run Ollama with Mistral
        command = ["ollama", "run", "hf.co/ArliAI/Mistral-Small-22B-ArliAI-RPMax-v1.1-GGUF:latest", prompt]
        logging.info(f"Running LLM command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')  # Updated line
        if result.returncode != 0:
            logging.error(f"LLM command failed: {result.stderr}")
            return [], []
        output = result.stdout.strip()
        # Parse the output to extract key points and characters
        key_points = []
        characters = []
        current_section = None
        for line in output.split('\n'):
            line = line.strip()
            if line.lower().startswith('key points'):
                current_section = 'key_points'
                continue
            elif line.lower().startswith('characters'):
                current_section = 'characters'
                continue
            elif line.startswith('-') or line.startswith('1.') or line.startswith('*'):
                item = line.lstrip('-*0123456789. ').strip()
                if current_section == 'key_points':
                    key_points.append(item)
                elif current_section == 'characters':
                    characters.append(item)
        logging.info(f"Extracted {len(key_points)} key points and {len(characters)} characters.")
        return key_points, characters
    except Exception as e:
        logging.error(f"Error processing script: {e}")
        return [], []

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script_processor.py <config_path> <script_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    script_path = sys.argv[2]
    config = load_config(config_path)
    key_points, characters = process_script(script_path, config)
    print("Key Points:")
    for point in key_points:
        print(f"- {point}")
    print("\nCharacters:")
    for char in characters:
        print(f"- {char}")
