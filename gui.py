import tkinter as tk
from tkinter import messagebox
from moitruongkthongtin_cothongtin_cucbo import PuzzleSolverUI
from moitruongphuctap import UnifiedPuzzleApp
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver - Main Menu")
        self.root.geometry("600x400")
        self.root.configure(bg="#e0e7ff")

        main_frame = tk.Frame(root, bg="#ffffff", bd=0, relief=tk.FLAT)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        main_frame.configure(highlightbackground="#d1d5db", highlightthickness=2)

        tk.Label(main_frame, text="8-Puzzle Solver", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#1e3a8a").pack(pady=15)

        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Môi trường có thông tin/Không có thông tin/Cục bộ",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=40,
            height=2,
            command=self.open_informed_uninformed_local
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Môi trường phức tạp",
            font=("Helvetica", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=40,
            height=2,
            command=self.open_complex_environment
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Compare Algorithms",
            font=("Helvetica", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=40,
            height=2,
            command=self.open_compare_window
        ).pack(pady=10)

    def open_informed_uninformed_local(self):
        try:
            new_window = tk.Toplevel(self.root)
            app = PuzzleSolverUI(new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Puzzle Solver: {str(e)}")

    def open_complex_environment(self):
        try:
            new_window = tk.Toplevel(self.root)
            app = UnifiedPuzzleApp(new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Complex Environment: {str(e)}")

    def open_compare_window(self):
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Compare Algorithms")
        compare_window.geometry("900x600")
        compare_window.configure(bg="#e0e7ff")

        compare_frame = tk.Frame(compare_window, bg="#ffffff", bd=0, relief=tk.FLAT)
        compare_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        compare_frame.configure(highlightbackground="#d1d5db", highlightthickness=2)

        tk.Button(
            compare_frame,
            text="View Excel File",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=30,
            height=2,
            command=self.open_excel
        ).pack(pady=10)

        tk.Button(
            compare_frame,
            text="View Charts",
            font=("Helvetica", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=30,
            height=2,
            command=lambda: self.generate_and_show_charts(compare_frame)
        ).pack(pady=10)

    def open_excel(self):
        if os.path.exists("puzzle_results.xlsx"):
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile("puzzle_results.xlsx")
                else:  # For Mac and Linux
                    subprocess.Popen(['open', 'puzzle_results.xlsx'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Excel file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No puzzle_results.xlsx file found. Run an algorithm first to generate data.")

    def generate_and_show_charts(self, parent_frame):
        # Clear any existing charts in the parent frame
        for widget in parent_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != parent_frame:
                widget.destroy()

        if not os.path.exists("puzzle_results.xlsx"):
            messagebox.showwarning("Warning", "No puzzle_results.xlsx file found. Run an algorithm first to generate data.")
            return

        # Read the Excel file
        try:
            df = pd.read_excel("puzzle_results.xlsx")
            algorithms = df["Algorithm"].tolist()
            times = df["Time (s)"].tolist()
            steps = df["Steps/Expansions"].tolist()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file: {str(e)}")
            return

        # Đổi tên hiển thị cho thuật toán nếu muốn
        display_names = []
        for name in algorithms:
            if name.lower() == "bfs":
                display_names.append("Breadth-First Search")
            elif name.lower() == "dfs":
                display_names.append("Depth-First Search")
            elif name.lower() == "ids":
                display_names.append("Iterative Deepening")
            elif name.lower() == "ucs":
                display_names.append("Uniform Cost Search")
            elif name.lower() == "greedy search":
                display_names.append("Greedy Search")
            elif name.lower() == "ida":
                display_names.append("IDA*")
            elif name.lower() == "a*":
                display_names.append("A* Search")
            elif name.lower() == "simple hill":
                display_names.append("Simple Hill Climbing")
            elif name.lower() == "steepest hill":
                display_names.append("Steepest Hill Climbing")
            elif name.lower() == "stochastic hill":
                display_names.append("Stochastic Hill Climbing")
            elif name.lower() == "simulated anneal":
                display_names.append("Simulated Annealing")
            elif name.lower() == "beam search":
                display_names.append("Beam Search")
            elif name.lower() == "genetic algo":
                display_names.append("Genetic Algorithm")
            elif name.lower() == "q-learning":
                display_names.append("Q-Learning")
            elif name.lower() == "and-or search":
                display_names.append("AND-OR Search")
            elif name.lower() == "belief search":
                display_names.append("Belief Search")
            else:
                display_names.append(name)

        # Create a frame to hold the charts
        chart_frame = tk.Frame(parent_frame, bg="#ffffff")
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Plot Time Comparison
        fig1, ax1 = plt.subplots(figsize=(max(8, len(display_names)*0.7), 3))
        ax1.bar(display_names, times, color="skyblue")
        ax1.set_xlabel("Algorithm")
        ax1.set_ylabel("Time (s)")
        ax1.set_title("Comparison of Algorithm Execution Time")
        ax1.set_xticks(range(len(display_names)))
        ax1.set_xticklabels(display_names, rotation=30, ha='right')

        plt.tight_layout()

        # Embed the time chart into the Tkinter window
        canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(pady=10)

        # Plot Steps/Expansions Comparison
        fig2, ax2 = plt.subplots(figsize=(max(8, len(display_names)*0.7), 3))
        ax2.bar(display_names, steps, color="lightgreen")
        ax2.set_xlabel("Algorithm")
        ax2.set_ylabel("Steps/Expansions")
        ax2.set_title("Comparison of Algorithm Steps/Expansions")
        ax2.set_xticks(range(len(display_names)))
        ax2.set_xticklabels(display_names, rotation=30, ha='right')

        plt.tight_layout()

        # Embed the steps chart into the Tkinter window
        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()