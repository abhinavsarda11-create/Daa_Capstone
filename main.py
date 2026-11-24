import json
import time
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def merge_sort_parcels(parcels):
    """Sort parcels by priority (high first), then deadline (earlier first)."""
    if len(parcels) <= 1:
        return parcels[:]
    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    result, i, j = [], 0, 0

    def key(p):
        return (-p["priority"], p["deadline"])

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def knapsack_select(parcels, capacity):
    """0/1 Knapsack DP: maximize total parcel value within weight capacity."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight = int(parcels[i - 1]["weight"])
        value = int(parcels[i - 1]["value"])
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(dp[i][cap],
                                 dp[i - 1][cap - weight] + value)

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            selected.append(parcels[i - 1])
            cap -= int(parcels[i - 1]["weight"])
    selected.reverse()
    return selected, dp[n][capacity], dp

def build_graph(edges):
    graph = {}
    for a, b, distance in edges:
        graph.setdefault(a, {})[b] = float(distance)
        graph.setdefault(b, {})[a] = float(distance)
    return graph

def dijkstra(graph, source):
    """Return shortest distances and predecessor map from source."""
    nodes = set(graph)
    for neighbors in graph.values():
        nodes.update(neighbors)
    if source not in nodes:
        raise ValueError(f"Unknown source location: {source}")

    distances = {node: float("inf") for node in nodes}
    previous = {node: None for node in nodes}
    unvisited = set(nodes)
    distances[source] = 0

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        if distances[current] == float("inf"):
            break
        unvisited.remove(current)
        for neighbor, weight in graph.get(current, {}).items():
            if neighbor in unvisited:
                candidate = distances[current] + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    previous[neighbor] = current
    return distances, previous

def reconstruct_path(previous, destination):
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))

def nearest_neighbor_tsp(graph, depot, destinations):
    """Approximate a closed delivery tour using shortest-path distances."""
    targets = list(dict.fromkeys([d for d in destinations if d != depot]))
    current = depot
    remaining = set(targets)
    route = [depot]
    total_distance = 0.0
    legs = []

    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [node for node in remaining if distances.get(node, float("inf")) < float("inf")]
        if not reachable:
            raise ValueError("Some delivery points are unreachable from the current route.")
        next_stop = min(reachable, key=lambda node: distances[node])
        leg_distance = distances[next_stop]
        leg_path = reconstruct_path(previous, next_stop)
        legs.append({"from": current, "to": next_stop,
                     "path": leg_path, "distance": leg_distance})
        total_distance += leg_distance
        route.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop

    if current != depot:
        distances, previous = dijkstra(graph, current)
        if distances.get(depot, float("inf")) == float("inf"):
            raise ValueError("The depot cannot be reached from the final delivery point.")
        leg_distance = distances[depot]
        legs.append({"from": current, "to": depot,
                     "path": reconstruct_path(previous, depot),
                     "distance": leg_distance})
        total_distance += leg_distance
        route.append(depot)

    return route, total_distance, legs

def load_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def run_planner(data):
    started = time.perf_counter()
    parcels = data["parcels"]
    capacity = int(data["vehicle_capacity"])
    depot = data["depot"]
    graph = build_graph(data["edges"])

    sort_start = time.perf_counter()
    sorted_parcels = merge_sort_parcels(parcels)
    sort_time = time.perf_counter() - sort_start

    dp_start = time.perf_counter()
    selected, total_value, dp_table = knapsack_select(sorted_parcels, capacity)
    dp_time = time.perf_counter() - dp_start

    delivery_points = list(dict.fromkeys(p["destination"] for p in selected))
    route_start = time.perf_counter()
    route, distance, legs = nearest_neighbor_tsp(graph, depot, delivery_points)
    route_time = time.perf_counter() - route_start

    total_time = time.perf_counter() - started
    return {
        "sorted_parcels": sorted_parcels,
        "selected_parcels": selected,
        "total_weight": sum(int(p["weight"]) for p in selected),
        "total_value": total_value,
        "capacity": capacity,
        "route": route,
        "route_distance": distance,
        "legs": legs,
        "timings": {"sorting_seconds": sort_time,
                    "knapsack_seconds": dp_time,
                    "routing_seconds": route_time,
                    "total_seconds": total_time}
    }

def display_result(result):
    print("\\n========== MINI-COURIER PLANNER ==========")
    print("\\n1. Parcels sorted by priority and deadline:")
    for p in result["sorted_parcels"]:
        print(f'  {p["id"]}: {p["name"]} | priority={p["priority"]} | '
              f'deadline={p["deadline"]} | weight={p["weight"]} | value={p["value"]}')
    print("\\n2. Optimal packing plan (0/1 Knapsack):")
    for p in result["selected_parcels"]:
        print(f'  {p["id"]}: {p["name"]} -> {p["destination"]} '
              f'({p["weight"]} kg, value {p["value"]})')
    print(f'Total weight: {result["total_weight"]}/{result["capacity"]} kg')
    print(f'Total parcel value: {result["total_value"]}')
    print("\\n3. Delivery route (Nearest Neighbor approximation):")
    print(" -> ".join(result["route"]))
    print(f'Total route distance: {result["route_distance"]:.2f} km')
    print("\\nRoute legs:")
    for leg in result["legs"]:
        print(f'  {leg["from"]} -> {leg["to"]}: '
              f'{" -> ".join(leg["path"])} ({leg["distance"]:.2f} km)')
    print("\\n4. Runtime:")
    for name, seconds in result["timings"].items():
        print(f"  {name}: {seconds:.8f} seconds")
    print("==========================================\\n")

def save_result(result, path):
    serializable = dict(result)
    serializable["route_distance"] = round(result["route_distance"], 4)
    serializable["timings"] = {k: round(v, 8) for k, v in result["timings"].items()}
    with open(path, "w", encoding="utf-8") as file:
        json.dump(serializable, file, indent=4)

def main():
    data_path = BASE_DIR / "data" / "sample_data.json"
    data = load_data(data_path)
    while True:
        print("MINI-COURIER PLANNER")
        print("1. Run complete courier planner")
        print("2. Show algorithm complexity")
        print("3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            try:
                result = run_planner(data)
                display_result(result)
                output_path = BASE_DIR / "results" / "latest_result.json"
                save_result(result, output_path)
                print(f"Result saved to: {output_path}")
            except (ValueError, KeyError) as error:
                print("Planner error:", error)
        elif choice == "2":
            print("\\nMerge Sort: O(n log n) time, O(n) auxiliary space")
            print("0/1 Knapsack DP: O(nW) time and O(nW) space")
            print("Dijkstra (array/min scan): O(V^2 + E) time, O(V) space")
            print("Nearest Neighbor TSP: O(V^3) with this Dijkstra-based implementation")
            print("Note: W is vehicle capacity, V is graph vertices, E is graph edges.")
        elif choice == "3":
            print("Exiting Mini-Courier Planner.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
