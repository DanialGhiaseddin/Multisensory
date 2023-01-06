#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on December 20, 2021, at 09:18
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import serial
from psychopy.hardware import keyboard

# Ensure that relative paths start from the same directory as this script

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'tone-selection'  # from the Builder filename that created this script
expInfo = {'participant': 'Danial', 'session': '001', 'date': data.getDateStr(), 'expName': expName,
           'psychopyVersion': psychopyVersion}

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = '.' + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
print(filename)
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath='./video.py',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Set up the Window
win = visual.Window(
    size=[1280, 720], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
print(expInfo['frameRate'])
print(frameDur)
# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

#
# Initialize components for Routine "setup"
setupClock = core.Clock()
tones = ['700', '750', '800', '850', '900', '925', '950', '975', '1000', '1025', '1050', '1075', '1100', '1150', '1200',
         '1250', '1300']
maxChoice = len(tones) - 1
soundDir = 'wav-files/'
text_instruct = visual.TextStim(win=win, name='text_instruct',
                                text='Listen to the video\n\nAfter the video you will hear a tone. '
                                     '\n\nPress the up arrow to increase the frequescy of the tone'
                                     '\nPress the down arrow to decrease the frequency of the tone.'
                                     '\n\nPress the enter key when you think you have matched the original sound.'
                                     '\n\nPress the enter key to start.',
                                font='Arial',
                                pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
                                color='white', colorSpace='rgb', opacity=None,
                                languageStyle='LTR',
                                depth=-1.0)

#
# Initialize components for Routine "video"
videoClock = core.Clock()

# Initialize components for Routine "tones"
tonesClock = core.Clock()
sound_1 = sound.Sound('A', secs=-1, stereo=True, hamming=True,
                      name='sound_1')
sound_1.setVolume(1.0)

text_freq = visual.TextStim(win=win, name='text_freq',
                            text='',
                            font='Arial',
                            pos=(.4, .4), height=0.05, wrapWidth=None, ori=0.0,
                            color='white', colorSpace='rgb', opacity=None,
                            languageStyle='LTR',
                            depth=-3.0)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
text_feedback = visual.TextStim(win=win, name='text_feedback',
                                text='',
                                font='Open Sans',
                                pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                color='white', colorSpace='rgb', opacity=None,
                                languageStyle='LTR',
                                depth=0.0)

# Initialize components for Routine "end"
endClock = core.Clock()
text = visual.TextStim(win=win, name='text',
                       text='Fin',
                       font='Open Sans',
                       pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                       color='white', colorSpace='rgb', opacity=None,
                       languageStyle='LTR',
                       depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# ------Prepare to start Routine "setup"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
setupComponents = [text_instruct]
for thisComponent in setupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
setupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "setup"-------
while continueRoutine:
    # get current time
    t = setupClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=setupClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *text_instruct* updates
    if text_instruct.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        text_instruct.frameNStart = frameN  # exact frame index
        text_instruct.tStart = t  # local t and not account for scr refresh
        text_instruct.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_instruct, 'tStartRefresh')  # time at next scr refresh
        text_instruct.setAutoDraw(True)

    # # *key_resp_2* updates
    # waitOnFlip = False
    # if tThisFlip >= 0.0 - frameTolerance:
    #     # keep track of start time/frame for later
    #     key_resp_2.frameNStart = frameN  # exact frame index
    #     key_resp_2.tStart = t  # local t and not account for scr refresh
    #     key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
    #     win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
    #     key_resp_2.status = STARTED
    #     # keyboard checking is just starting
    #     waitOnFlip = True
    #     win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
    #     win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    # if key_resp_2.status == STARTED and not waitOnFlip:
    #     theseKeys = key_resp_2.getKeys(keyList=['return'], waitRelease=False)
    #     _key_resp_2_allKeys.extend(theseKeys)
    #     if len(_key_resp_2_allKeys):
    #         key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
    #         key_resp_2.rt = _key_resp_2_allKeys[-1].rt
    #         # a response ends the routine
    #         continueRoutine = False

    # # check for quit (typically the Esc key)
    # if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
    #     core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

    core.wait(0.5)
    text_instruct.status = FINISHED

# -------Ending Routine "setup"-------
for thisComponent in setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_instruct.started', text_instruct.tStartRefresh)
thisExp.addData('text_instruct.stopped', text_instruct.tStopRefresh)
# the Routine "setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=2.0, method='random',
                           extraInfo=expInfo, originPath=-1,
                           trialList=data.importConditions('horse-demo.xlsx'),
                           seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2.0)
line = ser.readline().decode().strip()
assert line == "Device is ready ..."
ser.write('0'.encode())
line = ser.readline().decode().strip()
print(line)
assert line == "Operational Mode"

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

    # ------Prepare to start Routine "video"-------
    continueRoutine = True
    # update component parameters for each repeat
    movie = visual.MovieStim3(
        win=win, name='movie',
        noAudio=False,
        filename='./Stimulus/stim_0ms.mp4',
        ori=0.0, pos=(0, 0), opacity=None,
        loop=False,
        depth=0.0,
    )
    choice = randint(1, maxChoice)
    thisExp.addData('StartingChoice', tones[choice])
    allChoices = []

    toneFiles = []
    for Idx in range(maxChoice + 1):
        toneFiles.append(
            {'name': 'Horse' + '_' + tones[Idx] + '.wav', 'path': 'wav-files/' + 'Horse' + '_' + tones[Idx] + '.wav',
             'download': True})

    # keep track of which components have finished
    videoComponents = [movie]
    for thisComponent in videoComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    videoClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    win.flip()
    # core.wait(5.0)
    # -------Run Routine "video"-------
    while continueRoutine:
        # get current time
        t = videoClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=videoClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *movie* updates
        if movie.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            movie.frameNStart = frameN  # exact frame index
            movie.tStart = t  # local t and not account for scr refresh
            movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
            movie.setAutoDraw(True)

        # check for quit (typically the Esc key)
        # if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        #     core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in videoComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "video"-------
    for thisComponent in videoComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    movie.stop()

    arduino_delay = int(ser.readline().decode().strip().split(' ')[-1])
    print(arduino_delay)
    # the Routine "video" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    core.wait(1.0)
exit()
#
#     # set up handler to look after randomisation of conditions etc
#     tone_selection = data.TrialHandler(nReps=100.0, method='sequential',
#                                        extraInfo=expInfo, originPath=-1,
#                                        trialList=[None],
#                                        seed=None, name='tone_selection')
#     thisExp.addLoop(tone_selection)  # add the loop to the experiment
#     thisTone_selection = tone_selection.trialList[0]  # so we can initialise stimuli with some values
#     # abbreviate parameter names if possible (e.g. rgb = thisTone_selection.rgb)
#     if thisTone_selection != None:
#         for paramName in thisTone_selection:
#             exec('{} = thisTone_selection[paramName]'.format(paramName))
#
#     for thisTone_selection in tone_selection:
#         currentLoop = tone_selection
#         # abbreviate parameter names if possible (e.g. rgb = thisTone_selection.rgb)
#         if thisTone_selection != None:
#             for paramName in thisTone_selection:
#                 exec('{} = thisTone_selection[paramName]'.format(paramName))
#
#         # ------Prepare to start Routine "tones"-------
#         continueRoutine = True
#         # update component parameters for each repeat
#         if choice == 0 or choice == maxChoice:
#             sound_1, stop()
#
#         sound_1.setSound(soundDir + Voc + '_' + tones[choice] + '.wav', hamming=True)
#         sound_1.setVolume(1.0, log=False)
#         key_resp.keys = []
#         key_resp.rt = []
#         _key_resp_allKeys = []
#         text_freq.setText(tones[choice])
#         # keep track of which components have finished
#         tonesComponents = [sound_1, key_resp, text_freq]
#         for thisComponent in tonesComponents:
#             thisComponent.tStart = None
#             thisComponent.tStop = None
#             thisComponent.tStartRefresh = None
#             thisComponent.tStopRefresh = None
#             if hasattr(thisComponent, 'status'):
#                 thisComponent.status = NOT_STARTED
#         # reset timers
#         t = 0
#         _timeToFirstFrame = win.getFutureFlipTime(clock="now")
#         tonesClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
#         frameN = -1
#
#         # -------Run Routine "tones"-------
#         while continueRoutine:
#             # get current time
#             t = tonesClock.getTime()
#             tThisFlip = win.getFutureFlipTime(clock=tonesClock)
#             tThisFlipGlobal = win.getFutureFlipTime(clock=None)
#             frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
#             # update/draw components on each frame
#             # start/stop sound_1
#             if sound_1.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
#                 # keep track of start time/frame for later
#                 sound_1.frameNStart = frameN  # exact frame index
#                 sound_1.tStart = t  # local t and not account for scr refresh
#                 sound_1.tStartRefresh = tThisFlipGlobal  # on global time
#                 sound_1.play(when=win)  # sync with win flip
#
#             # *key_resp* updates
#             waitOnFlip = False
#             if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
#                 # keep track of start time/frame for later
#                 key_resp.frameNStart = frameN  # exact frame index
#                 key_resp.tStart = t  # local t and not account for scr refresh
#                 key_resp.tStartRefresh = tThisFlipGlobal  # on global time
#                 win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
#                 key_resp.status = STARTED
#                 # keyboard checking is just starting
#                 waitOnFlip = True
#                 win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
#                 win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
#             if key_resp.status == STARTED and not waitOnFlip:
#                 theseKeys = key_resp.getKeys(keyList=['up', 'down', 'return'], waitRelease=False)
#                 _key_resp_allKeys.extend(theseKeys)
#                 if len(_key_resp_allKeys):
#                     key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
#                     key_resp.rt = _key_resp_allKeys[-1].rt
#                     # a response ends the routine
#                     continueRoutine = False
#
#             # *text_freq* updates
#             if text_freq.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
#                 # keep track of start time/frame for later
#                 text_freq.frameNStart = frameN  # exact frame index
#                 text_freq.tStart = t  # local t and not account for scr refresh
#                 text_freq.tStartRefresh = tThisFlipGlobal  # on global time
#                 win.timeOnFlip(text_freq, 'tStartRefresh')  # time at next scr refresh
#                 text_freq.setAutoDraw(True)
#
#             # check for quit (typically the Esc key)
#             if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
#                 core.quit()
#
#             # check if all components have finished
#             if not continueRoutine:  # a component has requested a forced-end of Routine
#                 break
#             continueRoutine = False  # will revert to True if at least one component still running
#             for thisComponent in tonesComponents:
#                 if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
#                     continueRoutine = True
#                     break  # at least one component has not yet finished
#
#             # refresh the screen
#             if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
#                 win.flip()
#
#         # -------Ending Routine "tones"-------
#         for thisComponent in tonesComponents:
#             if hasattr(thisComponent, "setAutoDraw"):
#                 thisComponent.setAutoDraw(False)
#         if 'up' in key_resp.keys:
#             if choice < maxChoice:
#                 choice += 1
#             allChoices.append(tones[choice])
#         elif 'down' in key_resp.keys:
#             if choice > 0:
#                 choice -= 1
#             allChoices.append(tones[choice])
#         elif 'return' in key_resp.keys:
#             tone_selection.finished = true
#             thisExp.addData('All Choices', allChoices)
#             thisExp.addData('Choice', tones[choice])
#         sound_1.stop()  # ensure sound has stopped at end of routine
#         tone_selection.addData('sound_1.started', sound_1.tStartRefresh)
#         tone_selection.addData('sound_1.stopped', sound_1.tStopRefresh)
#         # check responses
#         if key_resp.keys in ['', [], None]:  # No response was made
#             key_resp.keys = None
#         tone_selection.addData('key_resp.keys', key_resp.keys)
#         if key_resp.keys != None:  # we had a response
#             tone_selection.addData('key_resp.rt', key_resp.rt)
#         tone_selection.addData('key_resp.started', key_resp.tStartRefresh)
#         tone_selection.addData('key_resp.stopped', key_resp.tStopRefresh)
#         # the Routine "tones" was not non-slip safe, so reset the non-slip timer
#         routineTimer.reset()
#         thisExp.nextEntry()
#
#     # completed 100.0 repeats of 'tone_selection'
#
#     # ------Prepare to start Routine "feedback"-------
#     continueRoutine = True
#     routineTimer.add(1.000000)
#     # update component parameters for each repeat
#     text_feedback.setText('You chose tone ' + tones[choice])
#     # keep track of which components have finished
#     feedbackComponents = [text_feedback]
#     for thisComponent in feedbackComponents:
#         thisComponent.tStart = None
#         thisComponent.tStop = None
#         thisComponent.tStartRefresh = None
#         thisComponent.tStopRefresh = None
#         if hasattr(thisComponent, 'status'):
#             thisComponent.status = NOT_STARTED
#     # reset timers
#     t = 0
#     _timeToFirstFrame = win.getFutureFlipTime(clock="now")
#     feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
#     frameN = -1
#
#     # -------Run Routine "feedback"-------
#     while continueRoutine and routineTimer.getTime() > 0:
#         # get current time
#         t = feedbackClock.getTime()
#         tThisFlip = win.getFutureFlipTime(clock=feedbackClock)
#         tThisFlipGlobal = win.getFutureFlipTime(clock=None)
#         frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
#         # update/draw components on each frame
#
#         # *text_feedback* updates
#         if text_feedback.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
#             # keep track of start time/frame for later
#             text_feedback.frameNStart = frameN  # exact frame index
#             text_feedback.tStart = t  # local t and not account for scr refresh
#             text_feedback.tStartRefresh = tThisFlipGlobal  # on global time
#             win.timeOnFlip(text_feedback, 'tStartRefresh')  # time at next scr refresh
#             text_feedback.setAutoDraw(True)
#         if text_feedback.status == STARTED:
#             # is it time to stop? (based on global clock, using actual start)
#             if tThisFlipGlobal > text_feedback.tStartRefresh + 1.0 - frameTolerance:
#                 # keep track of stop time/frame for later
#                 text_feedback.tStop = t  # not accounting for scr refresh
#                 text_feedback.frameNStop = frameN  # exact frame index
#                 win.timeOnFlip(text_feedback, 'tStopRefresh')  # time at next scr refresh
#                 text_feedback.setAutoDraw(False)
#
#         # check for quit (typically the Esc key)
#         if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
#             core.quit()
#
#         # check if all components have finished
#         if not continueRoutine:  # a component has requested a forced-end of Routine
#             break
#         continueRoutine = False  # will revert to True if at least one component still running
#         for thisComponent in feedbackComponents:
#             if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
#                 continueRoutine = True
#                 break  # at least one component has not yet finished
#
#         # refresh the screen
#         if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
#             win.flip()
#
#     # -------Ending Routine "feedback"-------
#     for thisComponent in feedbackComponents:
#         if hasattr(thisComponent, "setAutoDraw"):
#             thisComponent.setAutoDraw(False)
#     trials.addData('text_feedback.started', text_feedback.tStartRefresh)
#     trials.addData('text_feedback.stopped', text_feedback.tStopRefresh)
#     thisExp.nextEntry()
#
# # completed 1.0 repeats of 'trials'
#
#
# # ------Prepare to start Routine "end"-------
# continueRoutine = True
# # update component parameters for each repeat
# # keep track of which components have finished
# endComponents = [text]
# for thisComponent in endComponents:
#     thisComponent.tStart = None
#     thisComponent.tStop = None
#     thisComponent.tStartRefresh = None
#     thisComponent.tStopRefresh = None
#     if hasattr(thisComponent, 'status'):
#         thisComponent.status = NOT_STARTED
# # reset timers
# t = 0
# _timeToFirstFrame = win.getFutureFlipTime(clock="now")
# endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
# frameN = -1
#
# # -------Run Routine "end"-------
# while continueRoutine:
#     # get current time
#     t = endClock.getTime()
#     tThisFlip = win.getFutureFlipTime(clock=endClock)
#     tThisFlipGlobal = win.getFutureFlipTime(clock=None)
#     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
#     # update/draw components on each frame
#
#     # *text* updates
#     if text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
#         # keep track of start time/frame for later
#         text.frameNStart = frameN  # exact frame index
#         text.tStart = t  # local t and not account for scr refresh
#         text.tStartRefresh = tThisFlipGlobal  # on global time
#         win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
#         text.setAutoDraw(True)
#
#     # check for quit (typically the Esc key)
#     if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
#         core.quit()
#
#     # check if all components have finished
#     if not continueRoutine:  # a component has requested a forced-end of Routine
#         break
#     continueRoutine = False  # will revert to True if at least one component still running
#     for thisComponent in endComponents:
#         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
#             continueRoutine = True
#             break  # at least one component has not yet finished
#
#     # refresh the screen
#     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
#         win.flip()
#
# # -------Ending Routine "end"-------
# for thisComponent in endComponents:
#     if hasattr(thisComponent, "setAutoDraw"):
#         thisComponent.setAutoDraw(False)
# thisExp.addData('text.started', text.tStartRefresh)
# thisExp.addData('text.stopped', text.tStopRefresh)
# # the Routine "end" was not non-slip safe, so reset the non-slip timer
# routineTimer.reset()
#
# # Flip one final time so any remaining win.callOnFlip()
# # and win.timeOnFlip() tasks get executed before quitting
# win.flip()
#
# # these shouldn't be strictly necessary (should auto-save)
# thisExp.saveAsWideText(filename + '.csv', delim='auto')
# thisExp.saveAsPickle(filename)
# logging.flush()
# # make sure everything is closed down
# thisExp.abort()  # or data files will save again on exit
# win.close()
# core.quit()
