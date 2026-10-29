import streamlit as st
import psutil
import time
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Cloud Monitoring Dashboard",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Real-time Cloud Infrastructure Monitor")
st.write("نظام مراقبة أداء السيرفرات والموارد السحابية - عرض حي ومباشر")

# إنشاء أماكن عرض الأرقام والرسومات
col1, col2, col3 = st.columns(3)
cpu_metric = col1.empty()
ram_metric = col2.empty()
disk_metric = col3.empty()

chart_title = st.subheader("📈 Live Resource Usage Chart")
chart_placeholder = st.empty()

# تهيئة جدول البيانات للرسم البياني
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['CPU', 'RAM'])

# حلقة التحديث الحي
while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # عرض الأرقام والمؤشرات
    cpu_metric.metric("CPU Usage", f"{cpu}%", delta=f"{cpu - 50}%", delta_color="inverse")
    ram_metric.metric("RAM Usage", f"{ram}%")
    disk_metric.metric("Disk Space Used", f"{disk}%")

    # إضافة البيانات للرسم البياني
    new_data = pd.DataFrame({'CPU': [cpu], 'RAM': [ram]})
    st.session_state.history = pd.concat([st.session_state.history, new_data]).tail(20)

    # رسم المخطط البياني الحي
    chart_placeholder.line_chart(st.session_state.history)

    time.sleep(2)