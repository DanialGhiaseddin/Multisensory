import numpy as np
from scipy.io import wavfile
import numpy as np
import cv2
import moviepy.editor as mpe
from pathlib import Path
import math


def create_stimulus(name, audio_delay, size=None, duration=3.000, audio_duration=0.040,
                    flash_frames_count=2,
                    frame_pers_sec=60, audio_sample_rate=44100, audio_frequency=440):
    Path("./temp_files").mkdir(parents=True, exist_ok=True)

    # Create audio file
    flash_onset = duration / 2
    audio_onset = flash_onset + audio_delay
    audio_end = audio_onset + audio_duration
    start_index = int((audio_onset/duration) * (audio_sample_rate*duration))
    end_index = int((audio_end/duration) * (audio_sample_rate*duration))

    t = np.linspace(0, duration, int(audio_sample_rate * duration))
    y = np.sin(audio_frequency * 2 * np.pi * t)

    signal = np.zeros_like(y)

    signal[start_index:end_index] = y[start_index:end_index]

    wavfile.write('./temp_files/temp_audio.wav', audio_sample_rate, signal)

    # Create temp video file
    fixation = cv2.imread('../Images/fixation.png')
    fixation = np.max(fixation, axis=2)
    flash_frame = flash_onset / (1 / frame_pers_sec)
    flash_frame = round(flash_frame)
    out = cv2.VideoWriter('./temp_files/temp_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_pers_sec, (size[1], size[0]), False)
    for frame in range(int(frame_pers_sec * duration)):
        black = np.zeros(size, dtype='uint8')
        white = np.ones(size, dtype='uint8') * 255
        # data = np.random.randint(0, 256, size, dtype='uint8')
        if frame < flash_frame:
            out.write(fixation)
        elif flash_frame <= frame <= flash_frame + flash_frames_count:
            out.write(white)
        else:
            out.write(black)
    out.release()

    # Merge Audio and Video

    my_clip = mpe.VideoFileClip('./temp_files/temp_video.mp4')
    # for index, t in enumerate(my_clip.iter_frames()):
    #     print(index, t.mean())
    audio_background = mpe.AudioFileClip('./temp_files/temp_audio.wav')
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(name, fps=frame_pers_sec)


if __name__ == "__main__":
    delays = [-300, -200, -100, -50, -20, -10, 0, 10, 20, 50, 100, 200, 300]
    offset = 50
    for delay in delays:
        create_stimulus(f"stimulus_{delay}ms.mp4", audio_delay=(delay+offset)/1000, size=[1080, 1920])

