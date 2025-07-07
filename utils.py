import numpy as np

def min_max_normalize(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val) if max_val > min_val else 0.0

def haversine_distance(lat1, lon1, lat2, lon2):
    # Returns distance in kilometers
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def smooth_price(price_series, window=3):
    return price_series.rolling(window=window, min_periods=1).mean()

def encode_vehicle_type(vehicle_type):
    mapping = {'car': 1.0, 'bike': 0.6, 'truck': 1.5, 'cycle': 0.6}
    return mapping.get(vehicle_type, 1.0)

def encode_traffic(traffic):
    mapping = {'low': 1, 'average': 2, 'high': 3}
    return mapping.get(traffic, 2) 