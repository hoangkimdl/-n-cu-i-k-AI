import tkinter as tk
from tkinter import messagebox
from moitruongkthongtin_cothongtin_cucbo import PuzzleSolverUI
from moitruongphuctap import UnifiedPuzzleApp
import os
import subprocess
import webbrowser
import pandas as pd
import json

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
        compare_window.geometry("400x200")
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
            command=self.generate_and_show_charts
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

    def generate_and_show_charts(self):
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

        # Prepare data for Chart.js
        chart_data = {
            "algorithms": algorithms,
            "times": times,
            "steps": steps
        }

        # Generate HTML content with embedded data
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Algorithm Comparison Charts</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f0f4f8; }}
        .chart-container {{ width: 90%; margin: 20px auto; }}
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="timeChart"></canvas>
    </div>
    <div class="chart-container">
        <canvas id="stepsChart"></canvas>
    </div>
    <script>
        const chartData = {json.dumps(chart_data)};

        // Time Chart
        const timeCtx = document.getElementById('timeChart').getContext('2d');
        new Chart(timeCtx, {{
            type: 'bar',
            data: {{
                labels: chartData.algorithms,
                datasets: [{{
                    label: 'Time (s)',
                    data: chartData.times,
                    backgroundColor: 'rgba(76, 175, 80, 0.6)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                scales: {{
                    y: {{ beginAtZero: true, title: {{ display: true, text: 'Time (s)' }} }},
                    x: {{ title: {{ display: true, text: 'Algorithm' }}, ticks: {{ autoSkip: false, maxRotation: 45, minRotation: 45 }} }}
                }},
                plugins: {{ title: {{ display: true, text: 'Comparison of Algorithm Execution Time' }} }}
            }}
        }});

        // Steps/Expansions Chart
        const stepsCtx = document.getElementById('stepsChart').getContext('2d');
        new Chart(stepsCtx, {{
            type: 'bar',
            data: {{
                labels: chartData.algorithms,
                datasets: [{{
                    label: 'Steps/Expansions',
                    data: chartData.steps,
                    backgroundColor: 'rgba(33, 150, 243, 0.6)',
                    borderColor: 'rgba(33, 150, 243, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                scales: {{
                    y: {{ beginAtZero: true, title: {{ display: true, text: 'Steps/Expansions' }} }},
                    x: {{ title: {{ display: true, text: 'Algorithm' }}, ticks: {{ autoSkip: false, maxRotation: 45, minRotation: 45 }} }}
                }},
                plugins: {{ title: {{ display: true, text: 'Comparison of Algorithm Steps/Expansions' }} }}
            }}
        }});
    </script>
</body>
</html>
        """

        # Save the HTML file
        try:
            with open("algorithm_comparison.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            webbrowser.open("algorithm_comparison.html")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate charts: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()