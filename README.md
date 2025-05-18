# Nguyễn Thị Hoàng Kim - 23110248
# Môn học: Trí tuệ nhân tạo
# 🧩 8 Puzzle Solver - Báo cáo cá nhân

Đây là báo cáo cá nhân cho đồ án giải bài toán 8 ô chữ (8 puzzle) bằng nhiều thuật toán tìm kiếm khác nhau, bao gồm: tìm kiếm không có thông tin, có thông tin, tìm kiếm cục bộ, học tăng cường và các kỹ thuật mở rộng như môi trường không xác định và bài toán ràng buộc. Dự án tập trung vào so sánh hiệu quả các chiến lược khác nhau khi áp dụng lên cùng một môi trường.

---

## 🧭 1️⃣ Mục tiêu

Bài toán 8 puzzle là một trò chơi cổ điển được sử dụng rộng rãi trong lĩnh vực trí tuệ nhân tạo để kiểm tra hiệu quả của các thuật toán tìm kiếm. Dự án này được xây dựng với các mục tiêu chính như sau:

- ✅ Hiểu rõ lý thuyết và áp dụng vào thực tế: Thực hiện các thuật toán tìm kiếm học được trong môn học và triển khai chúng để giải bài toán thực tế 8 puzzle.
- ✅ So sánh hiệu quả thuật toán: Đánh giá và so sánh các chiến lược dựa trên:
  - Số lượng node duyệt
  - Độ sâu lời giải
  - Thời gian thực thi
  - Mức độ tối ưu của lời giải
- ✅ Phân tích theo nhóm chiến lược:
  - Tìm kiếm không có thông tin (BFS, DFS, IDS, UCS)
  - Tìm kiếm có thông tin (Greedy, IDA*, Beam Search, v.v.)
  - Tìm kiếm cục bộ và học tăng cường (Hill Climbing, Simulated Annealing, Q-Learning, Genetic Algorithm, ...)
  - Môi trường không xác định và chỉ quan sát một phần (Belief, AND-OR)
  - Ràng buộc và kiểm tra ràng buộc (Backtracking, AC-3)
- ✅ Trực quan hóa thuật toán: Sử dụng ảnh động (GIF) để biểu diễn quá trình hoạt động của từng thuật toán một cách trực quan.
- ✅ Tổng kết và đánh giá: Rút ra nhận xét về độ phù hợp của từng thuật toán đối với bài toán cụ thể này.

---

## 🧠 2️⃣ Nội dung

### 🔰 Tổng quan về thành phần bài toán 8 puzzle

Bài toán 8 puzzle là một trò chơi giải đố gồm 8 ô số và 1 ô trống nằm trên một bảng 3x3. Mục tiêu là đưa các ô về đúng vị trí theo một cấu hình đích bằng cách di chuyển ô trống.

#### ✅ Thành phần bài toán:
- Trạng thái ban đầu (initial state): vị trí cụ thể của 8 ô số và ô trống tại thời điểm bắt đầu.
- Tập hành động (actions): di chuyển ô trống theo các hướng: trái, phải, lên, xuống (nếu không bị giới hạn bởi biên).
- Trạng thái kế tiếp (transition model): mỗi hành động sẽ tạo ra trạng thái mới bằng cách hoán đổi ô trống với ô lân cận.
- Trạng thái đích (goal state):
  
  1 2 3  
  4 5 6  
  7 8 _

- Chi phí (path cost): mỗi bước di chuyển có chi phí = 1.

#### 🎯 Bài toán đặt ra:
Tìm một chuỗi các hành động từ trạng thái ban đầu đến trạng thái đích sao cho tổng chi phí là nhỏ nhất (tối ưu), đồng thời đánh giá độ hiệu quả của từng thuật toán sử dụng.

---

### 📚 Danh sách thuật toán được triển khai

---
#### 🔵 Tìm kiếm không có thông tin (Uninformed Search)
- [ ] Breadth-First Search (BFS)
- [ ] Depth-First Search (DFS)
- [ ] Iterative Deepening Search (IDS)
- [ ] Uniform Cost Search (UCS)

#### 🟢 Tìm kiếm có thông tin (Heuristic / Informed Search)
- [ ] Greedy Best-First Search
- [ ] IDA* (Iterative Deepening A*)
- [ ] Beam Search

#### 🟡 Tìm kiếm cục bộ & học tăng cường (Local Search & RL)
- [ ] Simple Hill Climbing
- [ ] Steepest-Ascent Hill Climbing
- [ ] Stochastic Hill Climbing
- [ ] Simulated Annealing
- [ ] Genetic Algorithm
- [ ] Q-Learning

#### 🔶 Tìm kiếm trong môi trường phức tạp (Uncertain / Partially Observable)
- [ ] AND-OR Search
- [ ] Belief State Search
- [ ] Không nhìn thấy gì (Conformant Planning)
- [ ] Quan sát một phần (Partial Observability)

#### 🟣 Tìm kiếm trong môi trường ràng buộc (Constraint-Based Search)
- [ ] Backtracking Search
- [ ] AC-3 (Arc Consistency Algorithm)

#### 🧪 Kiểm thử và đánh giá hiệu năng
- [ ] Kiểm thử đơn vị (Unit Test)
- [ ] Kiểm thử tổng thể (Integration Test)
- [ ] Đo lường hiệu suất: thời gian, số bước, tối ưu lời giải

---
#### 💡 Trong các phần tiếp theo, mỗi thuật toán sẽ được trình bày chi tiết theo cấu trúc:
- ✅ Mô tả nguyên lý hoạt động
- 🧮 Ưu điểm & Nhược điểm
- 🎬 Hình ảnh động minh họa (GIF)
- 📊 So sánh hiệu suất (nếu có)
#### 🔹 Breadth-First Search (BFS)

✅ Nguyên lý hoạt động:
- BFS tìm kiếm theo chiều rộng, mở rộng các nút theo từng tầng.
- Sử dụng hàng đợi FIFO.
- Đảm bảo tìm ra lời giải ngắn nhất (nếu chi phí di chuyển đều nhau).

📊 Ưu – Nhược điểm:

| Ưu điểm                          | Nhược điểm                                 |
|----------------------------------|---------------------------------------------|
| Đảm bảo tìm được lời giải ngắn nhất | Tốn bộ nhớ rất lớn                         |
| Dễ cài đặt                        | Không hiệu quả cho không gian tìm kiếm rộng |

---

#### 🔹 Depth-First Search (DFS)

✅ Nguyên lý hoạt động:
- Tìm kiếm theo chiều sâu, đi hết một nhánh trước khi quay lại.
- Sử dụng ngăn xếp (hoặc đệ quy).
- Không đảm bảo tìm ra lời giải tối ưu, có thể đi vào vòng lặp nếu không kiểm soát.

📊 Ưu – Nhược điểm:

| Ưu điểm               | Nhược điểm                       |
|------------------------|----------------------------------|
| Ít tốn bộ nhớ hơn BFS  | Có thể không tìm được lời giải  |
| Dễ cài đặt bằng đệ quy | Không tối ưu, dễ kẹt nhánh sai   |

---

#### 🔹 Iterative Deepening Search (IDS)

✅ Nguyên lý hoạt động:
- Kết hợp giữa BFS và DFS bằng cách tăng dần độ sâu tìm kiếm.
- Ở mỗi mức, thực hiện DFS với giới hạn độ sâu.
- Giải pháp cân bằng giữa thời gian và bộ nhớ.

📊 Ưu – Nhược điểm:

| Ưu điểm                  | Nhược điểm                           |
|--------------------------|--------------------------------------|
| Tiết kiệm bộ nhớ như DFS | Lặp lại việc duyệt nhiều node        |
| Tìm được lời giải ngắn nhất | Tốn thời gian hơn BFS một chút   |

🎬 Hình ảnh minh họa:

![IDS Demo](images/ids.gif)

---

#### 🔹 Uniform Cost Search (UCS)

✅ Nguyên lý hoạt động:
- Tương tự BFS nhưng mở rộng nút có chi phí đường đi thấp nhất trước.
- Sử dụng hàng đợi ưu tiên.
- Đảm bảo tìm được lời giải tối ưu nếu chi phí luôn dương.

📊 Ưu – Nhược điểm:

| Ưu điểm                             | Nhược điểm                             |
|-------------------------------------|----------------------------------------|
| Tìm được lời giải tối ưu            | Tốn thời gian nếu có nhiều đường đi    |
| Áp dụng được khi chi phí không đều | Cần cấu trúc dữ liệu ưu tiên           |

🎬 Hình ảnh minh họa:

![UCS Demo](images/ucs.gif)

---




