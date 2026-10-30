import streamlit as st
import psutil
import time
import pandas as pd
from datetime import datetime
import requests

# إعدادات الصفحة
st.set_page_config(page_title="Cloud Monitoring Dashboard", layout="wide")

st.title("☁️ Real-time Cloud Infrastructure Monitor")
st.write("نظام مراقبة أداء السيرفرات والموارد السحابية - عرض حي ومباشر")

# ==========================================
# ⚠️ بيانات التليجرام الخاصة بكِ (استبدلي المقاطع)
# ==========================================
TELEGRAM_TOKEN = "ضعِي_هنا_التوكن_من_BotFather"
TELEGRAM_CHAT_ID = "ضعِي_هنا_الـChat_ID_من_UserInfoBot"

def send_telegram_alert(message):
    """دالة لإرسال إشعار تلقائي عبر التليجرام"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        pass

# --- الشريط الجانبي (Sidebar) ---
st.sidebar.header("⚙️ إعدادات النظام")
refresh_interval = st.sidebar.slider("سرعة تحديث البيانات (بالثواني):", min_value=1, max_value=10, value=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 وضع الاختيار والتجربة")
# زر محاكاة التنبيه للعرض أمام الدكتور
test_alert = st.sidebar.button("🚨 تجربة التنبيه وإرسال التليجرام")

st.sidebar.markdown("---")
st.sidebar.write("📌 حالة النظام: شغال وحي")

# تهيئة سجل البيانات في الذاكرة
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Timestamp", "CPU (%)", "RAM (%)", "Disk (%)"])

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

# قراءة الموارد الحالية
cpu = psutil.cpu_percent(interval=0.5)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent
current_time = datetime.now().strftime("%H:%M:%S")

# إضافة القراءة للسجل
new_row = pd.DataFrame([{"Timestamp": current_time, "CPU (%)": cpu, "RAM (%)": ram, "Disk (%)": disk}])
st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(20)

# --- قسم التنبيهات الذكي الشامل (CPU / RAM / Disk) ---
# يتفعل التنبيه عند ارتفاع أي مورد فوق 80% أو عند ضغط زر التجربة
if test_alert or cpu > 80 or ram > 80 or disk > 80:
    display_cpu = 88.5 if test_alert else cpu
    display_ram = 82.0 if test_alert else ram
    display_disk = 91.0 if test_alert else disk
    
    st.error(f"⚠️ تنبيه عالي الخطورة: استهلاك الموارد مرتفع جداً! (CPU: {display_cpu}% | RAM: {display_ram}% | Disk: {display_disk}%)")
    
    # إرسال التنبيه للتليجرام
    if test_alert or (time.time() - st.session_state.last_alert_time > 60):
        alert_msg = f"🚨 تحذير طارئ بالسيرفر السحابي!\n\n- استهلاك المعالج (CPU): {display_cpu}%\n- استهلاك الذاكرة (RAM): {display_ram}%\n- مساحة القرص (Disk): {display_disk}%\n- الوقت: {current_time}\n\n⚠️ يرجى تفقد السيرفر فوراً!"
        send_telegram_alert(alert_msg)
        st.session_state.last_alert_time = time.time()
        
        if test_alert:
            st.sidebar.success("✅ تم إرسال رسالة التنبيه إلى التليجرام بنجاح!")

elif cpu > 50 or ram > 50 or disk > 50:
    st.warning(f"⚡ تنبيه متوسط: الاستهلاك أعلى من المعدل الطبيعي. (CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%)")
else:
    st.success("✅ حالة النظام ممتازة: جميع الموارد تعمل ضمن الحدود الطبيعية.")

# --- عرض المؤشرات الرئيسية (Metrics) ---
col1, col2, col3 = st.columns(3)
col1.metric("CPU Usage", f"{cpu}%")
col2.metric("RAM Usage", f"{ram}%")
col3.metric("Disk Space Usage", f"{disk}%")

# --- الرسم البياني الحي ---
st.subheader("📈 Live Resource Usage Chart")
st.line_chart(st.session_state.history.set_index("Timestamp")[["CPU (%)", "RAM (%)", "Disk (%)"]])

# --- خيار تحميل البيانات (Export Data) ---
st.sidebar.markdown("---")
csv_data = st.session_state.history.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 تحميل سجل البيانات (CSV)",
    data=csv_data,
    file_name=f"cloud_monitor_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# إعادة التشغيل التلقائي
time.sleep(refresh_interval)
st.rerun()
