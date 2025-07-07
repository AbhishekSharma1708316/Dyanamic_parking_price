import numpy as np
import pandas as pd

def baseline_linear_price(price_t, occupancy, capacity, alpha=2.0, base_price=10.0):
    price_next = price_t + alpha * (occupancy / capacity)
    return max(base_price * 0.5, min(price_next, base_price * 2))

if __name__ == "__main__":
    price = 10.0
    occupancy = 100
    capacity = 200
    next_price = baseline_linear_price(price, occupancy, capacity)
    print(f"Next price: ${next_price:.2f}") 