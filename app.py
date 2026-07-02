รับทราบครับ! ปรับเงื่อนไขให้เคลียร์และตรงตามต้องการที่สุด คือ ช่วงแรกสุดห้ามมีขีดล่าง (_) หรือจุด (.) หรือตัวเลขใดๆ ทั้งสิ้น ให้เป็นตัวอักษรพิมพ์ติดกันยาวๆ เท่านั้น (เช่น arayaburomsri) แล้วหลังจากนั้นค่อยๆ ทยอยใส่จุด ค่อยๆ ใส่ขีดล่าง และตามด้วยรหัสอื่นๆ ไล่ระดับความยากลงไปเท่าที่ AI จะขุดค้นรูปพฤติกรรมออกมาได้ทั้งหมดครับ

ก๊อปปี้โค้ดเวอร์ชันปรับปรุงการคัดกรอง (Strict Logic) ชุดนี้ไปวางทับใน app.py บน GitHub ได้เลยครับ:

Python
import streamlit as st
import urllib.parse
import json

# ตรวจสอบการติดตั้งโมดูล Google GenAI หลังบ้าน
try:
    import google.generativeai as genai
except ImportError:
    st.error("SYSTEM ERROR: 'google-generativeai' package missing in requirements.txt")

# ตั้งค่าหน้าเว็บสไตล์ระบบปฏิบัติการความมั่นคงปลอดภัยไซเบอร์ (Dark Mode OS)
st.set_page_config(
    page_title="NEO-OSINT // CYBER INTELLIGENCE SYSTEM", 
    page_icon="👁️‍🗨️", 
    layout="wide"
)

# ตกแต่ง UI ด้วย CSS ให้เป็นหน้าจอสายลับดาร์กโหมดขั้นสุด
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    .terminal-header {
        font-family: 'Courier New', Courier, monospace;
        font-size: 36px;
        font-weight: bold;
        color: #00F0FF;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    .terminal-sub {
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        color: #FF0055;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 35px;
        text-transform: uppercase;
    }
    .system-status {
        background-color: #111827;
        border-left: 4px solid #00F0FF;
        padding: 15px;
        border-radius: 4px;
        font-family: monospace;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# หน้าจอหลักของระบบปฏิบัติการ
st.markdown("<div class='terminal-header'>👁️‍🗨️ CORE-OSINT // TARGET RESOLVER</div>", unsafe_allow_html=True)
st.markdown("<div class='terminal-sub'>[ CLASSIFIED SYSTEM // DEEP IDENTITY PREDICTION ENGINE ]</div>", unsafe_allow_html=True)

# แถบควบคุมด้านซ้าย (Control Panel)
with st.sidebar:
    st.markdown("<h3 style='color: #00F0FF; font-family: monospace;'>🎛️ SYSTEM CONTROL</h3>", unsafe_allow_html=True)
    st.write("---")
    gemini_key = st.text_input("ENTER GEMINI API KEY:", type="password", help="กรอกรหัสผ่านเชื่อมต่อโครงข่ายสมองกล Google เพื่อเริ่มระบบสแกน")
    st.markdown("[🔓 คัดลอก API KEY ฟรีที่นี่](https://aistudio.google.com/)")
    st.write("---")
    st.markdown("<span style='color: #6B7280; font-family: monospace; font-size: 11px;'>SECURE CONNECTION: ACTIVE<br>CORE MODEL: GEMINI-2.5-FLASH</span>", unsafe_allow_html=True)

# ฟังก์ชันดึง AI มาวิเคราะห์และเรียงลำดับตามกฎเหล็ก (ติดกัน -> มีจุด/ขีด -> เดาพฤติกรรม)
def ask_gemini_for_variants(first_name, last_name, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        คุณคือระบบจำลอง AI OSINT อัจฉริยะ จงวิเคราะห์ชื่อภาษาไทย: "{first_name}" และนามสกุล: "{last_name}" 
        แล้วสร้างรายการชื่อผู้ใช้ (Username) ภาษาอังกฤษที่มีความน่าจะเป็นทั้งหมด โดยให้เรียงลำดับชุดข้อมูลใน Array ตามกฎข้อบังคับนี้อย่างเคร่งครัด:

        1. [ช่วงแรกสุด] ตัวอักษรพิมพ์ติดกันยาวๆ เท่านั้น ห้ามมีจุด (.) ห้ามมีขีดล่าง (_) และห้ามมีตัวเลขเด็ดขาด (เช่น supachaipimsut, pimsutsupachai)
        2. [ช่วงที่สอง] เริ่มใส่เครื่องหมายคั่นพื้นฐาน เช่น ใส่จุดหรือขีดล่างคั่นระหว่างชื่อและนามสกุลตรงตัว (เช่น supachai.pimsut, supachai_pimsut)
        3. [ช่วงที่สาม] เริ่มตัดทอนนามสกุลผสมกับเครื่องหมาย (เช่น supachai._pms, supachai.p)
        4. [ช่วงท้ายสุด] ใส่ชื่อเล่นเดาทางคนไทย ผสมตัวเลข หรืออักขระพิเศษขั้นสูงเท่าที่จะหามาได้ทั้งหมด (เช่น Benz.supachai, supachai2026, suppachai_p)

        จงตอบกลับเป็นรูปแบบ JSON array ของข้อความเท่านั้น ห้ามมีคำอธิบายหรือเครื่องหมายมาร์กดาวน์ใดๆ ทั้งสิ้น ตัวอย่างโครงสร้างผลลัพธ์:
        ["supachaipimsut", "supachai.pimsut", "supachai._pms", "Benz.supachai", "supachai2026"]
        """
        
        response = model.generate_content(prompt)
        clean_text = response.text.strip()
        
        if clean_text.startswith("```json"):
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1].split("```")[0].strip()
            
        result_data = json.loads(clean_text)
        if isinstance(result_data, list):
            return result_data
        elif isinstance(result_data, dict):
            for key in result_data:
                if isinstance(result_data[key], list):
                    return result_data[key]
            return list(result_data.values())[0]
        return []
        
    except Exception as e:
        st.error(f"[-] SYSTEM ERROR ACCESSING GEMINI NODE: {str(e)}")
        return []

# ฟอร์มรับข้อมูลเป้าหมาย
st.markdown("<div class='system-status'>[SYSTEM] READY TO INTEL: กรอกข้อมูลเป้าหมายคนไทยเพื่อส่งให้ AI คำนวณรอยเท้าดิจิทัล</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("TARGET FIRST NAME (ภาษาไทย)", placeholder="เช่น ศุภชัย")
with col2:
    last_name = st.text_input("TARGET LAST NAME (ภาษาไทย)", placeholder="เช่น พิมพสุทธิ์")

# ปุ่มกดรันระบบ
if st.button("⚡ INITIALIZE DEEP SCAN (วิเคราะห์โครงสร้างชื่อด้วย AI)", type="primary", use_container_width=True):
    if not gemini_key:
        st.error("[-] REJECTED: จำเป็นต้องกรอก GEMINI API KEY ที่แผงควบคุมด้านซ้ายก่อนรันระบบ")
    elif not first_name:
        st.warning("[-] WARNING: ระบุชื่อเป้าหมายอย่างน้อยหนึ่งรายการ")
    else:
        with st.spinner("🔄 CONNECTING TO GOOGLE AI NODE... SORTING STRUCTURAL ALIASES..."):
            ai_variants = ask_gemini_for_variants(first_name, last_name, gemini_key)
            
        if ai_variants:
            st.markdown(f"### 📊 TARGET ALIASES PREDICTED (คัดกรอง: ติดกัน ➔ เริ่มมีสัญลักษณ์ ➔ คาดเดาพฤติกรรม)")
            
            st.write("---")
            st.markdown("### 🌐 OSINT TARGET PROFILE VISUALIZER (คลังผลลัพธ์พร้อมภาพจำลองและจุดสืบค้น)")
            
            for index, name in enumerate(ai_variants):
                clean_name = name.replace(" ", "")
                
                # สร้างลิงก์สืบค้น
                fb_url = f"https://www.facebook.com/search/top/?q={urllib.parse.quote(name)}"
                ig_url = f"https://www.instagram.com/{clean_name}"
                x_url = f"https://x.com/search?q={urllib.parse.quote(name)}"
                
                card_col1, card_col2 = st.columns([2, 8])
                
                with card_col1:
                    st.image(f"https://api.dicebear.com/7.x/bottts/svg?seed={clean_name}", width=110, caption=f"LEVEL {index+1}")
                
                with card_col2:
                    # วิเคราะห์จำแนกประเภทแสดงสถานะความซับซ้อนของชื่อ
                    if "." not in name and "_" not in name and not any(char.isdigit() for char in name):
                        status_text = "RAW PLAIN STRING (พิมพ์ติดกันช่วงแรก)"
                        status_color = "#00F0FF"
                    elif "._" in name or "_." in name or ("." in name and "_" in name):
                        status_text = "ADVANCED SEPARATOR (สัญลักษณ์ผสม เช่นไอจี araya._brs)"
                        status_color = "#FF0055"
                    else:
                        status_text = "COMPLEX BEHAVIORAL PATTERN (สัญลักษณ์/ตัวเลข/ชื่อเล่นช่วงท้าย)"
                        status_color = "#FFB700"
                    
                    st.markdown(f"<h4 style='color: {status_color}; margin-bottom: 2px;'>ID: {name}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #6B7280; font-size: 12px;'>PRIORITY LEVEL: {index+1} // {status_text}</span>", unsafe_allow_html=True)
                    
                    # ลิงก์สืบค้นวางประกบข้างรูปภาพตามคำสั่ง
                    st.markdown(f"""
                    * 🟦 **FACEBOOK TARGET:** [`{name}`] ➔ [เปิดหน้าต่างสืบค้น ↗️]({fb_url})
                    * 📸 **INSTAGRAM HANDLE:** [`@{clean_name}`] ➔ [เปิดหน้าต่างเจาะโปรไฟล์ ↗️]({ig_url})
                    * 🐦 **X INTELLIGENCE:** [`{name}`] ➔ [เปิดคลังดักข้อมูล ↗️]({x_url})
                    """)
                
                st.markdown("<hr style='border-color: #1F2937; margin: 15px 0;'>", unsafe_allow_html=True)

            st.success("🎯 [COMPLETED] เรียงลำดับโครงสร้างตามเงื่อนไขเสร็จสมบูรณ์ ยื่นส่งงานประกวดได้เลยครับ!")
