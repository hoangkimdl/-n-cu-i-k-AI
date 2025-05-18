import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
import time

# ===================== AND-OR SEARCH (Single State) =====================
def and_or_search(start, goal, max_depth=50):
    expansions = 0
    def is_goal(state):
        return state == goal

    def is_cycle(state, path):
        return state in path

    def expand_state(state):
        neighbors = []
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        for dr, dc in directions.values():
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_index = nr * 3 + nc
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(tuple(new_state))
        return neighbors

    def evaluate_or(state, path, depth):
        nonlocal expansions
        if is_goal(state):
            return [state]
        if is_cycle(state, path) or depth > max_depth:
            return None
        expansions += 1
        for neighbor in expand_state(state):
            subplan = evaluate_and([neighbor], path + [state], depth + 1)
            if subplan:
                return [state] + subplan
        return None

    def evaluate_and(substates, path, depth):
        plan = []
        for s in substates:
            result = evaluate_or(s, path, depth)
            if result is None:
                return None
            plan.extend(result[1:] if plan else result)
        return plan

    start_time = time.perf_counter()
    final_plan = evaluate_or(start, [], 0)
    end_time = time.perf_counter()
    computation_time = end_time - start_time
    return (final_plan, expansions, computation_time) if final_plan else (None, expansions, computation_time)

# ===================== BELIEF SEARCH (Multiple States) =====================
def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        row1, col1 = divmod(i, 3)
        row2, col2 = divmod(goal.index(state[i]), 3)
        distance += abs(row1 - row2) + abs(col1 - col2)
    return distance

def is_valid_state(state):
    return sorted(state) == list(range(9))

def and_or_belief_search(b_initial_set, goal_state, max_depth=200):
    if not b_initial_set:
        return set(), None, 0, 0.0

    b_initial = {state: 1.0 / len(b_initial_set) for state in b_initial_set}
    expansions = 0
    possible_beliefs = set()
    visited = set()

    def is_goal_belief(belief):
        prob = belief.get(tuple(goal_state), 0.0)
        return prob > 0.05

    def expand_belief(belief):
        new_beliefs = {}
        for state, prob in belief.items():
            zero_idx = state.index(0)
            row, col = divmod(zero_idx, 3)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    new_idx = nr * 3 + nc
                    new_state = list(state)
                    new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                    new_state = tuple(new_state)
                    if is_valid_state(new_state):
                        new_beliefs[new_state] = new_beliefs.get(new_state, 0.0) + prob / 4.0
        return new_beliefs

    def normalize_belief(belief):
        total = sum(belief.values())
        return {k: v / total for k, v in belief.items()} if total > 0 else belief

    start_time = time.perf_counter()
    queue = deque([(b_initial, [next(iter(b_initial))], 0)])
    while queue:
        belief, path, depth = queue.popleft()
        belief_key = frozenset(belief.items())
        if belief_key in visited:
            continue
        visited.add(belief_key)
        expansions += 1
        possible_beliefs.add(belief_key)

        if is_goal_belief(belief):
            end_time = time.perf_counter()
            computation_time = end_time - start_time
            return possible_beliefs, path, expansions, computation_time

        if depth >= max_depth:
            continue

        new_belief = expand_belief(belief)
        updated_belief = normalize_belief(new_belief)

        next_state = min(updated_belief.items(), key=lambda x: manhattan_distance(x[0], goal_state))[0]
        if next_state not in path and is_valid_state(next_state):
            queue.append((updated_belief, path + [next_state], depth + 1))

    end_time = time.perf_counter()
    computation_time = end_time - start_time
    return possible_beliefs, None, expansions, computation_time

# ===================== GUI =====================
class UnifiedPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (AND-OR & Belief Search)")
        self.root.geometry("1200x700")
        self.root.configure(bg="#E6E6FA")

        self.mode_var = tk.StringVar(value="AND-OR Search")
        self.create_widgets()

    def create_widgets(self):
        # Top frame: chọn thuật toán
        top_frame = tk.Frame(self.root, bg="#E6E6FA")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Select Algorithm:", font=("Segoe UI", 12), bg="#E6E6FA").pack(side=tk.LEFT, padx=5)
        algo_menu = ttk.Combobox(top_frame, textvariable=self.mode_var, values=["AND-OR Search", "Belief Search"], state="readonly")
        algo_menu.pack(side=tk.LEFT, padx=5)
        algo_menu.bind("<<ComboboxSelected>>", self.toggle_mode)

        # Frame nhập trạng thái ban đầu
        self.input_frame = tk.LabelFrame(self.root, text="Initial State(s)", font=("Segoe UI", 12, "bold"), bg="#E6E6FA")
        self.input_frame.pack(pady=5)
        self.initial_state_entries = self.create_grid(self.input_frame)

        # Text hướng dẫn cho Belief Search
        self.belief_hint = tk.Label(self.input_frame, text="Nhập danh sách các trạng thái, ví dụ: [(1,2,3,4,5,6,0,7,8), ...]", font=("Segoe UI", 10), bg="#E6E6FA", fg="#555")
        self.initial_states_text = tk.Text(self.input_frame, height=3, width=60, font=("Segoe UI", 10))
        self.belief_hint.pack_forget()
        self.initial_states_text.pack_forget()

        # Nút xóa nhanh
        self.clear_btn = tk.Button(self.input_frame, text="Clear", command=self.clear_inputs, font=("Segoe UI", 10))
        self.clear_btn.pack(pady=2)

        # Frame nhập trạng thái đích
        self.goal_frame = tk.LabelFrame(self.root, text="Goal State", font=("Segoe UI", 12, "bold"), bg="#E6E6FA")
        self.goal_frame.pack(pady=5)
        self.goal_state_entries = self.create_grid(self.goal_frame)

        # Nút chạy thuật toán
        tk.Button(self.root, text="Run Search", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", command=self.run_search).pack(pady=5)

        # Khung kết quả có thanh cuộn
        result_frame = tk.LabelFrame(self.root, text="Solution Steps", font=("Segoe UI", 12, "bold"), bg="#E6E6FA")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.result_canvas = tk.Canvas(result_frame, bg="#FFFFFF")
        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.result_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.result_inner = tk.Frame(self.result_canvas, bg="#FFFFFF")
        self.result_canvas.create_window((0, 0), window=self.result_inner, anchor="nw")
        self.result_inner.bind("<Configure>", lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all")))

    def toggle_mode(self, event=None):
        if self.mode_var.get() == "Belief Search":
            for row in self.initial_state_entries:
                for e in row:
                    e.grid_remove()
            self.belief_hint.pack()
            self.initial_states_text.pack()
        else:
            self.belief_hint.pack_forget()
            self.initial_states_text.pack_forget()
            for i, row in enumerate(self.initial_state_entries):
                for j, e in enumerate(row):
                    e.grid(row=i, column=j, padx=2, pady=2)

    def create_grid(self, parent):
        entries = []
        frame = tk.Frame(parent, bg="#E6E6FA")
        frame.pack()
        for i in range(3):
            row = []
            for j in range(3):
                e = tk.Entry(frame, width=3, font=("Segoe UI", 14), justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            entries.append(row)
        return entries

    def clear_inputs(self):
        for row in self.initial_state_entries:
            for e in row:
                e.delete(0, tk.END)
        self.initial_states_text.delete("1.0", tk.END)
        for row in self.goal_state_entries:
            for e in row:
                e.delete(0, tk.END)
        for widget in self.result_inner.winfo_children():
            widget.destroy()

    def get_grid_state(self, entries):
        state = []
        try:
            for row in entries:
                for e in row:
                    state.append(int(e.get()))
            if sorted(state) != list(range(9)):
                raise ValueError
            return tuple(state)
        except:
            messagebox.showerror("Error", "Invalid grid state (must contain 0-8 uniquely)")
            return None

    def run_search(self):
        for widget in self.result_inner.winfo_children():
            widget.destroy()

        goal = self.get_grid_state(self.goal_state_entries)
        if not goal:
            return

        if self.mode_var.get() == "AND-OR Search":
            start = self.get_grid_state(self.initial_state_entries)
            if not start:
                return
            path, expansions, computation_time = and_or_search(start, goal)
            if path:
                for idx, state in enumerate(path):
                    self.display_state(state, idx)
            messagebox.showinfo("Done", f"Expansions: {expansions}\nComputation Time: {computation_time:.4f}s")

        else:
            try:
                states = eval(self.initial_states_text.get("1.0", tk.END).strip())
                if not isinstance(states, list) or not all(isinstance(s, tuple) and len(s) == 9 for s in states):
                    raise ValueError
                beliefs, path, expansions, computation_time = and_or_belief_search(set(states), goal)
                if path:
                    for idx, state in enumerate(path):
                        self.display_state(state, idx)
                else:
                    messagebox.showinfo("Result", "No solution found.")
                self.display_beliefs(beliefs)
                messagebox.showinfo("Done", f"Expansions: {expansions}\nComputation Time: {computation_time:.4f}s\nBeliefs found: {len(beliefs)}")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid initial states format\n{e}")

    def display_state(self, state, step):
        frame = tk.Frame(self.result_inner, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        frame.pack(pady=3)
        tk.Label(frame, text=f"Step {step}", font=("Segoe UI", 10, "bold"), bg="#FFFFFF").pack()
        for i in range(3):
            row_frame = tk.Frame(frame, bg="#FFFFFF")
            row_frame.pack()
            for j in range(3):
                val = state[i * 3 + j]
                e = tk.Entry(row_frame, width=3, font=("Segoe UI", 12), justify="center")
                e.insert(0, str(val))
                e.config(state="readonly")
                e.pack(side=tk.LEFT, padx=1, pady=1)

    def display_beliefs(self, possible_beliefs):
        frame = tk.Frame(self.result_inner, bg="#F0F8FF", bd=1, relief=tk.SOLID)
        frame.pack(pady=5)
        tk.Label(frame, text="Các belief đã duyệt:", font=("Segoe UI", 10, "bold"), bg="#F0F8FF").pack()
        count = 0
        for belief in possible_beliefs:
            count += 1
            sub_frame = tk.Frame(frame, bg="#F0F8FF")
            sub_frame.pack(pady=2, anchor="w")
            tk.Label(sub_frame, text=f"Belief #{count}:", font=("Segoe UI", 9, "bold"), bg="#F0F8FF").pack(anchor="w")
            for state, prob in sorted(belief, key=lambda x: -x[1]):
                grid_frame = tk.Frame(sub_frame, bg="#F0F8FF")
                grid_frame.pack(anchor="w")
                for i in range(3):
                    row = ""
                    for j in range(3):
                        row += f"{state[i*3+j]} "
                    if j == 2:
                        row += f"   (p={prob:.2f})"
                    tk.Label(grid_frame, text=row, font=("Consolas", 9), bg="#F0F8FF").pack(anchor="w")
                tk.Label(grid_frame, text="").pack()  # Khoảng cách

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedPuzzleApp(root)
    root.mainloop()