import arcpy
import os
from arcpy.sa import *
import json
import sys
import shutil
from Settings import Settings

Setting = Settings()
a = Setting.output
b = Raster(os.path.join(a, 'Results', 'result31'))