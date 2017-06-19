import numpy as np

mode = "train"
stream = "n"
is_new = "r"
is_calibration = False
c = "1025"

is_found = 0

learner = "na"
ver = ""

count_calibration = 0
FRAMES_CALIBRATION = 10
calibration_numbers = np.array([0 for n in range(132)]).astype(np.int64)
array_calibration = []
count_calibration = 0
is_calibration = False

fitted_data = None

face_expression = ["normal", "happy", "angry", "suprised", "sad", "others"]
