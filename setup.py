import os
import subprocess
import sys
import shutil
import logging

# Configure logging
logging.basicConfig(
    filename='setup.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define project structure
PROJECT_NAME = "youtube_short_creator"
DIRECTORY_STRUCTURE = {
    "config": {},
    "scripts": {},
    "outputs": {
        "images": {},
        "videos": {}
    },
    "logs": {}
}

# Define dependencies
REQUIREMENTS = [
    "requests",
    "moviepy",
    "Pillow",
    "opencv-python",
    "PyYAML",
    "argparse",
    # Add any other dependencies as needed
]

# Paths to existing tools
FFMPEG_PATH = r"D:\FFmpeg\ffmpeg-2024-03-20-git-e04c638f5f-full_build\bin\ffmpeg.exe"
AUTOMATIC1111_API = "http://localhost:7860"
OLLAMA_API = "http://localhost:11434"

def create_directories(base_path):
    try:
        logging.info(f"Creating project directories in {base_path}...")
        for folder, subfolders in DIRECTORY_STRUCTURE.items():
            path = os.path.join(base_path, folder)
            os.makedirs(path, exist_ok=True)
            for subfolder in subfolders:
                os.makedirs(os.path.join(path, subfolder), exist_ok=True)
        logging.info("Directories created successfully.")
    except Exception as e:
        logging.error(f"Error creating directories: {e}")
        sys.exit(1)

def create_virtual_environment(base_path):
    venv_path = os.path.join(base_path, "venv")
    try:
        if not os.path.exists(venv_path):
            logging.info("Creating virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            logging.info("Virtual environment created.")
        else:
            logging.info("Virtual environment already exists.")
        return venv_path
    except Exception as e:
        logging.error(f"Error creating virtual environment: {e}")
        sys.exit(1)

def install_dependencies(venv_path):
    try:
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
        logging.info("Installing/upgrading pip...")
        subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError as e:
        logging.warning(f"Could not upgrade pip: {e}. Proceeding without upgrading pip.")
    except Exception as e:
        logging.error(f"Unexpected error during pip upgrade: {e}")
        sys.exit(1)

    try:
        logging.info("Installing Python dependencies...")
        subprocess.check_call([python_executable, "-m", "pip", "install"] + REQUIREMENTS)
        logging.info("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error during dependencies installation: {e}")
        sys.exit(1)

def write_config_file(base_path):
    config_content = f"""
# config/config.yaml

ffmpeg_path: "{FFMPEG_PATH}"
automatic1111_api: "{AUTOMATIC1111_API}"
ollama_api: "{OLLAMA_API}"
default_style: "comics"
"""
    config_path = os.path.join(base_path, "config", "config.yaml")
    try:
        with open(config_path, "w") as f:
            f.write(config_content.strip())
        logging.info("Configuration file created at config/config.yaml.")
    except Exception as e:
        logging.error(f"Error writing config file: {e}")
        sys.exit(1)

def create_skeleton_scripts(base_path):
    scripts = {
        "script_processor.py": """\
import yaml
import logging

def process_script(script_path):
    try:
        with open(script_path, 'r') as f:
            script = f.read()
        # TODO: Implement script processing to identify key points
        key_points = [sentence.strip() for sentence in script.split('.') if sentence.strip()]
        logging.info(f"Processed script and found {len(key_points)} key points.")
        return key_points
    except Exception as e:
        logging.error(f"Error processing script: {e}")
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script_processor.py <script_path>")
        sys.exit(1)
    script_path = sys.argv[1]
    key_points = process_script(script_path)
    print(key_points)
""",
        "prompt_generator.py": """\
import yaml
import requests
import logging

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def generate_prompts(key_points, config):
    prompts = []
    for point in key_points:
        try:
            response = requests.post(
                f"{config['ollama_api']}/generate",
                json={"prompt": f"Generate an image prompt for: {point}", "model": "your-llm-model"}
            )
            response.raise_for_status()
            prompt = response.json().get("generated_text", f"Image for: {point}")
            prompts.append(prompt)
            logging.info(f"Generated prompt: {prompt}")
        except Exception as e:
            logging.error(f"Failed to generate prompt for '{point}': {e}")
            prompts.append(f"Image for: {point}")
    return prompts

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python prompt_generator.py <config_path> <script_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    script_path = sys.argv[2]
    from script_processor import process_script
    key_points = process_script(script_path)
    config = load_config(config_path)
    prompts = generate_prompts(key_points, config)
    print(prompts)
""",
        "image_generator.py": """\
import yaml
import requests
import os
import logging

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def generate_image(prompt, config, output_path, model=None, lora=None, style=None):
    try:
        payload = {
            "prompt": prompt,
            "style": style or config.get('default_style', 'comics'),
            "model": model or config.get('sd_model', 'sdxl'),
            "lora": lora or config.get('lora_model', 'default_lora')
            # Add other necessary parameters
        }
        response = requests.post(
            f"{config['automatic1111_api']}/sdapi/v1/txt2img",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        # Assuming the API returns images as base64 or URLs
        # Modify based on actual API response
        image_data = data['images'][0]  # This might need adjustment
        # If image_data is a base64 string:
        import base64
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
    if len(sys.argv) != 5:
        print("Usage: python image_generator.py <config_path> <prompt> <output_path> <style>")
        sys.exit(1)
    config_path = sys.argv[1]
    prompt = sys.argv[2]
    output_path = sys.argv[3]
    style = sys.argv[4]
    config = load_config(config_path)
    success = generate_image(prompt, config, output_path, style=style)
    if success:
        print(f"Image saved to {output_path}")
    else:
        print("Image generation failed.")
""",
        "image_editor.py": """\
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
""",
        "video_assembler.py": """\
import yaml
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import logging

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def assemble_video(image_paths, audio_path, output_path, config):
    try:
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        num_images = len(image_paths)
        if num_images == 0:
            logging.error("No images provided for video assembly.")
            return None
        clip_duration = duration / num_images
        clips = []
        for img_path in image_paths:
            clip = ImageClip(img_path).set_duration(clip_duration)
            clips.append(clip)
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio)
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        logging.info(f"Video assembled and saved to {output_path}.")
        return output_path
    except Exception as e:
        logging.error(f"Error assembling video: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python video_assembler.py <config_path> <image_paths_file> <audio_path> <output_video_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    image_paths_file = sys.argv[2]
    audio_path = sys.argv[3]
    output_video_path = sys.argv[4]
    try:
        with open(image_paths_file, 'r') as f:
            image_paths = [line.strip() for line in f.readlines()]
        config = load_config(config_path)
        video = assemble_video(image_paths, audio_path, output_video_path, config)
        if video:
            print(f"Video saved to {video}")
        else:
            print("Video assembly failed.")
    except Exception as e:
        logging.error(f"Error reading image paths file: {e}")
        print("Failed to read image paths file.")
""",
        "main.py": """\
import os
import sys
import yaml
import subprocess
import logging

from scripts.script_processor import process_script
from scripts.prompt_generator import generate_prompts
from scripts.image_generator import generate_image
from scripts.image_editor import enhance_image
from scripts.video_assembler import assemble_video

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def main(script_path, audio_path, output_video_path="outputs/videos/output_video.mp4"):
    try:
        logging.info("Starting main process.")
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, "..", "config", "config.yaml")
        config = load_config(config_path)

        # Step 1: Process Script
        key_points = process_script(script_path)
        if not key_points:
            logging.error("No key points found in script. Exiting.")
            sys.exit(1)

        # Step 2: Generate Prompts
        prompts = generate_prompts(key_points, config)
        if not prompts:
            logging.error("No prompts generated. Exiting.")
            sys.exit(1)

        # Step 3: Generate Images
        image_dir = os.path.join(base_path, "..", "outputs", "images")
        os.makedirs(image_dir, exist_ok=True)
        image_paths = []
        for idx, prompt in enumerate(prompts):
            image_path = os.path.join(image_dir, f"image_{idx+1}.png")
            success = generate_image(prompt, config, image_path)
            if success:
                # Step 4: Enhance Image
                enhanced_path = os.path.join(image_dir, f"enhanced_image_{idx+1}.png")
                enhance_image(image_path, enhanced_path)
                image_paths.append(enhanced_path)

        if not image_paths:
            logging.error("No images generated successfully. Exiting.")
            sys.exit(1)

        # Save image paths to a file
        image_paths_file = os.path.join(image_dir, "image_paths.txt")
        try:
            with open(image_paths_file, 'w') as f:
                for path in image_paths:
                    f.write(f"{path}\n")
            logging.info(f"Image paths saved to {image_paths_file}.")
        except Exception as e:
            logging.error(f"Error saving image paths: {e}")
            sys.exit(1)

        # Step 5: Assemble Video
        video = assemble_video(image_paths, audio_path, output_video_path, config)
        if video:
            logging.info(f"Video created at {video}")
            print(f"Video created at {video}")
        else:
            logging.error("Video assembly failed.")
            print("Video assembly failed.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(
        filename=os.path.join("logs", "app.log"),
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    if len(sys.argv) != 3:
        print("Usage: python main.py <script_path> <audio_path>")
        sys.exit(1)
    script_path = sys.argv[1]
    audio_path = sys.argv[2]
    main(script_path, audio_path)
"""
    }

    try:
        scripts_dir = os.path.join(base_path, "scripts")
        for script_name, content in scripts.items():
            script_path = os.path.join(scripts_dir, script_name)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
        logging.info("Skeleton scripts created in the scripts/ directory.")
    except Exception as e:
        logging.error(f"Error creating skeleton scripts: {e}")
        sys.exit(1)

def main():
    base_path = os.path.abspath(PROJECT_NAME)
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            logging.info(f"Project root directory '{PROJECT_NAME}' created.")
        else:
            logging.info(f"Project root directory '{PROJECT_NAME}' already exists.")
    except Exception as e:
        logging.error(f"Error creating project root directory: {e}")
        sys.exit(1)

    # Create directories
    create_directories(base_path)

    # Create virtual environment
    venv_path = create_virtual_environment(base_path)

    # Install dependencies
    install_dependencies(venv_path)

    # Write config file
    write_config_file(base_path)

    # Create skeleton scripts
    create_skeleton_scripts(base_path)

    # Final instructions
    print("\nSetup Complete!")
    print(f"To activate the virtual environment, run:")
    print(f"    {os.path.join(base_path, 'venv', 'Scripts', 'activate.bat')}")
    print("\nTo run the tool, use the following command:")
    print(f"    python main.py <path_to_script> <path_to_audio>")
    logging.info("Setup completed successfully.")

if __name__ == "__main__":
    main()
