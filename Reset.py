def reset():

    import shutil
    import arcpy
    import os
    import json
    from Settings import Settings

    Settings = Settings()
    arcpy.env.workspace = Settings.output
    fc = Settings.fc
    output = Settings.output
    log_path = Settings.log_path

    if os.path.exists(os.path.join(output, 'Vector')):
        shutil.rmtree(os.path.join(output, 'Vector'))

    os.mkdir(os.path.join(output, 'Vector'))

    # if os.path.exists(os.path.join(output, 'Results')):
        # shutil.rmtree(os.path.join(output, 'Results'))

    # os.mkdir(os.path.join(output, 'Results'))

    if os.path.exists(os.path.join(output, 'Raster')):
        shutil.rmtree(os.path.join(output, 'Raster'))

    shutil.copytree(os.path.join(output, 'Raster_base'), os.path.join(output, 'Raster'))

    if 0:
        with open(log_path, 'w') as o:
            reset = [0, 1]
            json.dump(reset, o)

    print ('Reset Completed!')
