import matplotlib.pyplot as plt

def visualize_dem_and_vector(grid, gdf=None):
    plt.figure(figsize=(10, 8))
    plt.contourf(grid[0], grid[1], grid[2], levels=20, cmap='terrain')
    plt.colorbar(label="Wysokość (m)")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.title("Digital Surface Model (DSM)")
    if gdf is not None:
        gdf.boundary.plot(ax=plt.gca(), color='red', linewidth=2)  # draw contours
    plt.show()


from scipy.spatial import Delaunay

def visualize_triangulation(points):
    tri = Delaunay(points[:, :2])  # 2D triangulacja
    plt.triplot(points[:, 0], points[:, 1], tri.simplices, 'go-')
    plt.scatter(points[:, 0], points[:, 1], color='red')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Triangulacja Delaunaya")
    plt.show()