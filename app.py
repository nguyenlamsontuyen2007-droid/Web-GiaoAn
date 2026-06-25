import streamlit as st
import docx
import PyPDF2
import google.generativeai as genai

# ==========================================
# GIAO DIỆN HỒNG PASTEL - TỐI GIẢN & SANG TRỌNG
# ==========================================
st.set_page_config(page_title="Tích hợp NLS & AI - Sơn Tuyền", layout="centered")

st.markdown("""
<style>
    /* Reset và thiết lập tông màu chủ đạo */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    
    /* Ẩn các thành phần mặc định để web sạch sẽ */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Tiêu đề sang trọng */
    .main-title { color: #D885A3; font-weight: 700; font-size: 28px; text-align: center; margin-bottom: 5px; letter-spacing: 1px; text-transform: uppercase; }
    .sub-title { color: #A9A9A9; font-size: 14px; text-align: center; margin-bottom: 40px; font-weight: 300; }
    
    /* Nút bấm tinh tế */
    .stButton>button { background-color: #F8C8D6 !important; color: #FFFFFF !important; border-radius: 25px !important; font-weight: 600 !important; font-size: 15px !important; padding: 12px 0px; border: none !important; width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(248, 200, 214, 0.3); }
    .stButton>button:hover { background-color: #F0A0B9 !important; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(240, 160, 185, 0.4); }
    
    /* Khu vực tải file thanh lịch */
    [data-testid="stFileUploadDropzone"] { background-color: #FFF5F8; border: 1.5px dashed #F8C8D6; border-radius: 15px; padding: 30px; transition: all 0.3s ease; }
    [data-testid="stFileUploadDropzone"]:hover { background-color: #FFF0F5; border-color: #F0A0B9; }
    
    /* Form nhập liệu */
    .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #F0E6EA; padding: 10px 15px; background-color: #FAFAFA; }
    .stTextInput>div>div>input:focus { border-color: #D885A3; box-shadow: 0 0 0 1px #D885A3; }
    
    /* Bản quyền */
    .copyright { text-align: center; color: #C0C0C0; font-size: 12px; margin-top: 60px; font-weight: 400; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HÀM XỬ LÝ ĐỌC ĐA ĐỊNH DẠNG TÀI LIỆU
# ==========================================
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
# CẤU TRÚC GIAO DIỆN
# ==========================================
st.markdown("<div class='main-title'>TÍCH HỢP NĂNG LỰC SỐ & AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Hệ thống tự động tái cấu trúc Kế hoạch bài dạy theo chuẩn Bộ GD&ĐT</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mon_hoc = st.text_input("Môn học (VD: Toán, Ngữ văn)")
with col2:
    lop_hoc = st.text_input("Lớp học (VD: 9)")

uploaded_file = st.file_uploader("Tải lên Kế hoạch bài dạy (Word, PDF, Text)", type=["docx", "pdf", "txt"])

doc_text = ""
if uploaded_file:
    doc_text = doc_noi_dung_file(uploaded_file)
    st.success(f"Đã nạp tài liệu: {uploaded_file.name}")

st.write("")
submit_btn = st.button("BẮT ĐẦU TÍCH HỢP")

# ==========================================
# XỬ LÝ AI VỚI PROMPT ĐƯỢC HUẤN LUYỆN TỪ 7 TÀI LIỆU CỦA BẠN
# ==========================================
if submit_btn:
    if not doc_text:
        st.warning("Vui lòng tải một tệp giáo án lên hệ thống.")
    elif not mon_hoc or not lop_hoc:
        st.warning("Vui lòng điền Môn học và Lớp học.")
    else:
        with st.spinner("Hệ thống đang phân tích và đối chiếu với Thông tư 02 & CV 3456..."):
            try:
                # CHÌA KHÓA API CỦA BẠN ĐƯỢC GIẤU KÍN Ở ĐÂY
                api_key = "AQ.Ab8RN6Jp15D-9J2mAdBD4jd2zzgML76nOYtWEDtlhXtYvZ5xFg"
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Bạn là một Chuyên gia Phát triển Chương trình và Công nghệ Giáo dục. 
                Nhiệm vụ: Nâng cấp Kế hoạch bài dạy môn {mon_hoc} lớp {lop_hoc} dựa trên các văn bản chỉ đạo khắt khe nhất:
                - Thông tư 02/2025/TT-BGDĐT (Khung năng lực số cho người học).
                - Công văn 3456/BGDĐT (Triển khai thực hiện khung năng lực số).
                - Các bộ mã hóa Năng lực số (TC1 cho lớp 6-7, TC2 cho lớp 8-9).
                
                YÊU CẦU TÍCH HỢP CHUYÊN MÔN:
                1. Dựa trên 5 thành phần Năng lực số (Thông tin & dữ liệu, Giao tiếp & hợp tác, Tạo lập nội dung số, Bảo vệ & an toàn, Môi trường số), hãy lồng ghép các hoạt động sử dụng thiết bị, phần mềm và học liệu số phù hợp với đặc thù môn {mon_hoc}.
                2. Tích hợp rõ ràng Năng lực AI: Yêu cầu học sinh hoặc giáo viên sử dụng các công cụ AI (ChatGPT, Gemini, v.v.) để tìm kiếm ý tưởng, kiểm chứng thông tin, hoặc hỗ trợ học tập, đồng thời nhắc nhở về đạo đức sử dụng AI.
                3. Đề xuất cụ thể tên phần mềm/công cụ số (VD: Padlet, GeoGebra, PhET, Quizizz, Canva...) vào ngay trong tiến trình hoạt động của giáo án.
                
                QUY TẮC TRÌNH BÀY (BẮT BUỘC):
                - Giữ nguyên 100% cấu trúc, đề mục và nội dung cốt lõi của giáo án gốc.
                - Chỉ thêm thắt các bước/hoạt động tích hợp công nghệ.
                - TẤT CẢ những câu chữ, hoạt động do bạn VỪA THÊM VÀO phải được bôi màu hồng đậm bằng thẻ HTML: <span style="color:#D885A3; font-weight:bold;">[Nội dung tích hợp]</span>. Tuyệt đối không dùng dấu sao (**) để in đậm.
                
                NỘI DUNG GIÁO ÁN GỐC:
                {doc_text}
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("<h3 style='margin-top: 40px;'>Kết quả tích hợp</h3>", unsafe_allow_html=True)
                st.markdown("<div style='background-color: #FFFFFF; padding: 30px; border-radius: 15px; border: 1px solid #F0E6EA; box-shadow: 0 5px 15px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
                st.markdown(response.text, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Hệ thống AI đang quá tải hoặc khóa API gặp sự cố. Vui lòng thử lại sau.")

st.markdown("<div class='copyright'>© 2026 Phiên bản độc quyền • Bản quyền Sơn Tuyền</div>", unsafe_allow_html=True)