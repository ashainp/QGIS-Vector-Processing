from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProject,
    QgsVectorFileWriter
)
from qgis.analysis import QgsNativeAlgorithms
import processing

# Start QGIS application
QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Add algorithms
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# User-defined file paths
roads_file = 'C:/Users/enoks/Desktop/test qgis/24000_HOME/05 - Data/Data In/The List/1721175336247330818096/RoadCentrelines.shp'
overlay_file = 'C:/Users/enoks/Desktop/test qgis/24000_HOME/05 - Data/Data In/The List/1721175336247330818096/BuildingFootprints.shp'
output_path = 'C:/Users/enoks/Desktop/test qgis/24000_HOME/08 - Model Files/QGIS/ICM_ROADS.shp'

# Load the roads shapefile
roads_layer = QgsVectorLayer(roads_file, 'Roads', 'ogr')
if not roads_layer.isValid():
    print("Layer failed to load!")
else:
    # Set buffer parameters
    buffer_distance = 4  # in meters
    end_cap_style = 0  # 0=Round, 1=Flat, 2=Square
    join_style = 0  # 0=Round, 1=Miter, 2=Bevel
    dissolve = True

    # Prepare the buffer processing parameters
    buffer_params = {
        'INPUT': roads_layer,
        'DISTANCE': buffer_distance,
        'END_CAP_STYLE': end_cap_style,
        'JOIN_STYLE': join_style,
        'MITER_LIMIT': 2,
        'DISSOLVE': dissolve,
        'OUTPUT': 'memory:'  # Temporary layer in memory
    }

    # Run the buffer process and load result as a temporary layer
    buffered_result = processing.run("native:buffer", buffer_params)['OUTPUT']

    # Run Multipart to Singleparts
    singleparts_params = {
        'INPUT': buffered_result,
        'OUTPUT': 'memory:'  # Temporary layer in memory
    }

    singleparts_result = processing.run("native:multiparttosingleparts", singleparts_params)['OUTPUT']

    # Add auto-incremental field
    auto_increment_params = {
        'INPUT': singleparts_result,
        'FIELD_NAME': 'UID',
        'START': 888,
        'GROUP_FIELDS': None,  # No grouping field
        'SORT_ASCENDING': True,
        'SORT_NULLS_FIRST': False,
        'OUTPUT': 'memory:'  # Temporary layer in memory
    }

    auto_increment_result = processing.run("native:addautoincrementalfield", auto_increment_params)['OUTPUT']

    # Load the overlay layer (Building footprints)
    overlay_layer = QgsVectorLayer(overlay_file, 'BuildingFootprints', 'ogr')
    if not overlay_layer.isValid():
        print("Overlay layer failed to load!")
    else:
        # Perform the Difference operation
        difference_params = {
            'INPUT': auto_increment_result,
            'OVERLAY': overlay_layer,
            'OUTPUT': 'memory:'  # Temporary layer in memory
        }

        difference_result = processing.run("native:difference", difference_params)['OUTPUT']

        # Save the final layer to the specified output path
        QgsVectorFileWriter.writeAsVectorFormat(difference_result, output_path, "UTF-8", difference_result.crs(), "ESRI Shapefile")

        # Load the saved layer into QGIS
        final_layer = QgsVectorLayer(output_path, "ICM ROADS", "ogr")
        if final_layer.isValid():
            QgsProject.instance().addMapLayer(final_layer)
            print(f"Final processed layer has been saved to {output_path} and loaded into QGIS.")
        else:
            print("Failed to load the saved layer into QGIS.")

# Do not exit QGIS if running within the application
# qgs.exitQgis()
