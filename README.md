# 📊 Air Quality Data Analysis Dashboard (HCMC)

Ứng dụng trực quan hóa và đối sánh dữ liệu Chất lượng Không khí (AQI) tại Thành phố Hồ Chí Minh (2022 - 2026). Dự án sử dụng **Streamlit** cho Presentation Layer và được đóng gói toàn bộ bằng **Docker** để đảm bảo tính nhất quán của môi trường triển khai (Environment Consistency) trên đa nền tảng.

---

## 🎯 Tổng quan & Tính năng

Hệ thống cung cấp các công cụ phân tích khám phá dữ liệu (EDA) song song giữa tập dữ liệu gốc (`hcmc_aqi_dataset_before_preprocess.csv`) và tập dữ liệu đã qua xử lý (`hcmc_aqi_dataset_after_preprocess.csv`), bao gồm 6 module chính:

1. **Tổng quan Dữ liệu:** Thống kê mô tả (Count, Mean, Std, Min, Max) và cấu trúc shape.
2. **Phân phối Dữ liệu (Distribution):** So sánh tần suất và hình dạng phân phối qua Side-by-side Histograms.
3. **Phân tích Ngoại lai (Outliers):** Trực quan hóa các điểm dị biệt bằng Box Plot.
4. **Ma trận Tương quan (Correlation):** Heatmap hệ số Pearson giữa các biến số môi trường.
5. **Chuỗi Thời gian (Time Series):** Đồ thị tuyến tính theo dõi xu hướng biến động.
6. **Dữ liệu Khuyết thiếu (Missing Values):** Thống kê và đánh giá tỷ lệ dữ liệu cần Imputation.

---

## 📁 Cấu trúc Repository

```text
aqi_dashboard/
├── dashboard_app_improved.py                 # Source code chính của giao diện Streamlit
├── requirements.txt                          # Python dependencies
├── docker-compose.yml                        # Cấu hình container orchestration
├── hcmc_aqi_dataset_before_preprocess.csv    # Dataset 1: data trước khi được xử lý
├── hcmc_aqi_dataset_after_preprocess.csv     # Dataset 2: data sau khi được xử lý
└── README.md                                 # Documentation
```
---

## 🚀 Hướng dẫn Triển khai (Quickstart)

Hệ thống được thiết kế để chạy độc lập không phụ thuộc vào môi trường Local Python của host machine.

Yêu cầu hệ thống: Đã cài đặt Docker Engine / Docker Desktop.

Sau khi tải về máy, tất cả các file trên đều để cùng 1 thư mục.

Khởi chạy Docker Desktop/ Docker Engine.

Các bước khởi chạy:

Mở Terminal tại thư mục gốc của dự án (aqi_dashboard).

Khởi tạo và chạy container ngầm bằng lệnh:

```bash
     docker-compose up -d
```
Truy cập Dashboard qua trình duyệt tại: http://localhost:8501 (có thể tốn 1 chút thời gian nếu chạy lần đậu ạ :3, mọi người gáng chờ xíu nhen ^^)

## 🛠️ Môi trường Phát triển (Development)
Hệ thống sử dụng Docker Volumes (- .:/app) để map trực tiếp source code và dataset từ host machine vào container.

Mọi thay đổi trong mã nguồn dashboard_app_improved.py hoặc cập nhật ghi đè file *.csv từ các luồng ETL (Airflow/Dagster) sẽ được Streamlit nhận diện lập tức (Hot-reload).

Người dùng chỉ cần làm mới trang (F5) để xem kết quả cập nhật mà không cần rebuild container.

Để dừng hệ thống và giải phóng tài nguyên network/container, sử dụng lệnh:

```bash
     docker-compose down
```
Developed by Đặng Đức Lộc _ Nguyễn Trung Kiên - University of Information Technology (UIT).