This Python script automates the processing of geospatial data within QGIS. It is designed to facilitate the preparation of road network data for further analysis and integration with other spatial datasets. The processed vectors can be use to import to hydraulic modelling software with no overlapping errors. For example, I use the processed vectors to import as mesh zones, roughness zones and infiltration zones to Infoworks ICM software.

The script includes the following key steps:

1. Buffering Road Networks: Creates a buffer around road centerlines with customizable parameters, including buffer distance and style options for end caps and joins. Road centrelines extracted from public GIS data from Australian councils can be buffered to user desired widths.

2. Conversion to Single Parts: Splits multipart geometries into single-part geometries, ensuring that each feature is represented individually.

3. Adding Auto-incremental Fields: Introduces unique identifiers for each feature, starting from a specified number, to aid in data management and analysis. This is to avoid errors of unique ID in modelling software.

4. Difference Operation: Subtracts building footprint geometries from the buffered road data, removing overlaps and refining the dataset. This is to avoid overlap errors in modelling software.

Output as Shapefile: The final processed layer is saved as a shapefile, named "ICM_ROADS.shp", and is also loaded into the current QGIS session for immediate use.

This script is particularly useful for urban planning, flood modeling, and other geospatial analyses. It ensures compatibility and accuracy when importing data into specialized software such as InfoWorks ICM. The output is tailored to be error-free and ready for further modeling and analysis.

Instructions for Use:

-Modify the file paths and parameters as needed for your specific data and analysis requirements.
-Run the script within the QGIS Python Console or as a standalone script, ensuring that QGIS and necessary dependencies are installed. Make sure you save your file before running the script.
