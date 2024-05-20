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

# 初始化音爆点位置和时间
initial_guess = np.random.rand(4, 4)  # 4个音爆点的(x, y, z, t)

def calculate_distance(x1, y1, z1, x2, y2, z2):
    # 计算两点之间的距离，忽略地面曲率
    lat_dist = (y1 - y2) * 111.263  # 纬度差距转换为距离（km）
    lon_dist = (x1 - x2) * 97.304  # 经度差距转换为距离（km）
    height_dist = (z1 - z2) / 1000  # 高度差转换为距离（km）
    return np.sqrt(lat_dist**2 + lon_dist**2 + height_dist**2) * 1000  # 转换为米

def residuals(params):
    residual = []
    for j in range(4):
        xj, yj, zj, tj = params[4*j:4*(j+1)]
        best_error = float('inf')
        for perm in permutations(range(4), 4):
            current_error = 0
            for i in range(7):
                xi, yi, zi = devices[i]
                tij = times[i, perm[j]]
                theoretical_tij = tj + calculate_distance(xi, yi, zi, xj, yj, zj) / v
                current_error += (tij - theoretical_tij) ** 2
            best_error = min(best_error, current_error)
        residual.append(best_error)
    return residual

# 使用最小二乘法优化
result = least_squares(residuals, initial_guess.flatten())

# 获取优化后的音爆点位置和时间
optimized_params = result.x.reshape(4, 4)
for j in range(4):
    print(f"音爆点{j+1}的位置: ({optimized_params[j, 0]}, {optimized_params[j, 1]}, {optimized_params[j, 2]})")
    print(f"音爆点{j+1}的发生时间: {optimized_params[j, 3]}")