import alphashape
from shapely.geometry import Polygon
import geopandas as gpd
import numpy as np

def alpha_shape(las_pd, alpha=0.1):
    """ Extract contours (alpha shape method) for points with the same value of pred_ID attribute

    Parameters:
        df (pd.DataFrame): 
            DataFrame with columns ['x', 'y', 'pred_ID']
        alpha (float): 
            Alpha shape parameters (less value, more accuracy)

    Returns:
        gpd.GeoDataFrame: 
            Alpha shape polygons
    """
    polygons = []
    ids = []

    for pred_id, group in las_pd.groupby("pred_ID"):
        points = group[["x", "y"]].values  
        if len(np.unique(points, axis=0)) < 3:  # Alpha Shape needs at least 3 points
            continue
    
        alpha_shape = alphashape.alphashape(points, alpha)

        if isinstance(alpha_shape, Polygon):
            polygons.append(alpha_shape)
            ids.append(pred_id)

    return gpd.GeoDataFrame({"pred_ID": ids, "geometry": polygons}, crs="EPSG:2180")