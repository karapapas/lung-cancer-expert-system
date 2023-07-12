import numpy as np

class Utils:
    
    def __init__(self):
        pass
        
    def gaussian(self, min_value, max_value):
        mean = (max_value + min_value) / 2.0
        std_dev = (max_value - min_value) / 4.0
        while True:
            sample = np.random.normal(mean, std_dev)
            if min_value <= sample <= max_value:
                return sample
            