import arcpy
import numpy as np
import random

def cellular_automata_model(land_use_raster, suitability_raster, land_use_type, change_type, neighborhood_type, neighborhood_threshold, suitability_threshold, max_changes, output_raster_path, constraint_raster=None):
    # Load raster data into numpy arrays
    land_use_info = arcpy.Describe(land_use_raster)
    suitability_info = arcpy.Describe(suitability_raster)
    
    # Handle NoData value
    land_use_no_data_value = land_use_info.noDataValue if land_use_info.noDataValue is not None else -9999
    suitability_no_data_value = suitability_info.noDataValue if suitability_info.noDataValue is not None else -9999

    land_use_array = arcpy.RasterToNumPyArray(land_use_raster, nodata_to_value=land_use_no_data_value)
    suitability_array = arcpy.RasterToNumPyArray(suitability_raster, nodata_to_value=suitability_no_data_value)
    
    # Initialize output array
    output_array = land_use_array.copy()
    
    # Define neighborhood offsets
    if neighborhood_type == "Moore":
        neighborhood_offsets = [(-1, -1), (-1, 0), (-1, 1), 
                                (0, -1), (0, 1), 
                                (1, -1), (1, 0), (1, 1)]
    elif neighborhood_type == "Von Neumann":
        neighborhood_offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    elif neighborhood_type == "Extended Moore":
        neighborhood_offsets = [(dr, dc) for dr in range(-2, 3) for dc in range(-2, 3) if not (dr == 0 and dc == 0)]
    elif neighborhood_type == "Extended Von Neumann":
        neighborhood_offsets = [(dr, dc) for dr in range(-2, 3) for dc in range(-2, 3) if abs(dr) + abs(dc) <= 2 and not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Invalid neighborhood type. Choose from 'Moore', 'Von Neumann', 'Extended Moore', or 'Extended Von Neumann'.")
    
    # Get the set of valid land use types
    valid_land_use_types = np.unique(land_use_array[land_use_array != land_use_no_data_value])
    
    # Load constraint raster if provided
    if constraint_raster:
        constraint_array = arcpy.RasterToNumPyArray(constraint_raster, nodata_to_value=0)
    else:
        constraint_array = np.zeros_like(land_use_array)

    if change_type == "expansion":
        rows, cols = np.where((land_use_array != land_use_type) & (land_use_array != land_use_no_data_value) & (constraint_array != 1))
    else:
        rows, cols = np.where((land_use_array == land_use_type) & (constraint_array != 1))
    
    available_cells = list(zip(rows, cols))
    random.shuffle(available_cells)

    changed_cells = 0

    # Iterate over cells until max_changes is reached
    for row, col in available_cells:
        if changed_cells >= max_changes:
            break
        
        # Calculate neighborhood count
        count = 0
        neighborhood_values = []
        for dr, dc in neighborhood_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < land_use_array.shape[0] and 0 <= nc < land_use_array.shape[1]:
                if land_use_array[nr, nc] == land_use_type:
                    count += 1
                if land_use_array[nr, nc] != land_use_no_data_value:
                    neighborhood_values.append(land_use_array[nr, nc])
        
        # Check neighborhood and suitability thresholds
        if count >= neighborhood_threshold and suitability_array[row, col] >= suitability_threshold:
            if change_type == "expansion":
                output_array[row, col] = land_use_type
            else:
                if len(neighborhood_values) > 0:
                    new_land_use_type = np.bincount(neighborhood_values).argmax()
                    # Ensure the new land use type is one of the valid types
                    if new_land_use_type in valid_land_use_types:
                        output_array[row, col] = new_land_use_type
            changed_cells += 1

    # Ensure the output values are within the range of original land use values
    for value in np.unique(output_array):
        if value not in valid_land_use_types and value != land_use_no_data_value:
            output_array[output_array == value] = land_use_type

    # Save output raster with coordinate system information
    x_cell_size = land_use_info.meanCellWidth
    y_cell_size = land_use_info.meanCellHeight
    lower_left_corner = arcpy.Point(land_use_info.extent.XMin, land_use_info.extent.YMin)
    spatial_reference = land_use_info.spatialReference
    
    output_raster = arcpy.NumPyArrayToRaster(output_array, lower_left_corner, x_cell_size, y_cell_size, land_use_no_data_value)
    arcpy.DefineProjection_management(output_raster, spatial_reference)
    output_raster.save(output_raster_path)

if __name__ == "__main__":
    # Parameters
    land_use_raster = arcpy.GetParameterAsText(0)
    suitability_raster = arcpy.GetParameterAsText(1)
    land_use_type = int(arcpy.GetParameterAsText(2))
    change_type = arcpy.GetParameterAsText(3).lower()  # "expansion" or "retraction"
    neighborhood_type = arcpy.GetParameterAsText(4)  # "Moore", "Von Neumann", "Extended Moore", or "Extended Von Neumann"
    neighborhood_threshold = int(arcpy.GetParameterAsText(5))
    suitability_threshold = float(arcpy.GetParameterAsText(6))
    max_changes = int(arcpy.GetParameterAsText(7))
    output_raster_path = arcpy.GetParameterAsText(8)
    constraint_raster = arcpy.GetParameterAsText(9) if arcpy.GetParameterAsText(9) else None

    # Run the model
    cellular_automata_model(land_use_raster, suitability_raster, land_use_type, change_type, neighborhood_type, neighborhood_threshold, suitability_threshold, max_changes, output_raster_path, constraint_raster)
