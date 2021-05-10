import arcpy
import os
from arcpy.sa import *
from Settings import Settings
from Reset import reset
import time

reset()
# setting the paths
Settings = Settings()
arcpy.env.workspace = Settings.output
fc = Settings.fc
output = Settings.output
log_path = Settings.log_path
result_path = Settings.result_path

# set the environment extent
arcpy.env.extent = arcpy.Extent(140.428953, -39.136649, 150.033447, -34.056565)

# Open the log file to get the information of the previous operation
count = 1

# indicator of how many times the loop goes
loop_time = 1

# set a list to store the field name needed
# put all items into one list which is cursor
fields = ['objectid', 'Shape', 'count']

# Put the base raster image into a variation
fire = Raster('D:/output/Raster/Fire0')

# iterates through the cursor list
for row in range(10, 21):

    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    fid = str(count)

    print t

    # set the name of the isolated vector layers
    filename_vector = str("Fire" + str(count) + '.shp')

    os.mkdir(os.path.join(output, 'Vector', "Fire" + str(count)))

    # the Feature Class To Feature Class tool will isolate every item within the main fire layer
    arcpy.FeatureClassToFeatureClass_conversion(os.path.join(output, 'Fire_data.gdb', 'fire_history_scar_Python_20' + str(22 - loop_time)),
                                                os.path.join(output, 'Vector', "Fire" + str(count)),
                                                filename_vector)

    print (str(os.path.join(output, 'Fire_data.gdb', 'fire_history_scar_Python_20' + str(22 - loop_time))))

    # set the manes for converted raster file
    filename_raster = str("Fire" + str(count))

    # covert every isolated polygon into raster layer
    arcpy.PolygonToRaster_conversion(os.path.join(output, 'Vector', "Fire" + str(count), filename_vector),
                                    'count', os.path.join(output, 'Raster', filename_raster)
                                    , 'CELL_CENTER', 'count', 0.001)

    temp_raster = Raster(os.path.join(output, 'Raster', filename_raster))

    # set names for calculated vector layer
    filename_raster_0 = str("Fire" + str(count) + '_0')

    # use the RasterCalculator to covert the Null pixel to 0
    arcpy.gp.RasterCalculator('Con(IsNull("{0}"),0,"{0}")'.format(temp_raster),
                              os.path.join(output, 'Raster', filename_raster_0))

    current_raster = Raster(os.path.join(output, 'Raster', filename_raster_0))
    #fire.append(current_raster)

    if loop_time != 1:

        # Use the raster calculator to calculate the new raster layer and accumulation layer
        fire = Plus(current_raster, fire)

        # Save the result every 10 steps
        if loop_time:

            # raster = Plus(fire[0], fire[1], fire[2], fire[3], fire[4], fire[5], fire[6], fire[7], fire[8], fire[9])
            fire.save(os.path.join(result_path, 'Result' + str(count)))
            print ('Saved! Result' + str(count) + ' ' + str(t))

    # count = 1 means this script is running under the first time, so the raster1_0 will become the new base map
    elif loop_time == 1:
        fire = current_raster

    # open the log file and save current situation

    count += 1
    loop_time += 1

    # the limitation of how many times this script will run in each round

end_ID = count

# show the information of which layer was interpreted in this round
print ('Completed! Form ' + ' to ' + str(end_ID))

