# Cellular Automata Model Script Tool for ArcGIS Pro

This repository contains a Python script tool for ArcGIS Pro that implements a cellular automata model for land-use change. The tool can simulate the expansion or retraction of a specified land-use type based on neighborhood and suitability criteria.

## Features

- **Land-use type modeling**: Choose the land-use type to be modeled (e.g., Urban). This can be used for various scenarios like urbanization (expansion) or deforestation (retraction).
- **Change type**: Select either expansion or retraction. Expansion simulates the growth of the selected land-use type, while retraction simulates its reduction.
- **Neighborhood types**: Four different neighborhood types (Moore, Von Neumann, Extended Moore, Extended Von Neumann) allow for flexible modeling of spatial influences on land-use change.
- **Threshold settings**: Specify thresholds for neighborhood influence and suitability. Cells with a suitability value greater than the threshold and a sufficient number of neighboring cells of the same land-use type can be converted.
- **Constraints**: Optionally provide a constraint raster to prevent changes in certain areas. This allows for the simulation of land-use change within specific spatial constraints.

## Model Explanation

The cellular automata model works by iteratively evaluating each cell in the input land-use raster. For each cell, the model checks its neighborhood and suitability value to determine if it should be converted to the specified land-use type.

- **Expansion**: In expansion mode, cells that are not currently of the selected land-use type can be converted based on their neighborhood and suitability value. If a cell meets the specified criteria, it is converted to the selected land-use type in the next iteration.
- **Retraction**: In retraction mode, cells that are currently of the selected land-use type can be converted based on their neighborhood and suitability value. If a cell meets the specified criteria, it is converted to the dominant land-use type in its neighborhood in the next iteration.

Randomization is applied to select cells for conversion, ensuring that the model does not always prioritize cells in a specific order. This helps create more realistic and varied land-use change patterns.


## Parameters

1. **Land Use Raster**:
   - **Data Type**: Raster Layer
   - The input land-use raster dataset.

2. **Suitability Raster**:
   - **Data Type**: Raster Layer
   - The input suitability raster dataset.

3. **Land Use Type**:
   - **Data Type**: Long
   - **Filter**: Value List
   - The land-use type to be modeled (e.g., 4).

4. **Change Type**:
   - **Data Type**: String
   - **Filter**: Value List
   - The type of change to model ("expansion" or "retraction").

5. **Neighborhood Type**:
   - **Data Type**: String
   - **Filter**: Value List
   - The type of neighborhood to consider ("Moore", "Von Neumann", "Extended Moore", or "Extended Von Neumann").

6. **Neighborhood Threshold**:
   - **Data Type**: Double
   - The threshold for the number of neighboring cells of the same land-use type.

7. **Suitability Threshold**:
   - **Data Type**: Double
   - The threshold for the suitability value.

8. **Max Changes**:
   - **Data Type**: Long
   - The maximum number of cells to change.

9. **Output Raster Path**:
   - **Data Type**: Raster Layer
   - The file path for the output raster dataset.

10. **Constraint Raster** (optional):
    - **Data Type**: Raster Layer
    - The constraint raster dataset where cells with value `1` will not be changed.

## Example

An example land-use dataset and suitability raster are included in the repository. These datasets can be used to test the script tool and understand how the parameters affect the output.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or further information, please contact [your email] or visit [your website].


