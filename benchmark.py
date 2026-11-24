import json
import random
import time
from pathlib import Path
from main import merge_sort_parcels, knapsack_select

random.seed(7)
sizes = [10, 25, 50, 75, 100]
capacity = 100
rows = []
for n in sizes:
    parcels = []
    for i in range(n):
        parcels.append({
            "id": f"P{i}", "name": f"Parcel {i}",
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100),
            "priority": random.randint(1, 5),
            "deadline": f"{random.randint(8, 18):02d}:{random.choice(['00','15','30','45'])}",
            "destination": "D1"
        })
    sort_samples, dp_samples = [], []
    for _ in range(5):
        start = time.perf_counter()
        ordered = merge_sort_parcels(parcels)
        sort_samples.append(time.perf_counter() - start)
        start = time.perf_counter()
        knapsack_select(ordered, capacity)
        dp_samples.append(time.perf_counter() - start)
    rows.append({
        "parcel_count": n,
        "merge_sort_avg_seconds": sum(sort_samples)/len(sort_samples),
        "knapsack_avg_seconds": sum(dp_samples)/len(dp_samples)
    })

out = Path(__file__).resolve().parent / "results" / "benchmark_results.json"
out.write_text(json.dumps(rows, indent=4), encoding="utf-8")
print(json.dumps(rows, indent=4))
