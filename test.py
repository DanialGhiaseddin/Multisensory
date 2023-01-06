from initialization import initialize_psychopy
from screeninfo import get_monitors
import serial
import yaml
import numpy as np


def main(config):
    initialize_psychopy(config)
    import psychopy.event
    import psychopy.visual
    import psychopy.monitors
    import psychopy.core
    import psychopy.info
    import psychopy.sound
    import psychtoolbox as ptb

    #
    delay_generator = psychopy.core.Clock()
    synchronizer = psychopy.core.Clock()
    # print(psychopy.monitors.getAllMonitors())
    audio_stim = psychopy.sound.Sound(cfg["audio"]["freq"], secs=cfg["audio"]["duration"])

    # make screen
    win = psychopy.visual.Window(fullscr=False, color=[0, 0, 0], size=cfg["screen"]["size"],checkTiming=True, waitBlanking=True)
    win.color = 'black'
    # print("Helloooow")
    # print(win.getMsPerFrame())
    # print(1/win.monitorFramePeriod)

    flash_stim = psychopy.visual.Rect(
        win=win,
        units="pix",
        width=cfg["screen"]["size"][0],
        height=cfg["screen"]["size"][1],
        fillColor=[1, 1, 1],
        lineColor=[-1, -1, 1]
    )

    now = ptb.GetSecs()
    ttt_last = 0


    # ISI.start(0.001)  # start a period of 0.5s
    t1 = ptb.GetSecs()
    # ISI.complete()  # finish the 0.5s, taking into account one 60Hz frame

    t2 = ptb.GetSecs()
    flash_stim.draw()
    win.flip()
    t3 = ptb.GetSecs()

    # print((t2-t1) * 1000)
    # print(t3-t2)

    temporal_var = 0

    mov = psychopy.visual.MovieStim(win, 'sample-mp4-file-small.mp4', flipVert=False)
    mov.autoDraw = True
    mov.play()
    win.flip()
    # print(mov.duration)
    # # give the original size of the movie in pixels:
    # print(mov.format.width, mov.format.height)
    #
    # for i in range(200):
    #
    #     # mov.draw()
    #     psychopy.core.wait(0.010)
    #     win.flip()
    #
    # exit()
    #
    # ISI = psychopy.core.StaticPeriod(screenHz=60)
    # for frame in range(240):
    #     temp = win.getFutureFlipTime()
    #     print(f"{frame}:", temp - temporal_var)
    #     temporal_var = temp
    #     ISI.start(2 / 60)
    #     if frame == 200:
    #         audio_stim.play()
    #     if 150 <= frame < 152:
    #         flash_stim.draw()
    #     win.flip()
    #     last = ptb.GetSecs()
    #     print(f"{frame}:", (last - now))
    #     now = last
    #     ISI.complete()
    #
    # #
    # exit()

    ser = serial.Serial(cfg["serial"]["port"], cfg["serial"]["baud_rate"], timeout=cfg["serial"]["timeout"])
    line = ser.readline().decode().strip()
    assert line == "Device is ready ..."

    ser.write('1'.encode())
    line = ser.readline().decode().strip()
    print(line)
    assert line == "Debug Mode"
    win.flip()
    psychopy.core.wait(2.0)

    for i in range(5):

        flash_stim.draw()
        win.flip()
        # psychopy.event.waitKeys()
        synchronizer.reset()
        synchronizer.add(0.040)
        while synchronizer.getTime() < 0:
            pass
        win.flip()

        line = ser.readline().decode().strip()
        print(line)
        if "optic Detected" in line:
            message = psychopy.visual.TextStim(
                win=win,
                units="pix",
                text=line
            )
        else:
            message = psychopy.visual.TextStim(
                win=win,
                units="pix",
                text="Error in Optic Sensor"
            )
        message.draw()
        win.flip()

        psychopy.core.wait(5.0)

    # for i in range(cfg["experiment"]["trials"]):
    #
    #     fixation.draw()
    #     win.flip()
    #
    #     psychopy.core.wait(cfg["experiment"]["fixation_time"])
    #
    #     command = 0.200
    #
    #     next_flip = win.getFutureFlipTime(clock='ptb')
    #     audio_stim.play(when=next_flip)
    #
    #     while ptb.GetSecs() < next_flip + command:
    #         pass
    #     flash_stim.draw()
    #     win.flip()
    #     # psychopy.event.waitKeys()
    #     synchronizer.reset()
    #     synchronizer.add(0.040)
    #     while synchronizer.getTime() < 0:
    #         pass
    #     win.flip()
    #
    #
    #     arduino_delay = 0#int(ser.readline().decode().strip().split(' ')[-1])
    #     delays[i] = arduino_delay
    #
    #     delay_generator.reset()
    #     delay_generator.add(0.5)
    #     while delay_generator.getTime() < 0:
    #         pass
    #
    #
    #     delay_generator.reset()
    #     delay_generator.add(3.0)
    #     while delay_generator.getTime() < 0:
    #         pass

    psychopy.event.waitKeys()



if __name__ == "__main__":

    with open("configs/config_base.yml", "r") as yml_file:
        cfg = yaml.safe_load(yml_file)

    if cfg["screen"]["size"] == "full-screen":
        cfg["screen"]["size"] = [get_monitors()[0].width, get_monitors()[0].width]

    main(cfg)
