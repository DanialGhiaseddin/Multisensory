from psychopy import visual, core
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), color=(1, 1, 1), units='pix')

# Generate Gaussian noise
width, height = 200, 200
mean = 0.5  # mean of the Gaussian noise
std = 0.1  # standard deviation of the Gaussian noise
noise = np.random.normal(mean, std, (height, width, 3))  # create noise in RGB format
noise = np.clip(noise, 0, 1)  # clip values to be between 0 and 1

# Create an ImageStim with the noise texture
noise_texture = visual.ImageStim(win, image=noise, size=(width, height))

# Draw the noise texture (which will appear as a rectangle with Gaussian noise)
noise_texture.draw()

# Display the window
win.flip()

# Keep the window open for a while
core.wait(5)

# Close the window
win.close()
