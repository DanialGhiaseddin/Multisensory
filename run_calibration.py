import yaml
from screeninfo import get_monitors
from experiment import experiment
from analyze.result_analyzer import compute_compensation_offset

with open("configs/config_calibration.yml", "r") as yml_file:
    config_file = yaml.safe_load(yml_file)

if config_file["screen"]["size"] == "full-screen":
    config_file["screen"]["size"] = [get_monitors()[0].width, get_monitors()[0].width]

result_file = experiment(config_file, 0)

