import streamlit as st
import docx
import google.generativeai as genai
import PyPDF2

# ==========================================
# CẤU HÌNH GIAO DIỆN & BẢO MẬT BẢN QUYỀN
# ==========================================
st.set_page_config(page_title="Hệ Sinh Thái AI Giáo Án", page_icon="🏫", layout="wide")

AUTHORIZED_USER = "SonTuyen" 
SECRET_PASSWORD = "123"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #2e6c80;'>🔒 HỆ THỐNG NÂNG CẤP GIÁO ÁN AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Bản quyền phát triển bởi Sơn Tuyền</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            username = st.text_input("👤 Tên đăng nhập")
            password = st.text_input("🔑 Mật khẩu", type="password")
            if st.button("Đăng nhập hệ thống", type="primary", use_container_width=True):
                if username == AUTHORIZED_USER and password == SECRET_PASSWORD:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("🚫 Thông tin đăng nhập không chính xác!")
    st.stop()

# ==========================================
# HÀM XỬ LÝ DỮ LIỆU FILE
# ==========================================
def doc_noi_dung_file(files):
    van_ban = ""
    for file in files:
        if file.name.endswith('.docx'):
            doc = docx.Document(file)
            van_ban += '\n'.join([para.text for para in doc.paragraphs]) + "\n\n"
        elif file.name.endswith('.pdf'):
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    if page.extract_text():
                        van_ban += page.extract_text() + "\n"
            except:
                pass
        elif file.name.endswith('.txt'):
            van_ban += file.getvalue().decode("utf-8") + "\n\n"
    return van_ban

# ==========================================
# GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
# ==========================================
# --- THANH CÔNG CỤ BÊN TRÁI (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3145/3145765.png", width=100)
    st.success(f"👨‍🏫 Chào mừng, **{AUTHORIZED_USER}**")
    st.markdown("---")
    st.markdown("### ⚙️ Cài đặt Hệ thống")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", help="Lấy khóa tại aistudio.google.com")
    
    st.markdown("---")
    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

# --- KHU VỰC LÀM VIỆC CHÍNH ---
st.markdown("<h2 style='color: #1f77b4;'>🚀 CÔNG CỤ TÍCH HỢP NĂNG LỰC SỐ & AI VÀO KẾ HOẠCH BÀI DẠY</h2>", unsafe_allow_html=True)
st.markdown("*Biến giáo án truyền thống thành bài giảng hiện đại chỉ với vài cú click chuột.*")

# Chia giao diện thành 3 Thẻ (Tabs) mang lại cảm giác ứng dụng chuyên nghiệp
tab1, tab2, tab3 = st.tabs(["📚 BƯỚC 1: TÀI LIỆU CHUẨN", "📝 BƯỚC 2: TẢI GIÁO ÁN GỐC", "✨ BƯỚC 3: XỬ LÝ & KẾT QUẢ"])

with tab1:
    st.info("💡 Tải lên các văn bản chỉ đạo, định nghĩa hoặc tài liệu tập huấn. Bạn có thể chọn nhiều file cùng lúc.")
    col_a, col_b = st.columns(2)
    with col_a:
        file_so = st.file_uploader("📂 Tệp Tài liệu Năng lực số (.pdf, .docx)", type=["docx", "pdf", "txt"], accept_multiple_files=True, key="so")
    with col_b:
        file_ai = st.file_uploader("🤖 Tệp Tài liệu Năng lực AI (.pdf, .docx)", type=["docx", "pdf", "txt"], accept_multiple_files=True, key="ai")
    
    tai_lieu_so = doc_noi_dung_file(file_so) if file_so else ""
    tai_lieu_ai = doc_noi_dung_file(file_ai) if file_ai else ""

with tab2:
    st.markdown("### 📌 Thông tin bài giảng")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        mon_hoc = st.text_input("Môn học (Ví dụ: Toán, Tin học...)")
    with col_info2:
        lop_hoc = st.text_input("Lớp (Ví dụ: Lớp 9)")
        
    st.markdown("### 📥 Tải tệp Kế hoạch bài dạy")
    uploaded_file = st.file_uploader("Chọn file giáo án (.docx)", type=["docx"], key="giaoan")
    document_text = ""
    if uploaded_file is not None:
        doc = docx.Document(uploaded_file)
        document_text = '\n'.join([para.text for para in doc.paragraphs])
        st.success(f"✅ Đã tải và đọc thành công giáo án: {uploaded_file.name}")

with tab3:
    st.markdown("### ⚙️ Trí tuệ nhân tạo thực thi")
    if st.button("🚀 KÍCH HOẠT NÂNG CẤP GIÁO ÁN", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh công cụ bên trái!")
        elif not tai_lieu_so or not tai_lieu_ai:
            st.error("⚠️ Vui lòng tải lên tài liệu ở Bước 1.")
        elif not document_text:
            st.error("⚠️ Vui lòng tải giáo án gốc ở Bước 2.")
        else:
            with st.spinner('🤖 AI đang phân tích dữ liệu và lồng ghép các hoạt động. Quá trình này mất khoảng 20-30 giây...'):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt_instructions = f"""
                    Bạn là một chuyên gia thiết kế Kế hoạch bài dạy (EdTech). 
                    Hãy lồng ghép các hoạt động phát triển Năng lực số và Năng lực AI vào giáo án môn {mon_hoc} lớp {lop_hoc} dưới đây.
                    
                    TÀI LIỆU CHUẨN ĐỂ ĐỐI CHIẾU:
                    1. Năng lực số: {tai_lieu_so}
                    2. Năng lực AI: {tai_lieu_ai}
                    
                    GIÁO ÁN GỐC:
                    {document_text}
                    
                    YÊU CẦU ĐẦU RA BẮT BUỘC:
                    - Giữ nguyên toàn bộ nội dung giáo án cũ (chữ thường).
                    - BẤT KỲ ĐOẠN NÀO ĐƯỢC THÊM VÀO ĐỂ ĐÁP ỨNG CÔNG NGHỆ, phải bọc trong thẻ HTML: <span style="color:red; font-weight:bold; background-color:#ffe6e6; padding:2px; border-radius:3px;">nội dung mới</span>
                    - Tuyệt đối không dùng markdown (**) để in đậm phần thêm mới.
                    """
                    
                    response = model.generate_content(prompt_instructions)
                    result_text = response.text
                    
                    st.balloons()
                    st.success("🎉 Xử lý hoàn tất! Xem kết quả bên dưới.")
                    
                    with st.expander("👁️ XEM TRƯỚC GIÁO ÁN ĐÃ TÍCH HỢP", expanded=True):
                        st.markdown(result_text, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi hệ thống: {e}")