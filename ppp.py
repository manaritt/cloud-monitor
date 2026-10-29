import time
import json
import urllib.request
import psutil

# -------------------------------------------------------------
# Configuration (سيرفر سحابي مجاني ومباشر)
# -------------------------------------------------------------
CLOUD_URL = "https://httpbin.org/post"
HEADERS = {
    "Content-Type": "application/json"
}


def get_system_metrics():
    """تجميع بيانات النظام المحلية"""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": cpu_usage,
        "ram_percent": ram_usage,
        "disk_percent": disk_usage
    }


def send_to_cloud(data):
    """إرسال البيانات إلى السحابة عبر HTTP POST Request"""
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(CLOUD_URL, data=json_data, headers=HEADERS, method='POST')

        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            # إرجاع تأكيد الاستلام من السيرفر السحابي
            return "SUCCESS-200"
    except Exception as e:
        print(f"[Error] فشل الاتصال بالسحاب: {e}")
        return None


def main():
    print("==================================================")
    print("   بدء تشغيل نظام مراقبة الأجهزة المربوط بالكلاود   ")
    print("==================================================")
    print("جاري جمع البيانات ورفعها كل 5 ثوانٍ...\n")

    try:
        while True:
            # 1. جمع البيانات من الجهاز
            metrics = get_system_metrics()

            print(f"[{metrics['timestamp']}]")
            print(f" ├─ استهلاك المعالج (CPU): {metrics['cpu_percent']}%")
            print(f" ├─ استهلاك الذاكرة (RAM): {metrics['ram_percent']}%")
            print(f" └─ استهلاك القرص (Disk): {metrics['disk_percent']}%")

            # تنبيه محلي في حال ارتفاع الاستهلاك
            if metrics['cpu_percent'] > 80:
                print(" ⚠️  [تنبيه]: استهلاك المعالج مرتفع جداً!")

            # 2. رفع البيانات للكلاود
            cloud_status = send_to_cloud(metrics)
            if cloud_status:
                print(f" ☁️  تم الرفع بنجاح للسحاب! (Cloud Status: {cloud_status})")

            print("-" * 50)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nتم إيقاف البرنامج بنجاح.")


if __name__ == "__main__":
    main()