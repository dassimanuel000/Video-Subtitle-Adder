import random
import whisper
import os
import shutil
import cv2
import numpy as np  # Import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
from tqdm import tqdm
from PIL import ImageFont, ImageDraw, Image

FONT_PATH = "fonts/Roboto-Regular.ttf"  # Path to your custom font
FONT_SIZE = 42  # Adjustable font size
FONT_COLOR = (255, 255, 255, 255)  # White color in RGBA
SHADOW_COLOR = (0, 0, 0, 255)  # Black color for shadow in RGBA
BACKGROUND_COLOR = (33, 69, 168, 255)  # Background color in RGBA

FONT_SCALE = 0.8
FONT_THICKNESS = 2

def textsizef(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def process_video(video_path, model_path="base", output_video_path="output.mp4"):
    def extract_audio(video_path, audio_path):
        print('Extracting audio')
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print('Audio extracted')

    def transcribe_audio(model, audio_path):
        print('Transcribing audio')
        return model.transcribe(audio_path)

    def extract_frames(video_path, text_array, output_folder, fps):
        print('Extracting frames')
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        N_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            for i in text_array:
                if N_frames >= i[1] and N_frames <= i[2]:
                    text = i[0]
                    img_pil = Image.fromarray(frame)
                    draw = ImageDraw.Draw(img_pil)
                    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

                    # Calculate text size
                    text_width, text_height = textsizef(text, font=font)
                    text_x = int((width - text_width) / 2)
                    text_y = int(height - text_height) // 2

                    # Draw background rectangle
                    margin = 10
                    draw.rectangle(
                        [(text_x - margin, text_y - margin), (text_x + text_width + margin, text_y + text_height + margin)],
                        fill=BACKGROUND_COLOR
                    )

                    # Draw shadow
                    shadow_offset = 2
                    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=SHADOW_COLOR)

                    # Draw text
                    draw.text((text_x, text_y), text, font=font, fill=FONT_COLOR)

                    frame = np.array(img_pil)  # Ensure numpy is imported
                    break

            cv2.imwrite(os.path.join(output_folder, str(N_frames) + ".jpg"), frame)
            N_frames += 1

        cap.release()
        print('Frames extracted')

    def create_video_with_subtitles(image_folder, audio_path, fps, output_video_path):
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split(".")[0]))

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        clip = ImageSequenceClip([os.path.join(image_folder, image) for image in images], fps=fps)
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)
        clip.write_videofile(output_video_path)
        shutil.rmtree(image_folder)
        os.remove(audio_path)

    model = whisper.load_model(model_path)
    audio_path = os.path.join(os.path.dirname(video_path), "audio.mp3")
    extract_audio(video_path, audio_path)

    result = transcribe_audio(model, audio_path)
    text = result["segments"][0]["text"]
    textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)[0]
    char_width = int(textsize[0] / len(text))

    text_array = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    asp = 16 / 9
    ret, frame = cap.read()
    width = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)].shape[1]
    width = width - (width * 0.1)

    for j in tqdm(result["segments"]):
        lines = []
        text = j["text"]
        end = j["end"]
        start = j["start"]
        total_frames = int((end - start) * fps)
        start = start * fps
        total_chars = len(text)
        words = text.split(" ")
        i = 0

        while i < len(words):
            words[i] = words[i].strip()
            if words[i] == "":
                i += 1
                continue
            length_in_pixels = (len(words[i]) + 1) * char_width
            remaining_pixels = width - length_in_pixels
            line = words[i]

            while remaining_pixels > 0:
                i += 1
                if i >= len(words):
                    break
                length_in_pixels = (len(words[i]) + 1) * char_width
                remaining_pixels -= length_in_pixels
                if remaining_pixels < 0:
                    continue
                else:
                    line += " " + words[i]

            line_array = [line, int(start) + 15, int(len(line) / total_chars * total_frames) + int(start) + 15]
            start = int(len(line) / total_chars * total_frames) + int(start)
            lines.append(line_array)
            text_array.append(line_array)

    cap.release()

    image_folder = os.path.join(os.path.dirname(video_path), "frames")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    extract_frames(video_path, text_array, image_folder, fps)
    create_video_with_subtitles(image_folder, audio_path, fps, output_video_path)

    print(f"Video created at {output_video_path}")

# Example usage
process_video(video_path="/home/tony/Pictures/result3.mp4", output_video_path=str(random.randint(5, 250)) + ".mp4")
