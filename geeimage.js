
// MODIS LST IMAGE COLLECTION CODE (Jo)

// loading in image collection
var LSTimageCollection = ee.ImageCollection("MODIS/006/MOD11A2");
// define visualization parameters
var LSTvisParams = {bands: ['LST_Day_1km'], min:14950, max:15500};


// temporal filtering
var y_2014 = LSTimageCollection.filterDate('2014-01-01', '2014-12-31').median();
var y_2013 = LSTimageCollection.filterDate('2013-01-01', '2013-12-31').median();
var y_2012 = LSTimageCollection.filterDate('2012-01-01', '2012-12-31').median();
var y_2011 = LSTimageCollection.filterDate('2011-01-01', '2011-12-31').median();
var y_2010 = LSTimageCollection.filterDate('2010-01-01', '2010-12-31').median();
var y_2009 = LSTimageCollection.filterDate('2009-01-01', '2009-12-31').median();
var y_2008 = LSTimageCollection.filterDate('2008-01-01', '2008-12-31').median();
var y_2007 = LSTimageCollection.filterDate('2007-01-01', '2007-12-31').median();
var y_2006 = LSTimageCollection.filterDate('2006-01-01', '2016-12-31').median();
var y_2005 = LSTimageCollection.filterDate('2005-01-01', '2005-12-31').median();
var y_2004 = LSTimageCollection.filterDate('2004-01-01', '2004-12-31').median();
var y_2003 = LSTimageCollection.filterDate('2003-01-01', '2003-12-31').median();
var y_2002 = LSTimageCollection.filterDate('2002-01-01', '2002-12-31').median();
var y_2001 = LSTimageCollection.filterDate('2001-01-01', '2001-12-31').median();
var y_2000 = LSTimageCollection.filterDate('2000-01-01', '2000-12-31').median();


// add layers
Map.addLayer(LST_2014, LSTvisParams, 'LST2014');
Map.addLayer(LST_2013, LSTvisParams, 'LST2013');
Map.addLayer(LST_2012, LSTvisParams, 'LST2012');
Map.addLayer(LST_2011, LSTvisParams, 'LST2011');
Map.addLayer(LST_2010, LSTvisParams, 'LST2010');
Map.addLayer(LST_2009, LSTvisParams, 'LST2009');
Map.addLayer(LST_2008, LSTvisParams, 'LST2008');
Map.addLayer(LST_2007, LSTvisParams, 'LST2007');
Map.addLayer(LST_2006, LSTvisParams, 'LST2006');
Map.addLayer(LST_2005, LSTvisParams, 'LST2005');
Map.addLayer(LST_2004, LSTvisParams, 'LST2004');
Map.addLayer(LST_2003, LSTvisParams, 'LST2003');
Map.addLayer(LST_2002, LSTvisParams, 'LST2002');
Map.addLayer(LST_2001, LSTvisParams, 'LST2001');
Map.addLayer(LST_2000, LSTvisParams, 'LST2000');

// EXAMPLE EXPORT CODE

// Export to google drive
// c_2000 is the year 2000 image set
var export_geometry = ee.Geometry.Rectangle([15.24156, -4.34307, 15.28258, -4.32108]);

// Export the image, specifying scale and region.
Export.image.toDrive({
  image: c_2000,
  description: 'year2000',
  scale: 30,
  region: export_geometry
});
