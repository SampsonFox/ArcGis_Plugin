import arcpy
import os

class Settings():

    def __init__(self):

        # setting the paths
        self.output = "D:/output"
        self.fc = "D:/output/Fire_data.gdb/fire_history_scar_Python_2021"
        self.log_path = "D:/output/save_log.json"
        self.result_path = os.path.join(self.output, 'Result_1021', 'Result_2021')

