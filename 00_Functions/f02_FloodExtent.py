""" 
Define Flood Extent

Returns:
    Flood extent and calculation of extent
"""

import ee

def FloodExtent(before_filtered, after_filtered, difference_threshold, aoi, polarization):
    
    # Calculate the difference between the before and after images
    difference = after_filtered.divide(before_filtered);

    # Apply the predefined difference-threshold and create the flood extent mask 
    threshold = difference_threshold;
    difference_binary = difference.gt(threshold);

    # Refine flood result using additional datasets

    # Include JRC layer on surface water seasonality to mask flood pixels from areas
    # of "permanent" water (where there is water > 10 months of the year)


    swater = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').select('seasonality');
    swater_mask = swater.gte(10).updateMask(swater.gte(10));

    # Flooded layer where perennial water bodies (water > 10 mo/yr) is assigned a 0 value
    flooded_mask = difference_binary.where(swater_mask,0);
    # final flooded area without pixels in perennial waterbodies
    flooded = flooded_mask.updateMask(flooded_mask);

    # Compute connectivity of pixels to eliminate those connected to 8 or fewer neighbours
    # This operation reduces noise of the flood extent product 
    connections = flooded.connectedPixelCount();    
    flooded = flooded.updateMask(connections.gte(8));

    # Mask out areas with more than 5 percent slope using a Digital Elevation Model 
    DEM = ee.Image('WWF/HydroSHEDS/03VFDEM');
    terrain = ee.Algorithms.Terrain(DEM);
    slope = terrain.select('slope');
    flooded = flooded.updateMask(slope.lt(5));

    # Calculate flood extent area
    # Create a raster layer containing the area information of each pixel 
    flood_pixelarea = (
        flooded.select(polarization)
        .multiply(ee.Image.pixelArea())
    )

    # Sum the areas of flooded pixels
    # default is set to 'bestEffort: true' in order to reduce compuation time, for a more 
    # accurate result set bestEffort to false and increase 'maxPixels'. 
    flood_stats = flood_pixelarea.reduceRegion(
      reducer= ee.Reducer.sum(),              
      geometry= aoi,
      scale= 10, # native resolution 
      #maxPixels= 1e9,
      bestEffort= True
      )

    # Convert the flood extent to hectares (area calculations are originally given in meters)  
    flood_area_ha = (flood_stats
      .getNumber(polarization)
      .divide(10000)
      .round()
    )

    return difference, flooded, flood_area_ha