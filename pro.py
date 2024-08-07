import os
import json

from engine import apply_subtitles, extract_audio, json_to_ass, json_to_srt


def go(video_path, language, choice):
    if video_path:
        audio_path = extract_audio(video_path)
        if choice > 5:
            srt_file_path = json_to_ass(audio=audio_path, language=language, choice=choice)
        else:        
            srt_file_path = json_to_srt(audio=audio_path, language=language, choice=choice)
        if srt_file_path and audio_path:
            apply_subtitles(video_path, srt_file_path, choice, 'output_force_style.mp4', '/usr/share/fonts/truetype/Montserrat/Montserrat-ExtraBold.ttf')

            print('ok ')
    else:
        return 'lol'




go(video_path="/mnt/extra-storage/Videos/vs.mp4", language='en', choice=15)
