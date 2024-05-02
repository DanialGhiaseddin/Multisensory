from psychopy import visual, core, event

# Create a window
win = visual.Window(size=(800, 600))

# Define the slider
slider = visual.Slider(win=win, ticks=(0, 1), labels=['Red', 'Violet'], granularity=0.01,
                       style='slider', pos=(0, -0.4), size=(0.8, 0.1), color='LightGray')

# Create a feedback stimulus (e.g., a circle)
feedback = visual.Circle(win, radius=0.1, fillColor='white', lineColor='white', pos=(0, 0.2))

# Experiment loop
while not event.getKeys(keyList=["escape"]):
    if slider.rating is not None:
        # Map the slider value to a color in the spectrum
        color_value = slider.getRating()  # This will be a value between 0 and 1
        color = [color_value - 1, 1 - color_value, color_value]  # This is a simple RGB color mapping

        # Update the feedback color
        feedback.fillColor = color
        feedback.lineColor = color

    # Draw the slider and feedback
    slider.draw()
    feedback.draw()
    win.flip()

# Cleanup
win.close()
core.quit()
