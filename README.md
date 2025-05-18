#Nguyễn Thị Hoàng Kim - 23110248
# Môn học: Trí tuệ nhân tạo
# 🧩 8 Puzzle Solver - Báo cáo cá nhân

Đây là báo cáo cá nhân cho đồ án giải bài toán 8 ô chữ (8 puzzle) bằng nhiều thuật toán tìm kiếm khác nhau, bao gồm: tìm kiếm không có thông tin, có thông tin, tìm kiếm cục bộ và học tăng cường. Dự án tập trung vào so sánh hiệu quả các chiến lược khác nhau khi áp dụng lên cùng một môi trường.

---

## 🧭 1️⃣ Mục tiêu

Bài toán 8 puzzle là một trò chơi cổ điển được sử dụng rộng rãi trong lĩnh vực trí tuệ nhân tạo để kiểm tra hiệu quả của các thuật toán tìm kiếm. Dự án này được xây dựng với các mục tiêu chính như sau:

- ✅ **Hiểu rõ lý thuyết và áp dụng vào thực tế**: Thực hiện các thuật toán tìm kiếm học được trong môn học và triển khai chúng để giải bài toán thực tế 8 puzzle.
- ✅ **So sánh hiệu quả thuật toán**: Đánh giá và so sánh các chiến lược dựa trên:
  - Số lượng node duyệt
  - Độ sâu lời giải
  - Thời gian thực thi
  - Mức độ tối ưu của lời giải
- ✅ **Phân tích theo nhóm chiến lược**:
  - **Tìm kiếm không có thông tin** (BFS, DFS, IDS, UCS)
  - **Tìm kiếm có thông tin** (Greedy, IDA*, Beam Search, v.v.)
  - **Tìm kiếm cục bộ và học tăng cường** (Hill Climbing, Simulated Annealing, Q-Learning, Genetic Algorithm, ...)
- ✅ **Trực quan hóa thuật toán**: Sử dụng ảnh động (GIF) để biểu diễn quá trình hoạt động của từng thuật toán một cách trực quan.
- ✅ **Tổng kết và đánh giá**: Rút ra nhận xét về độ phù hợp của từng thuật toán đối với bài toán cụ thể này.

---

## 🧠 2️⃣ Nội dung

### 🔰 Tổng quan về thành phần bài toán 8 puzzle

Bài toán 8 puzzle là một trò chơi giải đố gồm 8 ô số và 1 ô trống nằm trên một bảng 3x3. Mục tiêu là đưa các ô về đúng vị trí theo một cấu hình đích bằng cách di chuyển ô trống.

#### ✅ Thành phần bài toán:
- **Trạng thái ban đầu** (`initial state`): vị trí cụ thể của 8 ô số và ô trống tại thời điểm bắt đầu.
- **Tập hành động** (`actions`): di chuyển ô trống theo các hướng: trái, phải, lên, xuống (nếu không bị giới hạn bởi biên).
- **Trạng thái kế tiếp** (`transition model`): mỗi hành động sẽ tạo ra trạng thái mới bằng cách hoán đổi ô trống với ô lân cận.
- **Trạng thái đích (goal state)**:
1 2 3
4 5 6
7 8 _
- **Chi phí (path cost)**: mỗi bước di chuyển có chi phí = 1.

#### 🎯 Bài toán đặt ra:
Tìm một chuỗi các hành động từ trạng thái ban đầu đến trạng thái đích sao cho tổng chi phí là nhỏ nhất (tối ưu), đồng thời đánh giá độ hiệu quả của từng thuật toán sử dụng.

---

### 📚 Danh sách thuật toán được triển khai

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
- [ ] AND-OR Graph Search
- [ ] Belief State Search
- [ ] Không nhìn thấy gì (Blind Environment)
- [ ] Chỉ quan sát một phần (Partial Observability)

#### 🟣 Tìm kiếm trong môi trường ràng buộc (Constraint-Based Search)
- [ ] Backtracking Search
- [ ] AC-3 Algorithm (Arc Consistency)
- [ ] Testing Algorithm
---
#### 💡 Trong các phần tiếp theo, mỗi thuật toán sẽ được trình bày chi tiết theo cấu trúc:
- ✅ Mô tả nguyên lý hoạt động
- 🧮 Ưu điểm & Nhược điểm
- 🎬 Hình ảnh động minh họa (GIF)
- 📊 So sánh hiệu suất (nếu có)
---
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
### 🔹 Greedy Best-First Search

✅ Nguyên lý hoạt động:
- Mở rộng node gần đích nhất theo heuristic.
- Không xét chi phí đã đi (g(n)), chỉ xét h(n).
- Nhanh nhưng không đảm bảo tìm lời giải tối ưu.

📊 Ưu – Nhược điểm:

| Ưu điểm                   | Nhược điểm                        |
|----------------------------|-----------------------------------|
| Nhanh                     | Dễ sai nếu heuristic kém          |
| Tiết kiệm bộ nhớ hơn A*   | Không đảm bảo tối ưu              |

🎬 Hình ảnh minh họa:

![Greedy Demo](images/greedy.gif)

---

### 🔹 Beam Search

✅ Nguyên lý hoạt động:
- Chỉ giữ lại một số lượng node "tốt nhất" tại mỗi mức theo heuristic.
- Là phiên bản giới hạn của Greedy → tiết kiệm bộ nhớ.

📊 Ưu – Nhược điểm:

| Ưu điểm                   | Nhược điểm                            |
|----------------------------|----------------------------------------|
| Rất tiết kiệm tài nguyên | Có thể bỏ qua lời giải tốt hơn         |
| Nhanh                     | Không tối ưu, không hoàn chỉnh         |

🎬 Hình ảnh minh họa:

![Beam Demo](images/beam.gif)

---

### 🔹 IDA* (Iterative Deepening A*)

✅ Nguyên lý hoạt động:
- Kết hợp A* với DFS giới hạn theo hàm f(n) = g(n) + h(n).
- Mỗi lần tìm kiếm được lặp lại với ngưỡng f tăng dần.
- Cân bằng bộ nhớ và độ chính xác.

📊 Ưu – Nhược điểm:

| Ưu điểm                    | Nhược điểm                           |
|----------------------------|----------------------------------------|
| Bộ nhớ thấp hơn A*        | Tốn thời gian hơn A*                  |
| Tối ưu nếu heuristic tốt  | Có thể duyệt lặp lại nhiều node       |

🎬 Hình ảnh minh họa:

![IDA* Demo](images/idastar.gif)
---
### 🔹 Simple Hill Climbing

✅ Nguyên lý hoạt động:
- Di chuyển sang trạng thái kế tiếp nếu nó tốt hơn hiện tại (theo heuristic).
- Không quay lại các trạng thái trước đó → dễ kẹt ở đỉnh cục bộ.

📊 Ưu – Nhược điểm:

| Ưu điểm        | Nhược điểm                |
|----------------|---------------------------|
| Dễ cài đặt     | Dễ kẹt ở điểm cực đại cục bộ |
| Tốc độ nhanh   | Không hoàn chỉnh          |

🎬 Hình ảnh minh họa:

![Simple Hill](images/simple_hill.gif)

---

### 🔹 Steepest-Ascent Hill Climbing

✅ Nguyên lý hoạt động:
- Xét toàn bộ các trạng thái lân cận, chọn trạng thái tốt nhất.
- Giảm khả năng kẹt hơn so với simple hill climbing.

📊 Ưu – Nhược điểm:

| Ưu điểm             | Nhược điểm         |
|----------------------|--------------------|
| Tối ưu hơn Simple HC | Vẫn có thể kẹt     |

🎬 Hình ảnh minh họa:

![Steepest Hill](images/steepest_hill.gif)

---

### 🔹 Stochastic Hill Climbing

✅ Nguyên lý hoạt động:
- Chọn ngẫu nhiên một trạng thái tốt hơn hiện tại thay vì luôn chọn tốt nhất.
- Cân bằng giữa khai thác và khám phá.

📊 Ưu – Nhược điểm:

| Ưu điểm              | Nhược điểm                                |
|-----------------------|-------------------------------------------|
| Giảm nguy cơ bị kẹt  | Có thể không tìm ra lời giải tối ưu       |
| Đơn giản, dễ thực hiện | Không kiểm soát được toàn bộ hành trình |

🎬 Hình ảnh minh họa:

![Stochastic Hill](images/stochastic_hill.gif)

---

### 🔹 Simulated Annealing

✅ Nguyên lý hoạt động:
- Cho phép di chuyển sang trạng thái kém hơn trong giai đoạn đầu với xác suất.
- Xác suất này giảm theo thời gian (như quá trình làm nguội).

📊 Ưu – Nhược điểm:

| Ưu điểm                  | Nhược điểm                      |
|---------------------------|---------------------------------|
| Tránh được cực trị cục bộ | Cần tinh chỉnh nhiệt độ         |
| Khả năng tìm giải toàn cục | Không đảm bảo tối ưu ổn định   |

🎬 Hình ảnh minh họa:

![Annealing](images/annealing.gif)

---

### 🔹 Genetic Algorithm

✅ Nguyên lý hoạt động:
- Sử dụng quần thể lời giải (cá thể), tiến hóa qua nhiều thế hệ bằng cách:
  - Chọn lọc
  - Lai ghép
  - Đột biến
- Dựa trên cơ chế chọn lọc tự nhiên để tìm giải tốt.

📊 Ưu – Nhược điểm:

| Ưu điểm                        | Nhược điểm                             |
|---------------------------------|----------------------------------------|
| Tránh kẹt cực trị cục bộ       | Tốn thời gian tinh chỉnh tham số      |
| Khám phá không gian tốt hơn     | Kết quả không ổn định nếu cấu hình sai |

🎬 Hình ảnh minh họa:

![Genetic Algorithm](images/genetic.gif)

---

### 🔹 Q-Learning (Reinforcement Learning)

✅ Nguyên lý hoạt động:
- Là kỹ thuật học tăng cường không cần mô hình môi trường.
- Agent học hàm Q(s, a) để quyết định hành động tốt nhất từ trạng thái s.
- Cập nhật giá trị Q bằng công thức:
  Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]

📊 Ưu – Nhược điểm:

| Ưu điểm                          | Nhược điểm                         |
|----------------------------------|------------------------------------|
| Không cần mô hình môi trường    | Cần thời gian học dài              |
| Thích nghi tốt với thay đổi      | Hiệu quả phụ thuộc chính sách học |

🎬 Hình ảnh minh họa:

![Q Learning](images/qlearning.gif)

---
#### 🔶 Tìm kiếm trong môi trường phức tạp (Uncertain / Partially Observable)

---

### 🔹 AND-OR Graph Search

✅ Nguyên lý hoạt động:
- Dùng trong môi trường không xác định hoặc khi hành động có nhiều kết quả.
- Cây tìm kiếm gồm OR-nodes (lựa chọn hành động) và AND-nodes (một hành động dẫn đến nhiều kết quả cần giải quyết đồng thời).

📊 Ưu – Nhược điểm:

| Ưu điểm                             | Nhược điểm                        |
|-------------------------------------|-----------------------------------|
| Xử lý môi trường có tính bất định  | Phức tạp trong triển khai         |
| Hữu ích trong kế hoạch có điều kiện | Cần xử lý AND-nodes kỹ càng       |

🎬 Hình ảnh minh họa:

![AND-OR Search](images/andor.gif)

---

### 🔹 Belief State Search

✅ Nguyên lý hoạt động:
- Áp dụng cho môi trường quan sát hạn chế.
- Agent duy trì một tập các trạng thái có thể xảy ra (belief state).
- Mỗi hành động/quan sát sẽ cập nhật tập niềm tin.

📊 Ưu – Nhược điểm:

| Ưu điểm                              | Nhược điểm                                 |
|--------------------------------------|--------------------------------------------|
| Giải quyết tốt bài toán không quan sát đầy đủ | Trạng thái tăng theo cấp số mũ       |
| Mô hình hóa sự bất định hiệu quả     | Cần cập nhật belief liên tục               |

🎬 Hình ảnh minh họa:

![Belief Search](images/belief.gif)

---

### 🔹 Không nhìn thấy gì (Blind Environment)

✅ Mô tả:
- Agent không quan sát được trạng thái ban đầu hoặc kết quả hành động.
- Phải tạo kế hoạch đảm bảo đúng cho mọi khả năng có thể xảy ra.

✅ Chiến lược:
- Dùng AND-OR search, belief state hoặc kế hoạch xác suất.

📊 Ưu – Nhược điểm:

| Ưu điểm                           | Nhược điểm                          |
|-----------------------------------|--------------------------------------|
| Mô phỏng hệ thống thiếu thông tin | Khó tìm giải pháp chắc chắn         |
| Khuyến khích tư duy chiến lược    | Kết quả không luôn tối ưu           |

---

### 🔹 Chỉ quan sát một phần (Partial Observability)

✅ Mô tả:
- Agent chỉ thấy được một phần của trạng thái (ví dụ: vị trí tương đối, không gian khuất tầm nhìn).
- Phải dùng chiến lược quan sát và hành động thích nghi.

✅ Chiến lược:
- Cập nhật belief state liên tục.
- Kết hợp heuristic, Q-learning, POMDP, hoặc Hidden Markov Models.

📊 Ưu – Nhược điểm:

| Ưu điểm                           | Nhược điểm                               |
|-----------------------------------|------------------------------------------|
| Mô hình hóa thế giới thực rõ hơn | Tốn tài nguyên để theo dõi nhiều trạng thái |
| Tăng khả năng thích nghi          | Cần thuật toán mạnh để xử lý belief     |
- [ ] AND-OR Search
- [ ] Belief State Search
- [ ] Không nhìn thấy gì (Conformant Planning)
- [ ] Quan sát một phần (Partial Observability)

#### 🟣 Tìm kiếm trong môi trường ràng buộc (Constraint-Based Search)

---

### 🔹 Backtracking Search

✅ Nguyên lý hoạt động:
- Tìm kiếm lời giải cho bài toán ràng buộc (CSP) bằng cách gán từng biến một.
- Nếu phát hiện mâu thuẫn, quay lui và thử giá trị khác.
- Có thể kết hợp với các chiến lược chọn biến và giá trị thông minh.

📊 Ưu – Nhược điểm:

| Ưu điểm                          | Nhược điểm                              |
|----------------------------------|-----------------------------------------|
| Dễ cài đặt và trực quan         | Dễ bị "nổ" tổ hợp khi biến nhiều        |
| Hiệu quả nếu kết hợp ràng buộc  | Không tối ưu nếu không tối giản trước   |

🎬 Hình ảnh minh họa:

![Backtracking](images/backtracking.gif)

---

### 🔹 AC-3 Algorithm (Arc Consistency)

✅ Nguyên lý hoạt động:
- Duy trì tính nhất quán cung (arc-consistency) giữa các biến trong CSP.
- Lặp qua tất cả cặp biến (Xi, Xj). Nếu miền của Xi bị ảnh hưởng bởi ràng buộc với Xj, loại bỏ giá trị không phù hợp.
- Nếu miền của Xi thay đổi, thêm các cặp liên quan vào hàng đợi để kiểm tra lại.

📊 Ưu – Nhược điểm:

| Ưu điểm                              | Nhược điểm                              |
|--------------------------------------|-----------------------------------------|
| Giảm đáng kể số node khi backtracking | Không tự giải CSP hoàn toàn             |
| Tăng hiệu quả khi dùng trước khi tìm kiếm | Tốn thời gian với mạng ràng buộc lớn |

🎬 Hình ảnh minh họa:

![AC-3](images/ac3.gif)

---

### 🔹 Testing Algorithm

✅ Nguyên lý hoạt động:
- Kiểm thử không chỉ là kiểm tra đúng/sai, mà là một thuật toán quan trọng nhằm đánh giá tính đúng đắn và hiệu suất của các giải thuật trí tuệ nhân tạo.
- Một chiến lược kiểm thử bài bản cần đảm bảo mọi phần trong thuật toán được thử nghiệm trên nhiều trạng thái đầu vào, bao gồm cả trường hợp biên.
- Tập trung vào ba yếu tố chính: tính chính xác, tính hiệu quả, và tính tổng quát.

📊 Ưu – Nhược điểm:

| Ưu điểm                                 | Nhược điểm                                     |
|-----------------------------------------|------------------------------------------------|
| Giúp phát hiện lỗi logic trong thuật toán | Tốn thời gian tạo test case chất lượng       |
| Hỗ trợ đánh giá hiệu suất thực tế       | Không thể bao phủ mọi trường hợp phức tạp    |
| Có thể tự động hóa bằng khung kiểm thử  | Cần thiết kế test có ý nghĩa và đa dạng      |

🎬 Hình ảnh minh họa:

![Testing Algorithm](images/testing.gif)

---
## 📂 Thư mục ảnh minh họa
