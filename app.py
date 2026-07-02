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

# ฟังก์ชันดึง AI มาวิเคราะห์ความน่าจะเป็นของพฤติกรรมการตั้งชื่อ
def ask_gemini_for_variants(first_name, last_name, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        คุณคือผู้เชี่ยวชาญด้าน OSINT และจิตวิทยาพฤติกรรมมนุษย์บนอินเทอร์เน็ต 
        จงวิเคราะห์ชื่อภาษาไทย: "{first_name}" และนามสกุล: "{last_name}" 
        แล้วสร้างรายการ "ชื่อผู้ใช้ (Username)" หรือ "ชื่อโปรไฟล์" ภาษาอังกฤษที่คนๆ นี้มีแนวโน้มจะนำไปใช้ตั้งใน Facebook, Instagram, และ X (Twitter) 
        โดยคำนึงถึงพฤติกรรมจริงของคนไทย เช่น:
        1. การสะกดตรงตัวแบบต่างๆ (เช่น Supachai, Suppachai)
        2. การใส่ชื่อเล่นเดาทาง (เช่น นำหน้าด้วย Benz, Boy, Toon, Jack, Ice)
        3. การย่อนามสกุล (เช่น pms, pims, p)
        4. การใช้ตัวอักษรพิเศษและตัวเลขผสม (เช่น supachai._pms, supachai.2026, suppachai_pims)
        
        จงตอบกลับเป็นรูปแบบ JSON array ของข้อความเท่านั้น ห้ามมีคำอธิบายหรือเครื่องหมายมาร์กดาวน์ใดๆ ทั้งสิ้น ตัวอย่างผลลัพธ์:
        ["supachai_pms", "Benz.supachai", "supachai.pims", "suppachai_p", "supachai.2026"]
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
        try:
            model_backup = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model_backup.generate_content(prompt)
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            result_data = json.loads(clean_text)
            return result_data if isinstance(result_data, list) else list(result_data.values())[0]
        except Exception as backup_err:
            st.error(f"[-] SYSTEM ERROR ACCESSING GEMINI NODE: {str(backup_err)}")
            return []

# ฟอร์มรับข้อมูลเป้าหมาย
st.markdown("<div class='system-status'>[SYSTEM] READY TO INTEL: กรอกข้อมูลเป้าหมายคนไทยเพื่อส่งให้ AI คำนวณรอยเท้าดิจิทัล</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("TARGET FIRST NAME (ภาษาไทย)", placeholder="เช่น ศุภชัย")
with col2:
    last_name = st.text_input("TARGET LAST NAME (ภาษาไทย)", placeholder="เช่น พิมพสุทธิ์")

# ปุ่มกดสไตล์ทหาร/สายลับ
if st.button("⚡ INITIALIZE DEEP SCAN (วิเคราะห์โครงสร้างชื่อด้วย AI)", type="primary", use_container_width=True):
    if not gemini_key:
        st.error("[-] REJECTED: จำเป็นต้องกรอก GEMINI API KEY ที่แผงควบคุมด้านซ้ายก่อนรันระบบ")
    elif not first_name:
        st.warning("[-] WARNING: ระบุชื่อเป้าหมายอย่างน้อยหนึ่งรายการ")
    else:
        with st.spinner("🔄 CONNECTING TO GOOGLE AI NODE... ANALYZING BEHAVIOR PATTERNS..."):
            ai_variants = ask_gemini_for_variants(first_name, last_name, gemini_key)
            
        if ai_variants:
            st.markdown(f"### 📊 TARGET ALIASES PREDICTED ({len(ai_variants)} ITEMS)")
            st.info(", ".join([f"**{v}**" for v in ai_variants]))
            
            st.write("---")
            st.markdown("### 🌐 OSINT EXPLOIT PATHWAYS (ช่องทางแกะรอยเชิงลึกจำแนกคลังเป้าหมาย)")
            
            tab1, tab2, tab3 = st.tabs(["[💻 FACEBOOK SCAN]", "[📸 INSTAGRAM TRACK]", "[🐦 X INTELLIGENCE]"])
            
            with tab1:
                st.markdown("<span style='color: #6B7280;'>// แสดงรายชื่อเป้าหมายการค้นหาบัญชี Facebook</span>", unsafe_allow_html=True)
                for name in ai_variants:
                    fb_url = f"[https://www.facebook.com/search/top/?q=](https://www.facebook.com/search/top/?q=){urllib.parse.quote(name)}"
                    st.markdown(f"🔹 **[ 🟦 FACEBOOK ]** ➔ `{name}` ➔ [เปิดจุดสืบค้น ↗️]({fb_url})")
                    st.markdown("<hr style='border-color: #1F2937; margin: 5px 0;'>", unsafe_allow_html=True)
                    
            with tab2:
                st.markdown("<span style='color: #6B7280;'>// แสดงรายชื่อเป้าหมายบัญชีผู้ใช้ในระบบ Instagram</span>", unsafe_allow_html=True)
                for name in ai_variants:
                    clean_name = name.replace(" ", "")
                    ig_url = f"[https://www.instagram.com/](https://www.instagram.com/){clean_name}"
                    st.markdown(f"🔹 **[ 📸 INSTAGRAM ]** ➔ `@{clean_name}` ➔ [เจาะโปรไฟล์ ↗️]({ig_url})")
                    st.markdown("<hr style='border-color: #1F2937; margin: 5px 0;'>", unsafe_allow_html=True)
                    
            with tab3:
                st.markdown("<span style='color: #6B7280;'>// แสดงรายชื่อเป้าหมายการดักรับข้อมูลบนเครือข่าย X (Twitter)</span>", unsafe_allow_html=True)
                for name in ai_variants:
                    x_search_url = f"[https://x.com/search?q=](https://x.com/search?q=){urllib.parse.quote(name)}"
                    st.markdown(f"🔹 **[ 🐦 X TWITTER ]** ➔ `{name}` ➔ [ดักข้อมูลโครงข่าย ↗️]({x_search_url})")
                    st.markdown("<hr style='border-color: #1F2937; margin: 5px 0;'>", unsafe_allow_html=True)

            st.success("🎯 [COMPLETED] ระบบประมวลผลการจำลองพฤติกรรมเสร็จสิ้น นวัตกรรมนี้รันบนโครงข่าย Google Gemini API ฟรี 100% พร้อมสำหรับการนำเสนอผลงานเชิงลึก")
