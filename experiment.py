from initialization import initialize_psychopy
from screeninfo import get_monitors
import yaml
import numpy as np
import math
import os
import sys
import random
from nBack.utils import create_trial_list
from SerialPortManger import SerialPortManager


def experiment(cfg, id_number):
    # initialize_psychopy(config)
    import psychopy.event
    import psychopy.visual
    import psychopy.core
    import psychopy.sound
    import psychtoolbox as ptb
    import psychopy.data

    from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                    STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

    def present_multisensory(delay):

        frame_count = int((math.fabs(delay) // 16.6) + 10)
        video_frame = -1
        audio_frame = -1
        audio_delay = -1
        if delay < 0:
            delay *= -1
            audio_frame = 5
            video_frame = int((delay // 16.6) + 1 + audio_frame)
            audio_delay = (video_frame - audio_frame) * 16.6 - delay
        elif delay >= 0:
            video_frame = 5
            audio_frame = int((delay // 16.6) + video_frame)
            audio_delay = delay - ((audio_frame - video_frame) * 16.6)

        print(video_frame)
        print(audio_frame)
        print(audio_delay)

        static_timer = psychopy.core.StaticPeriod(screenHz=60)

        setup_clock = psychopy.core.Clock()
        time_to_first_frame = win.getFutureFlipTime(clock="now")
        setup_clock.reset(-time_to_first_frame)  # t0 is time of first possible flip

        now = ptb.GetSecs()
        for frame in range(frame_count):
            static_timer.start(2 / 60)
            time_to_first_frame = win.getFutureFlipTime(clock=setup_clock)
            # this_time = ptb.GetSecs()
            if frame == audio_frame:
                audio_stim.play(when=time_to_first_frame + (audio_delay / 1000))
            if video_frame <= frame <= video_frame + 2:
                flash_stim.draw()
                flash_stim.tStartRefresh = time_to_first_frame  # on global time
                win.timeOnFlip(flash_stim, 'tStartRefresh')
            win.flip()
            last = ptb.GetSecs()
            print(f"{frame}:", (last - now))
            now = last
            static_timer.complete()

    #

    def present_multisensory_v(delay, frame_tolerance=0.001):

        # ------Prepare to start Routine "video"-------
        video_clock = psychopy.core.Clock()
        continue_routine = True
        # update component parameters for each repeat
        movie = psychopy.visual.MovieStim3(
            win=win, name='movie',
            noAudio=False,
            filename=f'./stimulus/stimulus_{delay}ms.mp4',
            ori=0.0, pos=(0, 0), opacity=None,
            loop=False,
            depth=0.0,
        )

        # keep track of which components have finished
        video_components = [movie]
        for thisComponent in video_components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        video_clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frame_n = -1
        win.flip()
        # -------Run Routine "video"-------
        while continue_routine:
            # get current time
            t = video_clock.getTime()
            t_this_flip = win.getFutureFlipTime(clock=video_clock)
            t_this_flip_global = win.getFutureFlipTime(clock=None)
            frame_n = frame_n + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *movie* updates
            if movie.status == NOT_STARTED and t_this_flip >= 0.0 - frame_tolerance:
                # keep track of start time/frame for later
                movie.frameNStart = frame_n  # exact frame index
                movie.tStart = t  # local t and not account for scr refresh
                movie.tStartRefresh = t_this_flip_global  # on global time
                win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
                movie.setAutoDraw(True)

            # check for quit (typically the Esc key)
            # if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            #     core.quit()

            # check if all components have finished
            if not continue_routine:  # a component has requested a forced-end of Routine
                break
            continue_routine = False  # will revert to True if at least one component still running
            for thisComponent in video_components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continue_routine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continue_routine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "video"-------
        for thisComponent in video_components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        movie.stop()

    # make screen
    # win = psychopy.visual.Window(fullscr=True, color=[0, 0, 0], size=cfg["screen"]["size"])

    exp_name = cfg["experiment"]["name"]
    exp_info = {'participant': id_number, 'id': id_number, 'date': psychopy.data.getDateStr(), 'exp_name': exp_name}

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = '.' + os.sep + u'results/%s/%s_%s' % (exp_name, exp_info['id'], exp_info['date'])

    # An ExperimentHandler isn't essential but helps with data saving
    print(filename)
    if os.path.exists(filename):
        sys.exit("Data path " + filename + " already exists!")
    this_exp = psychopy.data.ExperimentHandler(name=exp_name, version='',
                                               extraInfo=None, runtimeInfo=None,
                                               originPath='./result_analyzer.py',
                                               savePickle=False, saveWideText=True,
                                               dataFileName=filename)

    # add some data for this trial
    # end of trial - move to next line in data output

    win = psychopy.visual.Window(
        size=[1280, 720], fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')

    win.color = 'black'

    # Welcome
    img = psychopy.visual.ImageStim(
        win=win,
        image="Images/Welcome.jpg",
        units="pix"
    )
    img.draw()
    win.flip()

    # pressed_keys = psychopy.event.waitKeys()
    # print(pressed_keys)
    # exit()

    pressed_keys = psychopy.event.waitKeys(keyList=["space"])
    win.flip()
    # Stimulus:
    fixation = psychopy.visual.ImageStim(
        win=win,
        image="Images/fixation.png",
        units="pix"
    )

    flash_stim = psychopy.visual.Rect(
        win=win,
        units="pix",
        width=cfg["screen"]["size"][0],
        height=cfg["screen"]["size"][1],
        fillColor=[1, 1, 1],
        lineColor=[-1, -1, 1]
    )

    response_instruction = psychopy.visual.ImageStim(
        win=win,
        image="Images/Instruction.jpg",
        units="pix"
    )

    audio_stim = psychopy.sound.Sound(cfg["audio"]["freq"], secs=cfg["audio"]["duration"])

    if cfg["experiment"]["arduino_enable"]:
        # ser = serial.Serial(cfg["serial"]["port"], cfg["serial"]["baud_rate"], timeout=cfg["serial"]["timeout"])
        # line = ser.readline().decode().strip()
        # assert line == "Device is ready ..."
        # ser.write('0'.encode())
        # line = ser.readline().decode().strip()
        # print(line)
        # assert line == "Operational Mode"
        ser = SerialPortManager(cfg["serial"]["port"], cfg["serial"]["baud_rate"], timeout=cfg["serial"]["timeout"])

    # delays = np.zeros(cfg["experiment"]["trials"])
    delay_generator = psychopy.core.Clock()
    initial_roa = cfg['experiment']['roa_list']
    roa_range = initial_roa * cfg["experiment"]["trials"]
    random.shuffle(roa_range)

    if cfg["experiment"]["nback"]["enable"]:
        nback_trials = create_trial_list(nback_level=1, total_count=len(roa_range), trials_per_block=21,
                                         targets_per_block=6)
        stim_back = psychopy.visual.ImageStim(
            win=win,
            image="Images/stim_back.jpg",
            units="pix"
        )
        nback_images = []
        for stim_number in range(10):
            temp = psychopy.visual.ImageStim(
                win=win,
                image=f"Images/stim_{stim_number+1}.jpeg",
                units="pix"
            )
            nback_images.append(temp)

    # roa_range = [+50, +50, +50, +50, +50, +50, +50, +50, +50, +50] * cfg["experiment"]["trials"]
    delays = np.zeros(len(roa_range))
    real_delays = np.zeros(len(roa_range))
    valid_keys = cfg["experiment"]["multi-sensory"]["feedback_keys"]
    for block in range(len(roa_range)):

        # Draw nback if is enable

        if cfg["experiment"]["nback"]["enable"]:

            isi_time = 2

            stim_back.draw()
            nback_images[int(nback_trials[0, block])].draw()
            win.flip()

            delay_generator.reset()
            delay_generator.add(isi_time)
            pressed_keys = psychopy.event.waitKeys(keyList=["space"], maxWait=isi_time)
            win.flip()
            response_time = delay_generator.getTime() + isi_time

            if pressed_keys is not None:
                this_exp.addData('nback.key', 1)
            else:
                this_exp.addData('nback.key', 0)

            this_exp.addData('nback.real', nback_trials[1, block])

            psychopy.core.wait(isi_time - response_time)

        fixation.draw()
        win.flip()

        psychopy.core.wait(cfg["experiment"]["fixation_time"])

        if cfg["experiment"]['multi-sensory']['enable']:

            present_multisensory_v(roa_range[block])
            # present_multisensory(roa_range[i])

            if cfg["experiment"]["arduino_enable"]:
                arduino_delay = ser.read_delay()
                if arduino_delay is None:
                    arduino_delay = "Invalid"
                    ser.restart()
                    psychopy.core.wait(1)
            else:
                arduino_delay = -1

            this_exp.addData('trial', block // len(initial_roa))
            this_exp.addData('delay.command', roa_range[block])
            this_exp.addData('delay.measured', arduino_delay)

            # Get Response
            isi_time = cfg["experiment"]["isi_time"]

            if cfg["experiment"]['multi-sensory']['instruction']:
                response_instruction.draw()
                win.flip()
            delay_generator.reset()
            delay_generator.add(isi_time)
            pressed_keys = psychopy.event.waitKeys(keyList=valid_keys, maxWait=isi_time)
            win.flip()
            response_time = delay_generator.getTime() + isi_time

            if pressed_keys is not None:
                this_exp.addData('response.key', pressed_keys)
                this_exp.addData('response.time', response_time)
            else:
                this_exp.addData('response.key', "None")
                this_exp.addData('response.time', -1)

            this_exp.nextEntry()
            psychopy.core.wait(isi_time - response_time)

    # psychopy.event.waitKeys()

    return filename


if __name__ == "__main__":

    import psychopy.gui

    gui = psychopy.gui.Dlg()
    gui.addField("Subject ID:")

    gui.show()

    assert gui.data[0] != ""

    with open("configs/config_calibration.yml", "r") as yml_file:
        config_file = yaml.safe_load(yml_file)

    if config_file["screen"]["size"] == "full-screen":
        config_file["screen"]["size"] = [get_monitors()[0].width, get_monitors()[0].width]

    experiment(config_file, gui.data[0])
