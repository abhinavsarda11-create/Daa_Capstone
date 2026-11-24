# Mini-Courier Planner — Capstone Project Report

## 1. Introduction
The Mini-Courier Planner is a prototype courier planning system. It accepts parcel information and a road network, sorts parcels by urgency, selects parcels that fit within a vehicle's capacity, and plans an approximate route from the warehouse to the selected delivery points.

## 2. Problem definition
A courier vehicle has a fixed carrying capacity. Each parcel has a weight, value, priority, deadline, and destination. The system must:
- prioritize parcels using sorting;
- select a high-value set of parcels without exceeding the weight capacity;
- calculate shortest paths through a weighted road graph;
- create an ordered delivery tour using an approximation technique;
- measure the runtime of the major algorithmic components.

## 3. Phase 1 — Courier Problem Design and Planning
### Input design
**Parcel:** parcel ID, parcel name, weight (kg), value, priority (1–5), deadline, destination.  
**Vehicle:** maximum weight capacity.  
**Road network:** undirected weighted graph. Vertices represent locations and edge weights represent distance in kilometres.  
**Depot:** warehouse starting and ending point.

### Processing flow
1. Read parcel and road-network data from JSON.
2. Sort parcels by priority (highest first) and deadline (earliest first).
3. Apply 0/1 Knapsack DP to select parcels within capacity.
4. Extract unique destinations of selected parcels.
5. Use Dijkstra to calculate shortest paths and Nearest Neighbor to construct a delivery tour.
6. Display and save the plan and runtime.

## 4. Phase 2 — Package Prioritization and Box Filling
### Sorting
Merge Sort is used. It divides the parcel list into halves, sorts each half recursively, and merges the sorted halves. The comparison key is descending priority followed by ascending deadline.

**Complexity:** O(n log n) time and O(n) auxiliary space.

### Dynamic Programming — 0/1 Knapsack
Let `dp[i][w]` be the maximum value obtainable from the first `i` parcels with capacity `w`.

Recurrence:
- If parcel `i` is too heavy: `dp[i][w] = dp[i-1][w]`
- Otherwise: `dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])`

The final cell gives the maximum total value. Backtracking through the table identifies the selected parcels.

**Complexity:** O(nW) time and O(nW) space.

## 5. Phase 3 — Route Maker and Graph Processing
### Graph representation
The road network is stored as an adjacency dictionary. Each location maps to its neighboring locations and road distances.

### Dijkstra's Algorithm
Dijkstra finds shortest distances from a source to all reachable vertices for non-negative edge weights. The program also stores predecessors to reconstruct each shortest path.

**Complexity of this implementation:** O(V² + E) time using a linear scan to choose the next vertex, and O(V) auxiliary space apart from the graph.

### Nearest Neighbor TSP approximation
Start at the warehouse. Repeatedly choose the nearest unvisited delivery destination using shortest-path distances. After visiting all selected destinations, return to the warehouse.

This heuristic is easy to implement but does not guarantee the optimal TSP tour.

**Complexity:** With Dijkstra rerun at each stop, worst-case O(V³ + VE), commonly O(V³) for a dense graph.

## 6. Phase 4 — Performance Testing and Optimization
The application records elapsed time for sorting, knapsack selection, route planning, and the complete run using Python's `time.perf_counter()`.

Suggested experiments:
- Small: 7 parcels and 5 locations (provided sample).
- Medium: 50 parcels and 15–20 locations.
- Large: 100 parcels and 30–40 locations.

For fair comparison, run each experiment several times and use the average runtime. Keep vehicle capacity moderate because the DP algorithm's time and memory depend on `W`, not only on the number of parcels.

### Optimization suggestions
- Use a heap-based Dijkstra implementation to improve shortest-path performance on sparse graphs.
- Use a one-dimensional DP array to reduce knapsack memory from O(nW) to O(W), while iterating capacity backwards.
- Cache shortest-path results from each current location when useful.
- For larger delivery networks, compare stronger TSP heuristics or local-search improvements.

## 7. Phase 5 — Results and Demonstration
Run `python main.py` and choose option 1. The program prints:
- sorted parcel list;
- selected parcels and total packed weight/value;
- ordered route and each route leg;
- measured runtime for each major step.

The output is also saved to `results/latest_result.json`.

## 8. Testing and validation
Use the provided sample JSON and verify:
1. Total selected parcel weight never exceeds vehicle capacity.
2. Selected parcel value equals the DP optimum.
3. Every selected destination appears in the route.
4. Route starts and ends at the warehouse when at least one destination is selected.
5. Each route leg follows valid graph edges through a shortest path.
6. Disconnected destinations produce a clear error message.

## 9. Limitations
- The sample system uses static input data; it does not use live maps or traffic.
- Knapsack capacity is an integer number of kilograms.
- Priority affects sorting but the current knapsack objective maximizes parcel value only.
- Nearest Neighbor is an approximate TSP method, so a shorter possible tour may exist.
- Road edges are treated as undirected.

## 10. Conclusion
The project integrates sorting, dynamic programming, shortest-path graph processing, and approximation algorithms into one courier-planning workflow. It demonstrates how individual algorithmic techniques can work together to solve a practical planning problem.

## 11. Viva preparation
**Q1. Why use Merge Sort?**  
It provides O(n log n) worst-case time and gives a predictable sorting method.

**Q2. Why is Knapsack a DP problem?**  
The problem has overlapping subproblems and optimal substructure. The DP table stores the best value for smaller parcel sets and capacities.

**Q3. What does 0/1 mean?**  
Each parcel is either selected once or not selected; it cannot be divided.

**Q4. Why use Dijkstra?**  
It finds shortest paths in a graph with non-negative edge weights.

**Q5. Does Nearest Neighbor guarantee the shortest TSP tour?**  
No. It is a heuristic that quickly produces a valid approximate tour.

**Q6. What happens if a location is disconnected?**  
The program detects that no reachable unvisited destination remains and reports an error.

**Q7. What is the difference between time and space complexity?**  
Time complexity describes how running time grows with input size; space complexity describes how memory usage grows.

**Q8. What does W mean in Knapsack complexity?**  
W is the vehicle's integer weight capacity.
