import numpy as np
from scipy.spatial import cKDTree

from scipy.interpolate import LinearNDInterpolator
import laspy


def las2dsm(pointcloud, gsd, interpolation="NN"):
    """Convert las to DSM structure

    Parameters
    ----------
    pointcloud: list
        (x,y,z) of pointcloud
    gsd : float
        Resolution of output DSM
    interpolation: string
        type of interpolation: Nearest neighbour (faster, less accurate) or TIN (slower, more accurate)

    Returns
    -------
    list
       list of dsm_x, dsm_y, dsm_z
    """
    points = np.vstack(pointcloud).T
    xy_points = points[:, :2]

    z_values = points[:, 2]
    grid_x, grid_y = np.meshgrid(np.arange(xy_points[:, 0].min(), xy_points[:, 0].max(), gsd),
                             np.arange(xy_points[:, 1].min(), xy_points[:, 1].max(), gsd))
    
    if interpolation == "TIN":
        interpolator = LinearNDInterpolator(xy_points, z_values)
        grid_z = interpolator(grid_x, grid_y)

    if interpolation == "NN":
        grid_points = np.vstack((grid_x.ravel(), grid_y.ravel())).T 
        tree = cKDTree(xy_points) 
        _, indices = tree.query(grid_points, k=1) 
        grid_z = z_values[indices].reshape(grid_x.shape) 

    return (grid_x, grid_y, grid_z)

def save_point_cloud_to_las(point_cloud, filename):
    """Save pointcloud to LAS file

    Parameters
    ----------
    pointcloud: list
        (x,y,z) of pointcloud
    filename: string
        filename to save LAS file
    """
    header = laspy.LasHeader(point_format=3, version="1.4")
    header.point_records_count = point_cloud.shape[1]
    
    las_data = laspy.LasData(header)
    las_data.x = point_cloud[0]
    las_data.y = point_cloud[1]
    las_data.z = point_cloud[2]

    las_data.write(filename)



def get_terrain_points(las):
    # Filter pointcloud to terrain points
    pred_class = las.points['pred_class']
    mask = pred_class == 0
    filtered_points = las.points[mask]
    return filtered_points




