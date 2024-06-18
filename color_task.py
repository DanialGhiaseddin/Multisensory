from screeninfo import get_monitors
import yaml
from psychopy import visual, core, event, data, logging, gui, os
import matplotlib.colors as mpl_colors

import random
from psychopy import visual
import matplotlib.colors as mpl_colors
import numpy as np
from psychopy.clock import Clock
from psychopy.hardware import keyboard
from pynput import keyboard


# Generate four random numbers between 0 and 1


class ColorTask:
    def __init__(self, config_path):
        self.config = self._read_and_refine_config(config_path)

        exp_name = self.config["experiment"]["name"]
        exp_info = {'Subject ID': '', 'Age': '', 'Gender': ['Male', 'Female', 'Other']}
        dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
        if not dlg.OK:
            core.quit()  # User pressed cancel

        # TODO: Verify if subject ID is not empty and generate a random ID if it is

        # Ensure there is a folder to save the data
        if not os.path.exists('data'):
            os.makedirs('data')

        # Data file setup
        self.filename = os.path.join('data', '{}_{}'.format(exp_info['Subject ID'], data.getDateStr()))
        self.this_exp = data.ExperimentHandler(name=exp_name, version='',
                                               extraInfo=exp_info, runtimeInfo=None,
                                               originPath='',
                                               savePickle=True, saveWideText=True,
                                               dataFileName=self.filename)

        self.win = visual.Window(size=self.config["screen"]["size"], fullscr=self.config["screen"]["full-screen"],
                                 units='height')

        self.color_bar = self.CircularColorBar(self.win)

        # Define stimuli
        self.instruction_text = visual.TextStim(self.win, text="Press any key to start.")
        self.fixation = visual.TextStim(self.win, color=(1, 1, 1), pos=(0, 0), text="+", height=0.1)
        self.stimulus = self.Stimulus(self.win)
        # Setup Trial Handler
        # conditions = [{'text': 'Condition 1'}, {'text': 'Condition 2'}]
        trials = self.config["experiment"]["trials"]
        conditions = []
        for i in range(trials):
            colors = [random.random() for _ in range(4)]
            print(colors)
            conditions.append({'colors': colors})
        self.trials = data.TrialHandler(trialList=conditions, nReps=1, method='random')
        self.this_exp.addLoop(self.trials)  # This allows logging at each iteration

        # Clock for precise timing
        self.trial_clock = core.Clock()
        # Timings
        self.fixation_delay = self.config["experiment"]["fixation_wait_time"]
        self.stimulus_duration = self.config["experiment"]["stimulus_duration"]
        self.response_timeout = self.config["experiment"]["response_timeout"]

    def _read_and_refine_config(self, config_path="configs/config_base.yml"):
        with open(config_path, "r") as yml_file:
            config_file = yaml.safe_load(yml_file)

        if config_file["screen"]["size"] == "full-screen":
            config_file["screen"]["size"] = [get_monitors()[0].width, get_monitors()[0].height]
            config_file["screen"]["full-screen"] = True
        else:
            config_file["screen"]["full-screen"] = False
        self.config = config_file
        return self.config

    class ColorBar:
        def __init__(self, win, width=1.2, height=0.02, pos=(0, -0.46), number_of_colors=200):
            self.win = win

            self.slider = visual.Slider(win=self.win, ticks=(0, 1), labels=['Red', 'Violet'],
                                        granularity=1 / number_of_colors,
                                        style='slider', pos=pos, size=(width, height), color='LightGray')

            # Create a feedback stimulus (e.g., a circle)
            self.feedback = visual.Circle(self.win, radius=height, fillColor='white', lineColor='white',
                                          pos=(width / 2 + 0.01 + height, pos[1] + height / 2))

            num_colors = number_of_colors
            self.gradient_bar = []
            bar_width = width / num_colors
            bar_height = height
            bar_start = pos[0] - (width / 2) + (bar_width / 2)

            for i in range(num_colors):
                color = mpl_colors.hsv_to_rgb([i / num_colors, 1, 1])
                rect = visual.Rect(win, width=bar_width, height=bar_height,
                                   pos=(bar_start + i * bar_width, pos[1] + height),
                                   fillColor=color,
                                   lineColor=color)
                self.gradient_bar.append(rect)

        def draw(self):

            if self.slider.rating is not None:
                # Map the slider value to a color in the spectrum
                color_value = self.slider.getRating()  # This will be a value between 0 and 1
                color = mpl_colors.hsv_to_rgb([color_value, 1, 1])  # Convert HSV to RGB

                # Update the feedback color
                self.feedback.fillColor = color
                self.feedback.lineColor = color

            # Draw the slider and feedback
            self.slider.draw()
            self.feedback.draw()

            for rect in self.gradient_bar:
                rect.draw(win=self.win)

        def reset(self):
            self.slider.reset()
            self.feedback.fillColor = 'white'
            self.feedback.lineColor = 'white'

    class CircularColorBar:
        def __init__(self, win, radius=0.5, pos=(0, 0), number_of_colors=200, feedback_radius=0.05):
            self.win = win
            self.radius = radius
            self.pos = pos

            self.num_colors = number_of_colors
            self.gradient_bar = []

            self.feedback_circle = visual.Circle(self.win, fillColor='white', lineColor='white', radius=feedback_radius)

            theta = np.linspace(0, 2 * np.pi, number_of_colors)
            for i in range(number_of_colors):
                color = mpl_colors.hsv_to_rgb([i / number_of_colors, 1, 1])
                x = pos[0] + radius * np.cos(theta[i])
                y = pos[1] + radius * np.sin(theta[i])
                circle = visual.Circle(win, radius=radius * 0.02,
                                       pos=(x, y),
                                       fillColor=color,
                                       lineColor=color)
                self.gradient_bar.append(circle)

            # Create a feedback stimulus (e.g., a circle)
            self.feedback = visual.Circle(self.win, radius=radius * 0.05, fillColor='white', lineColor='white',
                                          pos=(pos[0] + radius, pos[1]))

            self.slider_pos = 0

        def draw(self):
            # Draw the gradient bar
            for circle in self.gradient_bar:
                circle.draw(win=self.win)

            if self.slider_pos is not None:
                # Map the slider position to a color in the spectrum
                color_value = self.slider_pos / self.num_colors  # This will be a value between 0 and 1
                color = mpl_colors.hsv_to_rgb([color_value, 1, 1])  # Convert HSV to RGB

                # Update the feedback color
                self.feedback.fillColor = color
                self.feedback.lineColor = color
                self.feedback_circle.fillColor = color
                self.feedback_circle.lineColor = color

                # Update feedback position
                theta = 2 * np.pi * color_value
                self.feedback.pos = (self.pos[0] + self.radius * np.cos(theta),
                                     self.pos[1] + self.radius * np.sin(theta))

            # Draw the feedback
            self.feedback.draw()
            self.feedback_circle.draw()

        def incremental_update_slider(self, increment):
            # Update slider position based on increment
            self.slider_pos = (self.slider_pos + increment) % self.num_colors

        def update_slider(self, mouse_pos):
            # Update slider position based on mouse position
            dx = mouse_pos[0] - self.pos[0]
            dy = mouse_pos[1] - self.pos[1]
            angle = np.arctan2(dy, dx)
            if angle < 0:
                angle += 2 * np.pi
            self.slider_pos = int(self.num_colors * angle / (2 * np.pi))

        def reset(self):
            self.slider_pos = 0
            self.feedback.fillColor = 'white'
            self.feedback.lineColor = 'white'

        def get_feedback_color(self, position):

            mouse = event.Mouse(win=self.win)

            self.feedback_circle.pos = position

            while True:
                self.draw()
                self.win.flip()

                keys = event.getKeys()
                if 'escape' in keys:
                    break

                if 'left' in keys:
                    self.incremental_update_slider(1)
                if 'right' in keys:
                    self.incremental_update_slider(-1)

                if 'space' in keys:
                    return self.feedback.fillColor

                # Update the slider position if the left mouse button is pressed
                if mouse.getPressed()[0]:  # Left mouse button is pressed
                    mouse_pos = mouse.getPos()
                    self.update_slider(mouse_pos)

                # Small delay to prevent overloading the CPU
                core.wait(0.01)

    class Stimulus:
        def __init__(self, win, radius=0.05, distance=0.22):
            self.win = win
            # Create a feedback stimulus (e.g., a circle)
            self.circles = []

            # distances = [[-distance, -distance], [-distance, distance], [distance, -distance], [distance, distance]]
            positions = [(-distance, -distance), (-distance, distance), (distance, -distance), (distance, distance)]
            for i in range(4):
                self.circles.append(visual.Circle(self.win, radius=radius, fillColor='white', lineColor='white',
                                                  pos=positions[i]))

        def draw(self, colors):

            for i in range(4):
                color = mpl_colors.hsv_to_rgb([colors[i], 1, 1])
                self.circles[i].fillColor = color
                self.circles[i].lineColor = color
                self.circles[i].draw(win=self.win)

        def get_position(self, index):
            return self.circles[index].pos

    def _draw_instruction(self):
        self.instruction_text.draw()
        self.win.flip()
        event.waitKeys()

    def run(self):

        self._draw_instruction()

        for trial in self.trials:
            self.trial_clock.reset()  # Reset the clock at the start of each trial
            self.color_bar.reset()
            self.fixation.draw()
            self.win.flip()
            core.wait(self.fixation_delay)  # Present the stimulus for 2 seconds

            self.stimulus.draw(trial['colors'])
            self.fixation.draw()
            self.win.flip()
            core.wait(self.stimulus_duration)  # Present the stimulus for 2 seconds

            # Get Response
            # TODO: Start Here
            index = random.randint(0, 4)
            position = self.stimulus.get_position(index)

            # while not event.getKeys(keyList=["space", "escape"]):
            answer = self.color_bar.get_feedback_color(position)
            answer = mpl_colors.rgb_to_hsv(answer)
            # self.fixation.draw()
            # self.color_bar.draw()
            # self.win.flip()

            # Log data for the current trial
            self.this_exp.addData('Stimulus', trial['colors'])
            self.this_exp.addData('Stimulus Duration', 2)
            self.this_exp.addData('Trial Start', self.trial_clock.getTime())
            self.this_exp.addData('Feedback', answer)
            self.this_exp.addData('Selected Position', index)
            self.this_exp.nextEntry()

        # Clean up
        self.this_exp.saveAsWideText(self.filename + '.csv')
        self.this_exp.saveAsPickle(self.filename)
        self.win.close()
        core.quit()

        # Experiment loop


if __name__ == "__main__":
    experiment = ColorTask("configs/config_color_task.yml")
    experiment.run()
