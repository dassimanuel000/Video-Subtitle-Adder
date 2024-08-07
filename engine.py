
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
FONTSIZE = 18
PRIMARYCOLOUR = '&HFFFFFF'
OUTLINECOLOUR = '&H000000'
SHADOW = 1
FONTWEIGHT = 600 
MARGINV = 40 
COLOR_TEXT = 'yellow'
FONTNAME = 'Montserrat'
SECONDARYCOLOUR = '&HFF000000'
BACKCOLOUR = '&H000000FF'
BACKGROUND_COLOR = '&HFF0000'
BORDER_COLOR = '&H000000'



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

def seconds_to_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    centiseconds = int((seconds % 1) * 100)
    return f"{hours:01}:{minutes:02}:{int(seconds):02}.{centiseconds:02}"

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

def set_text_same_size(text):
    global COLOR_TEXT
    COLOR_TEXT = 'white'
    line_ = f"<font color={COLOR_TEXT}>{text}</font>"
    return line_

def set_text_with_word_bigger(text):
    line_ = f"<font color={COLOR_TEXT} size={FONTSIZE+2}>{text}</font>"
    return line_

def set_text_with_bold_word(text):
    line_ = f"<b><font color={COLOR_TEXT}>{text}</font></b>"
    return line_

def set_text_with_rect__word(text):
    line_ = f"<b><font color={COLOR_TEXT}>{text}</font></b>"
    return line_

def set_text_with_background_word_contour_on_text(text, background_color=BACKGROUND_COLOR, border_color=BORDER_COLOR):
    return f"{{\\3c{background_color}\\4c{border_color}\\bord2\\shad0\\xbord3\\ybord3}}{text}{{\\r}}"

"""def set_text_with_background_word(text, background_color=BACKGROUND_COLOR, border_color='&H000000'):
    #return f"{{\\3c{background_color}\\bord1\\xbord9}}{text}{{\\r}}"
    return f"{{\\alpha&H80&}}{text}{{\\r}}"""


def set_text_with_background_word(text, background_color='&H0000FF'):
    return f"{{\\p1\\c&H000000&\\bord0\\shad0}}m 0 0 l 200 0 l 200 50 l 0 50 l 0 0 {{\\p0}}{text}{{\\r}}"

def set_text_with_animation(text, background_color='&H0000FF'):
    return f"{{\\3c{background_color}\\bord0\\shad0}}{text}{{\\r}}"


def json_to_srt(audio, language, choice):
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
            #line_copy[word_idx] = f"<b><font color=yellow>{word}</font></b>"
            if choice == 1:
                line_copy[word_idx] = set_text_same_size(word)
            if choice == 2:
                line_copy[word_idx] = set_text_with_word_bigger(word)
            if choice == 3:
                line_copy[word_idx] = set_text_with_bold_word(word)
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


def json_to_ass(audio, language, choice):
    data = {"audio_url": audio, "sequence_length": [300, 10, 0.5], "language": language}
    res_timestamps = requests.post(f'http://{API_SERVICE_URL}/timestamp_generator/', json=data)
    wordlevel_info = json.loads(json.loads(res_timestamps.text)['wordlevel_info'])

    words = [entry['word'].strip() for entry in wordlevel_info]
    times = [(entry['start'], entry['end']) for entry in wordlevel_info]

    chunk_size = 5
    word_split = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    time_split = [times[i:i + chunk_size] for i in range(0, len(times), chunk_size)]

    ass_content = "[Script Info]\nScriptType: v4.00+\n\n[V4+ Styles]\n"
    #ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    #ass_content += f"Style: Default,{FONTNAME},{FONTSIZE},{PRIMARYCOLOUR},{SECONDARYCOLOUR},{OUTLINECOLOUR},{BACKCOLOUR},-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += f"Style: Default,{FONTNAME},{FONTSIZE},{PRIMARYCOLOUR},{SECONDARYCOLOUR},{OUTLINECOLOUR},{BACKCOLOUR},-1,0,0,0,100,100,0,0,1,0,0,2,10,10,10,1\n\n"
    ass_content += "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    line_index = 1
    for chunk_idx, line in enumerate(word_split):
        for word_idx, word in enumerate(line):
            start_time = seconds_to_ass_time(time_split[chunk_idx][word_idx][0])
            end_time = seconds_to_ass_time(time_split[chunk_idx][word_idx][1])

            line_copy = copy.deepcopy(line)
            if choice == 15:
                line_copy[word_idx] = set_text_with_animation(word)
            else:
                line_copy[word_idx] = set_text_with_background_word(word)
            lines = " ".join(line_copy)

            ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{lines}\n"
            line_index += 1

    ass_file_path = rans + "subtitle.ass"
    try:
        with open(ass_file_path, "w") as file:
            file.write(ass_content)
        return ass_file_path
    except Exception as e:
        print(e)

def apply_subtitles(input_video, subtitle_file, choice, output_video, font_path):
    global FONTSIZE, OUTLINECOLOUR
    output_video = rans + output_video

    if choice == 3:
        italic = ',Italic=1'
        bolder = ''
        shadow = f',OutlineColour={OUTLINECOLOUR},Shadow={SHADOW}'
    elif choice == 1:
        italic = ',Italic=0'
        bolder = f',Bold={FONTWEIGHT}'
        FONTSIZE = FONTSIZE + 4
        OUTLINECOLOUR = '&HFF000000'
        shadow = f',OutlineColour={OUTLINECOLOUR}'
    elif choice == 4:
        italic = ',Italic=0'
        bolder = f',Bold={FONTWEIGHT}'
        shadow = f',OutlineColour={OUTLINECOLOUR},Shadow={SHADOW}'
    else:
        italic = ',Italic=1'
        bolder = f',Bold={FONTWEIGHT}'
        shadow = f',OutlineColour={OUTLINECOLOUR},Shadow={SHADOW}'

    if choice == 4:
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-vf', f"subtitles={subtitle_file}",
            output_video
        ]
    else:
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-vf', f"subtitles={subtitle_file}:force_style='FontName=Montserrat,Fontfile={font_path},PrimaryColour={PRIMARYCOLOUR}{italic},FontSize={FONTSIZE}{bolder}{shadow},Alignment=2,MarginV={MARGINV}'",
            output_video
        ]

    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print("Subtitles applied successfully.")
        print('Video: ' + str(output_video))
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")