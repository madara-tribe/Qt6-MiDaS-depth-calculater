import numpy as np
from scipy.interpolate import RectBivariateSpline


def depth_to_distance(depth_value,depth_scale):
    return 1.0 / (depth_value * depth_scale)
  
def calcurate_depth_value(output_norm):
    h, w = output_norm.shape
    x_grid, y_grid = np.arange(w), np.arange(h)
    # Create a spline object using the output_norm array
    return RectBivariateSpline(y_grid, x_grid, output_norm)
    
