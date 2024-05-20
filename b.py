import numpy as np
from scipy.optimize import least_squares
from itertools import permutations

# 声音速度（米/秒）
v = 340

# 监测设备的经纬度和高程数据
devices = np.array([
    [110.241, 27.204, 824],
    [110.783, 27.456, 727],
    [110.762, 27.785, 742],
    [110.251, 28.025, 850],
    [110.524, 27.617, 786],
    [110.467, 28.081, 678],
    [110.047, 27.521, 575]
])

# 每个设备接收到的音爆时间
times = np.array([
    [100.767, 164.229, 214.850, 270.065],
    [92.453, 112.220, 169.362, 196.583],
    [75.560, 110.696, 156.936, 188.020],
    [94.653, 141.409, 196.517, 258.985],
    [78.600, 86.216, 118.443, 126.669],
    [67.274, 166.270, 175.482, 266.871],
    [103.738, 163.024, 206.789, 210.306]
])

# 基准点（用于坐标转换）
lat_base, lon_base = 27.204, 110.241

# 将经纬度转换为平面坐标
def latlon_to_xy(lat, lon, lat_base, lon_base):
    x = (lon - lon_base) * 97.304 * 1000
    y = (lat - lat_base) * 111.263 * 1000
    return x, y

# 转换设备坐标
devices_xy = np.array([latlon_to_xy(lat, lon, lat_base, lon_base) + (alt,) for lat, lon, alt in devices])

# 初始化音爆点位置和时间
initial_guess = np.random.rand(16)  # 4个音爆点的(x, y, z, t)

# 计算两点间距离
def calculate_distance(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

# 定义残差函数
def residuals(params):
    residual = []
    for j in range(4):
        xj, yj, zj, tj = params[4*j:4*(j+1)]
        for i in range(7):
            xi, yi, zi = devices_xy[i]
            tij = times[i, j]
            dij = calculate_distance(xi, yi, zi, xj, yj, zj)
            theoretical_tij = tj + dij / v
            residual.append(tij - theoretical_tij)
    return residual

# 使用最小二乘法优化
result = least_squares(residuals, initial_guess)

# 获取优化后的音爆点位置和时间
optimized_params = result.x.reshape(4, 4)

# 打印优化后的音爆点位置和时间
for j in range(4):
    print(f"音爆点{j+1}的位置: ({optimized_params[j, 0]}, {optimized_params[j, 1]}, {optimized_params[j, 2]})")
    print(f"音爆点{j+1}的发生时间: {optimized_params[j, 3]}")

# 计算并打印误差
def calculate_errors(params):
    errors = []
    for j in range(4):
        xj, yj, zj, tj = params[4*j:4*(j+1)]
        for i in range(7):
            xi, yi, zi = devices_xy[i]
            tij = times[i, j]
            dij = calculate_distance(xi, yi, zi, xj, yj, zj)
            theoretical_tij = tj + dij / v
            error = tij - theoretical_tij
            errors.append((i, j, error))
    return errors

errors = calculate_errors(result.x)
print("\n误差信息：")
for i, j, error in errors:
    print(f"设备{i+1} 接收到的音爆{j+1} 的误差: {error:.6f} 秒")
