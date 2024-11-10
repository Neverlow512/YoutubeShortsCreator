# main.py

import os
import sys
import yaml
import subprocess
import logging
from scripts.script_processor import process_script
from scripts.prompt_generator import generate_prompts
from scripts.image_generator import list_available_models, list_available_loras, generate_image
from scripts.image_editor import enhance_image
from scripts.video_assembler import assemble_video

def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def select_file_from_directory(directory, file_type, extensions=None):
    """
    Lists files in the specified directory with given extensions and prompts the user to select one.

    Args:
        directory (str): Path to the directory.
        file_type (str): Type of files (e.g., 'script', 'audio') for display purposes.
        extensions (list, optional): List of allowed file extensions (e.g., ['.txt']).

    Returns:
        str: Selected file path or exits if no files are available.
    """
    try:
        if extensions:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in extensions]
        else:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print(f"No {file_type} files found in {directory}. Please add some and try again.")
            sys.exit(1)
        print(f"\nAvailable {file_type} files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")
        while True:
            try:
                choice = int(input(f"Select a {file_type} file by entering its number (1-{len(files)}): ").strip())
                if 1 <= choice <= len(files):
                    selected_file = os.path.join(directory, files[choice - 1])
                    print(f"Selected {file_type} file: {selected_file}\n")
                    return selected_file
                else:
                    print(f"Please enter a number between 1 and {len(files)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except Exception as e:
        logging.error(f"Error selecting {file_type} file: {e}")
        sys.exit(1)

def get_user_input(prompt_text, default=None):
    if default:
        prompt = f"{prompt_text} [{default}]: "
    else:
        prompt = f"{prompt_text}: "
    response = input(prompt).strip()
    if not response and default is not None:
        return default
    return response

def select_from_list(options, prompt_text):
    if not options:
        print("No options available.")
        return None
    print(f"\n{prompt_text}:")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Configure logging
    logging.basicConfig(
        filename=os.path.join("logs", "app.log"),
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Load config
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config", "config.yaml")
    config = load_config(config_path)
    if not config:
        print("Failed to load configuration. Check logs for details.")
        sys.exit(1)

    # Define default directories
    scripts_dir = os.path.join(base_path, "story")
    audio_dir = os.path.join(base_path, "audio")

    # Ensure default directories exist
    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # Select script file with .txt extension
    script_path = select_file_from_directory(scripts_dir, "script", extensions=['.txt'])

    # Select audio file with .wav and .mp3 extensions
    audio_path = select_file_from_directory(audio_dir, "audio", extensions=['.wav', '.mp3'])

    # List available models and LoRAs
    models_dir = os.path.join(base_path, config.get('models_directory', 'models'))
    loras_dir = os.path.join(base_path, config.get('loras_directory', 'loras'))
    available_models = list_available_models(models_dir)
    available_loras = list_available_loras(loras_dir)

    # Process script
    key_points, characters = process_script(script_path, config)
    if not key_points:
        print("No key points extracted from the script. Exiting.")
        sys.exit(1)
    if not characters:
        print("No characters extracted from the script. Proceeding without character consistency.")

    # Display key points and characters
    print("\nKey Points:")
    for idx, point in enumerate(key_points, 1):
        print(f"{idx}. {point}")

    print("\nCharacters:")
    for idx, char in enumerate(characters, 1):
        print(f"{idx}. {char}")

    # Let user choose style
    style = get_user_input(
        "Enter the style you want for the images (e.g., comics, illustration)",
        default=config.get('default_style', 'comics')
    )

    # Let user select model
    selected_model = select_from_list(available_models, "Select the Stable Diffusion model you want to use")
    if not selected_model:
        print("No models available. Exiting.")
        sys.exit(1)
    config['sd_model'] = selected_model  # Update config if necessary

    # Let user select LoRA
    selected_lora = select_from_list(available_loras, "Select the LoRA you want to use")
    if not selected_lora:
        print("No LoRAs available. Proceeding without LoRA.")
    else:
        config['lora_model'] = selected_lora

    # Generate prompts
    print("\nGenerating prompts based on key points...")
    prompts = generate_prompts(key_points, config)
    if not prompts:
        print("Failed to generate prompts. Exiting.")
        sys.exit(1)

    # Display prompts
    print("\nGenerated Prompts:")
    for idx, prompt in enumerate(prompts, 1):
        print(f"{idx}. {prompt}")
    print(f"\nNumber of images to be generated: {len(prompts)}")

    # Get user approval
    approval = get_user_input("Do you approve the prompts and settings? (yes/no)", default="yes").lower()
    if approval not in ['yes', 'y']:
        print("Operation cancelled by the user.")
        sys.exit(0)

    # Generate images
    image_dir = os.path.join(base_path, "outputs", "images")
    os.makedirs(image_dir, exist_ok=True)
    image_paths = []
    for idx, prompt in enumerate(prompts, 1):
        image_path = os.path.join(image_dir, f"image_{idx}.png")
        print(f"Generating image {idx}/{len(prompts)}...")
        success = generate_image(prompt, config, image_path, model=selected_model, lora=selected_lora, style=style)
        if success:
            # Enhance image
            enhanced_path = os.path.join(image_dir, f"enhanced_image_{idx}.png")
            enhance_image(image_path, enhanced_path)
            image_paths.append(enhanced_path)
        else:
            print(f"Failed to generate image for prompt {idx}. Skipping.")

    if not image_paths:
        print("No images were successfully generated. Exiting.")
        sys.exit(1)

    # Assemble video
    video_output_dir = os.path.join(base_path, "outputs", "videos")
    os.makedirs(video_output_dir, exist_ok=True)
    output_video_path = os.path.join(video_output_dir, "output_video.mp4")
    print("Assembling video...")
    video = assemble_video(image_paths, audio_path, output_video_path, config)
    if video:
        print(f"Video created successfully at {video}")
    else:
        print("Failed to assemble video. Check logs for details.")

if __name__ == "__main__":
    main()
