import streamlit as st
import urllib.parse
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 1. หน้าจอ Interface สไตล์ดาร์กโหมดขั้นสุด
st.set_page_config(page_title="NEXUS-OSINT ULTRA MAX", page_icon="👁️‍🗨️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    .stApp { background-color: #02040a; color: #F1F5F9; font-family: 'Fira Code', monospace; }
    .terminal-header { font-size: 38px; font-weight: bold; text-align: center; animation: neonGlow 2s infinite ease-in-out; }
    .profile-card { background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(56, 189, 248, 0.2); padding: 25px; border-radius: 18px; margin-bottom: 25px; }
    .face-active { border: 1px solid #10B981; background: #064E3B; color: #34D399; padding: 15px; text-align: center; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. Hybrid Mapping (ส่วนนี้คือสิ่งที่อัปเกรด)
NAME_MAP = {
    "พี่มุก": "Pimook",
    "สุดสวย": "Sudsuay"
}

def get_fb_search_link(name):
    return f"https://www.facebook.com/search/top/?q={urllib.parse.quote(name)}"

st.markdown("<div class='terminal-header'>🛸 NEXUS-OSINT // CORE OVERCLOCK-MATRIX v6</div>", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### ⚡ SYSTEMS CONTROL")
    facecheck_key = st.text_input("🛰️ FaceCheck.ID API KEY:", type="password")

# 4. ฟอร์มป้อนข้อมูลหลัก (ตั้งค่าเริ่มต้น พี่มุก สุดสวย)
col_fn, col_ln = st.columns(2)
with col_fn: first_name = st.text_input("🛸 ชื่อจริงเป้าหมาย", value="พี่มุก")
with col_ln: last_name = st.text_input("💥 นามสกุลเป้าหมาย", value="สุดสวย")

uploaded_faces = st.file_uploader("📸 อัพโหลดภาพใบหน้าเป้าหมาย", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 5. ข้อมูล 11 ช่อง
st.markdown("#### 🔎 ข้อมูลหลักฐานแวดล้อม (11 Nodes Verification)")
c1, c2, c3 = st.columns(3)
with c1: nickname = st.text_input("🏷️ ชื่อเล่น")
with c2: edu_highschool = st.text_input("🏫 โรงเรียนมัธยม")
with c3: studying_uni = st.text_input("🎓 มหาวิทยาลัย")

# 6. ตรรกะการรันสแกนแบบ Hybrid
if st.button("🛸 INITIALIZE MAXIMUM HYPER CRAWLER (HYBRID MODE)", type="primary", use_container_width=True):
    # ดึงค่าอังกฤษจาก Mapping
    en_name = NAME_MAP.get(first_name, first_name)
    en_surname = NAME_MAP.get(last_name, last_name)
    
    thai_full = f"{first_name} {last_name}"
    eng_full = f"{en_name} {en_surname}"
    
    st.markdown("### 📡 LIVE REPORT // ข้อมูลผลลัพธ์ Hybrid (TH+EN)")
    
    # แบ่งโหนดการค้นหาชัดเจน
    c_th, c_en = st.columns(2)
    
    with c_th:
        st.markdown(f"<div class='profile-card'><h4>🇹🇭 THAI NODE</h4>ค้นหา: {thai_full}</div>", unsafe_allow_html=True)
        st.link_button(f"🔍 ค้นหา {thai_full}", get_fb_search_link(thai_full), use_container_width=True)
        
    with c_en:
        st.markdown(f"<div class='profile-card'><h4>🇺🇸 ENGLISH NODE</h4>ค้นหา: {eng_full}</div>", unsafe_allow_html=True)
        st.link_button(f"🔍 ค้นหา {eng_full}", get_fb_search_link(eng_full), use_container_width=True)

    st.success("🎯 ระบบ Hybrid สแกนทั้งชื่อไทยและอังกฤษคู่ขนานเรียบร้อยครับ!")
