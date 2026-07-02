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

# ฟังก์ชันดึง AI มาวิเคราะห์และเรียงลำดับความยากง่ายจากตรงตัวลงไป
def ask_gemini_for_variants(first_name, last_name, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        คุณคือผู้เชี่ยวชาญด้าน OSINT ระดับสูง หน้าที่ของคุณคือการแปลงชื่อภาษาไทยเป็นภาษาอังกฤษ 
        และสร้างชื่อผู้ใช้ (Username) ที่คนคนนี้มีโอกาสใช้บนโลกออนไลน์ โดย "ต้องเรียงลำดับจากง่ายไปยาก" อย่างเคร่งครัด ดังนี้:

        เป้าหมายชื่อไทย: "{first_name}" นามสกุล: "{last_name}"

        เงื่อนไขการเรียงลำดับใน Array (สำคัญมาก):
        อันดับที่ 1: ชื่อและนามสกุลสะกดตรงตัวเป๊ะๆ ตัวติดกันหรือคั่นด้วยจุด/ขีดล่าง (เช่น ArayaBuromsri, araya.buromsri)
        อันดับที่ 2: ชื่อตรงตัว ผสมนามสกุลแบบย่อตัวหน้าหรือตัวท้าย (เช่น araya.bur, arayab)
        อันดับที่ 3: ชื่อตรงตัว ผสมตัวเลขปีเกิด ค.ศ. หรือ พ.ศ. (เช่น araya2026, araya2569)
        อันดับที่ 4: ชื่อผู้ใช้ที่เริ่มเดาพฤติกรรมคนไทย เช่น ใส่ชื่อเล่นนำหน้า/ตามท้าย หรือใช้คำแสลง (เช่น Benz.araya, araya.ch)

        จงตอบกลับเป็นรูปแบบ JSON array ของข้อความเท่านั้น ห้ามมีคำอธิบายหรือเครื่องหมายมาร์กดาวน์ใดๆ ทั้งสิ้น ตัวอย่างผลลัพธ์:
        ["arayaburomsri", "araya.buromsri", "araya.bur", "araya2026", "araya_b"]
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
    first_name = st.text_input("TARGET FIRST NAME (ภาษาไทย)", placeholder="เช่น อารยา")
with col2:
    last_name = st.text_input("TARGET LAST NAME (ภาษาไทย)", placeholder="เช่น บุรมย์ศรี")

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
            st.markdown(f"### 📊 TARGET ALIASES PREDICTED (เรียงจากตรงตัว ➔ คาดเดาพฤติกรรม)")
            
            st.write("---")
            st.markdown("### 🌐 OSINT TARGET PROFILE VISUALIZER (คลังผลลัพธ์พร้อมภาพจำลองและจุดสืบค้น)")
            
            # วนลูปแสดงผลทีละชื่อตามลำดับที่ AI เรียงมาให้จากตรงตัวไปยาก
            for index, name in enumerate(ai_variants):
                clean_name = name.replace(" ", "")
                
                # สร้างลิงก์สืบค้นของแต่ละค่าย
                fb_url = f"https://www.facebook.com/search/top/?q={urllib.parse.quote(name)}"
                ig_url = f"https://www.instagram.com/{clean_name}"
                x_url = f"https://x.com/search?q={urllib.parse.quote(name)}"
                
                card_col1, card_col2 = st.columns([2, 8])
                
                with card_col1:
                    # แสดงภาพอวตารจำลองแล็บระบุตัวตนสไตล์ไซเบอร์เท่ๆ
                    st.image(f"https://api.dicebear.com/7.x/bottts/svg?seed={clean_name}", width=110, caption=f"LEVEL {index+1}")
                
                with card_col2:
                    # ไฮไลต์ให้เห็นระดับความลึกของการเดาชื่อ
                    status_text = "EXACT MATCH (ชื่อตรงตัว)" if index < 2 else "BEHAVIORAL PREDICTION (คาดเดาความน่าจะเป็น)"
                    status_color = "#00F0FF" if index < 2 else "#FF0055"
                    
                    st.markdown(f"<h4 style='color: {status_color}; margin-bottom: 2px;'>ID: {name}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #6B7280; font-size: 12px;'>PRIORITY LEVEL: {index+1} // {status_text}</span>", unsafe_allow_html=True)
                    
                    # วางช่องทางการเชื่อมโยงสืบค้นเชิงลึกไว้ข้างๆ รูปภาพทันทีตามสั่ง
                    st.markdown(f"""
                    * 🟦 **FACEBOOK TARGET:** [`{name}`] ➔ [เปิดหน้าต่างสืบค้น ↗️]({fb_url})
                    * 📸 **INSTAGRAM HANDLE:** [`@{clean_name}`] ➔ [เปิดหน้าต่างเจาะโปรไฟล์ ↗️]({ig_url})
                    * 🐦 **X INTELLIGENCE:** [`{name}`] ➔ [เปิดคลังดักข้อมูล ↗️]({x_url})
                    """)
                
                st.markdown("<hr style='border-color: #1F2937; margin: 15px 0;'>", unsafe_allow_html=True)

            st.success("🎯 [COMPLETED] จัดลำดับโครงสร้างรอยเท้าดิจิทัลเรียบร้อย พร้อมนำเสนอแบบไล่ระดับความยาก")
