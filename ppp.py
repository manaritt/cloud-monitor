

           from datetime import datetime
import pandas as pd
import psutil
import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(
    page_title="Single-Node Infrastructure Monitor", layout="wide"
)

st.title("🖥️ Real-Time Single-Node Server Monitor")
st.write(
    "نظام مراقبة السيرفر المباشر بالوقت الفعلي (Real-time Telemetry Stream)"
)

# ---------------------------------------------------------
# الشريط الجانبي (Sidebar)
# ---------------------------------------------------------
st.sidebar.header("🕹️ لوحة التحكم بالمراقبة")
refresh_rate = st.sidebar.slider("سرعة تحديث البيانات (بالثواني):", 1, 10, 2)

# زر المحاكاة بديل التليجرام لاختبار التنبيهات
sim_stress = st.sidebar.button("🚨 اختبر التنبيه (محاكاة ضغط عالي)")

# ---------------------------------------------------------
# قراءة بيانات السيرفر الحقيقية عبر psutil
# ---------------------------------------------------------
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

# في حال ضغط زر المحاكاة، نرفع القراءات لتجربة الإنذار
if sim_stress:
  cpu = 94.5
  ram = 89.0

# ---------------------------------------------------------
# عرض المؤشرات الثلاثة
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("CPU Load", f"{cpu}%")
col2.metric("RAM Usage", f"{ram}%")
col3.metric("Disk Storage", f"{disk}%")

# ---------------------------------------------------------
# نظام التنبيهات التلقائي (Auto Alerts)
# ---------------------------------------------------------
st.divider()
st.subheader("🔔 حالة السيرفر المباشرة")

if cpu > 80 or ram > 80:
  st.error(
      "🚨 خطر عالي: استهلاك الموارد تجاوز حد الأمان! (High Resource Load Detected)"
  )
elif cpu > 60 or ram > 60:
  st.warning(
      "⚠️ تحذير: يوجد ضغط متوسط على السيرفر (Moderate Resource Stress)."
  )
else:
  st.success("✅ السيرفر يعمل بحالة ممتازة وبدون أي مشاكل (Optimal State).")

# ---------------------------------------------------------
# تصدير التقرير CSV
# ---------------------------------------------------------
st.divider()
st.subheader("📊 تصدير البيانات (CSV Log Export)")

data_log = pd.DataFrame([{
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "CPU_Percent": cpu,
    "RAM_Percent": ram,
    "Disk_Percent": disk,
    "Status": (
        "High Load"
        if cpu > 80 or ram > 80
        else ("Warning" if cpu > 60 or ram > 60 else "Normal")
    ),
}])

csv_data = data_log.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 تنزيل تقرير السيرفر (CSV)",
    data=csv_data,
    file_name="single_server_telemetry_log.csv",
    mime="text/csv",
)
