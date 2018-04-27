
// MODIS LST IMAGE COLLECTION CODE (Jo)

// loading in image collection
var LSTimageCollection = ee.ImageCollection("MODIS/006/MOD11A2");
// var ls8Collection = ee.ImageCollection("LANDSAT/LC08/C01/T1");
var ls7Collection = ee.ImageCollection("LANDSAT/LE07/C01/T1");
var DMSPNLCollection = ee.ImageCollection("NOAA/DMSP-OLS/NIGHTTIME_LIGHTS");

// define visualization parameters
var LSTvisParams = {bands: ['LST_Day_1km'], min:14950, max:15500};
var ls7Params = {bands: ['B3', 'B2', 'B1'], max: 128};
var ls8Params = {bands: ['B4', 'B3', 'B2'], max: 128};
var DMSPNLParams = {bands: ['avg_lights_x_pct'], min:0, max:70};

// temporal filtering
var LST_2013 = LSTimageCollection.filterDate('2013-01-01', '2013-12-31').median();
var LST_2012 = LSTimageCollection.filterDate('2012-01-01', '2012-12-31').median();
var LST_2011 = LSTimageCollection.filterDate('2011-01-01', '2011-12-31').median();
var LST_2010 = LSTimageCollection.filterDate('2010-01-01', '2010-12-31').median();
var LST_2009 = LSTimageCollection.filterDate('2009-01-01', '2009-12-31').median();
var LST_2008 = LSTimageCollection.filterDate('2008-01-01', '2008-12-31').median();
var LST_2007 = LSTimageCollection.filterDate('2007-01-01', '2007-12-31').median();
var LST_2006 = LSTimageCollection.filterDate('2006-01-01', '2016-12-31').median();
var LST_2005 = LSTimageCollection.filterDate('2005-01-01', '2005-12-31').median();
var LST_2004 = LSTimageCollection.filterDate('2004-01-01', '2004-12-31').median();
var LST_2003 = LSTimageCollection.filterDate('2003-01-01', '2003-12-31').median();
var LST_2002 = LSTimageCollection.filterDate('2002-01-01', '2002-12-31').median();
var LST_2001 = LSTimageCollection.filterDate('2001-01-01', '2001-12-31').median();
var LST_2000 = LSTimageCollection.filterDate('2000-01-01', '2000-12-31').median();

// temporal filtering for DMSP Nightlights
var DMSPNL_2013 = DMSPNLCollection.filterDate('2013-01-01', '2013-12-31').median();
var DMSPNL_2012 = DMSPNLCollection.filterDate('2012-01-01', '2012-12-31').median();
var DMSPNL_2011 = DMSPNLCollection.filterDate('2011-01-01', '2011-12-31').median();
var DMSPNL_2010 = DMSPNLCollection.filterDate('2010-01-01', '2010-12-31').median();
var DMSPNL_2009 = DMSPNLCollection.filterDate('2009-01-01', '2009-12-31').median();
var DMSPNL_2008 = DMSPNLCollection.filterDate('2008-01-01', '2008-12-31').median();
var DMSPNL_2007 = DMSPNLCollection.filterDate('2007-01-01', '2007-12-31').median();
var DMSPNL_2006 = DMSPNLCollection.filterDate('2006-01-01', '2006-12-31').median();
var DMSPNL_2005 = DMSPNLCollection.filterDate('2005-01-01', '2005-12-31').median();
var DMSPNL_2004 = DMSPNLCollection.filterDate('2004-01-01', '2004-12-31').median();
var DMSPNL_2003 = DMSPNLCollection.filterDate('2003-01-01', '2003-12-31').median();
var DMSPNL_2002 = DMSPNLCollection.filterDate('2002-01-01', '2002-12-31').median();
var DMSPNL_2001 = DMSPNLCollection.filterDate('2001-01-01', '2001-12-31').median();
var DMSPNL_2000 = DMSPNLCollection.filterDate('2000-01-01', '2000-12-31').median();

// create a cleaned yearlong composite and filter by year
var landsat_2013 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2013-01-01', '2013-12-31'));
var landsat_2012 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2012-01-01', '2012-12-31'));
var landsat_2011 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2011-01-01', '2011-12-31'));
var landsat_2010 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2010-01-01', '2010-12-31'));
var landsat_2009 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2009-01-01', '2009-12-31'));
var landsat_2008 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2008-01-01', '2008-12-31'));
var landsat_2007 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2007-01-01', '2007-12-31'));
var landsat_2006 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2006-01-01', '2006-12-31'));
var landsat_2005 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2005-01-01', '2005-12-31'));
var landsat_2004 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2004-01-01', '2004-12-31'));
var landsat_2003 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2003-01-01', '2003-12-31'));
var landsat_2002 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2002-01-01', '2002-12-31'));
var landsat_2001 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2001-01-01', '2001-12-31'));
var landsat_2000 = ee.Algorithms.Landsat.simpleComposite(ls7Collection.filterDate('2000-01-01', '2000-12-31'));

// add layers
Map.addLayer(DMSPNL_2013, DMSPNLParams, 'DMSPNL2013');
Map.addLayer(DMSPNL_2012, DMSPNLParams, 'DMSPNL2012');
Map.addLayer(DMSPNL_2011, DMSPNLParams, 'DMSPNL2011');
Map.addLayer(DMSPNL_2010, DMSPNLParams, 'DMSPNL2010');
Map.addLayer(DMSPNL_2009, DMSPNLParams, 'DMSPNL2009');
Map.addLayer(DMSPNL_2008, DMSPNLParams, 'DMSPNL2008');
Map.addLayer(DMSPNL_2007, DMSPNLParams, 'DMSPNL2007');
Map.addLayer(DMSPNL_2006, DMSPNLParams, 'DMSPNL2006');
Map.addLayer(DMSPNL_2005, DMSPNLParams, 'DMSPNL2005');
Map.addLayer(DMSPNL_2004, DMSPNLParams, 'DMSPNL2004');
Map.addLayer(DMSPNL_2003, DMSPNLParams, 'DMSPNL2003');
Map.addLayer(DMSPNL_2002, DMSPNLParams, 'DMSPNL2002');
Map.addLayer(DMSPNL_2001, DMSPNLParams, 'DMSPNL2001');
Map.addLayer(DMSPNL_2000, DMSPNLParams, 'DMSPNL2000');

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

Map.addLayer(landsat_2013, ls7Params, '2013');
Map.addLayer(landsat_2012, ls7Params, '2012');
Map.addLayer(landsat_2011, ls7Params, '2011');
Map.addLayer(landsat_2010, ls7Params, '2010');
Map.addLayer(landsat_2009, ls7Params, '2009');
Map.addLayer(landsat_2008, ls7Params, '2008');
Map.addLayer(landsat_2007, ls7Params, '2007');
Map.addLayer(landsat_2006, ls7Params, '2006');
Map.addLayer(landsat_2005, ls7Params, '2005');
Map.addLayer(landsat_2004, ls7Params, '2004');
Map.addLayer(landsat_2003, ls7Params, '2003');
Map.addLayer(landsat_2002, ls7Params, '2002');
Map.addLayer(landsat_2001, ls7Params, '2001');
Map.addLayer(landsat_2000, ls7Params, '2000');

// Merge each of our respective collections into a complete year-long collection
var complete_2013 = ee.ImageCollection.fromImages([LST_2013, landsat_2013, DMSPNL_2013])


// Export to google drive
// NOTE: not our final geometry, just a small example region for testing
var export_geometry = ee.Geometry.Rectangle([15.24156, -4.34307, 15.28258, -4.32108]);

Export.image.toDrive({
  image: complete_2013,
  description: 'year2013',
  scale: 30,
  region: export_geometry
});



// EXAMPLE EXPORT CODE

// Export the image, specifying scale and region.
