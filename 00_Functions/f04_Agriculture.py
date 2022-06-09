import ee
def Agriculture(aoi, flooded, after_end, polarization):
    # using MODIS Land Cover Type Yearly Global 500m
    # filter image collection by the most up-to-date MODIS Land Cover product 

    # using MODIS Land Cover Type Yearly Global 500m
    # filter image collection by the most up-to-date MODIS Land Cover product 
    LC = (ee.ImageCollection('MODIS/006/MCD12Q1')
      .filterDate('2014-01-01',after_end)
      .sort('system:index',False)
      .select("LC_Type1")
      .first()
      .clip(aoi))

    # Extract only cropland pixels using the classes cropland (>60%) and Cropland/Natural 
    # Vegetation Mosaics: mosaics of small-scale cultivation 40-60% incl. natural vegetation
    cropmask = (LC.eq(12).Or(LC.eq(14)))
    cropland = (LC.updateMask(cropmask))

    # get MODIS projection
    MODISprojection = LC.projection();

    # Reproject flood layer to MODIS scale
    flooded_res = (flooded
        .reproject(
        crs= MODISprojection
      ))

    # Calculate affected cropland using the resampled flood layer
    cropland_affected = flooded_res.updateMask(cropland)

    # get pixel area of affected cropland layer
    #calcuate the area of each pixel 
    crop_pixelarea = cropland_affected.multiply(ee.Image.pixelArea())

    # sum pixels of affected cropland layer
    crop_stats = (crop_pixelarea.reduceRegion(
      reducer= ee.Reducer.sum(), # sum all pixels with area information                
      geometry= aoi,
      scale= 500,
      maxPixels= 1e9
      ))

    # convert area to hectares
    crop_area_ha = (crop_stats
      .getNumber(polarization)
      .divide(10000)
      .round())

    #  Affected urban area
    
    return cropland, cropland_affected, crop_area_ha, LC, flooded_res