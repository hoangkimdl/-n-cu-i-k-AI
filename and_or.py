import tkinter as tk
from tkinter import messagebox, ttk

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
        directions = {
            'up': (-1, 0), 'down': (1, 0),
            'left': (0, -1), 'right': (0, 1)
        }
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
            if neighbor not in path:
                subgoals = [neighbor]
                subplan = evaluate_and(subgoals, path + [state], depth + 1)
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

    final_plan = evaluate_or(start, [], 0)
    return (final_plan, expansions) if final_plan else (None, expansions)

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle AND-OR Search")
        self.root.geometry("1100x800")
        self.root.configure(bg="#E6E6FA")
        self.after_ids = []  # Store after IDs for animation cancellation
        self.start_entries = []
        self.goal_entries = []
        self.process_entries = []
        self.create_interface()

    def create_interface(self):
        title = tk.Label(self.root, text="8-Puzzle Solver - AND-OR Search", font=("Segoe UI", 20, "bold"), bg="#E6E6FA")
        title.pack(pady=20)

        matrix_frame = tk.Frame(self.root, bg="#E6E6FA")
        matrix_frame.pack(pady=10)

        self.start_entries = self.create_grid(matrix_frame, "Initial State", 0)
        self.goal_entries = self.create_grid(matrix_frame, "Goal State", 1)
        self.process_entries = self.create_grid(matrix_frame, "Current State", 2)

        control_btn = tk.Button(self.root, text="Run Search", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white",
                                command=self.run_search)
        control_btn.pack(pady=15)

        self.output_frame = tk.Frame(self.root, bg="#F5F5F5")
        self.output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.output_frame, bg="#FFFFFF")
        self.scrollbar = tk.Scrollbar(self.output_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_grid(self, parent, label, col):
        frame = tk.Frame(parent, bg="#F5F5F5")
        frame.grid(row=0, column=col, padx=20)
        tk.Label(frame, text=label, font=("Segoe UI", 14, "bold"), bg="#F5F5F5").pack(pady=5)
        grid = tk.Frame(frame)
        grid.pack()
        entries = []
        for i in range(3):
            row = []
            for j in range(3):
                e = tk.Entry(grid, width=3, font=("Segoe UI", 16), justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                row.append(e)
            entries.append(row)
        return entries

    def create_readonly_grid(self, parent, label, state, row, col, bg_color="#FFFFFF", moved_from=None):
        frame = tk.Frame(parent, bg=bg_color, bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        tk.Label(frame, text=label, font=("Segoe UI", 10, "bold"), bg=bg_color).pack(pady=2)
        grid_frame = tk.Frame(frame, bg=bg_color)
        grid_frame.pack(pady=2)
        entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                val = state[i * 3 + j]
                entry = tk.Entry(grid_frame, width=3, font=("Segoe UI", 14), justify="center", relief=tk.RIDGE, bd=2)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, str(val))
                entry.config(state="readonly")
                if moved_from and moved_from == (i, j):
                    entry.config(bg="#1E90FF", fg="white", font=("Segoe UI", 14, "bold"))
                else:
                    entry.config(bg=bg_color)
                row_entries.append(entry)
            entries.append(row_entries)
        return entries

    def get_state(self, entries):
        state = []
        try:
            for row in entries:
                for e in row:
                    val = e.get().strip()
                    state.append(int(val) if val else 0)
            if sorted(state) != list(range(9)):
                raise ValueError
            return tuple(state)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter unique numbers 0 to 8.")
            return None

    def update_process_grid(self, state):
        for i in range(3):
            for j in range(3):
                self.process_entries[i][j].delete(0, tk.END)
                self.process_entries[i][j].insert(0, str(state[i * 3 + j]))

    def cancel_pending_updates(self):
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass
        self.after_ids.clear()

    def display_step(self, state, step_num, last_state=None):
        bg_color = "#FFFFFF"
        moved_from = None
        if last_state and step_num > 0:
            x1 = last_state.index(0)
            x2 = state.index(0)
            r1, c1 = divmod(x1, 3)
            r2, c2 = divmod(x2, 3)
            dr, dc = r2 - r1, c2 - c1
            if dr == -1:  # Up
                bg_color = "#FCA5A5"
            elif dr == 1:  # Down
                bg_color = "#FEF08A"
            elif dc == -1:  # Left
                bg_color = "#BBF7D0"
            elif dc == 1:  # Right
                bg_color = "#93C5FD"
            moved_from = (r1, c1)
        self.update_process_grid(state)
        self.create_readonly_grid(self.scrollable_frame, f"Step {step_num}", state, step_num // 3, step_num % 3, bg_color, moved_from)
        self.root.update()

    def run_search(self):
        self.cancel_pending_updates()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        start = self.get_state(self.start_entries)
        goal = self.get_state(self.goal_entries)
        if not start or not goal:
            return

        path, expansions = and_or_search(start, goal)

        if path:
            delay = 1000  # 1 second delay between steps
            last_state = None
            for step, state in enumerate(path):
                after_id = self.root.after(step * delay, lambda s=state, n=step, ls=last_state: self.display_step(s, n, ls))
                self.after_ids.append(after_id)
                last_state = state
        else:
            messagebox.showinfo("Result", "No solution found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()