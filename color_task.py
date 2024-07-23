from screeninfo import get_monitors
import yaml
from psychopy import visual, core, event, data, logging, gui, os

import random
from psychopy import visual
import matplotlib.colors as mpl_colors
import numpy as np
from psychopy.clock import Clock
from psychopy.hardware import keyboard
from pynput import keyboard

from utils import generate_distant_numbers, generate_fixed_distant_numbers, generate_stimulus_trial_two_rectangles

from utils import hue_to_degrees, round_to_nearest, hue_difference_signed


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

        self.color_bar = self.CircularColorBar(self.win, radius=self.config["color_bar"]["radius"],
                                               feedback_radius=self.config["stimulus"]["size"],
                                               number_of_colors=self.config["color_bar"]["number_of_colors"],
                                               slider_radius=self.config["color_bar"]["slider_radius"],
                                               saturation=self.config["color_bar"]["saturation"],
                                               value=self.config["color_bar"]["value"],
                                               is_colorful=self.config["color_bar"]["colorful"]
                                               )

        # Define stimuli

        self.instruction_text = visual.ImageStim(
            win=self.win,
            image="Images/color_task/Instruction.jpg",
            units="pix"
        )

        self.rest_text = visual.ImageStim(
            win=self.win,
            image="Images/color_task/Rest.jpg",
            units="pix"
        )

        self.training_img = []
        self.training_img.append(visual.ImageStim(
            win=self.win,
            image="Images/color_task/1.png",
            units="pix"
        ))
        self.training_img.append(visual.ImageStim(
            win=self.win,
            image="Images/color_task/3.png",
            units="pix"
        ))
        self.training_img.append(visual.ImageStim(
            win=self.win,
            image="Images/color_task/4.png",
            units="pix"
        ))

        self.n_blocks = self.config["experiment"]["n_blocks"]
        assert self.n_blocks <= 5, "Number of blocks should be less than or equal to 5"
        self.blocks = []
        for i in range(self.n_blocks):
            self.blocks.append(visual.ImageStim(
                win=self.win,
                image="Images/color_task/block0{}.JPG".format(i + 1),
                units="pix"
            ))

        # self.instruction_text = visual.TextStim(self.win, text="Press any key to start.")
        self.fixation = visual.TextStim(self.win, color=(-1, -1, -1), pos=(0, 0), text="+",
                                        height=self.config["experiment"]["fixation_size"])
        self.stimulus = self.Stimulus(self.win, size=self.config["stimulus"]["size"],
                                      distance=self.config["stimulus"]["distance"],
                                      saturation=self.config["color_bar"]["saturation"],
                                      value=self.config["color_bar"]["value"])

        self.confident_response = self.ConfidentResponse(self.win)

        # Setup Trial Handler
        # conditions = [{'text': 'Condition 1'}, {'text': 'Condition 2'}]
        trials = self.config["experiment"]["n_trials"] * self.n_blocks
        conditions = []

        self.number_of_rectangles = 2
        easy_hard_balance = self.config["experiment"]["easy_hard_balance"]
        for i in range(trials):
            if self.config["experiment"]["fixed_dist_distractor"]:
                colors, selected_index, distractor_diff = generate_stimulus_trial_two_rectangles(
                    self.number_of_rectangles)
            else:
                colors = [random.random() for _ in range(self.number_of_rectangles)]
                selected_index = random.randint(0, self.number_of_rectangles - 1)
                distractor_diff = -1
            conditions.append(
                {'colors': colors, 'selected_index': selected_index, 'distractor_diff': distractor_diff,
                 'difficulty': random.choices(['Easy', 'Difficult'],
                                              weights=[
                                                  easy_hard_balance,
                                                  1 - easy_hard_balance],
                                              k=1)[0],
                 'angle_offset': np.random.uniform(0, 2 * np.pi)})

        self.trials = data.TrialHandler(trialList=conditions, nReps=1, method='random')

        self.total_trials = len(conditions)
        self.trial_per_block = len(conditions) // self.n_blocks

        self.this_exp.addLoop(self.trials)  # This allows logging at each iteration

        dummy_conditions = []
        training_trials = self.config["experiment"]["training_trials"]
        for i in range(training_trials):
            if self.config["experiment"]["fixed_dist_distractor"]:
                colors, selected_index, distractor_diff = generate_stimulus_trial_two_rectangles(
                    self.number_of_rectangles)
            else:
                colors = [random.random() for _ in range(self.number_of_rectangles)]
                selected_index = random.randint(0, self.number_of_rectangles - 1)
                distractor_diff = -1
            dummy_conditions.append(
                {'colors': colors, 'selected_index': selected_index, 'distractor_diff': distractor_diff,
                 'difficulty': random.choices(['Easy', 'Difficult'],
                                              weights=[
                                                  easy_hard_balance,
                                                  1 - easy_hard_balance],
                                              k=1)[0],
                 'angle_offset': np.random.uniform(0, 2 * np.pi)})

        self.dummy_trials = data.TrialHandler(trialList=dummy_conditions, nReps=1, method='sequential')

        # Clock for precise timing
        self.trial_clock = core.Clock()
        # Timings
        self.fixation_delay = self.config["experiment"]["fixation_wait_time"]
        self.stimulus_duration = self.config["experiment"]["stimulus_duration"]
        self.mask_duration = self.config["experiment"]["mask_duration"]
        self.wm_duration_easy = self.config["experiment"]["wm_duration_easy"]
        self.wm_duration_hard = self.config["experiment"]["wm_duration_hard"]
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
        def __init__(self, win, width=1.2, height=0.02, pos=(0, -0.46), number_of_colors=200, saturation=1, value=1):
            self.win = win
            self.saturation = saturation
            self.value = value

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
                color = mpl_colors.hsv_to_rgb([i / num_colors, self.saturation, self.value])
                color = [(c * 2) - 1 for c in color]
                rect = visual.Rect(win, width=bar_width, height=bar_height,
                                   pos=(bar_start + i * bar_width, pos[1] + height),
                                   fillColor=color,
                                   lineColor=color)
                self.gradient_bar.append(rect)

        def draw(self):

            if self.slider.rating is not None:
                # Map the slider value to a color in the spectrum
                color_value = self.slider.getRating()  # This will be a value between 0 and 1
                color = mpl_colors.hsv_to_rgb([color_value, self.saturation, self.value])
                color = [(c * 2) - 1 for c in color]  # Convert HSV to RGB

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
        def __init__(self, win, radius=0.5, pos=(0, 0), number_of_colors=200, feedback_radius=0.05, slider_radius=0.01,
                     saturation=1, value=1, is_colorful=True):
            self.win = win
            self.saturation = saturation
            self.value = value
            self.radius = radius
            self.pos = pos

            self.num_colors = number_of_colors
            self.gradient_bar = []

            # self.feedback_object = (self.win, fillColor='white', lineColor='white', radius=feedback_radius)
            self.feedback_object = visual.Rect(self.win, width=feedback_radius, height=feedback_radius,
                                               fillColor=[0, 0, 0],
                                               lineColor=[0, 0, 0])

            theta = np.linspace(0, 2 * np.pi, number_of_colors)

            # angle_offset = np.random.uniform(0, 2 * np.pi)

            for i in range(number_of_colors):
                if is_colorful:
                    color = mpl_colors.hsv_to_rgb([i / number_of_colors, self.saturation, self.value])  #
                    color = [(c * 2) - 1 for c in color]
                else:
                    color = [0.3, 0.3, 0.3]
                x = pos[0] + radius * np.cos(theta[i])
                y = pos[1] + radius * np.sin(theta[i])
                circle = visual.Circle(win, radius=radius * 0.01,
                                       pos=(x, y),
                                       fillColor=color,  # color,
                                       lineColor=color, colorSpace='rgb')
                self.gradient_bar.append(circle)

            # Create a feedback stimulus (e.g., a circle)
            self.feedback = visual.Circle(self.win, radius=slider_radius, fillColor='white', lineColor='white',
                                          pos=(pos[0] + radius, pos[1]))

            self.slider_pos = 0
            self.feedback_started = False

        def draw(self, angle_offset=0.0):
            # Draw the gradient bar
            theta = np.linspace(angle_offset, (2 * np.pi) + angle_offset, self.num_colors)
            for index, circle in enumerate(self.gradient_bar):
                x = self.pos[0] + self.radius * np.cos(theta[index])
                y = self.pos[1] + self.radius * np.sin(theta[index])
                circle.pos = (x, y)
                circle.draw(win=self.win)

            if self.slider_pos is not None:
                # Map the slider position to a color in the spectrum
                # color_value = self.slider_pos / self.num_colors  # This will be a value between 0 and 1
                corrected_pos = (((self.slider_pos / self.num_colors) * 2 * np.pi) - angle_offset) / (
                        2 * np.pi) * self.num_colors
                color_value = self.gradient_bar[int(corrected_pos)].fillColor
                if self.feedback_started:
                    color = color_value
                    # color = mpl_colors.hsv_to_rgb([color_value, self.saturation, self.value])  # Convert HSV to RGB
                    # color = [(c * 2) - 1 for c in color]
                else:
                    color = [0.3, 0.3, 0.3]
                # Update the feedback color
                self.feedback.fillColor = color
                self.feedback.lineColor = color
                self.feedback_object.fillColor = color
                self.feedback_object.lineColor = color

                # Update feedback position
                theta = 2 * np.pi * (self.slider_pos / self.num_colors)
                self.feedback.pos = (self.pos[0] + self.radius * np.cos(theta),
                                     self.pos[1] + self.radius * np.sin(theta))

            # Draw the feedback
            self.feedback.draw()
            self.feedback_object.draw()

        def incremental_update_slider(self, increment):
            # Update slider position based on increment
            self.slider_pos = (self.slider_pos + increment) % self.num_colors
            self.feedback_started = True

        def update_slider(self, mouse_pos):
            # Update slider position based on mouse position
            dx = mouse_pos[0] - self.pos[0]
            dy = mouse_pos[1] - self.pos[1]
            angle = np.arctan2(dy, dx)
            if angle < 0:
                angle += 2 * np.pi
            self.slider_pos = int(self.num_colors * angle / (2 * np.pi))
            self.feedback_started = True

        def reset(self):
            self.slider_pos = 0
            self.feedback.fillColor = 'white'
            self.feedback.lineColor = 'white'
            self.feedback_started = False

        def get_feedback_color(self, position, angle_offset, timeout=5):

            mouse = event.Mouse(win=self.win)

            self.feedback_object.pos = position

            response_clock = core.Clock()
            timeout_clock = core.Clock()

            while timeout_clock.getTime() < timeout:
                self.draw(angle_offset=angle_offset)
                self.win.flip()

                keys = event.getKeys()
                if 'escape' in keys:
                    break
                if 'left' in keys:
                    self.incremental_update_slider(1)
                if 'right' in keys:
                    self.incremental_update_slider(-1)
                if 'space' in keys:
                    response_time = response_clock.getTime()
                    return self.feedback.fillColor, response_time

                # Update the slider position if the left mouse button is pressed
                if mouse.getPressed()[0]:  # Left mouse button is pressed
                    mouse_pos = mouse.getPos()
                    self.update_slider(mouse_pos)

                # Small delay to prevent overloading the CPU
                core.wait(0.01)

            return None, None

    class Stimulus:
        def __init__(self, win, size=0.05, distance=0.22, saturation=1, value=1):
            self.win = win
            self.saturation = saturation
            self.value = value
            self.size = size
            self.distance = distance
            # Create a feedback stimulus (e.g., a circle)
            self.objects = []

            # # distances = [[-distance, -distance], [-distance, distance], [distance, -distance], [distance, distance]]
            # positions = [(-distance, -distance), (-distance, distance), (distance, -distance), (distance, distance)]
            self.positions = [(distance, 0), (-distance, 0)]
            # for i in range(4):
            #     self.circles.append(visual.Circle(self.win, radius=radius, fillColor='white', lineColor='white',
            #                                       pos=positions[i]))
            # self.rectangles = []

            # Define the positions for the rectangles
            # Calculate positions for an equilateral triangle centered at (0, 0)
            # self.distance = distance
            # angle_offset = np.pi  # Start with one rectangle at the top
            # positions = []
            # for i in range(3):
            #     angle = angle_offset + (i * 2 * np.pi / 3)  # 120 degrees apart
            #     x = distance * np.cos(angle)
            #     y = distance * np.sin(angle)
            #     positions.append((x, y))

            for pos in self.positions:
                self.objects.append(
                    visual.Rect(self.win, width=size, height=size, fillColor='white', lineColor='white', pos=pos))

        def draw(self, colors, angle_offset=0.0):

            # positions = []
            # for i in range(3):
            #     angle = angle_offset + (i * 2 * np.pi / 3)  # 120 degrees apart
            #     x = self.distance * np.cos(angle)
            #     y = self.distance * np.sin(angle)
            #     positions.append((x, y))

            for i in range(len(self.objects)):
                color = mpl_colors.hsv_to_rgb([colors[i], self.saturation, self.value])
                color = [(c * 2) - 1 for c in color]
                self.objects[i].fillColor = color
                self.objects[i].lineColor = color
                # self.objects[i].pos = positions[i]
                self.objects[i].draw(win=self.win)

        def get_position(self, index):
            return self.objects[index].pos

        def draw_mask(self):
            # Generate Gaussian noise
            for pos in self.positions:
                mean = 0.5  # mean of the Gaussian noise
                std = 0.1  # standard deviation of the Gaussian noise

                pixel_size = int(self.size * self.win.size[0] / 2)

                noise = np.random.normal(mean, std, (pixel_size, pixel_size, 3))  # create noise in RGB format
                noise = np.clip(noise, 0, 1)  # clip values to be between 0 and 1

                # Create an ImageStim with the noise texture
                noise_texture = visual.ImageStim(self.win, image=noise, size=(self.size, self.size), pos=pos)

                # Draw the noise texture (which will appear as a rectangle with Gaussian noise)
                noise_texture.draw()

    class ConfidentResponse:
        def __init__(self, win):

            self.win = win

            self.instruction_text = visual.ImageStim(
                win=self.win,
                image="Images/color_task/Confident.jpg",
                units="pix"
            )

            self.confidence_slider = visual.Slider(
                win=win,
                startValue=1,
                size=(1, 0.05),
                pos=(0, -0.3),
                ticks=(0, 1, 2, 3, 4, 5),
                granularity=1,
                labels=["0", "1", "2", "3", "4", "5"],
                style='rating'
            )
            self.current_value_text = visual.TextStim(win, text='1', pos=(0.55, -0.3), height=0.03)

        def get_confidence(self, timeout=5):
            response_clock = core.Clock()
            timeout_clock = core.Clock()

            while timeout_clock.getTime() < timeout:
                # Draw the slider and text
                self.instruction_text.draw()
                self.confidence_slider.draw()
                self.current_value_text.draw()
                self.win.flip()

                # Update the text to show the current slider value
                current_confidence = self.confidence_slider.getRating()
                if current_confidence is None:
                    current_confidence = 1
                self.current_value_text.text = f'{int(current_confidence)}'

                # Check for keypress to exit
                keys = event.getKeys()
                if 'escape' in keys:
                    core.quit()
                if 'space' in keys:
                    response_time = response_clock.getTime()
                    if self.confidence_slider.getRating() is not None:
                        return self.confidence_slider.getRating(), response_time
                    else:
                        return 1, response_time

            return None, None

        def reset(self):
            self.confidence_slider.reset()
            self.current_value_text.text = '50'

    def _draw_instruction(self):
        self.instruction_text.draw()
        self.win.flip()
        event.waitKeys()

    def _draw_rest(self):
        self.rest_text.draw()
        self.win.flip()
        keys = event.waitKeys(keyList=['s', 'escape'])

    def _draw_draw_training(self, index):
        self.training_img[index].draw()
        self.win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])

    def run(self):

        self._draw_instruction()

        for dummy_index, trial in enumerate(self.dummy_trials):

            self._draw_draw_training(0)

            self.fixation.draw()
            self.win.flip()
            core.wait(self.fixation_delay)  # Present the stimulus for 2 seconds

            # Step2
            self.stimulus.draw(trial['colors'], angle_offset=0.0)
            self.fixation.draw()
            self.win.flip()
            core.wait(self.stimulus_duration)

            # Step3
            self.stimulus.draw_mask()
            self.fixation.draw()
            self.win.flip()
            core.wait(self.mask_duration)

            # Step4
            self.fixation.draw()
            self.win.flip()
            difficulty_condition = trial['difficulty']
            if difficulty_condition == 'Easy':
                core.wait(self.wm_duration_easy)  # Present the stimulus for 2 seconds

            else:
                core.wait(self.wm_duration_hard)

            # Step5

            # index = random.randint(0, self.number_of_rectangles - 1)
            index = trial['selected_index']
            position = self.stimulus.get_position(index)

            # while not event.getKeys(keyList=["space", "escape"]):
            # angle_offset = np.random.uniform(0, 2 * np.pi)
            self._draw_draw_training(1)

            angle_offset = trial['angle_offset']
            _ = self.color_bar.get_feedback_color(position,
                                                  angle_offset,
                                                  timeout=self.config["experiment"][
                                                      "response_timeout"])

            # Step6

            self._draw_draw_training(2)
            _ = self.confident_response.get_confidence(timeout=self.config["experiment"][
                "response_timeout"])

        # TODO Introduction to the task
        response_acc = []
        for block in range(self.n_blocks):

            self.blocks[block].draw()
            self.win.flip()
            core.wait(2)

            for _ in range(self.trial_per_block):
                trial = self.trials.next()
                if trial is None:
                    break

                self.trial_clock.reset()  # Reset the clock at the start of each trial
                self.color_bar.reset()
                self.confident_response.reset()
                # Step 1
                self.fixation.draw()
                self.win.flip()
                core.wait(self.fixation_delay)  # Present the stimulus for 2 seconds

                # Step2
                self.stimulus.draw(trial['colors'], angle_offset=0.0)
                self.fixation.draw()
                self.win.flip()
                core.wait(self.stimulus_duration)

                # Step3
                self.stimulus.draw_mask()
                self.fixation.draw()
                self.win.flip()
                core.wait(self.mask_duration)

                # Step4
                self.fixation.draw()
                self.win.flip()
                difficulty_condition = trial['difficulty']
                if difficulty_condition == 'Easy':
                    core.wait(self.wm_duration_easy)  # Present the stimulus for 2 seconds

                else:
                    core.wait(self.wm_duration_hard)

                # Step5

                # index = random.randint(0, self.number_of_rectangles - 1)
                index = trial['selected_index']
                position = self.stimulus.get_position(index)

                # while not event.getKeys(keyList=["space", "escape"]):
                # angle_offset = np.random.uniform(0, 2 * np.pi)
                angle_offset = trial['angle_offset']
                fb_color, response_time = self.color_bar.get_feedback_color(position,
                                                                            angle_offset,
                                                                            timeout=self.config["experiment"][
                                                                                "response_timeout"])
                if fb_color is not None:
                    fb_color = [(c + 1) / 2 for c in fb_color]
                    fb_color = mpl_colors.rgb_to_hsv(fb_color)

                # Step6

                confidence, confidence_rt = self.confident_response.get_confidence(timeout=self.config["experiment"][
                    "response_timeout"])

                error = hue_difference_signed(reference=trial['colors'][index], feedback=fb_color[0])
                if abs(error) < 30:
                    response_acc.append(1)
                else:
                    response_acc.append(0)
                # Log data for the current trial
                self.this_exp.addData('Stimulus', trial['colors'])
                self.this_exp.addData('Selected Position', index)
                self.this_exp.addData('Angle_offset', angle_offset)
                self.this_exp.addData('Distractor Distance', round_to_nearest(hue_to_degrees(trial['distractor_diff'])))
                self.this_exp.addData('Trial Start', self.trial_clock.getTime())
                self.this_exp.addData('Feedback', fb_color)
                self.this_exp.addData('Response Time', response_time)
                self.this_exp.addData('Confidence', confidence)
                self.this_exp.addData('Confidence Response Time', confidence_rt)
                self.this_exp.addData('Difficulty', difficulty_condition)
                self.this_exp.addData('Error', error)
                self.this_exp.nextEntry()

            if (block + 1) == (self.n_blocks // 2):
                self._draw_rest()

        # Clean up
        # self.this_exp.saveAsWideText(self.filename + '.csv')
        # self.this_exp.saveAsPickle(self.filename)

        accuracy = sum(response_acc) / len(response_acc)

        text = f'Thanks for your attendance!\n Your accuracy: {accuracy * 100.0:.2f}%\nPress space to exit.'

        end_message = visual.TextStim(win=self.win, text=text, height=0.1, pos=(0, 0), color='black')
        end_message.draw()
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])
        self.win.close()
        core.quit()

        # Experiment loop


if __name__ == "__main__":
    experiment = ColorTask("configs/config_color_task.yml")
    experiment.run()
