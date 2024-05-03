from psychopy import visual, core, event, data, logging, gui, os

# Set up experiment info
expName = 'My Experiment'
expInfo = {'Subject ID': '', 'Age': '', 'Gender': ['Male', 'Female', 'Other']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if not dlg.OK:
    core.quit()  # User pressed cancel

# Ensure there is a folder to save the data
if not os.path.exists('data'):
    os.makedirs('data')

# Data file setup
filename = os.path.join('data', '{}_{}'.format(expInfo['Subject ID'], data.getDateStr()))
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath='',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)

# Window setup
win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")

# Define stimuli
instruction_text = visual.TextStim(win, text="Press any key to start.")
stimulus = visual.TextStim(win, color=(1, 1, 1))

# Setup Trial Handler
conditions = [{'text': 'Condition 1'}, {'text': 'Condition 2'}]
trials = data.TrialHandler(trialList=conditions, nReps=3, method='random')
thisExp.addLoop(trials)  # This allows logging at each iteration

# Clock for precise timing
trial_clock = core.Clock()

# Experiment flow
instruction_text.draw()
win.flip()
event.waitKeys()  # Wait for key press

for trial in trials:
    stimulus.setText(trial['text'])  # Set text based on condition
    trial_clock.reset()  # Reset the clock at the start of each trial
    stimulus.draw()
    win.flip()
    core.wait(2)  # Present the stimulus for 2 seconds

    # Log data for the current trial
    thisExp.addData('Stimulus', trial['text'])
    thisExp.addData('Stimulus Duration', 2)
    thisExp.addData('Trial Start', trial_clock.getTime())
    thisExp.nextEntry()

# Clean up
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
win.close()
core.quit()
