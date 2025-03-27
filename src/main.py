import geopandas as gpd
import pandas as pd
import laspy
import numpy as np
import os, sys

import las_utils
import analysis
import contour
import vis


def main():
    VECTOR_PATH = sys.argv[1]
    LAS_PATH = sys.argv[2]
    RESULTS_PATH = sys.argv[3]
    GSD = 0.1
    LAS_CRS = "EPSG:2180"

    las = laspy.read(LAS_PATH)
    pred_contours_gdf = gpd.read_file(VECTOR_PATH)
    pred_contours_gdf = pred_contours_gdf.to_crs(LAS_CRS) # transform contours to point cloud crs

    x = np.array(las.x)
    y = np.array(las.y)
    z = np.array(las.z)
    dsm_grid = las_utils.las2dsm((x,y,z), GSD, interpolation="NN")  # faster
        # OR:
    # dsm_grid = las_utils.las2dsm((x,y,z), GSD, interpolation="TIN")  # slower
    vis.visualize_dem_and_vector(dsm_grid, pred_contours_gdf)

    # Save LAS in DataFrame - it will be useful for selection points by pred_ID
    points = np.vstack((las.x, las.y, las.z)).T
    pred_id = las.pred_ID
    las_pd = pd.DataFrame({'x': points[:, 0], 'y': points[:, 1], 'z': points[:, 1],
                                    'pred_ID': pred_id})
                                 
    # CALCULATE STATISTICS
    analysis.calculate_statistics_for_polygons(las_pd, dsm_grid, GSD, pred_contours_gdf)

    # SAVE RESLTS
    isExist = os.path.exists(RESULTS_PATH)
    if not isExist:
        os.makedirs(RESULTS_PATH)
        
    pred_contours_gdf.to_file(os.path.join(RESULTS_PATH, "res_statistics.geojson"), driver="GeoJSON", mode="w")
    
    alpha_contours_gdf = contour.alpha_shape(las_pd[las_pd["pred_ID"] != 0], alpha=0.1)
    alpha_contours_gdf.to_file(os.path.join(RESULTS_PATH, "alphashape_contours.geojson"), driver="GeoJSON", mode="w")


if __name__ == "__main__":
    main()












