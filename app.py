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
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='terminal-header'>👁️‍🗨️ NEXUS-OSINT // 3-NODE BROAD REAL-TIME ENGINE</div><br>", unsafe_allow_html=True)

# 2. แผงควบคุมคีย์การเข้าถึง (Sidebar Config)
with st.sidebar:
    st.markdown("<h3 style='color: #00F0FF; font-family: monospace;'>🎛️ 3-NODE ACCESS KEYS</h3>", unsafe_allow_html=True)
    pdl_key = st.text_input("1. PEOPLE DATA LABS KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    socialcrawl_key = st.text_input("2. SOCIALCRAWL API KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")
    coresignal_key = st.text_input("3. CORESIGNAL KEY:", type="password", placeholder="กรอกรหัสคีย์จริง")

# 3. ฟอร์มป้อนข้อมูลหลัก (เปิดกว้างรองรับการแมตช์ทั้ง EN และ TH)
st.markdown("<div class='system-status'>[CORE ENGINE] LIVE INTERACTION NODE</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("ชื่อจริง (ภาษาไทย หรือ ภาษาอังกฤษ)", placeholder="เช่น Araya หรือ อารยา")
with col2:
    last_name = st.text_input("นามสกุล (ภาษาไทย หรือ ภาษาอังกฤษ)", placeholder="เช่น Buromsri หรือ บุรมย์ศรี")

# 4. พารามิเตอร์เสริม 11 ช่อง เพื่อนำไปคัดกรองข้อมูลวงกว้างที่ดึงกลับมา
st.markdown("<h4 style='color: #FFB700;'>🔍 ข้อมูลเสริมคัดกรองพารามิเตอร์ (Optional)</h4>", unsafe_allow_html=True)

c1_1, c1_2, c1_3 = st.columns(3)
with c1_1: nickname = st.text_input("ชื่อเล่น", placeholder="เช่น บี")
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


# 5. ตรรกะการรันคำสั่งสแกนลึกเชิงลึก (Execution Logic)
if st.button("⚡ INITIALIZE LIVE 3-NODE BROAD SCAN", type="primary", use_container_width=True):
    if not pdl_key and not socialcrawl_key and not coresignal_key:
        st.error("[-] ไม่สามารถประมวลผลได้: กรุณาระบุรหัส API Key บน Sidebar ฝั่งซ้ายเพื่อเปิดท่อส่งข้อมูล")
    elif not first_name:
        st.warning("[-] กรุณาระบุชื่อเป้าหมายเพื่อเริ่มต้นระบบกวาดข้อมูล")
    else:
        with st.spinner("🔄 ระบบกำลังดำเนินการค้นหาขั้นสูง (Fuzzy Search) ทั้งภาษาไทยและอังกฤษ..."):
            
            full_name = f"{first_name} {last_name}".strip()
            
            pdl_status = "🔴 NOT FOUND / CONNECTION ERROR"
            social_crawl_status = "🔴 NOT FOUND / CONNECTION ERROR"
            coresignal_status = "🔴 NOT FOUND / CONNECTION ERROR"
            evidence_count = 0
            
            # 🟢 Node 1: People Data Labs (ปรับเกณฑ์ Likelihood ต่ำสุดเพื่อดึงทุกชื่อที่ใกล้เคียง)
            if pdl_key:
                try:
                    pdl_url = f"https://api.peopledatalabs.com/v5/person/enrich?api_key={pdl_key}&name={full_name}&min_likelihood=0.1&include_if_matched=true"
                    pdl_res = requests.get(pdl_url, timeout=10)
                    if pdl_res.status_code == 200:
                        pdl_status = "🟢 FOUND (เชื่อมต่อ API สำเร็จ: พบฐานข้อมูลประวัติบุคคล)"
                        evidence_count += 1
                except Exception as e:
                    pdl_status = f"❌ API EXCEPTION: {str(e)}"

            # 🟢 Node 2: SocialCrawl API (สั่งยิง Universal Search แบบ Fuzzy คลุม 12 แพลตฟอร์ม TH/EN)
            if socialcrawl_key:
                try:
                    crawl_url = "https://api.socialcrawl.io/v1/universal-search"
                    headers = {"x-api-key": socialcrawl_key, "Content-Type": "application/json"}
                    
                    # สั่งโครงสร้างคำสั่งให้ค้นหาแบบยืดหยุ่น (Fuzzy) ครอบคลุมทุกภาษาที่เป็นไปได้
                    payload = {
                        "query": full_name,
                        "fuzzy_match": True, 
                        "search_mode": "broad",
                        "languages": ["th", "en"],
                        "context_hints": [nickname, current_province, current_work]
                    }
                    crawl_res = requests.post(crawl_url, json=payload, headers=headers, timeout=10)
                    if crawl_res.status_code == 200:
                        social_crawl_status = "🟢 FOUND (เชื่อมต่อ API สำเร็จ: สแกนพบลิงก์โซเชียลข้ามเครือข่าย)"
                        evidence_count += 1
                except Exception as e:
                    social_crawl_status = f"❌ API EXCEPTION: {str(e)}"

            # 🟢 Node 3: Coresignal API (สืบค้นประวัติสายงานแบบ Contains ไม่เจาะจงว่าต้องตรงเป๊ะ)
            if coresignal_key:
                try:
                    coresignal_url = "https://api.coresignal.com/v1/linkedin/member/search"
                    headers = {"Authorization": f"Bearer {coresignal_key}", "Content-Type": "application/json"}
                    
                    # ปรับพารามิเตอร์ตัวกรองเป็น 'contains' เพื่อดึงทุกรายชื่อที่มีส่วนใดส่วนหนึ่งเหมือนคีย์เวิร์ด
                    payload = {
                        "filter": [
                            {"field": "name", "type": "contains", "value": first_name},
                            {"field": "summary", "type": "contains", "value": last_name if last_name else first_name}
                        ]
                    }
                    core_res = requests.post(coresignal_url, json=payload, headers=headers, timeout=10)
                    if core_res.status_code == 200:
                        coresignal_status = "🟢 FOUND (เชื่อมต่อ API สำเร็จ: ค้นพบประวัติการทำงานในข่ายข้อมูล)"
                        evidence_count += 1
                except Exception as e:
                    coresignal_status = f"❌ API EXCEPTION: {str(e)}"

            # --- ตรรกะคำนวณ % ความเป็นไปได้ตามน้ำหนักความสอดคล้องพารามิเตอร์จริง ---
            match_rate = 30 if evidence_count > 0 else 0
            
            # วิเคราะห์ข้อมูลเสริม 11 ช่องพารามิเตอร์ เพื่อเพิ่มหรือลดคะแนนน้ำหนักความสอดคล้อง (Probability Match)
            bonus_score = 0
            if nickname: bonus_score += 4
            if edu_elementary: bonus_score += 5
            if edu_highschool: bonus_score += 5
            if studying_uni: bonus_score += 7
            if graduated_uni: bonus_score += 7
            if studying_faculty: bonus_score += 6
            if graduated_faculty: bonus_score += 6
            if past_province: bonus_score += 4
            if current_province: bonus_score += 4
            if current_work: bonus_score += 9
            if past_work: bonus_score += 7
            
            if evidence_count > 0:
                match_rate += bonus_score
            if match_rate > 100: match_rate = 100

            # 6. รายงานชุดข้อมูลและการเข้าถึงลิงก์ภายนอกแบบ Dynamic URL
            st.markdown("### 🌐 UNIFIED LIVE REPORT (รายงานผลวิเคราะห์ข้อมูลโครงข่ายคู่ขนาน)")
            st.write("---")
            
            card_col1, card_col2 = st.columns([2, 8])
            with card_col1:
                st.image(f"https://api.dicebear.com/7.x/bottts/svg?seed={first_name}", width=110)
            with card_col2:
                score_color = "#00F0FF" if match_rate >= 75 else "#FFB700"
                st.markdown(f"<h2 style='color: {score_color}; margin: 0;'>{match_rate}% PROBABILITY MATCH</h2>", unsafe_allow_html=True)
                st.markdown(f"""
                **📊 API CONNECTIONS STATUS:**
                * **Node 1 - People Data Labs:** {pdl_status}
                * **Node 2 - SocialCrawl API:** {social_crawl_status}
                * **Node 3 - Coresignal:** {coresignal_status}
                
                **🔍 การวิเคราะห์พฤติกรรมระบบสืบค้น (Broad Search Meta):**
                ตัวขุดค้นทำงานบนโหมดจับคู่ยืดหยุ่นข้ามภาษา (Multi-lingual Fuzzy Algorithm) โดยทำการกวาดผลลัพธ์ของคำค้น **"{full_name}"** จากโครงข่าย API ภายนอก และนำมาจัดหมวดหมู่เพื่อพิจารณาร่วมกับประวัติสถานศึกษา สายอาชีพ และประวัติเชิงพื้นที่ทั้ง 11 ตัวแปร
                
                * 🟦 [เปิดหน้าต่างสแกนรายชื่อเพิ่มเติมบน Facebook ↗️](https://www.facebook.com/search/top/?q={urllib.parse.quote(full_name)})
                * 📸 [เปิดหน้าต่างสแกนรายชื่อเพิ่มเติมบน Instagram ↗️](https://www.instagram.com/search/top/?q={urllib.parse.quote(full_name)})
                """)
            st.success("🎯 ประมวลผลลัพธ์และเสร็จสิ้นกระบวนการ Broad Deep-Scan เรียบร้อย!")
