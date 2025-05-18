import tkinter as tk
from tkinter import ttk, messagebox
import time
from queue import PriorityQueue
from collections import deque
import random
import math
import heapq
import threading

class ScrolledFrame:
    def __init__(self, parent, height=400):
        self.canvas = tk.Canvas(parent, bg="#ffffff", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(height=height)

class PuzzleSolverUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver")
        self.root.geometry("1100x850")
        self.root.configure(bg="#e0e7ff")
        self.after_ids = []
        self.is_running = False  # Track if an algorithm is running
        main_frame = tk.Frame(root, bg="#ffffff", bd=0, relief=tk.FLAT)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        main_frame.configure(highlightbackground="#d1d5db", highlightthickness=2)
        tk.Label(main_frame, text="8 Puzzle Solver", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#1e3a8a").pack(pady=15)
        content_frame = tk.Frame(main_frame, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True)
        left_column = tk.Frame(content_frame, bg="#ffffff")
        left_column.pack(side=tk.LEFT, fill=tk.Y)
        right_column = tk.Frame(content_frame, bg="#ffffff")
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        top_frame = tk.Frame(left_column, bg="#ffffff")
        top_frame.pack(fill=tk.BOTH, expand=False)
        self.original_grid = self.create_labeled_grid(top_frame, "Initial State", 0, 0)
        self.target_grid = self.create_labeled_grid(top_frame, "Goal State", 0, 1)
        self.process_grid = self.create_labeled_grid(top_frame, "Current State", 1, 0)
        control_frame = tk.Frame(top_frame, bg="#ffffff")
        control_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=20, sticky="ns")
        tk.Label(control_frame, text="Algorithms", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1e3a8a").pack(pady=(10, 5))
        algo_frame = tk.Frame(control_frame, bg="#ffffff")
        algo_frame.pack(pady=5)
        button_style = {"width": 12, "font": ("Helvetica", 10, "bold"), "relief": tk.RAISED, "bd": 3}
        algorithms = [
            ("BFS", self.run_bfs, "#4CAF50"),
            ("DFS", self.run_dfs, "#2196F3"),
            ("IDS", self.run_ids, "#FF9800"),
            ("UCS", self.run_ucs, "#9C27B0"),
            ("Greedy Search", self.run_greedy, "#D2691E"),
            ("IDA", self.run_ida, "#EE82EE"),
            ("A*", self.run_a_star, "#C0C0C0"),
            ("Simple Hill", self.run_hill_climbing, "#FF6A6A"),
            ("Steepest Hill", self.run_steepest_hill_climbing, "#87CEFF"),
            ("Stochastic Hill", self.run_stochastic_hill_climbing, "#FF8C00"),
            ("Simulated Anneal", self.run_simulated_annealing, "#2196F3"),
            ("Beam Search", self.run_beam_search, "#8B0000"),
            ("Genetic Algo", self.run_genetic_algorithm, "#6B8E23"),
            ("Q-Learning", self.run_q_learning, "#FF4500"),
        ]
        for idx, (text, command, color) in enumerate(algorithms):
            row = idx // 3
            col = idx % 3
            tk.Button(algo_frame, text=text, command=command, bg=color, fg="white", **button_style).grid(row=row, column=col, padx=2, pady=2)
        tk.Button(control_frame, text="Reset", bg="#DC143C", fg="white", command=self.reset, **button_style).pack(pady=10)
        speed_frame = tk.Frame(control_frame, bg="#f1f5f9", bd=2, relief=tk.GROOVE)
        speed_frame.pack(pady=10)
        tk.Label(speed_frame, text="Animation Speed", font=("Helvetica", 12, "bold"), bg="#f1f5f9", fg="#1e3a8a").pack(pady=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_label = tk.Label(speed_frame, text="1.0s", font=("Helvetica", 10), bg="#f1f5f9", fg="#1e3a8a")
        self.speed_label.pack()
        speed_scale = tk.Scale(speed_frame, from_=0.2, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.speed_var,
                               length=150, showvalue=0, command=self.update_speed_label, bg="#f1f5f9", troughcolor="#4CAF50", activebackground="#2196F3")
        speed_scale.pack(pady=5)
        detail_frame = tk.Frame(control_frame, bg="#ffffff")
        detail_frame.pack(pady=10)
        tk.Label(detail_frame, text="Details", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1e3a8a").pack()
        self.time_label = tk.Label(detail_frame, text="Time: 0.0s", font=("Helvetica", 12), bg="#ffffff")
        self.time_label.pack(pady=5)
        self.steps_label = tk.Label(detail_frame, text="Steps: 0", font=("Helvetica", 12), bg="#ffffff")
        self.steps_label.pack(pady=5)
        steps_title = tk.Label(right_column, text="Solution Steps", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1e3a8a")
        steps_title.pack(pady=5)
        self.steps_frame = ScrolledFrame(right_column, height=700)
        self.last_matrix = None

    def create_labeled_grid(self, parent, label, row, col):
        frame = tk.Frame(parent, bg="#f9fafb", bd=2, relief=tk.GROOVE)
        frame.grid(row=row, column=col, padx=15, pady=15, sticky="n")
        tk.Label(frame, text=label, font=("Helvetica", 14, "bold"), bg="#f9fafb", fg="#1e3a8a").pack(pady=5)
        grid_frame = tk.Frame(frame, bg="#f9fafb")
        grid_frame.pack(pady=5)
        entries = [[tk.Entry(grid_frame, width=5, justify="center", font=("Helvetica", 14), relief=tk.RIDGE, bd=2) for _ in range(3)] for _ in range(3)]
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                entry.grid(row=i, column=j, padx=5, pady=5)
        return entries

    def create_readonly_grid(self, parent, label, matrix, row, col):
        frame = tk.Frame(parent, bg="#f9fafb", bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        tk.Label(frame, text=label, font=("Helvetica", 10, "bold"), bg="#f9fafb", fg="#1e3a8a").pack(pady=2)
        grid_frame = tk.Frame(frame, bg="#f9fafb")
        grid_frame.pack(pady=2)
        entries = [[tk.Entry(grid_frame, width=5, justify="center", font=("Helvetica", 14), relief=tk.RIDGE, bd=2) for _ in range(3)] for _ in range(3)]
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, str(matrix[i][j]))
                entry.config(state="readonly")
        return entries

    def update_speed_label(self, value):
        self.speed_label.config(text=f"{float(value):.1f}s")

    def get_grid_values(self, grid):
        try:
            values = [[int(grid[i][j].get().strip()) if grid[i][j].get().strip() else 0 for j in range(3)] for i in range(3)]
            flat_values = [num for row in values for num in row]
            if sorted(flat_values) != list(range(9)):
                return None
            return values
        except ValueError:
            return None

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def reset(self):
        if self.is_running:
            self.is_running = False  # Signal to stop the algorithm
            self.cancel_pending_updates()
            self.root.update()  # Force UI update
        for i in range(3):
            for j in range(3):
                self.original_grid[i][j].delete(0, tk.END)
                self.target_grid[i][j].delete(0, tk.END)
                self.process_grid[i][j].delete(0, tk.END)
        for widget in self.steps_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.time_label.config(text="Time: 0.0s")
        self.steps_label.config(text="Steps: 0")
        self.speed_var.set(1.0)
        self.speed_label.config(text="1.0s")
        self.last_matrix = None
        self.cancel_pending_updates()
        messagebox.showinfo("Reset", "The puzzle has been reset.")

    def is_solvable(self, start, goal):
        start_flat = [num for row in start for num in row if num != 0]
        goal_flat = [num for row in goal for num in row if num != 0]
        inversions = 0
        for i in range(len(start_flat)):
            for j in range(i + 1, len(start_flat)):
                if start_flat[i] > start_flat[j]:
                    inversions += 1
        return inversions % 2 == 0

    def validate_input(self):
        for i in range(3):
            for j in range(3):
                if not self.original_grid[i][j].get().strip() or not self.target_grid[i][j].get().strip():
                    self.show_error("Please enter all numbers in both Initial and Goal states.")
                    return None, None
        start_state = self.get_grid_values(self.original_grid)
        goal_state = self.get_grid_values(self.target_grid)
        if not start_state or not goal_state:
            self.show_error("Please enter valid numbers (0-8) in both grids.")
            return None, None
        return start_state, goal_state

    def run_bfs(self):
        self.solve_puzzle(self.bfs)

    def run_dfs(self):
        self.solve_puzzle(self.dfs)

    def run_ids(self):
        self.solve_puzzle(self.ids_solve)

    def run_ucs(self):
        self.solve_puzzle(self.ucs)

    def run_greedy(self):
        self.solve_puzzle(self.gbfs)

    def run_ida(self):
        self.solve_puzzle(self.ida)

    def run_a_star(self):
        self.solve_puzzle(self.a_star_search)

    def run_hill_climbing(self):
        self.solve_puzzle(self.hill_climbing)

    def run_steepest_hill_climbing(self):
        self.solve_puzzle(self.steepest_hill_climbing)

    def run_stochastic_hill_climbing(self):
        self.solve_puzzle(self.stochastic_hill_climbing)

    def run_simulated_annealing(self):
        self.solve_puzzle(self.simulated_annealing)

    def run_beam_search(self):
        self.solve_puzzle(self.beam_search)

    def run_genetic_algorithm(self):
        self.solve_puzzle(self.genetic_algorithm)

    def run_q_learning(self):
        self.solve_puzzle(self.q_learning)

    def cancel_pending_updates(self):
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass  # Ignore errors if the ID is invalid
        self.after_ids.clear()

    def bfs(self, start, goal):
        queue = deque([(start, [])])
        visited = set()
        while queue and self.is_running:
            current, path = queue.popleft()
            if current == goal:
                return path + [current]
            visited.add(tuple(map(tuple, current)))
            for neighbor in self.get_neighbors(current):
                if tuple(map(tuple, neighbor)) not in visited:
                    queue.append((neighbor, path + [current]))
        return None

    def dfs(self, start, goal, depth=0, max_depth=50, visited=None):
        if not self.is_running:
            return None
        if visited is None:
            visited = set()
        if start == goal:
            return [start]
        if depth >= max_depth:
            return None
        visited.add(tuple(map(tuple, start)))
        for neighbor in self.get_neighbors(start):
            if tuple(map(tuple, neighbor)) not in visited:
                result = self.dfs(neighbor, goal, depth + 1, max_depth, visited)
                if result:
                    return [start] + result
        visited.remove(tuple(map(tuple, start)))
        return None

    def dfs_limited(self, state, goal, depth, visited):
        if not self.is_running:
            return None
        if state == goal:
            return [state]
        if depth == 0:
            return None
        visited.add(tuple(map(tuple, state)))
        for neighbor in self.get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                result = self.dfs_limited(neighbor, goal, depth - 1, visited)
                if result:
                    return [state] + result
        visited.remove(tuple(map(tuple, state)))
        return None

    def ids_solve(self, start, goal, max_depth=50):
        for depth in range(max_depth):
            if not self.is_running:
                return None
            visited = set()
            result = self.dfs_limited(start, goal, depth, visited)
            if result:
                return result
        return None

    def ucs(self, start, goal):
        pq = PriorityQueue()
        pq.put((0, start, []))
        visited = set()
        while not pq.empty() and self.is_running:
            cost, current, path = pq.get()
            if current == goal:
                return path + [current]
            visited.add(tuple(map(tuple, current)))
            for neighbor in self.get_neighbors(current):
                if tuple(map(tuple, neighbor)) not in visited:
                    pq.put((cost + 1, neighbor, path + [current]))
        return None

    def get_neighbors(self, state):
        neighbors = []
        x, y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def gbfs(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristic(start), start, []))
        visited = set()
        while open_list and self.is_running:
            _, current, path = heapq.heappop(open_list)
            if current == goal:
                return path + [current]
            visited.add(tuple(map(tuple, current)))
            for neighbor in self.get_neighbors(current):
                if tuple(map(tuple, neighbor)) not in visited:
                    heapq.heappush(open_list, (self.heuristic(neighbor), neighbor, path + [current]))
        return None

    def heuristic(self, state, goal=None):
        if goal is None:
            goal = self.get_grid_values(self.target_grid)
        distance = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    for x in range(3):
                        for y in range(3):
                            if goal[x][y] == val:
                                distance += abs(i - x) + abs(j - y)
        return distance

    def ida(self, start, goal):
        bound = self.heuristic(start)
        path = [start]
        while self.is_running:
            t = self.ida_search(path, 0, bound, goal)
            if isinstance(t, list):
                return t
            if t == float('inf'):
                return None
            bound = t
        return None

    def ida_search(self, path, g, bound, goal):
        if not self.is_running:
            return None
        node = path[-1]
        f = g + self.heuristic(node, goal)
        if f > bound:
            return f
        if node == goal:
            return path
        min_cost = float('inf')
        for neighbor in self.get_neighbors(node):
            if neighbor not in path:
                path.append(neighbor)
                t = self.ida_search(path, g + 1, bound, goal)
                if isinstance(t, list):
                    return t
                if t < min_cost:
                    min_cost = t
                path.pop()
        return min_cost

    def a_star_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start), 0, start, []))
        visited = set()
        while open_set and self.is_running:
            _, g, current, path = heapq.heappop(open_set)
            if current == goal:
                return path + [current]
            visited.add(tuple(map(tuple, current)))
            for neighbor in self.get_neighbors(current):
                if tuple(map(tuple, neighbor)) not in visited:
                    heapq.heappush(open_set, (g + 1 + self.heuristic(neighbor), g + 1, neighbor, path + [current]))
        return None

    def hill_climbing(self, start, goal):
        current = start
        path = [current]
        visited = set()
        max_iterations = 1000
        for _ in range(max_iterations):
            if not self.is_running:
                return None
            if current == goal:
                return path
            visited.add(tuple(map(tuple, current)))
            neighbors = [n for n in self.get_neighbors(current) if tuple(map(tuple, n)) not in visited]
            if not neighbors:
                break
            next_state = min(neighbors, key=lambda x: self.heuristic(x, goal), default=None)
            if next_state is None or self.heuristic(next_state, goal) >= self.heuristic(current, goal):
                break
            current = next_state
            path.append(current)
        return path if current == goal else None

    def steepest_hill_climbing(self, start, goal):
        current = start
        path = [current]
        visited = set()
        max_iterations = 1000
        for _ in range(max_iterations):
            if not self.is_running:
                return None
            if current == goal:
                return path
            visited.add(tuple(map(tuple, current)))
            neighbors = [n for n in self.get_neighbors(current) if tuple(map(tuple, n)) not in visited]
            if not neighbors:
                break
            best_neighbor = min(neighbors, key=lambda x: self.heuristic(x, goal), default=None)
            if best_neighbor is None or self.heuristic(best_neighbor, goal) >= self.heuristic(current, goal):
                break
            current = best_neighbor
            path.append(current)
        return path if current == goal else None

    def stochastic_hill_climbing(self, start, goal):
        current = start
        path = [current]
        visited = set()
        max_iterations = 1000
        for _ in range(max_iterations):
            if not self.is_running:
                return None
            if current == goal:
                return path
            visited.add(tuple(map(tuple, current)))
            neighbors = [n for n in self.get_neighbors(current) if tuple(map(tuple, n)) not in visited]
            if not neighbors:
                break
            better_neighbors = [n for n in neighbors if self.heuristic(n, goal) <= self.heuristic(current, goal)]
            if better_neighbors:
                current = random.choice(better_neighbors)
                path.append(current)
            else:
                break
        return path if current == goal else None

    def simulated_annealing(self, start, goal):
        current = [row[:] for row in start]  # Sao chép trạng thái ban đầu
        path = [current]
        T = 2000.0  # Tăng nhiệt độ ban đầu để có nhiều cơ hội khám phá
        alpha = 0.9  # Giảm nhiệt độ chậm hơn nữa
        min_T = 0.5  # Duy trì nhiệt độ tối thiểu cao hơn để tăng khả năng chấp nhận bước xấu
        max_iterations = 10000  # Tăng số vòng lặp tối đa để đảm bảo tìm được lời giải

        target_empty_pos = [(i, j) for i in range(3) for j in range(3) if goal[i][j] == 0][0]  # Vị trí ô trống mục tiêu (2,2)

        for i in range(max_iterations):
            if not self.is_running:
                return None
            if current == goal:
                return path
            if T < min_T:
                break

            # Lấy các trạng thái lân cận
            neighbors = self.get_neighbors(current)
            if not neighbors:
                break

            # Tìm vị trí ô trống hiện tại
            current_empty_pos = [(i, j) for i in range(3) for j in range(3) if current[i][j] == 0][0]
            # Ưu tiên lân cận di chuyển ô trống gần mục tiêu hơn (dựa trên khoảng cách Manhattan đến (2,2))
            neighbors_with_distance = []
            for neighbor in neighbors:
                neighbor_empty_pos = [(i, j) for i in range(3) for j in range(3) if neighbor[i][j] == 0][0]
                dist = abs(neighbor_empty_pos[0] - target_empty_pos[0]) + abs(neighbor_empty_pos[1] - target_empty_pos[1])
                neighbors_with_distance.append((neighbor, dist))

            # Sắp xếp theo khoảng cách đến vị trí ô trống mục tiêu
            neighbors_with_distance.sort(key=lambda x: x[1])
            # Chọn ngẫu nhiên từ 3 trạng thái tốt nhất (hoặc tất cả nếu ít hơn)
            top_neighbors = neighbors_with_distance[:min(3, len(neighbors_with_distance))]
            next_state, _ = random.choice(top_neighbors) if top_neighbors else (random.choice(neighbors), 0)

            # Tính delta_E dựa trên heuristic
            delta_E = self.heuristic(next_state, goal) - self.heuristic(current, goal)
            # Chấp nhận trạng thái mới nếu tốt hơn hoặc theo xác suất
            if delta_E <= 0 or random.random() < math.exp(-delta_E / max(T, 1e-10)):
                current = next_state
                path.append(current)

            # Giảm nhiệt độ
            T *= alpha

        return path if current == goal else None

    def beam_search(self, start, goal, beam_width=5):
        open_list = [(self.heuristic(start, goal), start, [])]
        visited = set([tuple(map(tuple, start))])
        while open_list and self.is_running:
            new_open_list = []
            for h, current, path in open_list:
                if current == goal:
                    return path + [current]
                for neighbor in self.get_neighbors(current):
                    neighbor_tuple = tuple(map(tuple, neighbor))
                    if neighbor_tuple not in visited:
                        visited.add(neighbor_tuple)
                        new_open_list.append((self.heuristic(neighbor, goal), neighbor, path + [current]))
            open_list = sorted(new_open_list, key=lambda x: x[0])[:beam_width]
        return None
    def genetic_algorithm(self, start, goal):
        def fitness(state):
            return -self.heuristic(state, goal)

        def generate_random_state():
            numbers = list(range(9))
            random.shuffle(numbers)
            return [numbers[i*3:(i+1)*3] for i in range(3)]

        def crossover(parent1, parent2):
            flat1 = [num for row in parent1 for num in row]
            flat2 = [num for row in parent2 for num in row]
            point = random.randint(1, 7)
            child_flat = flat1[:point] + flat2[point:]
            seen = set()
            for i in range(9):
                if child_flat[i] in seen or child_flat[i] not in range(9):
                    for num in range(9):
                        if num not in seen and num not in child_flat:
                            child_flat[i] = num
                            break
                seen.add(child_flat[i])
            return [child_flat[i*3:(i+1)*3] for i in range(3)]

        def mutate(state):
            flat = [num for row in state for num in row]
            i, j = random.sample(range(9), 2)
            flat[i], flat[j] = flat[j], flat[i]
            return [flat[i*3:(i+1)*3] for i in range(3)]

        population_size = 100
        generations = 500
        mutation_rate = 0.2
        population = [generate_random_state() for _ in range(population_size - 1)] + [start]
        for _ in range(generations):
            if not self.is_running:
                return None
            population = sorted(population, key=fitness, reverse=True)
            if fitness(population[0]) == 0:
                return self.reconstruct_path(start, population[0])
            next_gen = population[:population_size // 4]
            while len(next_gen) < population_size:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                child = crossover(parent1, parent2)
                if random.random() < mutation_rate:
                    child = mutate(child)
                next_gen.append(child)
            population = next_gen
        best_state = max(population, key=fitness)
        return self.reconstruct_path(start, best_state) if fitness(best_state) == 0 else None

    def reconstruct_path(self, start, end):
        if not self.is_running:
            return None
        if start == end:
            return [start]
        path = []
        current = start
        visited = set()
        max_steps = 1000
        for _ in range(max_steps):
            if not self.is_running:
                return None
            path.append(current)
            if current == end:
                return path
            visited.add(tuple(map(tuple, current)))
            neighbors = [n for n in self.get_neighbors(current) if tuple(map(tuple, n)) not in visited]
            if not neighbors:
                break
            current = min(neighbors, key=lambda x: self.heuristic(x, end), default=None)
            if current is None:
                break
        return path if current == end else None

    def q_learning(self, start, goal):
        # Kiểm tra tính khả thi trước khi huấn luyện
        if not self.is_solvable(start, goal):
            return None
        
        alpha = 0.2  # Learning rate
        gamma = 0.95  # Discount factor
        epsilon = 0.8  # Initial exploration rate
        min_epsilon = 0.01
        epsilon_decay = 0.995
        episodes = 10000
        max_steps = 2000
        
        Q = {}
        actions = 4  # Up, Down, Left, Right

        def state_to_key(state):
            return tuple(tuple(row) for row in state)

        def get_action(state, neighbors, epsilon):
            state_key = state_to_key(state)
            if state_key not in Q:
                Q[state_key] = [0.0] * actions
            valid_action_mappings = []
            x, y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            for neighbor_idx, neighbor in enumerate(neighbors):
                x2, y2 = [(i, row.index(0)) for i, row in enumerate(neighbor) if 0 in row][0]
                dx, dy = x2 - x, y2 - y
                try:
                    action_idx = moves.index((dx, dy))
                    valid_action_mappings.append((neighbor_idx, action_idx))
                except ValueError:
                    continue
            if not valid_action_mappings:
                return None
            if random.random() < epsilon:
                neighbor_idx, _ = random.choice(valid_action_mappings)
                return neighbor_idx
            best_q = float('-inf')
            best_neighbor_idx = valid_action_mappings[0][0]
            for neighbor_idx, action_idx in valid_action_mappings:
                q_value = Q[state_key][action_idx]
                if q_value > best_q:
                    best_q = q_value
                    best_neighbor_idx = neighbor_idx
            return best_neighbor_idx

        # Training phase
        current_epsilon = epsilon
        for episode in range(episodes):
            if not self.is_running:
                return None
            current = [row[:] for row in start]
            visited = set()
            steps = 0
            while steps < max_steps:
                if not self.is_running:
                    return None
                if current == goal:
                    break
                state_key = state_to_key(current)
                if state_key in visited:
                    break  # Avoid getting stuck
                visited.add(state_key)
                neighbors = self.get_neighbors(current)
                if not neighbors:
                    break
                action_idx = get_action(current, neighbors, current_epsilon)
                if action_idx is None:
                    break
                next_state = neighbors[action_idx]
                next_state_key = state_to_key(next_state)
                current_h = self.heuristic(current, goal)
                next_h = self.heuristic(next_state, goal)
                if next_state == goal:
                    reward = 100
                elif next_h < current_h:
                    reward = 10
                else:
                    reward = -1
                if next_state_key not in Q:
                    Q[next_state_key] = [0.0] * actions
                x, y = [(i, row.index(0)) for i, row in enumerate(current) if 0 in row][0]
                x2, y2 = [(i, row.index(0)) for i, row in enumerate(next_state) if 0 in row][0]
                dx, dy = x2 - x, y2 - y
                moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                try:
                    q_action_idx = moves.index((dx, dy))
                except ValueError:
                    q_action_idx = 0
                future_rewards = max(Q.get(next_state_key, [0.0] * actions))
                Q[state_key][q_action_idx] = Q[state_key][q_action_idx] + alpha * (
                    reward + gamma * future_rewards - Q[state_key][q_action_idx]
                )
                current = next_state
                steps += 1
            current_epsilon = max(min_epsilon, current_epsilon * epsilon_decay)

        # Testing phase
        current = [row[:] for row in start]
        path = [current]
        visited = set()
        max_path_length = 200
        steps = 0
        while steps < max_path_length:
            if not self.is_running:
                return None
            if current == goal:
                break
            state_key = state_to_key(current)
            if state_key in visited:
                return None  # Cycle detected
            visited.add(state_key)
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return None
            action_idx = get_action(current, neighbors, 0)  # Greedy policy
            if action_idx is None:
                return None
            next_state = neighbors[action_idx]
            path.append(next_state)
            current = next_state
            steps += 1
        if current == goal:
            return path
        return None
    def update_process_grid(self, steps):
        if not steps:
            return
        delay = int(self.speed_var.get() * 1000)
        for i, step in enumerate(steps):
            if not self.is_running:
                break
            after_id = self.root.after(i * delay if i > 0 else 0, lambda s=step, step_num=i: self.display_matrix(s, step_num))
            self.after_ids.append(after_id)

    def display_matrix(self, matrix, step_num):
        for i in range(3):
            for j in range(3):
                self.process_grid[i][j].delete(0, tk.END)
                self.process_grid[i][j].insert(0, str(matrix[i][j]))
        self.root.update()
        row = step_num // 2
        col = step_num % 2
        if step_num == 0:
            bg_color = "#dbeafe"
            moved_from = None
        else:
            prev_matrix = self.last_matrix
            x1, y1 = [(i, row.index(0)) for i, row in enumerate(prev_matrix) if 0 in row][0]
            x2, y2 = [(i, row.index(0)) for i, row in enumerate(matrix) if 0 in row][0]
            dx, dy = x2 - x1, y2 - y1
            if dx == -1:
                bg_color = "#fca5a5"  # Up
            elif dx == 1:
                bg_color = "#fef08a"  # Down
            elif dy == -1:
                bg_color = "#bbf7d0"  # Left
            elif dy == 1:
                bg_color = "#93c5fd"  # Right
            else:
                bg_color = "#e5e7eb"
            moved_from = (x1, y1)
        self.create_colored_grid(self.steps_frame.scrollable_frame, f"Step {step_num}", matrix, row, col, bg_color, moved_from)
        self.last_matrix = matrix

    def create_colored_grid(self, parent, label, matrix, row, col, bg_color, moved_from=None):
        frame = tk.Frame(parent, bg=bg_color, bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        tk.Label(frame, text=label, font=("Helvetica", 10, "bold"), bg=bg_color, fg="#1e3a8a").pack(pady=2)
        grid_frame = tk.Frame(frame, bg=bg_color)
        grid_frame.pack(pady=2)
        entries = [[tk.Entry(grid_frame, width=5, justify="center", font=("Helvetica", 14), relief=tk.RIDGE, bd=2) for _ in range(3)] for _ in range(3)]
        for i, row_ in enumerate(entries):
            for j, entry in enumerate(row_):
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, str(matrix[i][j]))
                entry.config(state="readonly")
                if moved_from == (i, j):
                    entry.config(bg="#1e40af", fg="white", font=("Helvetica", 14, "bold"))
                else:
                    entry.config(bg=bg_color)

    def solve_puzzle(self, algorithm):
        if self.is_running:
            messagebox.showwarning("Warning", "Another algorithm is already running. Please reset first.")
            return
        start_state, goal_state = self.validate_input()
        if start_state is None or goal_state is None:
            return
        if not self.is_solvable(start_state, goal_state):
            self.show_error("This puzzle configuration is not solvable.")
            return
        self.is_running = True
        self.cancel_pending_updates()
        for widget in self.steps_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.last_matrix = None
        for i in range(3):
            for j in range(3):
                self.process_grid[i][j].delete(0, tk.END)
                self.process_grid[i][j].insert(0, str(start_state[i][j]))
        self.root.update()
        self.time_label.config(text="Time: 0.0s")
        self.steps_label.config(text="Steps: 0")
        start_time = time.time()

        # Run the algorithm in a separate thread to prevent UI freeze
        def run_algorithm():
            path = algorithm(start_state, goal_state)
            self.root.after(0, lambda: self.finish_algorithm(path, start_time))

        thread = threading.Thread(target=run_algorithm)
        thread.start()

    def finish_algorithm(self, path, start_time):
        end_time = time.time()
        if path and self.is_running:
            self.update_process_grid(path)
            self.steps_label.config(text=f"Steps: {len(path)}")
            self.time_label.config(text=f"Time: {end_time - start_time:.2f}s")
        else:
            self.show_error("No solution found for this configuration.")
        self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleSolverUI(root)
    root.mainloop()