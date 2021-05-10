import arcpy
import os
from arcpy.sa import *
import json
import shutil
from Settings import Settings
from Reset import reset
import time

t = time.time()
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

if len(os.listdir(os.path.join(output, 'Results'))) and save_time != 1:
    fire = Raster(os.path.join(output, 'Results', 'Result' + str(save_time-1)))

# iterates through the cursor list
for row in cursor:

    fid = str(count)

    print ('objectid: {0},count: {1}, loop time: {2}'.format(fid, row.count, loop_time))

    # set the name of the isolated vector layers
    filename_vector = str("Fire" + str(count) + '.shp')

    os.mkdir(os.path.join(output, 'Vector', "Fire" + str(count)))

    # the Feature Class To Feature Class tool will isolate every item within the main fire layer
    arcpy.FeatureClassToFeatureClass_conversion(fc,
                                                os.path.join(output, 'Vector', "Fire" + str(count)),
                                                filename_vector,
                                                '"objectid" = {0}'.format(fid))

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

    if loop_time > 50:
        # remove extra vector layer
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.cpg'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.dbf'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.prj'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.sbn'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.sbx'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.shp'))
        #os.remove(os.path.join(output, 'Vector', "Fire" + str(count - 20) + '.shx'))
        if os.path.exists(os.path.join(output, 'Vector', "Fire" + str(count - 20))):
            shutil.rmtree(os.path.join(output, 'Vector', "Fire" + str(count - 20)))

        # remove extra raster layer
        shutil.rmtree(os.path.join(output, 'Raster', "Fire" + str(count - 20)))
        shutil.rmtree(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '_0'))
        os.remove(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '.ovr'))

        if os.path.exists(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '.aux.xml')):
            os.remove(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '.aux.xml'))

        if os.path.exists(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '_0.aux.xml')):
            os.remove(os.path.join(output, 'Raster', "Fire" + str(count - 20) + '_0.aux.xml'))

    #if loop_time == 1:
        #fire = Raster(os.path.join('D:/output/Results', 'Result' + str(save_time)))

    if loop_time != 1:

        # Use the raster calculator to calculate the new raster layer and accumulation layer
        fire = Plus(current_raster, fire)

        # Save the result every 10 steps
        if not loop_time % 10:

            # raster = Plus(fire[0], fire[1], fire[2], fire[3], fire[4], fire[5], fire[6], fire[7], fire[8], fire[9])
            fire.save(os.path.join(result_path, 'Result' + str(save_time)))
            print ('Saved! Result' + str(save_time) + ' ' + str(t))

            if loop_time > 110:
                # delete extra result
                os.remove(os.path.join(output, 'Raster', "Fire" + str(count - 10) + '_0.aux.xml'))
                print ('Removed! ' + str(save_time - 10))

            save_time += 1
            # fire = [Raster('D:/output/Raster/Fire0')]
            with open(log_path, 'w') as saving:
                save = [count, save_time]
                json.dump(save, saving)



    # count = 1 means this script is running under the first time, so the raster1_0 will become the new base map
    elif count == 1:
        fire = current_raster

    # open the log file and save current situation


    count += 1
    loop_time += 1

    # the limitation of how many times this script will run in each round
    if loop_time == 2000:
        break

end_ID = count

# show the information of which layer was interpreted in this round
print ('Completed! Form ' + str(start_ID) + ' to ' + str(end_ID))

