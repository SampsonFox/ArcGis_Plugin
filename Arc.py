import arcpy
import os
from arcpy.sa import *
import json
import sys
import shutil

# setting the paths
arcpy.env.workspace = "C:/Users/Sampson/Desktop/Fire_data.gdb"
fc = "C:/Users/Sampson/Desktop/Fire_data.gdb/fire_history_scar_Python"
output = "D:/output"
log_path = "D:/output/save_log.json"

# set the environment extent
arcpy.env.extent = arcpy.Extent(140.428953, -39.136649, 150.033447, -34.056565)

# Open the log file to get the information of the previous operation
with open(log_path) as saving:
    save = json.load(saving)
    start_ID = save[0]
    count = save[0]
    save_time = save[1]
    count += 1

# indicator of how many times the loop goes
loop_time = 1

# set a list to store the field name needed
# put all items into one list which is cursor
fields = ['objectid', 'Shape', 'count']
cursor = arcpy.SearchCursor(fc, fields)

# Put the base raster image into a variation
fire = Raster('D:/output/Raster/Fire0')

# iterates through the cursor list
for row in cursor:

    fid = str(count)

    print ('objectid: {0},count: {1}'.format(fid, row.count))

    # set the name of the isolated vector layers
    filename_vector = str("Fire" + str(count) + '.shp')

    # the Feature Class To Feature Class tool will isolate every item within the main fire layer
    arcpy.FeatureClassToFeatureClass_conversion('fire_history_scar_Python',
                                                os.path.join(output, 'Vector'),
                                                filename_vector,
                                                '"objectid" = {}'.format(fid))

    # set the manes for converted raster file
    filename_raster = str("Fire" + str(count))

    # covert every isolated polygon into raster layer
    arcpy.PolygonToRaster_conversion(os.path.join(output, 'Vector', filename_vector),
                                    'count', os.path.join(output, 'Raster', filename_raster)
                                    , 'CELL_CENTER', 'count', 0.001)
    temp_raster = Raster(os.path.join(output, 'Raster', filename_raster))

    # set names for calculated vector layer
    filename_raster_0 = str("Fire" + str(count) + '_0')

    # use the RasterCalculator to covert the Null pixel to 0
    arcpy.gp.RasterCalculator('Con(IsNull("{0}"),0,"{0}")'.format(temp_raster),
                              os.path.join(output, 'Raster', filename_raster_0),)

    current_raster = Raster(os.path.join(output, 'Raster', filename_raster_0))

    if count != 1:

        # Use the raster calculator to calculate the new raster layer and accumulation layer
        fire = Plus(current_raster, fire)

        # Save the result every 10 steps
        if not loop_time % 10:
            fire.save(os.path.join('D:/output/Results', 'Result' + str(save_time)))
            print ('Saved! Result' + str(save_time))
            # we can also delete all wasted result using following codes

            # hutil.rmtree('D:/output/Results/result' + str(save_time - 1))
            # os.remove('D:/output/Results/Result' + str(save_time - 1) + '.aux.xml')
            save_time += 1

    # count = 1 means this script is running under the first time, so the raster1_0 will become the new base map
    else:
        fire = current_raster

    # open the log file and save current situation
    with open(log_path,'w') as saving:
        save = [count, save_time]
        json.dump(save, saving)

    count += 1
    loop_time += 1

    # the limitation of how many times this script will run in each round
    if loop_time == 11:
        break

end_ID = count

# show the information of which layer was interpreted in this round
print ('Completed! Form ' + str(start_ID) + ' to ' + str(end_ID))

