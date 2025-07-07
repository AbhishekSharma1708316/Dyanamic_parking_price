import pandas as pd
import sys
import os
from stream_simulator import stream_simulation, quick_stream_test

def main():
    print("Dynamic Pricing Engine - Summer Analytics 2025")
    print("=" * 50)
    if not os.path.exists('dataset.csv'):
        print("Error: dataset.csv not found in current directory")
        return
    try:
        df = pd.read_csv('dataset.csv')
        lot_ids = df['ID'].unique()
        print(f"Loaded dataset with {len(lot_ids)} parking lots")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    try:
        from visualization import RealTimeVisualizer
        use_visualization = True
        print("Bokeh visualization available")
    except ImportError:
        use_visualization = False
        print("Bokeh not available, running in console mode")
    if use_visualization:
        visualizer = RealTimeVisualizer(lot_ids)
        def on_new_batch(batch):
            visualizer.update(batch)
        print("Starting real-time simulation with visualization...")
        stream_simulation('dataset.csv', on_new_batch, delay=0.1)
        print("Opening Bokeh dashboard...")
        visualizer.show()
    else:
        print("Running in console mode...")
        quick_stream_test('dataset.csv', max_records=200)

if __name__ == "__main__":
    main() 