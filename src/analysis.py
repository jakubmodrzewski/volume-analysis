import numpy as np
from scipy.spatial import cKDTree, Delaunay
from shapely.vectorized import contains
from shapely.geometry import Polygon

def calculate_statistics_for_polygons(las_gdf, dsm_grid, GSD, polygons):
    volumes = []
    # areas_25D = [] ## 2.5D - calculate from DSM
    areas_3D = []
    coverages = []

    for _, polygon in polygons.iterrows():
        polygon_geom = polygon['geometry']
        points_in_polygon = las_gdf[las_gdf['pred_ID'] == polygon['pred_ID']]
        dsm_inside = extract_dsm_inside_polygon(dsm_grid, polygon_geom)
        # VOLUME
        base_height = extract_base_height_along_polygon(dsm_grid, polygon_geom)
        volume = calculate_volume(base_height, dsm_inside, GSD)
        #AREA    
        # area_dsm = analysis.calculate_surface_area_from_dsm(dsm_inside) # AREA 2.5D
        area_las = calculate_area_from_point_cloud(points_in_polygon) # AREA 3D
        #COVERAGE
        coverage = calculate_coverage_area(points_in_polygon, polygon)

        volumes.append(volume)
        # areas_25D.append(area_dsm)
        areas_3D.append(area_las)
        coverages.append(coverage)
    
    polygons["volume"] = volumes
    # polygons["area2.5D"] = areas_25D
    polygons["area3D"] = areas_3D
    polygons["coverage"] = coverages
    print(polygons)
    return polygons




def calculate_volume(base_height, dsm_inside, gsd):
    """calculate volume relative to base surface (mean height value on polygon boundary)

    Parameters
    ----------
    base_height: float
        mean Z-value on polygon boundary
    dsm_inside : array
        DSM pixels within analyzed polygon. Grid of numpy arrays: DSM_X, DSM_Y, DSM_Z
    gsd: float
        resolution of dsm

    Returns
    -------
    float
       volume analyzed in dsm_inside pixels
    """
    height_diff  = np.maximum(dsm_inside[2] - base_height, 0)  # Maximum for eliminating negative values
    volume = np.sum(height_diff * gsd**2)
    return volume


def extract_dsm_inside_polygon(dsm: list, polygon: Polygon):
    """Extract dsm pixels within polygon

    Parameters
    ----------
    dsm : list
        grid of numpy arrays: DSM_X, DSM_Y, DSM_Z
    polygon : shapely.geometry.polygon.Polygon
        polygon to check which pixels are within 

    Returns
    -------
    list of DSM masked
       list of masked DSM grid of numpy arrays: DSM_X, DSM_Y, DSM_Z
    """

    dsm_x, dsm_y, dsm_z = dsm
    mask = contains(polygon, dsm_x, dsm_y)
    return [ dsm_x[mask], dsm_y[mask], dsm_z[mask] ]


def extract_base_height_along_polygon(dsm: list, polygon: Polygon):
    """Extract Z-values from DSM pixels located on polygon boundary and calculate mean Z-value

    Parameters
    ----------
    dsm : list
        Grid of numpy arrays: DSM_X, DSM_Y, DSM_Z
    polygon : shapely.geometry.polygon.Polygon
        polygon which boundary is used to calculate mean Z-Value from DSM

    Returns
    -------
    float
        mean of DSM Z-values located on polygon boundary
    """

    # Gets boundary of polygon
    boundary_coords = np.array(polygon.exterior.coords)
    x_boundary, y_boundary = boundary_coords[:,0], boundary_coords[:,1]

    # Flatten DSM
    dsm_x, dsm_y, dsm_z = dsm
    dsm_points = np.vstack((dsm_x.ravel(), dsm_y.ravel())).T
    dsm_values = dsm_z.ravel()

    # Find DSM pixels on polygon boundary
    tree = cKDTree(dsm_points)  
    _, idx = tree.query(np.vstack((x_boundary, y_boundary)).T, k=1) 
    boundary_dsm_values = dsm_values[idx]

    return np.mean(boundary_dsm_values)


def calculate_area_from_point_cloud(points):
    """Calculate 3D surface area from point cloud

    Parameters
    ----------
    points : geopandas.geodataframe.GeoDataFrame
        points in geodataframe

    Returns
    -------
    float
        3D surface area
    """
        
    x = points['x'].T.values 
    y = points['y'].T.values
    z = points['z'].T.values
    points_2d = np.c_[x, y]

    tri = Delaunay(points_2d)
    triangles = tri.simplices

    # Calculate area by sum triangles from Delaunay
    area = 0.0
    for tri in triangles:
        p1, p2, p3 = np.array([x[tri[0]], y[tri[0]], z[tri[0]]]), \
                     np.array([x[tri[1]], y[tri[1]], z[tri[1]]]), \
                     np.array([x[tri[2]], y[tri[2]], z[tri[2]]])

        a = np.linalg.norm(p2 - p1)
        b = np.linalg.norm(p3 - p1)
        c = np.linalg.norm(p3 - p2)
        s = (a + b + c) / 2 
        triangle_area = np.sqrt(s * (s - a) * (s - b) * (s - c))  # Heron formula
        area += triangle_area

    return area


def calculate_surface_area_from_dsm(dsm):
    """Calculate 2.5D surface area based on triangulation of DSM pixels

    Parameters
    ----------
    dsm : list
        Grid of numpy arrays: DSM_X, DSM_Y, DSM_Z

    Returns
    -------
    float
        2.5D surface area calculated from DSM
    """
    dsm_x, dsm_y, dsm_z = dsm
    points = np.vstack((dsm_x, dsm_y)).T
    tri = Delaunay(points)

    surface_area = 0.0
    for simplex in tri.simplices:
        p1,p2,p3 = points[simplex]
        z1, z2, z3 = dsm_z[simplex]

        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1], z2-z1])
        v2 = np.array([p3[0] - p1[0], p2[1] - p3[1], z3-z1])

        area = 0.5 * np.linalg.norm(np.cross(v1, v2)) # triangle area using cross product
        surface_area += area

    return surface_area


def calculate_coverage_area(points_gdf, polygon):
    """Calculate the number of points (point cloud) in polygon and coverage_area

    Parameters
    ----------
    points_gdf : Geodataframe
        Geodataframe with 3D points (point cloud)

    Returns
    -------
    float
        The area covered by the points within the polygon - the ratio of the number of points in the polygon to the total number of points in the cloud
    """

    polygon_geom = polygon['geometry']

    # get nunbmer of points inside polygon
    num_points_in_polygon = len(points_gdf)
    
    # area of polygon
    polygon_area = polygon_geom.area
    
    if num_points_in_polygon > 0:
        coverage_area = (num_points_in_polygon / len(points_gdf)) * polygon_area
    else:
        coverage_area = 0
    return coverage_area