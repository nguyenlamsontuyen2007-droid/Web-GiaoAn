import streamlit as st
import docx
import PyPDF2
import google.generativeai as genai
import time

# ==========================================
# CẤU HÌNH TRANG CHỦ & ÉP CSS GIAO DIỆN
# ==========================================
st.set_page_config(page_title="Giáo viên Đổi mới - Công Cụ", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Reset font và khoảng cách mặc định của Streamlit */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding: 0rem !important; max-width: 100%;}
    
    /* 1. THANH MENU (NAVBAR) */
    .navbar { display: flex; justify-content: space-between; align-items: center; padding: 15px 50px; background-color: white; border-bottom: 1px solid #eaeaea; }
    .nav-logo { font-size: 24px; font-weight: 800; color: #6b5ce7; }
    .nav-buttons { display: flex; gap: 12px; }
    .btn-nav { padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; text-decoration: none; color: white; border: none; cursor: pointer;}
    .btn-ai { background-color: #00b894; }
    .btn-tienich { background-color: #00cec9; }
    .btn-thamgia { background-color: #2ecc71; }
    .btn-login { background-color: #6c5ce7; }
    
    /* 2. KHỐI HERO (BANNER TO MÀU XANH TÍM) */
    .hero { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; text-align: center; padding: 80px 20px; }
    .hero h1 { font-size: 46px; font-weight: 800; margin-bottom: 10px; color: white !important; font-family: 'Inter', sans-serif;}
    .hero h3 { font-size: 22px; font-weight: 600; margin-bottom: 15px; color: white !important;}
    .hero p { font-size: 16px; margin-bottom: 35px; opacity: 0.9; color: white !important;}
    .hero-btns { display: flex; justify-content: center; gap: 20px; }
    .btn-hero-white { background-color: white; color: #6c5ce7; padding: 14px 28px; border-radius: 30px; font-weight: 700; border: none; font-size: 16px; cursor: pointer;}
    .btn-hero-green { background-color: #2ecc71; color: white; padding: 14px 28px; border-radius: 30px; font-weight: 700; border: none; font-size: 16px; cursor: pointer;}
    
    /* 3. KHU VỰC CÔNG CỤ AI BÊN DƯỚI */
    .app-section { padding: 50px 10%; background-color: #f8f9fa; }
    .stButton>button { background-color: #6c5ce7 !important; color: white !important; border-radius: 8px !important; font-weight: bold !important; padding: 12px 24px; border: none; width: 100%; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #5b4bc4 !important; }
    [data-testid="stFileUploadDropzone"] { background-color: #FFFFFF; border: 2px dashed #6c5ce7; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# VẼ GIAO DIỆN TRANG CHỦ BẰNG HTML
# ==========================================
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Giáo viên Đổi mới</div>
    <div class="nav-buttons">
        <button class="btn-nav btn-ai">✨ Công cụ AI</button>
        <button class="btn-nav btn-tienich">🧩 Tiện ích GD</button>
        <button class="btn-nav btn-thamgia">🎮 Tham gia (dành cho học sinh)</button>
        <button class="btn-nav btn-login">Đăng nhập</button>
    </div>
</div>

<div class="hero">
    <h1>Giáo viên Đổi mới</h1>
    <h3>Trò chơi dạy học, công cụ AI và hơn thế nữa</h3>
    <p>Nền tảng dành cho giáo viên công nghệ, cung cấp các công cụ dạy học thông minh để tối ưu hóa việc giảng dạy</p>
    <div class="hero-btns">
        <button class="btn-hero-white">Đăng nhập ngay - Không cần đăng ký!</button>
        <button class="btn-hero-green">🎮 Tham gia (dành cho học sinh)</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HÀM ĐỌC FILE ---
def doc_noi_dung_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            text = '\n'.join([para.text for para in doc.paragraphs])
        elif uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.getvalue().decode("utf-8")
    except Exception:
        pass
    return text

# ==========================================
# KHU VỰC TÍCH HỢP AI NẰM BÊN DƯỚI KHỐI HERO
# ==========================================
st.markdown("<div class='app-section'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#6c5ce7; margin-bottom: 30px;'>Khu Vực Làm Việc: Tích Hợp Năng Lực Số Bằng AI</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 📝 Cài đặt bài dạy")
    bo_sach = st.selectbox("📚 Bộ sách:", ["Kết nối tri thức", "Chân trời sáng tạo", "Cánh diều", "Khác"])
    mon_hoc = st.text_input("Môn học (VD: Toán, Văn):")
    lop_hoc = st.text_input("Lớp (VD: 9):")
    
    st.markdown("### 📂 Tải tài liệu")
    uploaded_file = st.file_uploader("Kéo thả Word/PDF vào đây", type=["docx", "pdf", "txt"])
    
    doc_text = ""
    if uploaded_file:
        doc_text = doc_noi_dung_file(uploaded_file)
        st.success(f"Đã nạp tệp: {uploaded_file.name}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("🚀 BẮT ĐẦU XỬ LÝ AI")

with col2:
    st.markdown("### 🎯 Kết Quả")
    if submit_btn:
        if not uploaded_file or not mon_hoc:
            st.warning("Vui lòng nhập tên môn và tải file lên!")
        else:
            with st.spinner("AI đang tái cấu trúc giáo án..."):
                try:
                    # MÃ API CỦA CHỊ ĐÃ NẰM Ở ĐÂY
                    api_key = "AQ.Ab8RN6Jp15D-9J2mAdBD4jd2zzgML76nOYtWEDtlhXtYvZ5xFg"
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Nâng cấp Giáo án môn {mon_hoc} lớp {lop_hoc} (Bộ: {bo_sach}). 
                    Lồng ghép Năng lực số và AI theo chuẩn. Giữ nguyên toàn bộ bài gốc.
                    Chỉ bôi đỏ các phần THÊM MỚI bằng thẻ HTML: <span style="color:red; font-weight:bold;">[nội dung]</span>
                    
                    NỘI DUNG GỐC:
                    {doc_text}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("<div style='background: white; padding: 20px; border-radius: 8px; border: 1px solid #ccc; max-height: 500px; overflow-y: auto;'>", unsafe_allow_html=True)
                    st.markdown(response.text, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error("Lỗi khóa API. Vui lòng kiểm tra lại mã.")
    else:
        st.info("Kết quả tích hợp của AI sẽ hiện ở đây.")

st.markdown("</div>", unsafe_allow_html=True) # Kết thúc div khối công cụ