import streamlit as st
import docx
import PyPDF2
import google.generativeai as genai
import time

# ==========================================
# CẤU HÌNH GIAO DIỆN Y CHANG GIAOVIENDOIMOI
# ==========================================
st.set_page_config(page_title="Công cụ AI - Giáo viên đổi mới", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f2f5; }
    
    /* Ẩn các thành phần mặc định của nền tảng */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Khung chứa nội dung (Card) */
    .card { background-color: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.12); margin-bottom: 24px; }
    
    /* Tiêu đề */
    .main-title { color: #1a73e8; font-weight: 800; font-size: 32px; margin-bottom: 8px; }
    .sub-title { color: #5f6368; font-size: 16px; margin-bottom: 24px; }
    
    /* Nút bấm Kích hoạt */
    .stButton>button { background-color: #1a73e8 !important; color: white !important; border-radius: 8px !important; font-weight: 700 !important; padding: 14px 24px !important; border: none !important; width: 100% !important; transition: all 0.2s; }
    .stButton>button:hover { background-color: #1557b0 !important; box-shadow: 0 4px 6px rgba(32,33,36,0.28) !important; }
    
    /* Khu vực tải file */
    [data-testid="stFileUploadDropzone"] { border: 2px dashed #1a73e8; border-radius: 12px; background-color: #f8faff; padding: 30px; }
</style>
""", unsafe_allow_html=True)

# --- HÀM ĐỌC FILE TÀI LIỆU ---
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
# THANH MENU BÊN TRÁI (SIDEBAR TÀI KHOẢN)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #1a73e8; font-weight: 800; text-align: center;'>AI TOOLS HUB</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🛠️ Bộ công cụ AI")
    st.radio("Chọn chức năng:", ["📚 Giáo án tích hợp NLS", "📝 Tạo bài tập (Sắp ra mắt)", "📊 Làm Slide (Sắp ra mắt)"])
    st.markdown("---")
    st.success("💎 TÀI KHOẢN VIP (Miễn phí)")
    st.info("✔️ Không giới hạn lượt dùng\n\n✔️ Không cần nạp tiền\n\n✔️ Không cần API Key")

# ==========================================
# KHU VỰC LÀM VIỆC CHÍNH (MAIN WORKSPACE)
# ==========================================
st.markdown("<div class='main-title'>⚡ Xử lý Giáo án Tích hợp Năng Lực Số</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Hệ thống tự động đọc giáo án và lồng ghép chuẩn công nghệ theo tiêu chuẩn của Bộ Giáo Dục.</div>", unsafe_allow_html=True)

# Chia màn hình làm 2 cột
col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 1. Thông tin bài học")
    # Các trường thông tin giống hệt trang giaoviendoimoi
    bo_sach = st.selectbox("📚 Bộ sách giáo khoa:", ["Kết nối tri thức với cuộc sống", "Chân trời sáng tạo", "Cánh diều", "Khác"])
    mon_hoc = st.text_input("📝 Môn học:", placeholder="VD: Toán, Ngữ văn...")
    lop_hoc = st.selectbox("🎓 Lớp học:", [str(i) for i in range(1, 13)])
    
    st.markdown("### 2. Tài liệu đầu vào")
    uploaded_file = st.file_uploader("Tải lên giáo án (.docx, .pdf)", type=["docx", "pdf", "txt"])
    
    doc_text = ""
    if uploaded_file:
        doc_text = doc_noi_dung_file(uploaded_file)
        st.success(f"✅ Đã tải thành công: {uploaded_file.name}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("🚀 KÍCH HOẠT XỬ LÝ AI")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Kết quả hiển thị")
    
    if submit_btn:
        if not uploaded_file:
            st.warning("⚠️ Vui lòng tải tài liệu lên trước khi Kích hoạt.")
        elif not mon_hoc:
            st.warning("⚠️ Vui lòng nhập tên Môn học.")
        else:
            with st.spinner("🤖 Trí tuệ nhân tạo đang phân tích và tái cấu trúc giáo án..."):
                try:
                    # --- CHÌA KHÓA CỦA CHỊ ĐÃ ĐƯỢC GIẤU Ở ĐÂY ---
                    api_key = "AQ.Ab8RN6Jp15D-9J2mAdBD4jd2zzgML76nOYtWEDtlhXtYvZ5xFg"
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Nhiệm vụ: Nâng cấp Kế hoạch bài dạy môn {mon_hoc} lớp {lop_hoc} (Thuộc bộ sách: {bo_sach}).
                    Hãy lồng ghép các hoạt động phát triển Năng lực số và AI theo chuẩn Thông tư 02.
                    
                    QUY TẮC HIỂN THỊ:
                    1. Giữ nguyên 100% cấu trúc và nội dung gốc.
                    2. Tại vị trí nào bạn thêm hoạt động công nghệ vào, hãy bôi đỏ bằng thẻ: <span style="color:red; font-weight:bold;">[Nội dung tích hợp công nghệ]</span>
                    
                    NỘI DUNG GIÁO ÁN GỐC:
                    {doc_text}
                    """
                    
                    response = model.generate_content(prompt)
                    time.sleep(1) # Tạo cảm giác AI đang xử lý giống thật
                    
                    # Khung hiển thị kết quả có thanh cuộn chuyên nghiệp
                    st.markdown("<div style='height: 600px; overflow-y: auto; border: 1px solid #e0e0e0; padding: 25px; border-radius: 8px; background: #fff;'>", unsafe_allow_html=True)
                    st.markdown(response.text, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.success("🎉 Tích hợp thành công! Bạn có thể bôi đen copy đoạn trên dán vào Word.")
                except Exception as e:
                    # Đề phòng mã lỗi, hệ thống sẽ báo để chị biết đường thay mã mới
                    st.error("Lỗi xác thực: Mã API của bạn không hợp lệ hoặc đã hết hạn. Hãy tạo mã AIza... từ Google và thay vào code.")
    else:
        st.info("👆 Khi bạn bấm Kích hoạt, giáo án hoàn chỉnh sẽ xuất hiện tại đây.")
    st.markdown("</div>", unsafe_allow_html=True)