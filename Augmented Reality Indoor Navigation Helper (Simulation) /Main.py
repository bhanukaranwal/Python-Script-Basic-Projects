# Augmented Reality Indoor Navigation Helper (Simulation) — main.py

class IndoorNavigationSimulator:
    def __init__(self, building_map):
        self.building_map = building_map  # dict of rooms and adjacency
        self.current_position = 'Entrance'

    def find_path(self, destination):
        # Simple Breadth-First Search path finder
        queue = [[self.current_position]]
        visited = set()
        while queue:
            path = queue.pop(0)
            room = path[-1]
            if room == destination:
                return path
            if room not in visited:
                visited.add(room)
                neighbors = self.building_map.get(room, [])
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def navigate_to(self, destination):
        path = self.find_path(destination)
        if not path:
            return f"No path found to {destination}."
        directions = []
        for i in range(len(path)-1):
            directions.append(f"From {path[i]} go to {path[i+1]}")
        return directions

if __name__ == '__main__':
    # Simulated building map structure
    building_map = {
        'Entrance': ['Lobby'],
        'Lobby': ['Entrance', 'Elevator', 'Conference Room'],
        'Elevator': ['Lobby', 'Office 101', 'Office 102'],
        'Conference Room': ['Lobby'],
        'Office 101': ['Elevator'],
        'Office 102': ['Elevator', 'Cafeteria'],
        'Cafeteria': ['Office 102']
    }

    navigator = IndoorNavigationSimulator(building_map)

    destinations = ['Cafeteria', 'Conference Room', 'Office 101', 'Gym']
    for dest in destinations:
        print(f"Navigating to {dest}:")
        directions = navigator.navigate_to(dest)
        if isinstance(directions, list):
            for step in directions:
                print(f"- {step}")
        else:
            print(directions)
        print()

# Extension ideas:
# - Integrate with real device sensors (SLAM) and camera feeds for AR
# - Add voice guidance or mobile/AR UI
# - Crowdsource maps for large buildings and campuses
# - Implement lost item/asset finder
