import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import haversine_distance

def competitive_price(
    lot_id, lots_df, current_row, prev_prices, base_price=10.0,
    alpha=1.2, beta=0.8, gamma=0.5, delta=1.0, epsilon=1.0, lambd=0.7
):
    from models.model2_demand_based import demand_based_price
    price = demand_based_price(
        base_price=base_price,
        occupancy=current_row['Occupancy'],
        capacity=current_row['Capacity'],
        queue_length=current_row['QueueLength'],
        traffic=current_row['TrafficConditionNearby'],
        is_special_day=current_row['IsSpecialDay'],
        vehicle_type=current_row['VehicleType'],
        alpha=alpha, beta=beta, gamma=gamma, delta=delta, epsilon=epsilon, lambd=lambd
    )
    current_lat = current_row['Latitude']
    current_lon = current_row['Longitude']
    lots_df = lots_df[lots_df['ID'] != lot_id]
    lots_df['distance'] = lots_df.apply(
        lambda row: haversine_distance(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1)
    nearest = lots_df.nsmallest(3, 'distance')
    competitor_prices = [prev_prices.get(lot, base_price) for lot in nearest['ID']]
    reroute = False
    if current_row['Occupancy'] >= current_row['Capacity']:
        if any(p < price for p in competitor_prices):
            price = min(price, min(competitor_prices))
            reroute = True
    elif all(p > price for p in competitor_prices):
        price = min(price * 1.05, base_price * 2)
    price = max(base_price * 0.5, min(price, base_price * 2))
    return price, reroute

if __name__ == "__main__":
    lots_df = pd.DataFrame({
        'ID': ['A', 'B', 'C', 'D'],
        'Latitude': [26.1, 26.2, 26.3, 26.4],
        'Longitude': [91.7, 91.8, 91.9, 92.0],
        'Capacity': [100, 100, 100, 100],
        'Occupancy': [100, 80, 90, 95],
        'QueueLength': [2, 3, 1, 0],
        'TrafficConditionNearby': ['low', 'average', 'high', 'low'],
        'IsSpecialDay': [0, 1, 0, 0],
        'VehicleType': ['car', 'bike', 'truck', 'car']
    })
    current_row = lots_df.iloc[0]
    prev_prices = {'B': 9, 'C': 12, 'D': 11}
    price, reroute = competitive_price('A', lots_df, current_row, prev_prices)
    print(f"Competitive price: ${price:.2f}, Reroute: {reroute}") 