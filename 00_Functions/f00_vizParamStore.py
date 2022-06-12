"""
All visualizations stored for each subfunction
  
"""

def vizParamStore():
    
    floodVizParam = {
      'palette':"0000FF", 
      'opacity':0.4,
    }
    
    populationCountVis = {
      'min':0,
      'max':200.0,
      'palette':['060606','337663','337663','ffffff'],
    }
    
    populationExposedVis = {
      'min':0,
      'max':200.0,
      'palette':['yellow', 'orange', 'red'],
      'opacity':0.3
    }
    
    # MODIS Land Cover
    LCVis = {
      'min':1.0,
      'max':17.0,
      'palette': [
          '05450a', '086a10', '54a708', 
          '78d203', '009900', 'c6b044', 
          'dcd159', 'dade48', 'fbff13', 
          'b6ff05', '27ff87', 'c24f44', 
          'a5a5a5', 'ff6d4c','69fff8', 
          'f9ffa4', '1c0dff'
      ],
    }
    
    croplandVis = {
      'min':0,
      'max':14.0,
      'palette':['30b21c'],
    }
    
    urbanVis = {
      'min':0,
      'max':13.0,
      'palette':['grey'],
      'opacity':0.3
    }
    
    return (floodVizParam, populationCountVis, 
            populationExposedVis, LCVis, 
            croplandVis, urbanVis
            )