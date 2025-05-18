import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file Excel
df = pd.read_excel("puzzle_results.xlsx")

# Vẽ biểu đồ thời gian chạy
plt.figure(figsize=(10, 6))
plt.bar(df["Algorithm"], df["Time (s)"], color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Algorithm")
plt.ylabel("Time (s)")
plt.title("Comparison of Algorithm Execution Time")
plt.tight_layout()
plt.savefig("time_comparison.png")

# Vẽ biểu đồ số bước/số lần mở rộng
plt.figure(figsize=(10, 6))
plt.bar(df["Algorithm"], df["Steps/Expansions"], color="lightgreen")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Algorithm")
plt.ylabel("Steps/Expansions")
plt.title("Comparison of Algorithm Steps/Expansions")
plt.tight_layout()
plt.savefig("steps_comparison.png")