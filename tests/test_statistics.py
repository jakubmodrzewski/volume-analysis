import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest

import numpy as np
import pandas as pd

from analysis import calculate_volume, calculate_area_from_point_cloud
from las_utils import las2dsm, save_point_cloud_to_las
from vis import visualize_dem_and_vector, visualize_triangulation



def generate_pyramid_point_cloud(base_size=2, height=3, num_points=100):
    """Generuje chmurę punktów w kształcie piramidy o znanych parametrach."""
    x = np.random.uniform(-base_size / 2, base_size / 2, num_points)
    y = np.random.uniform(-base_size / 2, base_size / 2, num_points)
    z = height - (np.abs(x) + np.abs(y)) * (height / base_size)  # Simple formula for pyramid
    z = np.clip(z, 0, None)  # Base height is 0
    return np.array([x, y, z])


# Parameters of pyramid
base_size = np.random.randint(2,10)  
height = np.random.randint(2,10)    
# Get volume of pyramid
expected_volume = (1/3) * (base_size**2) * height
# Get area of pyramid
slant_height = np.sqrt((base_size / 2) ** 2 + height ** 2)
expected_area = 2 * base_size * slant_height  # only sides, because pcd does not have basemenet
# Generate point cloud in the form of pyramid
point_cloud = generate_pyramid_point_cloud(base_size, height, num_points=np.random.randint(10000,50000))

# save_point_cloud_to_las(point_cloud, r'./data/tests/piramid.las')
# visualize_triangulation(point_cloud.T)


def test_calculate_area_from_point_cloud():
    """Testing area3D calculation """
   
    las_pd = pd.DataFrame({'x': point_cloud[0], 'y': point_cloud[1], 'z': point_cloud[2]}    )   # convert pyramid to dataframe
    area = calculate_area_from_point_cloud(las_pd)
    
    assert np.isclose(expected_area, area, rtol=0.2), f"Expected {expected_area}, but got {area}"


def test_pyramid_volume():
    """Testing volume calculation (based on DSM method)"""

    dsm_gsd = 0.1  
    dsm = las2dsm(point_cloud, dsm_gsd, "NN")
    # visualize_dem_and_vector(dsm)
    base_height = 0  # base height pyramid
    volume = calculate_volume(base_height, dsm, dsm_gsd)

    min_height = np.min(dsm[2])
    max_height = np.max(dsm[2])
    height_range = max_height - min_height
    
    # Dynamic tolerance based on height difference on DSM
    # 20% of range - large tolerance due to volume computation based on raster (dependent from GSD and interpolation method)
    DYNAMIC_TOLERANCE = height_range * 0.2

    print(f"volume_dsm: {volume}, volume_cloud: {expected_volume}")
    assert np.isclose(expected_volume, volume, rtol=DYNAMIC_TOLERANCE, atol=0), f"Expected {expected_volume}, but got {volume}"
