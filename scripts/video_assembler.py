# scripts/video_assembler.py

import yaml
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import logging
import os

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
