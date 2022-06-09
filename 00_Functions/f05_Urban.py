import ee
def Urban(LC, aoi, flooded_res):
    # Using the same MODIS Land Cover Product 
    # Filter urban areas
    urbanmask = LC.eq(13)
    urban = LC.updateMask(urbanmask)

    # Calculate affected urban areas using the resampled flood layer
    urban_affected = (urban
      .mask(flooded_res)
      .updateMask(urban))

    # get pixel area of affected urban layer
    urban_pixelarea = (urban_affected
      .multiply(ee.Image.pixelArea())) # calcuate the area of each pixel 

    # sum pixels of affected cropland layer
    urban_stats = (urban_pixelarea.reduceRegion(
      reducer= ee.Reducer.sum(), #sum all pixels with area information                
      geometry= aoi,
      scale= 500,
      bestEffort= True,
      ))

    # convert area to hectares
    urban_area_ha = (urban_stats
      .getNumber('LC_Type1')
      .divide(100) # Orig 10000
      .round())
    
    return urban, urban_affected, urban_area_ha