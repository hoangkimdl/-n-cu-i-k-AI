# utils.py
import pandas as pd
import os
from tkinter import messagebox

def save_to_excel(new_results):
    file_path = "puzzle_results.xlsx"
    try:
        # If the file exists, load existing data
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            # Convert new results to DataFrame
            new_df = pd.DataFrame(new_results, columns=["Algorithm", "Steps/Expansions", "Time (s)"])
            # Append new results to existing data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # If file doesn't exist, create a new DataFrame
            combined_df = pd.DataFrame(new_results, columns=["Algorithm", "Steps/Expansions", "Time (s)"])
        
        # Save the combined DataFrame back to Excel
        combined_df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Results have been saved to puzzle_results.xlsx")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save results: {str(e)}")