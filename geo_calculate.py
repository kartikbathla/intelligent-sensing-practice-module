import numpy as np

def compute_bbox_geo_coordinates(
    img_width, img_height, fov_h, camera_altitude, ground_altitude,
    fov_lft, fov_rt, bbox_x, bbox_y, bbox_width, bbox_height, ground_ratio=0.8
):
    """
    计算边界框左边界中心的地理坐标。
    """
    # 计算摄像头距离地面的高度
    h = camera_altitude - ground_altitude
    
    # 计算地面覆盖范围（假设视场角在地面投影）
    ground_width = 2 * h * np.tan(np.radians(fov_h / 2))
    ground_height = (img_height / img_width) * ground_width
    
    # 计算地理坐标变化范围
    lon_range = fov_rt[0] - fov_lft[0]
    lat_range = fov_lft[1] - fov_rt[1]
    
    # 计算边界框的中心点（像素）
    bbox_center_x = bbox_x  # 取左边界中心
    bbox_center_y = bbox_y + bbox_height / 2
    
    # 计算图像下半部分的起点（像素）
    ground_y_start = img_height * (1 - ground_ratio)
    ground_y_height = img_height * ground_ratio
    
    # 计算比例
    lon_ratio = bbox_center_x / img_width
    lat_ratio = (bbox_center_y - ground_y_start) / ground_y_height
    
    # 计算地理坐标
    bbox_left_lon = fov_lft[0] + lon_ratio * lon_range
    bbox_left_lat = fov_lft[1] - lat_ratio * lat_range
    
    return bbox_left_lon, bbox_left_lat

# 示例数据
img_width, img_height = 1440, 810  # 图像分辨率
fov_h = 62.8  # 水平视场角 (FOV)
camera_altitude = 126  # 摄像头海拔
ground_altitude = 120  # 地面海拔

# 视场角边界对应的地理坐标
fov_lft = (-117.178071707873, 32.5855631046602)  # 左边界
fov_rt = (-117.512184555061, 32.6929470726712)  # 右边界

# 边界框参数（像素）
bbox_x, bbox_y = 0, 0  # 左上角坐标
bbox_width, bbox_height = 1440, 810

# 计算左边界中心的地理坐标
bbox_left_lon, bbox_left_lat = compute_bbox_geo_coordinates(
    img_width, img_height, fov_h, camera_altitude, ground_altitude,
    fov_lft, fov_rt, bbox_x, bbox_y, bbox_width, bbox_height
)

print(f"边界框左边界中心的地理坐标: 经度 {bbox_left_lon}, 纬度 {bbox_left_lat}")