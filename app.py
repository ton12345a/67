เปลี่ยนกลับมาเป็นตัวอย่างข้อมูลของ คุณอารยา บุรมศรี ให้เรียบร้อยตามคำขอแล้วครับ! โครงสร้างระบบ ลำดับการกรองความยากจากตรงตัวพิมพ์ติดกันไปจนถึงการผสมสัญลักษณ์ซับซ้อน และการแสดงผลภาพคู่กับลิงก์สืบค้นยังคงอยู่ครบถ้วนร้อยเปอร์เซ็นต์ครับ

ก๊อปปี้โค้ดทั้งหมดด้านล่างนี้ไปวางทับในไฟล์ app.py บน GitHub ได้เลยครับ:

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

# ฟังก์ชันดึง AI มาวิเคราะห์และเรียงลำดับตามกฎเหล็ก (ตรงตัวติดกันก่อน -> เริ่มมีสัญลักษณ์ -> ผสมยาก)
def ask_gemini_for_variants(first_name, last_name, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        คุณคือระบบผู้เชี่ยวชาญด้าน OSINT ระดับสูง จงวิเคราะห์ชื่อภาษาไทย: "{first_name}" และนามสกุล: "{last_name}"
        Alienation คลังประวัติศาสตร์แล้วสร้างรายการ "ชื่อผู้ใช้ (Username)" หรือ "ชื่อโปรไฟล์" ภาษาอังกฤษที่คนคนนี้มีแนวโน้มจะนำไปใช้ตั้งบน Social Media มากที่สุด โดยจัดเรียงลำดับใน Array ตามระดับความง่ายไปยากดังนี้:

        1. [ช่วงแรกสุด - ตรงตัวเป๊ะๆ ติดกัน]: แปลงชื่อและนามสกุลเป็นภาษาอังกฤษตรงตัว (รวมถึงการสะกดตรงตัวที่คนไทยนิยมใช้ได้ทุกรูปแบบ เช่น Araya, Buromsri) แล้วให้พิมพ์ติดกันเป็นพืดตัวเล็กทั้งหมด "ห้ามมีจุด ห้ามมีขีดล่าง ห้ามมีตัวเลขเด็ดขาด" (ตัวอย่างเช่น arayaburomsri) เอาออกมาให้ครบทุกแบบการสะกดตรงตัวเท่าที่จะเป็นไปได้
        2. [ช่วงที่สอง - ตรงตัวคั่นสัญลักษณ์]: เริ่มเอาชื่อตรงตัวมาคั่นด้วยเครื่องหมายพื้นฐานจุดหรือขีดล่าง (เช่น araya.buromsri, araya_buromsri)
        3. [ช่วงที่สาม - เริ่มย่อและผสมซับซ้อน]: นามสกุลเริ่มสั้นลงหรือย่อผสมกับเครื่องหมาย (เช่น araya.bur, araya._brs, arayab)
        4. [ช่วงท้ายสุด - คาดเดาพฤติกรรม/ตัวเลข]: ใส่ชื่อเล่น, คำสร้อย, ปีเกิด ค.ศ. หรือ พ.ศ. (เช่น Benz.araya, araya2026, araya2569)

        จงตอบกลับเป็นรูปแบบ JSON array ของข้อความเท่านั้น ห้ามมีคำอธิบายหรือเครื่องหมายมาร์กดาวน์ใดๆ ทั้งสิ้น ตัวอย่างโครงสร้างผลลัพธ์:
        ["arayaburomsri", "araya.buromsri", "araya._brs", "araya2026"]
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

# ฟอร์มรับข้อมูลเป้าหมาย (เปลี่ยนกลับเป็น อารยา บุรมศรี)
st.markdown("<div class='system-status'>[SYSTEM] READY TO INTEL: กรอกข้อมูลเป้าหมายคนไทยเพื่อส่งให้ AI คำนวณรอยเท้าดิจิทัล</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("TARGET FIRST NAME (ภาษาไทย)", value="อารยา", placeholder="เช่น อารยา")
with col2:
    last_name = st.text_input("TARGET LAST NAME (ภาษาไทย)", value="บุรมย์ศรี", placeholder="เช่น บุรมย์ศรี")

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
            st.markdown(f"### 📊 TARGET ALIASES PREDICTED (คัดกรอง: ตรงตัวพิมพ์ติดกัน ➔ เริ่มมีสัญลักษณ์ ➔ คาดเดาซับซ้อน)")
            
            st.write("---")
            st.markdown("### 🌐 OSINT TARGET PROFILE VISUALIZER (คลังผลลัพธ์พร้อมภาพจำลองและจุดสืบค้น)")
            
            for index, name in enumerate(ai_variants):
                clean_name = name.replace(" ", "")
                
                # สร้างลิงก์สืบค้นของแต่ละแพลตฟอร์ม
                fb_url = f"https://www.facebook.com/search/top/?q={urllib.parse.quote(name)}"
                ig_url = f"https://www.instagram.com/{clean_name}"
                x_url = f"https://x.com/search?q={urllib.parse.quote(name)}"
                
                card_col1, card_col2 = st.columns([2, 8])
                
                with card_col1:
                    # แสดงภาพอวตารจำลองแล็บระบุตัวตนสไตล์ไซเบอร์เท่ๆ
                    st.image(f"https://api.dicebear.com/7.x/bottts/svg?seed={clean_name}", width=110, caption=f"LEVEL {index+1}")
                
                with card_col2:
                    # ตรรกะแยกแยะประเภทเพื่อติดป้ายแสดงสถานะ (Tag) ให้เห็นความแม่นยำของการไล่ระดับชื่อ
                    if "." not in name and "_" not in name and not any(char.isdigit() for char in name):
                        status_text = "EXACT MATCH PLAIN STRING (ตรงตัวเป๊ะๆ พิมพ์ติดกันช่วงแรก)"
                        status_color = "#00F0FF"
                    elif "._" in name or "_." in name or ("." in name and "_" in name):
                        status_text = "ADVANCED SEPARATOR (สัญลักษณ์ผสม เช่นไอจี araya._brs)"
                        status_color = "#FF0055"
                    else:
                        status_text = "COMPLEX BEHAVIORAL PATTERN (ผสมชื่อเล่น/สัญลักษณ์/ตัวเลขช่วงท้าย)"
                        status_color = "#FFB700"
                    
                    st.markdown(f"<h4 style='color: {status_color}; margin-bottom: 2px;'>ID: {name}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #6B7280; font-size: 12px;'>PRIORITY LEVEL: {index+1} // {status_text}</span>", unsafe_allow_html=True)
                    
                    # ลิงก์สืบค้นวางประกบข้างรูปภาพอย่างเป็นระเบียบตามสั่ง
                    st.markdown(f"""
                    * 🟦 **FACEBOOK TARGET:** [`{name}`] ➔ [เปิดหน้าต่างสืบค้น ↗️]({fb_url})
                    * 📸 **INSTAGRAM HANDLE:** [`@{clean_name}`] ➔ [เปิดหน้าต่างเจาะโปรไฟล์ ↗️]({ig_url})
                    * 🐦 **X INTELLIGENCE:** [`{name}`] ➔ [เปิดคลังดักข้อมูล ↗️]({x_url})
                    """)
                
                st.markdown("<hr style='border-color: #1F2937; margin: 15px 0;'>", unsafe_allow_html=True)

            st.success("🎯 [COMPLETED] คัดกรองและเรียงลำดับรอยเท้าดิจิทัลของ อารยา บุรมศรี เรียบร้อยครับ!")
