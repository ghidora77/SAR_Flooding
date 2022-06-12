"""
Primary SAR Function

Returns:
    Before and after filtered image
"""
import ee
def SAR(
    aoi, polarization, pass_direction, 
    difference_threshold, before_start, 
    before_end, after_start, after_end
    ):

    # Load and filter Sentinel-1 GRD data by predefined parameters 
    collection= (
        ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.eq('instrumentMode','IW'))
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', polarization))
        .filter(ee.Filter.eq('orbitProperties_pass',pass_direction))
        .filter(ee.Filter.eq('resolution_meters',10))
        #.filter(ee.Filter.eq('relativeOrbitNumber_start',relative_orbit ))
        .filterBounds(aoi)
        .select(polarization)
    )

    # Select images by predefined dates
    before_collection = collection.filterDate(before_start, before_end)
    after_collection = collection.filterDate(after_start,after_end)

    # Create a mosaic of selected tiles and clip to study area
    before = before_collection.mosaic().clip(aoi)
    after = after_collection.mosaic().clip(aoi)

    # Apply reduce the radar speckle by smoothing  
    smoothing_radius = 10;
    before_filtered = before.focal_mean(smoothing_radius, 'circle', 'meters')
    after_filtered = after.focal_mean(smoothing_radius, 'circle', 'meters')
    
    return before_filtered, after_filtered