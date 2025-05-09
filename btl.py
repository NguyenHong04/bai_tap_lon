# 1. Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
import schedule

# 2. Hàm trích xuất giá và diện tích từ mô tả nếu không tìm được từ DOM
def extract_price_area(text):
    price_match = re.search(r"Giá[:\-]?\s*([0-9.,]+[^m\n]*)", text, re.IGNORECASE)
    area_match = re.search(r"Diện tích[:\-]?\s*([0-9.,]+[^m\n]*)", text, re.IGNORECASE)
    price = price_match.group(1).strip() if price_match else "N/A"
    area = area_match.group(1).strip() if area_match else "N/A"
    return price, area

# 3. Hàm lấy nội dung an toàn từ xpath
def safe_xpath(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return "N/A"

# 4. Hàm crawl dữ liệu chính
def crawl_data():
    # 1. Vào website alonhadat.com.vn
    options = webdriver.ChromeOptions()
    # Có thể bật dòng dưới nếu muốn chạy ở chế độ ẩn
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    data = []
    page = 1

    # 2. Chọn tỉnh/thành và loại nhà đất — ở đây ví dụ Đà Nẵng, căn hộ chung cư
    # 3. Bấm tìm kiếm(nếu trang web tin tức không có Button tìm kiếm thì có thể bỏ qua).
    url_template = "https://alonhadat.com.vn/nha-dat/can-ban/can-ho-chung-cu/3/da-nang.html?page={}"

    # 5. Duyệt tất cả các trang
    while True:
        url = url_template.format(page)
        print(f"\nĐang xử lý trang {page}: {url}")
        driver.get(url)
        time.sleep(3)

        # Xử lý nếu CAPTCHA xuất hiện
        try:
            captcha_element = driver.find_element(By.XPATH, '//*[@id="captcha"]')
            if captcha_element:
                print("CAPTCHA phát hiện. Hãy nhập mã CAPTCHA!")
                input("Nhấn Enter sau khi đã nhập mã CAPTCHA để tiếp tục...")
        except:
            pass

        links = []
        i = 1
        while True:
            try:
                xpath = f'//*[@id="left"]/div[1]/div[{i}]/div[1]/div[1]/a'
                link_element = driver.find_element(By.XPATH, xpath)
                link = link_element.get_attribute("href")
                if link:
                    links.append(link)
                i += 1
            except:
                break

        if not links:
            print("Không còn bài đăng. Kết thúc.")
            break

        # 4. Lấy tất cả dữ liệu trong bài viết (Tiêu đề, Mô tả, Địa chỉ, Diện tích, Giá)
        for link in links:
            try:
                print(f"Đang xử lý: {link}")
                driver.get(link)
                time.sleep(3)

                title = safe_xpath(driver, '//*[@id="left"]/div[1]/div[1]/div[1]/div[1]/a')
                description = safe_xpath(driver, '//*[@id="left"]/div[1]/div[2]')
                address = safe_xpath(driver, '//*[@id="left"]/div[1]/div[4]')
                area = safe_xpath(driver, '//*[@id="left"]/div[1]/div[3]/span[2]')
                price = safe_xpath(driver, '//*[@id="left"]/div[1]/div[3]/span[1]')

                # Dùng mô tả để bổ sung giá/diện tích nếu thiếu
                if (price == "N/A" or area == "N/A") and description != "N/A":
                    desc_price, desc_area = extract_price_area(description)
                    if price == "N/A" and desc_price != "N/A":
                        price = desc_price
                    if area == "N/A" and desc_area != "N/A":
                        area = desc_area

                if title == "N/A":
                    title = driver.title.strip()

                data.append([title, description, address, area, price])

            except Exception as e:
                print(f"Lỗi bài đăng: {e}")
                continue

        page += 1

    driver.quit()

    # 6. Lưu dữ liệu vào file Excel
    df = pd.DataFrame(data, columns=["Tiêu đề", "Mô tả", "Địa chỉ", "Diện tích", "Giá"])
    df.to_excel("nha_dat_da_nang.xlsx", index=False)
    print("Đã lưu dữ liệu vào 'nha_dat_da_nang.xlsx'.")

# 7. Set lịch chạy tự động vào lúc 6h sáng hàng ngày
schedule.every().day.at("06:00").do(crawl_data)
print("Đang chờ lịch chạy chương trình...")

while True:
    schedule.run_pending()
    time.sleep(60)
