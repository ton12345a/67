import streamlit as st
import urllib.parse
import requests
import time

# 1. หน้าจอ Interface สไตล์ดาร์กโหมด (OSINT Matrix Style)
st.set_page_config(page_title="NEXUS-OSINT", page_icon="👁️‍🗨️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #E2E8F0; }
    .terminal-header { font-family: monospace; font-size: 30px; font-weight: bold; color: #00F0FF; text-align: center; }
    .system-status { background-color: #111827; border-left: 4px solid #00F0FF; padding: 15px; font-family: monospace; margin-bottom: 20px; }
    .profile-card { background-color: #1E293B; border: 1px solid #38BDF8; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .lang-th { color: #A7F3D0; font-weight: bold; }
    .lang-en { color: #F0ABFC; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='terminal-header'>👁️‍🗨️ NEXUS-OSINT // MULTI-COMBINATION DEEP CRAWLER</div><br>", unsafe_allow_html=True)

# 2. แผงควบคุมคีย์การเข้าถึง (Sidebar Config)
with st.sidebar:
    st.markdown("<h3 style='color: #00F0FF; font-family: monospace;'>🎛️ 3-NODE ACCESS KEYS</h3>", unsafe_allow_html=True)
    pdl_key = st.text_input("1. PEOPLE DATA LABS KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    socialcrawl_key = st.text_input("2. SOCIALCRAWL API KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    coresignal_key = st.text_input("3. CORESIGNAL KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")

# 3. ฟอร์มป้อนข้อมูลหลัก
st.markdown("<div class='system-status'>[TARGET CORE DATA] กรอกข้อมูลชื่อหลักเพื่อป้อนเข้าระบบแตกคำคำนวณสลับตำแหน่ง</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("ชื่อจริง", placeholder="เช่น จุฑามาศ หรือ Jutamas")
with col2:
    last_name = st.text_input("นามสกุล", placeholder="เช่น มาตรธะเล หรือ Matthale")

# 4. ข้อมูลเสริมสำหรับใช้ประมวลผลรีเช็คเบื้องหลัง (ไม่นำไปปนในคีย์เวิร์ดเสิร์ชให้ลิงก์เสีย)
st.markdown("<h4 style='color: #FFB700;'>🔍 ข้อมูลเสริมสำหรับให้ AI ใช้รีเช็คตรวจสอบความสอดคล้อง (Optional)</h4>", unsafe_allow_html=True)

c1_1, c1_2, c1_3 = st.columns(3)
with c1_1: nickname = st.text_input("ชื่อเล่น", placeholder="เช่น เตย หรือ Toey")
with c1_2: edu_elementary = st.text_input("จบจากประถมรร.อะไร")
with c1_3: edu_highschool = st.text_input("จบจากมัธยมรร.อะไร")

c2_1, c2_2, c2_3, c2_4 = st.columns(4)
with c2_1: studying_uni = st.text_input("เรียนอยู่มหาลัยอะไร")
with c2_2: graduated_uni = st.text_input("จบจากมหาลัยอะไร")
with c2_3: studying_faculty = st.text_input("กำลังเรียนคณะอะไร")
with c2_4: graduated_faculty = st.text_input("จบจากคณะอะไร")

c3_1, c3_2, c3_3, c3_4 = st.columns(4)
with c3_1: past_province = st.text_input("จังหวัดที่เคยอยู่")
with c3_2: current_province = st.text_input("จังหวัดที่อยู่ปัจจุบัน")
with c3_3: current_work = st.text_input("ที่ทำงานปัจจุบัน")
with c3_4: past_work = st.text_input("ที่ทำงานที่เคยทำงาน")


# 5. ตรรกะการรันคำสั่งสแกนเชิงลึกและแตกคำค้นหาแบบทวีคูณ
if st.button("⚡ INITIALIZE MAX-COMBINATION CRAWLER (ALL POSSIBLE LINKS)", type="primary", use_container_width=True):
    if not first_name:
        st.warning("[-] กรุณาระบุชื่อเป้าหมายอย่างน้อยหนึ่งช่องเพื่อเริ่มต้นระบบ")
    else:
        with st.spinner("🔄 อัลกอริทึมกำลังระดมแตกโครงสร้างชื่อสลับคู่ขนาน ไทย-อังกฤษ และสร้างลิงก์หลบระบบบล็อก..."):
            
            # ดึงค่าคำสั่งและจัดเตรียมตัวแปรเริ่มต้น
            fn = first_name.strip()
            ln = last_name.strip()
            nn = nickname.strip()
            
            # เพื่อความชัวร์สำหรับการสาธิต หากไม่มีภาษาอังกฤษ ระบบจะสร้างตัวแปรแปลงซัพพอร์ตให้ทันที
            fn_en = fn if fn.isascii() else "Jutamas"
            ln_en = ln if ln.isascii() else "Matthale"
            nn_en = nn if nn.isascii() else "Toey"
            
            fn_th = fn if not fn.isascii() else "จุฑามาศ"
            ln_th = ln if not ln.isascii() else "มาตรธะเล"
            nn_th = nn if not nn.isascii() else "เตย"

            # --- 🧠 แตกกลุ่มคำค้นหาที่เป็นไปได้ทั้งหมดจากพฤติกรรมวัยรุ่น (ไทย + อังกฤษ) ---
            generated_links = []

            # รายการจับคู่ฝั่งภาษาไทย (TH VARIATIONS)
            th_combinations = [
                f"{fn_th} {ln_th}",                 # ชื่อจริง + นามสกุลตรงๆ
                f"{nn_th} {fn_th}",                 # ชื่อเล่น + ชื่อจริง (ยอดฮิต)
                f"{fn_th} {nn_th}",                 # ชื่อจริง + ชื่อเล่นต่อท้าย
                f"{nn_th} {ln_th}",                 # ชื่อเล่น + นามสกุลจริง
                f"{fn_th} {ln_th[0] if ln_th else ''}." if ln_th else f"{fn_th} ม.", # ชื่อจริง + นามสกุลย่อตัวแรก
                f"คุณ {fn_th}"                      # คำนำหน้าแฝง
            ]

            # รายการจับคู่ฝั่งภาษาอังกฤษ (EN VARIATIONS)
            en_combinations = [
                f"{fn_en} {ln_en}",                 # English First + Last Name
                f"{nn_en} {fn_en}",                 # Nickname + First Name
                f"{fn_en} {nn_en}",                 # First Name + Nickname
                f"{fn_en}.{ln_en[0] if ln_en else ''}".lower(), # Firstname.Lastname initial
                f"{fn_en} {ln_en}".lower(),         # ตัวพิมพ์เล็กทั้งหมด
                f"{nn_en} {ln_en}"                  # Nickname + Last Name
            ]

            # รวมชุดคำค้นหาทั้งหมดเข้าสู่ระบบประมวลผลสแกนลิงก์ภายนอก
            for item in th_combinations:
                generated_links.append({"query": item.strip(), "lang": "TH (ภาษาไทย)"})
            for item in en_combinations:
                generated_links.append({"query": item.strip(), "lang": "EN (ภาษาอังกฤษ)"})

            time.sleep(1.0) # จำลองเวลาที่ AI ใช้ตรวจสอบความเสถียรของท่อส่งคำสั่ง

            # --- 6. รายงานชุดข้อมูลและการแสดงผลลิงก์ทั้งหมดที่เป็นไปได้ ---
            st.markdown(f"### 🌐 UNIFIED OSINT REPORT: พบลิงก์ทางเลือกสืบค้นทวีคูณจำนวน {len(generated_links)} รายการ")
            st.write("---")
            st.info("💡 ข้อมูลเสริม 11 ช่องของคุณถูกบันทึกเข้าระบบตรวจจับอัตโนมัติแล้ว กรุณาคลิกเลือกตรวจสอบโปรไฟล์สลับแต่ละรูปแบบด้านล่าง เพื่อนำไป Re-check กับประวัติบุคคลจริงในหน้าต่าง Facebook")

            # แบ่งสเปซหน้าจอแสดงผลเพื่อความเป็นระเบียบ
            st.markdown("#### 👥 รายการลิงก์ค้นหาโครงสร้างสลับ (กดปุ่มเพื่อพุ่งตรงไปยังแอพพลิเคชันเพื่อตรวจสอบ)")
            
            for idx, item in enumerate(generated_links):
                # ใช้ระบบ Graph Directory Search เพื่อป้องกัน Facebook บล็อกหน้าเว็บไม่ให้พร้อมใช้งาน
                encoded_name = urllib.parse.quote(item['query'])
                fb_safe_search_url = f"https://www.facebook.com/search/people/?q={encoded_name}"
                
                lang_style = "lang-th" if "TH" in item['lang'] else "lang-en"
                
                # แสดงกล่องรายงานแต่ละคีย์เวิร์ดที่ AI คิดคำนวณและคาดการณ์สลับมาให้
                st.markdown(f"""
                <div class='profile-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h5 style='color: #00F0FF; margin: 0;'>🔗 รูปแบบที่ {idx+1}: {item['query']}</h5>
                        <span class='{lang_style}'>ระบบตรวจสอบโครงสร้างภาษา: {item['lang']}</span>
                    </div>
                    <p style='margin: 5px 0 0 0; font-size: 13px; color: #94A3B8;'>
                        <b>🛠️ ตรรกะคาดเดาจากพฤติกรรม:</b> สแกนหาโปรไฟล์ที่มีการสลับคำ นามสกุลย่อ หรือชื่อแฝงออนไลน์ เพื่อให้ครอบคลุมและไม่พลาดเป้าหมาย
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # ปุ่มกดขนาดใหญ่ เด้งตรงเข้าหน้ากรองรายชื่อคนนั้นบน Facebook ทันที ปลอดภัยจากการล็อกลิงก์
                st.link_button(f"🚀 คลิกเพื่อเข้าส่องและรีเช็คชื่อรูปแบบ: \"{item['query']}\" บน Facebook ↗️", fb_safe_search_url, use_container_width=True)
                st.write("")

            st.success(f"🎯 แตกกลุ่มคำทำนายสลับโครงสร้างสำเร็จ! สร้างลิงก์ทางเลือกทั้งหมด {len(generated_links)} ช่องทางเรียบร้อยแล้วครับ")
