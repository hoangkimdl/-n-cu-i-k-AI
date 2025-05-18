import tkinter as tk
from tkinter import messagebox
from moitruongkthongtin_cothongtin_cucbo import PuzzleSolverUI
from moitruongphuctap import UnifiedPuzzleApp

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver - Main Menu")
        self.root.geometry("600x400")
        self.root.configure(bg="#e0e7ff")

        # Frame chính
        main_frame = tk.Frame(root, bg="#ffffff", bd=0, relief=tk.FLAT)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        main_frame.configure(highlightbackground="#d1d5db", highlightthickness=2)

        # Tiêu đề
        tk.Label(main_frame, text="8-Puzzle Solver", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#1e3a8a").pack(pady=15)

        # Frame chứa các nút
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=20)

        # Nút cho môi trường có thông tin/không có thông tin/cục bộ
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

        # Nút cho môi trường phức tạp
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

    def open_informed_uninformed_local(self):
        # Mở giao diện từ A.py (PuzzleSolverUI) trực tiếp trong main thread
        try:
            new_window = tk.Toplevel(self.root)
            app = PuzzleSolverUI(new_window)
            # Không gọi mainloop() ở đây vì Toplevel không cần nó
            # mainloop() chính đã được gọi ở cửa sổ root
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Puzzle Solver: {str(e)}")

    def open_complex_environment(self):
        # Mở giao diện từ giaodien.py (UnifiedPuzzleApp) trực tiếp trong main thread
        try:
            new_window = tk.Toplevel(self.root)
            app = UnifiedPuzzleApp(new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Complex Environment: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()