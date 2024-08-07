import os
import json

from engine import apply_subtitles, extract_audio, json_to_srt


def go(video_path, language):
    if video_path:
        audio_path = extract_audio(video_path)
        srt_file_path = json_to_srt(audio=audio_path, language=language)
        if srt_file_path and audio_path:
            apply_subtitles(video_path, srt_file_path, 'output_force_style.mp4', '/usr/share/fonts/truetype/Montserrat/Montserrat-ExtraBold.ttf')

            print('ok ')
    else:
        return 'lol'




go(video_path="/home/tony/Pictures/result3.mp4", language='en')
