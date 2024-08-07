
import copy
import os
import random
import subprocess
import requests
import json
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip

API_SERVICE_URL = "0.0.0.0:1111"
max_chars, max_duration, max_gap = 24, 2.5, 1.5
rans = str(random.randint(5, 250)) 
FONTSIZE = 28
PRIMARYCOLOUR = '&H00FFFF00' # Example color
OUTLINECOLOUR = '&H00000000'  # Black outline color
SHADOW = 1  # Shadow size

def extract_audio(video_path):

    audio_path = os.path.join(os.path.dirname(video_path), rans + "audio.mp3")
    
    video = VideoFileClip(video_path)
    audio = video.audio
    try:    
        audio.write_audiofile(audio_path)
        print('Audio extracted')
        return audio_path
    except Exception as e:
        print(e)

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

"""def json_to_srt(audio, language):
    # Example API request setup, replace API_SERVICE_URL and parameters as necessary
    data = {"audio_url": audio, "sequence_length": [300, 10, 0.5], "language": language}
    res_timestamps = requests.post(f'http://{API_SERVICE_URL}/timestamp_generator/', json=data)
    wordlevel_info = json.loads(json.loads(res_timestamps.text)['wordlevel_info'])

    # Extract words and timing
    words = [entry['word'].strip() for entry in wordlevel_info]
    times = [(entry['start'], entry['end']) for entry in wordlevel_info]

    word = {
        "word" : #le mot,
        "start" : #le debut,
        "end": #le fin
    }

    words = # tableu constitué de words

    word_split = # [[word1,word,...,word5],[word6,word7, ...word10],....] 

    lines = []
    for line in word_split:
        for idx,w in enumerate(line):
            start_time = seconds_to_srt_time(times[i][0])
        end_time = seconds_to_srt_time(times[i][1])
            line_copy = copy.copy(line)
            line_copy[idx] = f"<b>{w}</b>" 
            lines.append(" ".join(line_copy))
    


    # Create the SRT content
    srt_content = ""
    chunk_size = 5  # Number of words to display at a time
    for i in range(len(words)):
        start_time = seconds_to_srt_time(times[i][0])
        end_time = seconds_to_srt_time(times[i][1])
        
        # Calculate the start and end index for the current chunk of words
        chunk_start = max(0, i - chunk_size + 1)
        chunk_end = min(len(words), i + 1)
        
        # Construct the current sentence with the current word highlighted
        current_sentence = " ".join(words[chunk_start:i]) + f" <b>{words[i]}</b> " + " ".join(words[i+1:chunk_end])
        current_sentence = current_sentence.strip()
        
        srt_content += f"{i + 1}\n{start_time} --> {end_time}\n{current_sentence}\n\n"

    # Save the SRT content to a file
    srt_file_path = rans + "subtitle.srt"
    try:
        with open(srt_file_path, "w") as file:
            file.write(srt_content)
        return srt_file_path
    except Exception as e:
        print(e)"""


def json_to_srt(audio, language):
    # Example API request setup, replace API_SERVICE_URL and parameters as necessary
    data = {"audio_url": audio, "sequence_length": [300, 10, 0.5], "language": language}
    res_timestamps = requests.post(f'http://{API_SERVICE_URL}/timestamp_generator/', json=data)
    wordlevel_info = json.loads(json.loads(res_timestamps.text)['wordlevel_info'])

    # Extract words and timing
    words = [entry['word'].strip() for entry in wordlevel_info]
    times = [(entry['start'], entry['end']) for entry in wordlevel_info]

    # Split words into chunks of 5
    chunk_size = 5
    word_split = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    time_split = [times[i:i + chunk_size] for i in range(0, len(times), chunk_size)]

    # Create the SRT content
    srt_content = ""
    line_index = 1
    for chunk_idx, line in enumerate(word_split):
        for word_idx, word in enumerate(line):
            start_time = seconds_to_srt_time(time_split[chunk_idx][word_idx][0])
            end_time = seconds_to_srt_time(time_split[chunk_idx][word_idx][1])
            
            # Create a copy of the line with the current word highlighted
            line_copy = copy.deepcopy(line)
            line_copy[word_idx] = f"<b>{word}</b>"
            lines = " ".join(line_copy)
            
            srt_content += f"{line_index}\n{start_time} --> {end_time}\n{lines}\n\n"
            line_index += 1

    # Save the SRT content to a file
    srt_file_path = rans + "subtitle.srt"
    try:
        with open(srt_file_path, "w") as file:
            file.write(srt_content)
        return srt_file_path
    except Exception as e:
        print(e)


def apply_subtitles(input_video, subtitle_file, output_video, font_path):
    output_video = rans + output_video
    # Define the ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f"subtitles={subtitle_file}:force_style='FontName=Montserrat,Fontfile={font_path},PrimaryColour={PRIMARYCOLOUR},Italic=1,FontSize={FONTSIZE},OutlineColour={OUTLINECOLOUR},Shadow={SHADOW}'",
        output_video
    ]
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print("Subtitles applied successfully.")
        print('Video: ' + str(output_video))
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")