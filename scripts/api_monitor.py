import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# 1. โหลดค่า Config จากไฟล์ .env
load_dotenv()

# 2. เชื่อมต่อ InfluxDB
client = InfluxDBClient(
    url=os.getenv("INFLUXDB_URL"),
    token=os.getenv("INFLUXDB_TOKEN"),
    org=os.getenv("INFLUXDB_ORG")
)
write_api = client.write_api(write_options=SYNCHRONOUS)
bucket = os.getenv("INFLUXDB_BUCKET")

def categorize_error(e, response=None):
    """ระบบคัดแยกประเภท Error อัจฉริยะ"""
    if response is not None:
        if 400 <= response.status_code < 500:
            return "Application Logic Error", f"HTTP {response.status_code}"
        if 500 <= response.status_code < 600:
            return "Infrastructure Server Error", f"HTTP {response.status_code}"
    
    err_msg = str(e).lower()
    if "timeout" in err_msg:
        return "Network Error", "Request Timeout"
    if "connection" in err_msg:
        return "Network Error", "Connection Refused"
    return "Unknown Error", "General Failure"

def run_monitor():
    # รายชื่อ API ที่เราจะเฝ้าระวัง
    endpoints = {
        "Product_Catalog": "https://api.github.com",           # API ที่ใช้งานได้ปกติ
        "Checkout_Service": "https://httpbin.org/status/500"   # จำลอง API ที่พัง (500)
    }

    print(f"\n🚀 [{datetime.now().strftime('%H:%M:%S')}] Smart Monitoring Loop Started...")
    
    for name, url in endpoints.items():
        start_time = time.time()
        try:
            # ยิง HTTP Request
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            
            # ถ้าสำเร็จ (Success)
            latency = (time.time() - start_time) * 1000
            send_to_db(name, "Success", "None", 1, latency)
            print(f"  ✅ {name.ljust(18)}: UP (Latency: {latency:.2f}ms)")

        except Exception as e:
            # ถ้าพลาด (Error) -> เข้ากระบวนการคัดแยกประเภท
            resp = getattr(e, 'response', None)
            err_type, err_detail = categorize_error(e, resp)
            latency = (time.time() - start_time) * 1000
            send_to_db(name, err_type, err_detail, 0, latency)
            print(f"  ❌ {name.ljust(18)}: {err_type} ({err_detail})")

def send_to_db(api_name, err_cat, err_det, status, latency):
    """ส่งข้อมูลเข้า InfluxDB"""
    point = Point("api_health") \
        .tag("endpoint", api_name) \
        .tag("category", err_cat) \
        .tag("detail", err_det) \
        .field("status", status) \
        .field("latency", latency) \
        .time(datetime.utcnow(), WritePrecision.NS)
    
    write_api.write(bucket=bucket, org=os.getenv("INFLUXDB_ORG"), record=point)

if __name__ == "__main__":
    try:
        while True:
            run_monitor()
            print("  💤 Waiting 10 seconds for next check...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped by user.")