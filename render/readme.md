
---

# Video Subtitle Adder

This project allows you to add subtitles to any MP4 video using FFmpeg, OpenAI Whisper, and subtitle files in ASS and SRT formats.

## Requirements

- Python 3.x
- FFmpeg
- OpenAI Whisper
- Font file: `Montserrat-ExtraBold.ttf` (or any other desired font)

## Installation

1. Install FFmpeg:
    ```bash
    sudo apt-get install ffmpeg
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the necessary font file located at `/usr/share/fonts/truetype/Montserrat/Montserrat-ExtraBold.ttf`. If you are using a different font, update the path accordingly in the `pro.py` script.

## Usage

### Main Script: `pro.py`

The `pro.py` script is the primary script to use for adding subtitles to your videos.

#### Functionality

1. Extracts audio from the video.
2. Converts the audio to a subtitle file (SRT or ASS format).
3. Applies the subtitle file to the video and saves the output.

### Running the Script

To run the script, provide the path to your video, the language, and the choice for subtitle format and style.

```python
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

go(video_path="/path/to/your/video.mp4", language='en', choice=15)
```

### Output Files

The script will generate output files with the naming convention `output_force_style.mp4`. Here are some of the output files from different runs:

#### Video Outputs

- **Video 1**:
    <video width="320" height="240" controls>
      <source src="130output_force_style.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>

- **Video 2**:
    <video width="320" height="240" controls>
      <source src="38output_force_style.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>

- **Video 3**:
    <video width="320" height="240" controls>
      <source src="15output_force_style.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>

- **Video 4**:
    <video width="320" height="240" controls>
      <source src="47output_force_style.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>

## Notes

- Ensure the paths in the script are correctly set to your local environment.
- You can adjust the subtitle style by modifying the `choice` parameter.
