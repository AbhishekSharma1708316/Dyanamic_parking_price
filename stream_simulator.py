import pandas as pd
import numpy as np
import time
from datetime import datetime
from models.model1_baseline import baseline_linear_price
from models.model2_demand_based import demand_based_price
from models.model3_competitive import competitive_price

def stream_simulation(csv_path, callback, delay=0.1):
    print("Starting Real-Time Streaming Simulation...")
    df = pd.read_csv(csv_path)
    df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'], dayfirst=True)
    df = df.sort_values('Timestamp')
    lot_ids = df['ID'].unique()
    prev_prices = {lot: 10.0 for lot in lot_ids}
    lots_df = df[['ID', 'Latitude', 'Longitude', 'Capacity']].drop_duplicates('ID')
    print(f"Processing {len(df)} records across {len(lot_ids)} parking lots")
    print(f"Time range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    for ts, group in df.groupby('Timestamp'):
        output = []
        for _, row in group.iterrows():
            lot_id = row['ID']
            price1 = baseline_linear_price(prev_prices[lot_id], row['Occupancy'], row['Capacity'])
            price2 = demand_based_price(
                base_price=10.0,
                occupancy=row['Occupancy'],
                capacity=row['Capacity'],
                queue_length=row['QueueLength'],
                traffic=row['TrafficConditionNearby'],
                is_special_day=row['IsSpecialDay'],
                vehicle_type=row['VehicleType']
            )
            price3, reroute = competitive_price(lot_id, lots_df, row, prev_prices, base_price=10.0)
            prev_prices[lot_id] = price3
            output.append({
                'Timestamp': ts,
                'LotID': lot_id,
                'Price1': round(price1, 2),
                'Price2': round(price2, 2),
                'Price3': round(price3, 2),
                'Reroute': reroute,
                'Occupancy': row['Occupancy'],
                'Capacity': row['Capacity'],
                'QueueLength': row['QueueLength'],
                'TrafficLevel': row['TrafficConditionNearby'],
                'VehicleType': row['VehicleType']
            })
        time.sleep(delay)
        callback(output)
        print(f"Processed timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')} - {len(output)} lots updated")
    print("Streaming simulation completed!")

def quick_stream_test(csv_path, max_records=100):
    def test_callback(batch):
        for record in batch:
            print(f"Lot {record['LotID']}: Model1=${record['Price1']}, Model2=${record['Price2']}, Model3=${record['Price3']}")
    print("Running Quick Stream Test...")
    stream_simulation(csv_path, test_callback, delay=0.01)

if __name__ == "__main__":
    quick_stream_test('dataset.csv', max_records=50) 