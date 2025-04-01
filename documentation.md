# YouTube Shorts Automation Tool

![YouTube Shorts Automation Tool](https://via.placeholder.com/800x200?text=YouTube+Shorts+Automation+Tool)

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Directory Structure](#directory-structure)
4. [Configuration](#configuration)
5. [Scripts](#scripts)
    - [1. `script_processor.py`](#1-script_processorpy)
    - [2. `prompt_generator.py`](#2-prompt_generatorpy)
    - [3. `image_generator.py`](#3-image_generatorpy)
    - [4. `image_editor.py`](#4-image_editorpy)
    - [5. `video_assembler.py`](#5-video_assemblerpy)
6. [Main Orchestration](#main-orchestration)
7. [Usage](#usage)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Running the Tool](#running-the-tool)
8. [Logging](#logging)
9. [Troubleshooting](#troubleshooting)
10. [Future Enhancements](#future-enhancements)
11. [Contributing](#contributing)
12. [License](#license)
13. [Contact](#contact)

---

## Overview

The **YouTube Shorts Automation Tool** is designed to streamline the creation of engaging YouTube Shorts by automating the processes of script analysis, prompt generation, image creation, image enhancement, and video assembly. Leveraging powerful technologies like **Stable Diffusion** for image generation and **Mistral LLM** via **Ollama** for natural language processing, this tool transforms textual scripts and audio narrations into visually appealing short videos ready for upload.

---

## Features

- **Script Analysis:** Extracts key narrative points and characters from your script using advanced language models.
- **Prompt Generation:** Generates detailed image prompts tailored to each key point in the script.
- **Image Creation:** Utilizes Stable Diffusion to create high-quality images based on generated prompts.
- **Image Enhancement:** Enhances generated images for improved visual appeal using image processing techniques.
- **Video Assembly:** Compiles enhanced images into a cohesive video synchronized with your audio narration.
- **Interactive CLI:** Guides users through each step with an intuitive Command-Line Interface.
- **Model and LoRA Selection:** Allows selection from available Stable Diffusion models and LoRA extensions.
- **Logging:** Maintains detailed logs for monitoring and troubleshooting.

---

## Directory Structure

The project follows a structured directory layout to organize configurations, scripts, outputs, and logs efficiently.

```
youtube_short_creator/
├── config/
│   └── config.yaml
├── scripts/
│   ├── __init__.py
│   ├── script_processor.py
│   ├── prompt_generator.py
│   ├── image_generator.py
│   ├── image_editor.py
│   └── video_assembler.py
├── outputs/
│   ├── images/
│   └── videos/
├── logs/
│   └── app.log
├── requirements.txt
├── setup.py
└── main.py
```

### Detailed Breakdown

- **`config/`**
  - **`config.yaml`**: Centralized configuration file containing paths to external tools, default settings, and model directories.

- **`scripts/`**
  - **`__init__.py`**: Makes the `scripts` directory a Python package.
  - **`script_processor.py`**: Processes the input script to extract key points and characters.
  - **`prompt_generator.py`**: Generates detailed image prompts based on extracted key points.
  - **`image_generator.py`**: Creates images using Stable Diffusion based on generated prompts.
  - **`image_editor.py`**: Enhances generated images for better visual quality.
  - **`video_assembler.py`**: Assembles enhanced images into a final video synchronized with audio narration.

- **`outputs/`**
  - **`images/`**: Stores generated and enhanced images.
  - **`videos/`**: Stores the final assembled videos ready for upload.

- **`logs/`**
  - **`app.log`**: Contains detailed logs of the tool's operations for monitoring and troubleshooting.

- **`requirements.txt`**
  - Lists all Python dependencies required for the tool to function correctly.

- **`setup.py`**
  - Python script to initialize the project, create necessary directories, set up the virtual environment, and install dependencies.

- **`main.py`**
  - The main orchestration script that ties together all components, providing an interactive CLI for user input and managing the video creation workflow.

---

## Configuration

The **`config.yaml`** file centralizes all essential configurations, making it easier to manage paths and default settings.

```yaml
# config/config.yaml

ffmpeg_path: "D:\\FFmpeg\\ffmpeg-2024-03-20-git-e04c638f5f-full_build\\bin\\ffmpeg.exe"
automatic1111_api: "http://localhost:7860"
ollama_api: "http://localhost:11434"
default_style: "comics"
sd_model: "sdxl"  # Default Stable Diffusion model
lora_model: "default_lora"  # Default LoRA model
models_directory: "models"  # Directory containing Stable Diffusion models
loras_directory: "loras"    # Directory containing LoRA models
```

### Configuration Parameters

- **`ffmpeg_path`**: Absolute path to the FFmpeg executable on your system.
- **`automatic1111_api`**: URL where AUTOMATIC1111's Stable Diffusion WebUI API is accessible.
- **`ollama_api`**: URL where Ollama's API is accessible.
- **`default_style`**: Default artistic style for image generation (e.g., "comics", "illustration").
- **`sd_model`**: Default Stable Diffusion model to use.
- **`lora_model`**: Default LoRA model to apply.
- **`models_directory`**: Directory containing all Stable Diffusion model files (`.ckpt` or `.safetensors`).
- **`loras_directory`**: Directory containing all LoRA model files (`.ckpt` or `.safetensors`).

**Ensure that the specified directories (`models_directory` and `loras_directory`) contain the appropriate model files managed by AUTOMATIC1111's WebUI.**

---

## Scripts

Each script within the `scripts/` directory serves a specific purpose in the video creation workflow. Below is a detailed explanation of each script, including its location, functionality, and key components.

### 1. `script_processor.py`

**Location:** `youtube_short_creator/scripts/script_processor.py`

**Purpose:**  
Analyzes the input script to extract key narrative points and characters using the Mistral LLM via Ollama. This foundational step ensures that each segment of the script is accurately represented in the generated images.

**Key Functionalities:**

- **Load Configuration:** Reads `config.yaml` to access API endpoints and other settings.
- **Process Script:** Utilizes the Mistral LLM to analyze the script and identify key points and characters.
- **Output:** Returns lists of key points and characters extracted from the script.

**Code Highlights:**

```python
def process_script(script_path, config):
    # Reads the script and uses LLM to extract key points and characters
    ...
    return key_points, characters
```

**Usage Example:**

```bash
python scripts/script_processor.py config/config.yaml story/Aliens_are_taking_over_v1_transcript.txt
```

---

### 2. `prompt_generator.py`

**Location:** `youtube_short_creator/scripts/prompt_generator.py`

**Purpose:**  
Generates detailed image prompts based on the extracted key points from the script. These prompts guide the image generation process, ensuring that visuals align with the narrative.

**Key Functionalities:**

- **Load Configuration:** Accesses API endpoints and default settings from `config.yaml`.
- **Generate Prompts:** Uses the Mistral LLM to create descriptive prompts for each key point.
- **Output:** Writes the generated prompts to a specified file and prints them for user review.

**Code Highlights:**

```python
def generate_prompts(key_points, config):
    # Uses LLM to generate detailed prompts for each key point
    ...
    return prompts
```

**Usage Example:**

```bash
python scripts/prompt_generator.py config/config.yaml story/Aliens_are_taking_over_v1_transcript.txt prompts/generated_prompts.txt
```

---

### 3. `image_generator.py`

**Location:** `youtube_short_creator/scripts/image_generator.py`

**Purpose:**  
Creates high-quality images based on the generated prompts using AUTOMATIC1111's Stable Diffusion WebUI API. This script ensures that each image accurately reflects the corresponding narrative segment.

**Key Functionalities:**

- **Load Configuration:** Retrieves API endpoints and model settings from `config.yaml`.
- **List Available Models and LoRAs:** Scans designated directories to present available options for image generation.
- **Generate Image:** Sends prompts to the Stable Diffusion API to create images, applying selected models and LoRAs.
- **Output:** Saves the generated images to the specified output path.

**Code Highlights:**

```python
def generate_image(prompt, config, output_path, model=None, lora=None, style=None):
    # Sends a request to the Stable Diffusion API to generate an image based on the prompt
    ...
    return True
```

**Usage Example:**

```bash
python scripts/image_generator.py config/config.yaml "A heroic figure..." outputs/images/image_1.png sdxl.ckpt default_lora
```

---

### 4. `image_editor.py`

**Location:** `youtube_short_creator/scripts/image_editor.py`

**Purpose:**  
Enhances the generated images to improve visual quality and engagement. This step applies image processing techniques such as brightness and contrast adjustments.

**Key Functionalities:**

- **Enhance Image:** Uses the Pillow library to adjust brightness and contrast.
- **Output:** Saves the enhanced image to the specified output path.

**Code Highlights:**

```python
def enhance_image(image_path, output_path):
    # Enhances the image by adjusting brightness and contrast
    ...
    return output_path
```

**Usage Example:**

```bash
python scripts/image_editor.py outputs/images/image_1.png outputs/images/enhanced_image_1.png
```

---

### 5. `video_assembler.py`

**Location:** `youtube_short_creator/scripts/video_assembler.py`

**Purpose:**  
Assembles the enhanced images into a final video synchronized with the provided audio narration. This script ensures that the timing of image displays aligns with the duration of the audio.

**Key Functionalities:**

- **Load Configuration:** Accesses settings from `config.yaml`.
- **Assemble Video:** Utilizes MoviePy to concatenate image clips and synchronize them with the audio file.
- **Output:** Writes the final video file to the specified output path.

**Code Highlights:**

```python
def assemble_video(image_paths, audio_path, output_path, config):
    # Assembles images into a video synchronized with audio
    ...
    return output_path
```

**Usage Example:**

```bash
python scripts/video_assembler.py config/config.yaml outputs/images/image_paths.txt audio/narration.wav outputs/videos/output_video.mp4
```

---

## Main Orchestration

### `main.py`

**Location:** `youtube_short_creator/main.py`

**Purpose:**  
Serves as the central orchestrator of the entire workflow. It provides an interactive Command-Line Interface (CLI) that guides the user through each step, from script and audio input to video creation. This script integrates all components, ensuring a seamless and automated video generation process.

**Key Functionalities:**

1. **Interactive CLI:** Prompts the user for necessary inputs and selections.
2. **Script Processing:** Extracts key points and characters from the provided script.
3. **Prompt Generation:** Creates detailed image prompts based on key points.
4. **Model and LoRA Selection:** Allows the user to choose from available Stable Diffusion models and LoRAs.
5. **Image Generation and Enhancement:** Generates and enhances images based on prompts.
6. **Video Assembly:** Compiles the enhanced images into a synchronized video.
7. **Logging:** Records all operations and errors for monitoring and troubleshooting.

**Code Highlights:**

```python
def main():
    # Orchestrates the entire video creation workflow
    ...
    logging.info("Video created successfully at {video}")
    print(f"Video created successfully at {video}")
```

**Usage Example:**

```bash
python main.py
```

**Interactive Workflow:**

1. **Input Paths:** Enter the paths to your script file and audio narration file.
2. **View Extracted Data:** Review the key points and characters extracted from your script.
3. **Select Style:** Choose the artistic style for image generation (e.g., "comics", "illustration").
4. **Select Model and LoRA:** Pick from available Stable Diffusion models and LoRAs.
5. **Review Prompts:** Examine the generated image prompts and approve to proceed.
6. **Generate and Enhance Images:** The tool creates and enhances images based on your inputs.
7. **Assemble Video:** Compiles the images into a final video synchronized with the audio.
8. **Completion:** Notifies you of the video's location upon successful creation.

---

## Usage

### Prerequisites

Before using the tool, ensure the following are set up:

1. **Python Installation:**
   - **Version:** Python 3.8 or higher (Python 3.10.1 is recommended).
   - **Download:** [Python Official Website](https://www.python.org/downloads/)

2. **FFmpeg Installation:**
   - **Path:** Ensure FFmpeg is installed at the path specified in `config.yaml` (e.g., `D:\FFmpeg\ffmpeg-2024-03-20-git-e04c638f5f-full_build\bin\ffmpeg.exe`).
   - **Download:** [FFmpeg Official Website](https://ffmpeg.org/download.html)

3. **AUTOMATIC1111's Stable Diffusion WebUI:**
   - **Access:** Must be running and accessible via `http://localhost:7860`.
   - **Setup Guide:** [AUTOMATIC1111's Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

4. **Ollama Installation:**
   - **Access:** Must be running and accessible via `http://localhost:11434`.
   - **Installation Guide:** [Ollama Official Website](https://ollama.com/)

5. **Models and LoRAs:**
   - **Stable Diffusion Models:** Place your `.ckpt` or `.safetensors` files in the `models/` directory.
   - **LoRA Models:** Place your `.ckpt` or `.safetensors` files in the `loras/` directory.

### Setup

1. **Clone the Repository:**

   If you haven't already, clone or download the project to your local machine.

2. **Navigate to the Project Directory:**

   ```bash
   cd D:\Tools made by me\YouTubeShortsTool\youtube_short_creator
   ```

3. **Activate the Virtual Environment:**

   - **Command Prompt:**
     ```bash
     venv\Scripts\activate.bat
     ```
   - **PowerShell:**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
     *If you encounter an execution policy error in PowerShell, temporarily allow script execution:*
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     ```

4. **Install Dependencies:**

   If you haven't run `setup.py` or need to reinstall dependencies:

   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

### Running the Tool

1. **Prepare Your Script and Audio Files:**

   - **Script File:** Place your video script (e.g., `Aliens_are_taking_over_v1_transcript.txt`) in the `story/` directory.
   - **Audio File:** Ensure your audio narration file (e.g., `narration.wav`) is placed in the `audio/` directory.

2. **Execute the Main Script:**

   - **Interactive Mode:**
     ```bash
     python main.py
     ```
   - **With Command-Line Arguments:**
     ```bash
     python main.py story/Aliens_are_taking_over_v1_transcript.txt audio/narration.wav
     ```

3. **Follow the Interactive Prompts:**

   - **Enter Script and Audio Paths:** Provide the full paths to your script and audio files.
   - **Select Image Style:** Choose your desired artistic style.
   - **Select Stable Diffusion Model:** Pick from the list of available models.
   - **Select LoRA Model:** Choose from the list of available LoRAs or proceed without one.
   - **Review Generated Prompts:** Examine the prompts and approve to continue.
   - **Image Generation and Enhancement:** The tool will generate and enhance images based on prompts.
   - **Video Assembly:** Compiles the images into a synchronized video.
   - **Completion:** The final video is saved in the `outputs/videos/` directory.

---

## Logging

The tool maintains detailed logs to assist in monitoring operations and troubleshooting issues.

- **Setup Logs:**
  - **File:** `setup.log`
  - **Location:** Project root directory.
  - **Purpose:** Records the setup process, including directory creation, virtual environment setup, and dependency installation.

- **Application Logs:**
  - **File:** `logs/app.log`
  - **Location:** `youtube_short_creator/logs/`
  - **Purpose:** Captures detailed information about the tool's operations, including script processing, prompt generation, image creation, and video assembly. Any errors or warnings encountered during execution are also logged here.

**Reviewing Logs:**

- Open `app.log` using any text editor to view real-time operations and diagnose issues.
- Regularly monitor logs to ensure the tool is functioning as expected and to identify areas for improvement.

---

## Troubleshooting

### Common Issues and Solutions

1. **Script File Not Found:**
   - **Error Message:** `Script file not found: <path>`
   - **Solution:** Ensure you're providing the full path to the script file, including the filename and extension (e.g., `story/Aliens_are_taking_over_v1_transcript.txt`).

2. **Unsupported Audio Format:**
   - **Issue:** Audio file not processed correctly.
   - **Solution:** Convert your audio file to a supported format like `.wav` or `.mp3` using tools like [Audacity](https://www.audacityteam.org/) or [Online Audio Converter](https://online-audio-converter.com/).

3. **API Accessibility Issues:**
   - **Issue:** Unable to connect to AUTOMATIC1111's WebUI or Ollama.
   - **Solution:**
     - Verify that both services are running.
     - Check that the URLs in `config.yaml` are correct.
     - Ensure there are no firewall or network restrictions blocking access.

4. **Permission Denied Errors:**
   - **Issue:** Unable to create or modify files/directories.
   - **Solution:**
     - Run Command Prompt or PowerShell as Administrator.
     - Ensure you have the necessary permissions for the project directory.

5. **Missing Dependencies:**
   - **Issue:** Import errors or missing packages.
   - **Solution:**
     - Activate the virtual environment.
     - Run `pip install -r requirements.txt` to install all dependencies.

6. **LLM Command Failures:**
   - **Issue:** Errors when executing Ollama commands.
   - **Solution:**
     - Ensure Ollama is running and accessible at the specified API endpoint.
     - Verify that the model path in the command is correct.

### Reviewing Logs

Always check the `app.log` and `setup.log` files for detailed error messages and operational insights. These logs provide valuable information to diagnose and resolve issues effectively.

---

## Future Enhancements

To further improve the YouTube Shorts Automation Tool, consider implementing the following features:

1. **Advanced Synchronization:**
   - **Description:** Integrate speech-to-text capabilities to map specific audio segments to corresponding images, ensuring precise synchronization.
   - **Benefit:** Enhances viewer engagement by aligning visuals accurately with narration.

2. **Enhanced Script Analysis:**
   - **Description:** Utilize more sophisticated NLP techniques or libraries (e.g., **spaCy**, **NLTK**) to improve the extraction of key points and characters.
   - **Benefit:** Increases the accuracy and relevance of generated prompts and visuals.

3. **Dynamic Transitions and Effects:**
   - **Description:** Add smooth transitions (e.g., fade-ins, fade-outs) and visual effects between images during video assembly.
   - **Benefit:** Creates a more polished and professional-looking video.

4. **Text Overlays and Subtitles:**
   - **Description:** Incorporate text overlays or subtitles matching the narration for better accessibility and clarity.
   - **Benefit:** Enhances comprehension and engagement, especially for viewers watching without sound.

5. **Graphical User Interface (GUI):**
   - **Description:** Develop a GUI to provide a more user-friendly and intuitive interaction experience.
   - **Benefit:** Makes the tool accessible to users less comfortable with CLI interactions.

6. **Batch Processing:**
   - **Description:** Enable the tool to process multiple scripts and audio files in batches.
   - **Benefit:** Increases efficiency, especially for content creators producing numerous shorts.

7. **Template Integration:**
   - **Description:** Implement predefined video templates to maintain consistent formatting across videos.
   - **Benefit:** Ensures brand consistency and saves time on styling.

---

## Contributing

Contributions are welcome! If you'd like to enhance the tool or fix issues, please follow these guidelines:

1. **Fork the Repository:** Create a personal copy of the project.
2. **Create a Branch:** Develop your feature or fix in a separate branch.
3. **Commit Changes:** Provide clear and descriptive commit messages.
4. **Submit a Pull Request:** Share your changes for review and integration.

**Please ensure that all contributions maintain the existing coding standards and are thoroughly tested.**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions, suggestions, or support, please contact:

- **Name:** [Your Name]
- **Email:** [your.email@example.com]
- **GitHub:** [Your GitHub Profile](https://github.com/yourusername)

---

# Conclusion

This comprehensive documentation serves as a guide to understanding, setting up, and using the YouTube Shorts Automation Tool. By following the outlined structure and instructions, you can efficiently create engaging short videos from scripts and audio narrations. Continuous enhancements and adherence to best practices will further elevate the tool's capabilities, ensuring it remains a valuable asset in your content creation process.

**Happy Creating!** 🎬🚀

---

# Appendix

### A. Sample `requirements.txt`

```plaintext
requests
moviepy
Pillow
opencv-python
PyYAML
argparse
spacy
SpeechRecognition
pydub
```

### B. Sample `config.yaml`

```yaml
# config/config.yaml

ffmpeg_path: "D:\\FFmpeg\\ffmpeg-2024-03-20-git-e04c638f5f-full_build\\bin\\ffmpeg.exe"
automatic1111_api: "http://localhost:7860"
ollama_api: "http://localhost:11434"
default_style: "comics"
sd_model: "sdxl"  # Default Stable Diffusion model
lora_model: "default_lora"  # Default LoRA model
models_directory: "models"  # Directory containing Stable Diffusion models
loras_directory: "loras"    # Directory containing LoRA models
```

### C. Sample `setup.py` Overview

The `setup.py` script automates the initial setup process by creating necessary directories, setting up a virtual environment, and installing required dependencies. It ensures that the project is ready for use with minimal manual intervention.

**Key Steps:**

1. **Directory Creation:** Establishes the project structure.
2. **Virtual Environment Setup:** Isolates project dependencies.
3. **Dependency Installation:** Installs all required Python packages.
4. **Configuration File Creation:** Generates `config.yaml` with predefined settings.
5. **Skeleton Scripts Creation:** Generates placeholder scripts for each component.

**Running `setup.py`:**

```bash
python setup.py
```

**Post-Execution Instructions:**

- **Activate Virtual Environment:**
  ```bash
  venv\Scripts\activate.bat
  ```
- **Run the Tool:**
  ```bash
  python main.py <path_to_script> <path_to_audio>
  ```
