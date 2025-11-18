# KTPM Selenium Testing Project

Project kiểm thử tự động giao diện web sử dụng Selenium WebDriver.

## Cấu trúc thư mục

```
KTPM_SELENIUM/
├── venv/                   # Virtual environment
├── config/                 # File cấu hình
├── drivers/                # WebDriver binaries (tự động tải)
├── tests/                  # Test cases
├── pages/                  # Page Object Model
├── utils/                  # Utilities
├── data/                   # Test data (JSON, Excel)
├── reports/                # Test reports
├── screenshots/            # Screenshots
└── requirements.txt        # Dependencies
```

## Cài đặt

### 1. Tạo Virtual Environment

```bash
python -m venv venv
```

### 2. Kích hoạt Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy test

```bash
pytest tests/
```

### Chạy test với report HTML

```bash
pytest tests/ --html=reports/report.html
```

### Chạy test parallel

```bash
pytest tests/ -n auto
```

## Tính năng

- ✅ Selenium WebDriver với hỗ trợ multiple browsers (Chrome, Firefox, Edge)
- ✅ Tự động tải và quản lý WebDriver
- ✅ Đọc/ghi file Excel (openpyxl, pandas, xlsxwriter)
- ✅ Xử lý JSON
- ✅ Page Object Model pattern
- ✅ Screenshot khi test fail
- ✅ HTML và Allure reports
- ✅ Parallel testing

## Browsers được hỗ trợ

- Chrome
- Firefox
- Edge
- (Có thể mở rộng cho các browser khác)
