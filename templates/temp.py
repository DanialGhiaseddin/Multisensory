import psychopy.visual
import psychopy.event

win = psychopy.visual.Window(
    size=[400, 400],
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

line = psychopy.visual.Line(
    win=win,
    units="pix",
    lineColor=[-1, -1, -1]
)

line.start = [-200, -200]
line.end = [+200, +200]

line.draw()

win.flip()

psychopy.event.waitKeys()

win.close()