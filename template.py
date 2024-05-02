from psychopy import visual, core, data, logging, gui
# import pyschopy.event as event
import psychopy.event

# Create a dialog box to collect participant information
info = {'Subject ID': '', 'Age': '', 'Gender': ['Male', 'Female', 'Other']}
dlg = gui.DlgFromDict(dictionary=info, title='Experiment Information')
if not dlg.OK:
    core.quit()  # User pressed cancel, so exit

# Setup the Window
win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")

# Define Stimuli
instruction_text = visual.TextStim(win, text="Press any key to start.")
stimulus = visual.TextStim(win, color=(1, 1, 1))

# Setup Trial Handler
conditions = [{'text': 'Condition 1'}, {'text': 'Condition 2'}]
trials = data.TrialHandler(trialList=conditions, nReps=3, method='random')

# Clock for timing
trial_clock = core.Clock()

# Experiment flow
instruction_text.draw()
win.flip()
print("Im here")
pressed_keys = psychopy.event.waitKeys(keyList=["space"])  # Wait for key press

for trial in trials:
    stimulus.setText(trial['text'])  # Set the condition-specific text
    trial_clock.reset()  # Reset the clock at the start of each trial
    while trial_clock.getTime() < 2:  # Show the stimulus for 2 seconds
        stimulus.draw()
        win.flip()

    # Collect responses here or add a response phase

# Clean up
win.close()
core.quit()
