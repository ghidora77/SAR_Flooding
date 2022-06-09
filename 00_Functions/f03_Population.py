import ee
def Population(aoi, flooded):

    # Load JRC Global Human Settlement Popluation Density layer
    # Resolution: 250. Number of people per cell is given.
    population_count = ee.Image('JRC/GHSL/P2016/POP_GPW_GLOBE_V1/2015').clip(aoi);

    # Calculate the amount of exposed population
    # get GHSL projection
    GHSLprojection = population_count.projection();

    # Reproject flood layer to GHSL scale
    flooded_res1 = (flooded
        .reproject(
        crs= GHSLprojection
        ))

    # Create a raster showing exposed population only using the resampled flood layer
    population_exposed = (population_count
      .updateMask(flooded_res1)
      .updateMask(population_count))

    # Sum pixel values of exposed population raster 
    stats = (population_exposed.reduceRegion(
      reducer= ee.Reducer.sum(),
      geometry= aoi,
      scale= 250,
      maxPixels=1e9 
    ))

    # get number of exposed people as integer
    number_pp_exposed = stats.getNumber('population_count').round();
    
    return population_count, population_exposed, number_pp_exposed