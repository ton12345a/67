import streamlit as st
import itertools
import urllib.parse
import json

# ตรวจสอบการติดตั้งโมดูล Google GenAI
try:
    import google.generativeai as genai
except ImportError:
    st.error("กรุณาเพิ่ม 'google-generativeai' ลงในไฟล์ requirements.txt")

# ตั้งค่าหน้าเว็บให้สวยงามสไตล์ Cyber Investigation
st.set_page_config(page_title="AI-Powered OSINT Target Finder", page_icon="🕵️‍♂️", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 16px; color: #4B5563; text-align: center; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🕵️‍♂️ AI-Powered OSINT Target Finder (Gemini Edition)</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>ระบบใช้ Google Gemini AI วิเคราะห์แนวโน้มการตั้งชื่อและการย่อนามสกุลเพื่อสืบค้นโซเชียลมีเดีย (ใช้งานฟรี)</div>", unsafe_allow_html=True)

# แถบข้างสำหรับใส่ API Key 
with st.sidebar:
    st.header("🔑 การตั้งค่าระบบ AI หลังบ้าน")
    gemini_key = st.text_input("ระบุ Google Gemini API Key ของคุณ", type="password", help="จำเป็นต้องใช้เพื่อให้ Gemini ทำหน้าที่คิดและวิเคราะห์ชื่อผู้ใช้")
    st.markdown("[👉 คลิกที่นี่เพื่อเอา Gemini API Key ฟรี](https://aistudio.google.com/)")

# ฟังก์ชันส่งให้ Google Gemini คิดชื่อในรูปแบบต่างๆ
def ask_gemini_for_variants(first_name, last_name, api_key):
    try:
        # ตั้งค่าคีย์เชื่อมต่อกับ Google
        genai.configure(api_key=api_key)
        
        # เลือกใช้โมเดลระดับท็อปที่ประมวลผลเร็วและแม่นยำ
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        คุณคือผู้เชี่ยวชาญด้าน OSINT และจิตวิทยาพฤติกรรมมนุษย์บนอินเทอร์เน็ต 
        จงวิเคราะห์ชื่อภาษาไทย: "{first_name}" และนามสกุล: "{last_name}" 
        แล้วสร้างรายการ "ชื่อผู้ใช้ (Username)" หรือ "ชื่อโปรไฟล์" ภาษาอังกฤษที่คนๆ นี้มีแนวโน้มจะนำไปใช้ตั้งใน Facebook, Instagram, และ X (Twitter) 
        โดยคำนึงถึงพฤติกรรมจริงของคนไทย เช่น:
        1. การสะกดตรงตัวแบบต่างๆ (เช่น Chawee, Chawi)
        2. การใส่ชื่อเล่นเดาทาง (เช่น นำหน้าด้วย Mew, Mook, Benz, Ice, Tang)
        3. การย่อนามสกุล (เช่น brs, brm, ch)
        4. การใช้ตัวอักษรพิเศษและตัวเลขผสม (เช่น araya._brs, chawee.2026, chawi_ch)
        
        จงตอบกลับเป็นรูปแบบ JSON array ของข้อความเท่านั้น ห้ามมีคำอธิบายหรือเครื่องหมายมาร์กดาวน์ใดๆ ทั้งสิ้น ตัวอย่างผลลัพธ์:
        ["araya_brs", "Mook.araya", "araya.brm", "chawi_ch", "chawee.2026"]
        """
        
        response = model.generate_content(prompt)
        
        # คลีนข้อมูลกรณีเจอมาร์กดาวน์หุ้ม JSON
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
        st.error(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ Gemini AI: {str(e)}")
        return []

# ส่วนรับข้อมูลจากผู้ใช้งาน
col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("ชื่อเป้าหมาย (ภาษาไทย)", placeholder="เช่น อารยา, ชาวี")
with col2:
    last_name = st.text_input("นามสกุลเป้าหมาย (ภาษาไทย)", placeholder="เช่น บุรมศรี, สมาร์ท")

if st.button("🧠 สั่งการ Gemini AI สแกนหาเป้าหมาย", type="primary", use_container_width=True):
    if not gemini_key:
        st.error("⚠️ กรุณากรอก Gemini API Key ที่แถบด้านซ้ายก่อนใช้งานระบบ")
    elif not first_name:
        st.warning("⚠️ กรุณาระบุชื่อเป้าหมายอย่างน้อยหนึ่งชื่อ")
    else:
        with st.spinner("🤖 Google Gemini กำลังจำลองแนวคิดและสุ่มพฤติกรรมการตั้งชื่อของผู้ใช้..."):
            ai_variants = ask_gemini_for_variants(first_name, last_name, gemini_key)
            
        if ai_variants:
            st.subheader(f"📋 ผลลัพธ์คาดการณ์พฤติกรรมโดย Gemini AI ({len(ai_variants)} รูปแบบที่น่าจะเป็นที่สุด)")
            st.write(", ".join([f"**{v}**" for v in ai_variants]))
            
            st.divider()
            
            st.subheader("🌐 ช่องทางการเชื่อมโยงสืบค้นเชิงลึก (AI-Generated OSINT Targets)")
            tab1, tab2, tab3 = st.tabs(["Facebook Search Engine", "Instagram Profile Link", "X (Twitter) Intelligence"])
            
            with tab1:
                st.info("💡 ค้นหาบน Facebook ดึงข้อมูลจากคีย์เวิร์ดที่ผสมผสานโดย AI")
                for name in ai_variants:
                    fb_url = f"https://www.facebook.com/search/top/?q={urllib.parse.quote(name)}"
                    st.markdown(f"🔹 Target Alias: **{name}** -> [ค้นหาบน Facebook ↗️]({fb_url})")
                    
            with tab2:
                st.info("💡 ค้นหาบน IG ตรวจสอบโครงสร้างชื่อที่ใช้สัญลักษณ์พิเศษตามที่ AI จำลอง")
                for name in ai_variants:
                    clean_name = name.replace(" ", "")
                    ig_url = f"https://www.instagram.com/{clean_name}"
                    st.markdown(f"📸 IG Handle: **@{clean_name}** -> [สแกนโปรไฟล์ Instagram ↗️]({ig_url})")
                    
            with tab3:
                st.info("💡 ค้นหาบน X ทั้งในรูปแบบของทวีตและชื่อบัญชีผู้ใช้")
                for name in ai_variants:
                    x_search_url = f"https://x.com/search?q={urllib.parse.quote(name)}"
                    st.markdown(f"🐦 X Keyword: **{name}** -> [แกะรอยบน X (Twitter) ↗️]({x_search_url})")
                    
         st.success("🎯 **กลยุทธ์การส่งประกวด:** ระบบนี้เปลี่ยนมาขับเคลื่อนด้วย Google Gemini API (Free Tier) ช่วยให้โปรเจกต์รันได้ฟรี 100% ตอบโจทย์นวัตกรรมเพื่อสังคมที่เข้าถึงง่ายและไม่มีค่าใช้จ่ายแอบแฝง!")
