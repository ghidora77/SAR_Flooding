//------------------------------------- EXPORTS ------------------------------------//
# Export flooded area as TIFF file 
Export.image.toDrive({
  image: flooded, 
  description: 'Flood_extent_raster',
  fileNamePrefix: 'flooded',
  region: aoi, 
  maxPixels: 1e10
});

# Export flooded area as shapefile (for further analysis in e.g. QGIS)
# Convert flood raster to polygons
flooded_vec = flooded.reduceToVectors({
  scale: 10,
  geometryType:'polygon',
  geometry: aoi,
  eightConnected: false,
  bestEffort:true,
  tileScale:2,
});

# Export flood polygons as shape-file
Export.table.toDrive({
  collection:flooded_vec,
  description:'Flood_extent_vector',
  fileFormat:'SHP',
  fileNamePrefix:'flooded_vec'
});

# Export auxcillary data as shp?
# Exposed population density
Export.image.toDrive({
  image:population_exposed,
  description:'Exposed_Populuation',
  scale: 250,
  fileNamePrefix:'population_exposed',
  region: aoi,
  maxPixels:1e10
});

//---------------------------------- MAP PRODUCTION --------------------------------//

//-------------------------- Display the results on the map -----------------------//

# set position of panel where the results will be displayed 
results = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '8px 15px',
    width: '350px'
  }
});

//Prepare the visualtization parameters of the labels 
textVis = {
  'margin':'0px 8px 2px 0px',
  'fontWeight':'bold'
  };
numberVIS = {
  'margin':'0px 0px 15px 0px', 
  'color':'bf0f19',
  'fontWeight':'bold'
  };
subTextVis = {
  'margin':'0px 0px 2px 0px',
  'fontSize':'12px',
  'color':'grey'
  };

titleTextVis = {
  'margin':'0px 0px 15px 0px',
  'fontSize': '18px', 
  'font-weight':'', 
  'color': '3333ff'
  };

# Create lables of the results 
# Titel and time period
title = ui.Label('Results', titleTextVis);
text1 = ui.Label('Flood status between:',textVis);
number1 = ui.Label(after_start.concat(" and ",after_end),numberVIS);

# Alternatively, print dates of the selected tiles
//number1 = ui.Label('Please wait...',numberVIS); 
//(after_collection).evaluate(function(val){number1.setValue(val)}),numberVIS;

# Estimated flood extent 
text2 = ui.Label('Estimated flood extent:',textVis);
text2_2 = ui.Label('Please wait...',subTextVis);
dates(after_collection).evaluate(function(val){text2_2.setValue('based on Senintel-1 imagery '+val)});
number2 = ui.Label('Please wait...',numberVIS); 
flood_area_ha.evaluate(function(val){number2.setValue(val+' hectares')}),numberVIS;

# Estimated number of exposed people
text3 = ui.Label('Estimated number of exposed people: ',textVis);
text3_2 = ui.Label('based on GHSL 2015 (250m)',subTextVis);
number3 = ui.Label('Please wait...',numberVIS);
number_pp_exposed.evaluate(function(val){number3.setValue(val)}),numberVIS;

# Estimated area of affected cropland 
MODIS_date = ee.String(LC.get('system:index')).slice(0,4);
text4 = ui.Label('Estimated affected cropland:',textVis);
text4_2 = ui.Label('Please wait', subTextVis)
MODIS_date.evaluate(function(val){text4_2.setValue('based on MODIS Land Cover '+val +' (500m)')}), subTextVis;
number4 = ui.Label('Please wait...',numberVIS);
crop_area_ha.evaluate(function(val){number4.setValue(val+' hectares')}),numberVIS;

# Estimated area of affected urban
text5 = ui.Label('Estimated affected urban areas:',textVis);
text5_2 = ui.Label('Please wait', subTextVis)
MODIS_date.evaluate(function(val){text5_2.setValue('based on MODIS Land Cover '+val +' (500m)')}), subTextVis;
number5 = ui.Label('Please wait...',numberVIS);
urban_area_ha.evaluate(function(val){number5.setValue(val+' hectares')}),numberVIS;

# Disclaimer
text6 = ui.Label('Disclaimer: This product has been derived automatically without validation data. All geographic information has limitations due to the scale, resolution, date and interpretation of the original source materials. No liability concerning the content or the use thereof is assumed by the producer.',subTextVis)

# Produced by...
text7 = ui.Label('Script produced by: UN-SPIDER December 2019', subTextVis)

# Add the labels to the panel 
results.add(ui.Panel([
        title,
        text1,
        number1,
        text2,
        text2_2,
        number2,
        text3,
        text3_2,
        number3,
        text4,
        text4_2,
        number4,
        text5,
        text5_2,
        number5,
        text6,
        text7]
      ));

# Add the panel to the map 
Map.add(results);

//----------------------------- Display legend on the map --------------------------//

# Create legend (*credits to thisearthsite on Open Geo Blog: https://mygeoblog.com/2016/12/09/add-a-legend-to-to-your-gee-map/)
# set position of panel
legend = ui.Panel({
  style: {
    position: 'bottom-right',
    padding: '8px 15px',
  }
});
 
# Create legend title
legendTitle = ui.Label('Legend',titleTextVis);
 
# Add the title to the panel
legend.add(legendTitle);
 
# Creates and styles 1 row of the legend.
makeRow = function(color, name) {
 
      # Create the label that is actually the colored box.
      colorBox = ui.Label({
        style: {
          backgroundColor: color,
          # Use padding to give the box height and width.
          padding: '8px',
          margin: '0 0 4px 0'
        }
      });
 
      # Create the label filled with the description text.
      description = ui.Label({
        value: name,
        style: {margin: '0 0 4px 6px'}
      });
 
      # return the panel
      return ui.Panel({
        widgets: [colorBox, description],
        layout: ui.Panel.Layout.Flow('horizontal')
      });
};
 
#  Palette with the colors
palette =['#0000FF', '#30b21c', 'grey'];
 
# name of the legend
names = ['potentially flooded areas','affected cropland','affected urban'];
 
# Add color and and names
for (i = 0; i < 3; i++) {
  legend.add(makeRow(palette[i], names[i]));
  }  

# Create second legend title to display exposed population density
legendTitle2 = ui.Label({
value: 'Exposed population density',
style: {
fontWeight: 'bold',
fontSize: '15px',
margin: '10px 0 0 0',
padding: '0'
}
});

# Add second title to the panel
legend.add(legendTitle2);

# create the legend image
lon = ee.Image.pixelLonLat().select('latitude');
gradient = lon.multiply((populationExposedVis.max-populationExposedVis.min)/100.0).add(populationExposedVis.min);
legendImage = gradient.visualize(populationExposedVis);
 
# create text on top of legend
panel = ui.Panel({
widgets: [
ui.Label('> '.concat(populationExposedVis['max']))
],
});
 
legend.add(panel);
 
# create thumbnail from the image
thumbnail = ui.Thumbnail({
image: legendImage,
params: {bbox:'0,0,10,100', dimensions:'10x50'},
style: {padding: '1px', position: 'bottom-center'}
});
 
# add the thumbnail to the legend
legend.add(thumbnail);
 
# create text on top of legend
panel = ui.Panel({
widgets: [
ui.Label(populationExposedVis['min'])
],
});
 
legend.add(panel);
 
# add legend to map (alternatively you can also print the legend to the console)
Map.add(legend);