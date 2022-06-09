import ee
# Extract date from meta data
def dates(imgcol):
    range = imgcol.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])
    printed = (
        ee.String('from ')
        .cat(ee.Date(range.get('min')).format('YYYY-MM-dd'))
        .cat(' to ')
        .cat(ee.Date(range.get('max')).format('YYYY-MM-dd'))
    )
    return printed

"""
# TODO: Pythonic

# Prints dates to the console

before_count = before_collection.size().getInfo()
print(before_count)

before_count = before_collection.size();
print(ee.String('Tiles selected: Before Flood ').cat('(').cat(before_count).cat(')'),
dates(before_collection), before_collection);

after_count = before_collection.size();
print(ee.String('Tiles selected: After Flood ').cat('(').cat(after_count).cat(')'),
dates(after_collection), after_collection);
"""