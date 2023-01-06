
def initialize_psychopy(config):
    from psychopy import prefs
    prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']
    prefs.hardware['audioLatencyMode'] = 3
