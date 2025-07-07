import numpy as np
import pandas as pd

def encode_vehicle_type(vehicle_type):
    mapping = {'car': 1.0, 'bike': 0.6, 'truck': 1.5, 'cycle': 0.6}
    return mapping.get(vehicle_type, 1.0)

def encode_traffic(traffic):
    mapping = {'low': 1, 'average': 2, 'high': 3}
    return mapping.get(traffic, 2)

def demand_based_price(
    base_price, occupancy, capacity, queue_length, traffic, is_special_day, vehicle_type,
    alpha=1.2, beta=0.8, gamma=0.5, delta=1.0, epsilon=1.0, lambd=0.7
):
    vehicle_weight = encode_vehicle_type(vehicle_type)
    traffic_num = encode_traffic(traffic)
    demand = (
        alpha * (occupancy / capacity)
        + beta * queue_length
        - gamma * traffic_num
        + delta * is_special_day
        + epsilon * vehicle_weight
    )
    norm_demand = (demand - 0) / (10 - 0)
    norm_demand = np.clip(norm_demand, 0, 1)
    price = base_price * (1 + lambd * norm_demand)
    price = max(0.5 * base_price, min(price, 2 * base_price))
    return price

if __name__ == "__main__":
    price = demand_based_price(
        base_price=10.0,
        occupancy=100,
        capacity=200,
        queue_length=3,
        traffic='average',
        is_special_day=1,
        vehicle_type='car'
    )
    print(f"Demand-based price: ${price:.2f}") 