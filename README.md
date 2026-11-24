# Mini-Courier Planner
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**University:** K.R. Mangalam University

## Project overview
Mini-Courier Planner is a Python prototype that prioritizes parcels, selects the best group of parcels within a vehicle's weight capacity, and generates an approximate delivery tour from a warehouse.

## Algorithms used
1. **Merge Sort:** sorts parcels by descending priority and then by earliest deadline.
2. **0/1 Knapsack using Dynamic Programming:** selects the combination of parcels with maximum total value without exceeding vehicle capacity.
3. **Dijkstra's Algorithm:** calculates shortest paths between delivery locations.
4. **Nearest Neighbor TSP approximation:** repeatedly visits the nearest unvisited delivery point and returns to the warehouse.

## Project structure
- `main.py` — integrated application and algorithms
- `data/sample_data.json` — sample parcels, vehicle capacity, depot and road network
- `results/latest_result.json` — generated result after running the application
- `results/runtime_chart.png` — illustrative measured runtime chart
- `report.md` — project report and phase-wise explanation
- `benchmark.py` — runtime experiment for sorting and knapsack

## Requirements
- Python 3.9 or later
- No external package is required to run `main.py`
- Matplotlib is needed only to regenerate the runtime chart: `pip install matplotlib`

## How to run
1. Extract the ZIP file.
2. Open the project folder in VS Code or a terminal.
3. Run: `python main.py`
4. Enter `1` to execute the full planner.
5. Enter `2` to view algorithm complexities.
6. The latest result is saved automatically in `results/latest_result.json`.

## Input data format
Edit `data/sample_data.json`. Each parcel has:
`id`, `name`, `weight`, `value`, `priority`, `deadline`, and `destination`.
The road network is an undirected weighted graph represented by edge rows:
`[location_1, location_2, distance_in_km]`.

## Important assumptions
- Road distances are non-negative.
- The graph is undirected.
- Parcel weight and vehicle capacity are whole-number kilograms because the DP table uses integer capacity.
- The planner optimizes parcel value under the capacity limit. Priority and deadline determine the display/sorting order; they are not additional knapsack constraints.
- The nearest-neighbor tour is an approximation and is not guaranteed to be globally optimal.
- If a selected destination is unreachable, the application reports an error rather than inventing a route.

## Complexity summary
Let `n` be number of parcels, `W` vehicle capacity, `V` graph vertices and `E` graph edges.
- Merge Sort: `O(n log n)` time, `O(n)` auxiliary space.
- 0/1 Knapsack DP: `O(nW)` time and `O(nW)` space.
- Dijkstra implementation using a linear minimum scan: `O(V^2 + E)` time and `O(V)` auxiliary space.
- Nearest Neighbor with Dijkstra recomputed for each next stop: worst-case `O(V^3 + VE)`; commonly summarized as `O(V^3)` for a dense/small graph.

## Academic note
This is a prototype for the assignment. Review the logic, run it yourself, and be prepared to explain the algorithms and complexity during the viva. Replace or extend the sample dataset if your instructor expects your own test cases.
