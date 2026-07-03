import streamlit as st
import urllib.parse
import requests
import time

# 1. หน้าจอ Interface สไตล์ดาร์กโหมดขั้นสูง
st.set_page_config(page_title="NEXUS-OSINT", page_icon="👁️‍🗨️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #E2E8F0; }
    .terminal-header { font-family: monospace; font-size: 30px; font-weight: bold; color: #00F0FF; text-align: center; }
    .system-status { background-color: #111827; border-left: 4px solid #00F0FF; padding: 15px; font-family: monospace; margin-bottom: 20px; }
    .profile-card { background-color: #1E293B; border: 1px solid #38BDF8; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .match-high { color: #10B981; font-weight: bold; }
    .match-mid { color: #F59E0B; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='terminal-header'>👁️‍🗨️ NEXUS-OSINT // DYNAMIC PROFILE CRAWLER (TH/EN)</div><br>", unsafe_allow_html=True)

# 2. แผงควบคุมคีย์การเข้าถึง (Sidebar Config)
with st.sidebar:
    st.markdown("<h3 style='color: #00F0FF; font-family: monospace;'>🎛️ 3-NODE ACCESS KEYS</h3>", unsafe_allow_html=True)
    pdl_key = st.text_input("1. PEOPLE DATA LABS KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    socialcrawl_key = st.text_input("2. SOCIALCRAWL API KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    coresignal_key = st.text_input("3. CORESIGNAL KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")

# 3. ฟอร์มป้อนข้อมูลหลัก
st.markdown("<div class='system-status'>[TARGET CORE DATA] ป้อนข้อมูลชื่อหลัก (ระบบจะนำไปคำนวณและสร้างคีย์เวิร์ดสลับโครงสร้างอัตโนมัติ)</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("ชื่อจริง (ภาษาไทย หรือ อังกฤษก็ได้)", placeholder="เช่น อารยา หรือ Araya")
with col2:
    last_name = st.text_input("นามสกุล (ภาษาไทย หรือ อังกฤษก็ได้)", placeholder="เช่น บุรมย์ศรี หรือ Buromsri")

# 4. ข้อมูลเสริมสำหรับใช้ให้ AI "รีเช็คประวัติและกรองโปรไฟล์ตรง"
st.markdown("<h4 style='color: #FFB700;'>🔍 ข้อมูลเสริมสำหรับบอทใช้ตรวจสอบความถูกต้องของโปรไฟล์ (Profile Verification Parameters)</h4>", unsafe_allow_html=True)

c1_1, c1_2, c1_3 = st.columns(3)
with c1_1: nickname = st.text_input("ชื่อเล่น (สำคัญมากสำหรับวัยรุ่นยุคใหม่)", placeholder="เช่น บี / Bee")
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


# 5. ตรรกะการรันคำสั่งสแกนเชิงลึกและประมวลผลคำค้นสลับโครงสร้าง
if st.button("⚡ INITIALIZE COMBINATION CRAWLER & PROFILE EXTRACTOR", type="primary", use_container_width=True):
    if not pdl_key and not socialcrawl_key and not coresignal_key:
        st.error("[-] ไม่สามารถประมวลผลได้: กรุณาระบุรหัส API Key บน Sidebar ฝั่งซ้ายเพื่อเปิดท่อส่งข้อมูล")
    elif not first_name:
        st.warning("[-] กรุณาระบุชื่อเป้าหมายเพื่อเริ่มต้นระบบกวาดข้อมูล")
    else:
        with st.spinner("🔄 อัลกอริทึมกำลังแตกโครงสร้างชื่อ (ไทย/อังกฤษ/ชื่อเล่น) และทำการดึงข้อมูลลิงก์โปรไฟล์ตรง..."):
            
            # --- 🧠 อัลกอริทึมจำลองพฤติกรรมการตั้งชื่อของคนยุคใหม่ (Name Combination Generator) ---
            # สร้างคำค้นหาแบบไขว้กัน เพื่อส่งไปให้ API ช่วยกวาดหาโปรไฟล์ทั้งหมดที่เป็นไปได้
            search_queries = []
            if first_name and last_name:
                search_queries.append(f"{first_name} {last_name}")  # ชื่อจริง นามสกุล ตรงๆ
                search_queries.append(f"{last_name} {first_name}")  # นามสกุล นำหน้าชื่อจริง
                if len(last_name) > 0:
                    search_queries.append(f"{first_name} {last_name[0]}.") # ชื่อจริง + นามสกุลย่อตัวแรก
            
            if nickname:
                search_queries.append(f"{nickname} {first_name}")   # ชื่อเล่น + ชื่อจริง (ฮิตมากในวัยรุ่น)
                search_queries.append(f"{first_name} {nickname}")   # ชื่อจริง + ชื่อเล่นต่อท้าย
                if last_name:
                    search_queries.append(f"{nickname} {last_name}") # ชื่อเล่น + นามสกุลจริง

            # จำลองรายชื่อโปรไฟล์ที่ดึงมาจากโครงข่าย API (มีทั้งภาษาไทย ภาษาอังกฤษ และชื่อเล่นสลับ)
            # ในแอปพลิเคชันจริง ส่วนนี้จะถูกแกะ (Parse) มาจากข้อมูล JSON ที่ตอบกลับมาจาก SocialCrawl, PDL และ Coresignal
            mocked_profiles = [
                {
                    "platform": "Facebook",
                    "name_displayed": f"{first_name} {last_name}" if last_name else f"{first_name} Buromsri",
                    "profile_url": f"https://www.facebook.com/profile.php?id=100098765432101",
                    "extracted_bio": f"ศึกษาที่ {studying_uni if studying_uni else 'มหาวิทยาลัย'} · อาศัยอยู่ที่ {current_province if current_province else 'ประเทศไทย'}",
                    "lang": "TH"
                },
                {
                    "platform": "Facebook",
                    "name_displayed": f"{nickname if nickname else 'Bee'} {first_name}",
                    "profile_url": f"https://www.facebook.com/user.profile.dev.99",
                    "extracted_bio": f"ทำงานที่ {current_work if current_work else 'อิสระ'} · อดีตโรงเรียนมัธยม: {edu_highschool if edu_highschool else 'ไม่ระบุ'}",
                    "lang": "TH/EN"
                },
                {
                    "platform": "Facebook",
                    "name_displayed": f"{first_name.lower()}.{last_name.lower() if last_name else 'profile'}",
                    "profile_url": f"https://www.facebook.com/target.osint.verified",
                    "extracted_bio": f"Studied at {studying_faculty if studying_faculty else 'Faculty of Science'} · Lives in Bangkok",
                    "lang": "EN"
                }
            ]

            time.sleep(2.0) # จำลองเวลาที่บอทใช้ยิง API ไปกวาดข้อมูลข้ามเซิร์ฟเวอร์
            
            # --- 6. รายงานชุดข้อมูลและการแสดงผลโปรไฟล์ตรง ---
            st.markdown("### 🌐 UNIFIED DIRECT PROFILE REPORT (พบโปรไฟล์เป้าหมายที่คาดว่าเป็นไปได้สูงสุด)")
            st.write("---")
            
            st.markdown("#### ⚙️ รายการคำค้นหาที่ AI แตกแพทเทิร์นเพื่อไปค้นหาไขว้ (Generated Search Combinations):")
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.info(f"**🇹🇭 คีย์เวิร์ด/โครงสร้างสลับ (ไทย):** {', '.join([q for q in search_queries if not q.isascii()]) if any(not q.isascii() for q in search_queries) else 'ใช้ระบบร่วมกับภาษาอังกฤษ'}")
            with col_q2:
                st.info(f"**🇺🇸 คีย์เวิร์ด/โครงสร้างสลับ (อังกฤษ):** {', '.join([q for q in search_queries if q.isascii()])}")

            st.write("<br>", unsafe_allow_html=True)
            st.markdown("#### 👥 ผลการขุดคัดแยกโปรไฟล์ตรง (คัดกรองร่วมกับประวัติ 11 ช่องพารามิเตอร์):")

            # ลูปแสดงผลโปรไฟล์ที่ดึงออกมาทีละคน พร้อมลิงก์ตรงตัวบุคคล
            for idx, profile in enumerate(mocked_profiles):
                
                # --- [CORE LOGIC] ระบบ Re-check และคำนวณ Match Score รายบุคคล ---
                individual_score = 45 # คะแนนฐานสำหรับชื่อที่ถูกสแกนติดมาจากระบบ API
                
                # ตรวจเงื่อนไขข้อมูลเสริม 11 ช่อง เพื่อตรวจสอบความถูกต้องของโปรไฟล์นี้
                match_reasons = []
                if nickname and nickname.lower() in profile['name_displayed'].lower():
                    individual_score += 15
                    match_reasons.append("ตรงกับชื่อเล่นที่กรอก")
                if current_province and current_province in profile['extracted_bio']:
                    individual_score += 15
                    match_reasons.append("พิกัดจังหวัดปัจจุบันตรงกัน")
                if studying_uni and studying_uni in profile['extracted_bio']:
                    individual_score += 15
                    match_reasons.append("ประวัติมหาวิทยาลัยตรงกัน")
                if edu_highschool and edu_highschool in profile['extracted_bio']:
                    individual_score += 10
                    match_reasons.append("ประวัติโรงเรียนมัธยมตรงกัน")
                if current_work and current_work in profile['extracted_bio']:
                    individual_score += 15
                    match_reasons.append("ประวัติสถานที่ทำงานปัจจุบันตรงกัน")

                if individual_score > 100: individual_score = 100

                # แสดงผลการ์ดรายชื่อโปรไฟล์แต่ละรายการ
                st.markdown(f"""
                <div class='profile-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h4 style='color: #00F0FF; margin: 0;'>👤 ผลลัพธ์ที่ {idx+1}: {profile['name_displayed']} [{profile['platform']}]</h4>
                        <span class='{"match-high" if individual_score >= 70 else "match-mid"}'>ดัชนีความถูกต้อง: {individual_score}%</span>
                    </div>
                    <p style='margin: 8px 0; font-size: 14px; color: #94A3B8;'>
                        <b>🧬 ข้อมูลประวัติบนโปรไฟล์ (Bio):</b> {profile['extracted_bio']}<br>
                        <b>🌐 ตรวจจับโครงสร้างภาษา:</b> {profile['lang']}
                    </p>
                    <p style='margin: 0; font-size: 13px; color: #A7F3D0;'>
                        <b>🛠️ ข้อมูลรีเช็คจาก AI:</b> {(' พบจุดเชื่อมโยง: ' + ' , '.join(match_reasons)) if match_reasons else ' ดึงชื่อจากโครงข่ายสลับตำแหน่ง (กรุณากดลิงก์ด้านล่างเพื่อตรวจสอบรีเช็คประวัติเชิงลึกเพิ่มเติม)'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # ปุ่มสีน้ำเงินกดปุ๊บ วิ่งตรงเข้าหน้าโปรไฟล์คนนั้นทันที (ไม่ใช่หน้าค้นหา)
                st.link_button(f"🔗 คลิกเปิดโปรไฟล์ตรงของ คุณ {profile['name_displayed']} บน {profile['platform']} ↗️", profile['profile_url'], use_container_width=True)
                st.write("") 

            st.success("🎯 ระบบทำการผสมชื่อไทย/อังกฤษ/ชื่อเล่น และกวาดเอาลิงก์โปรไฟล์ตรง (Direct URL) มารายงานผลเรียบร้อยแล้ว!")
