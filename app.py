import streamlit as st
import docx
import google.generativeai as genai
import PyPDF2 # Thư viện hỗ trợ đọc PDF

# ==========================================
# CẤU HÌNH GIAO DIỆN & CSS HỒNG PASTEL
# ==========================================
st.set_page_config(page_title="Hệ thống Giáo án AI", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    h1, h2, h3 { color: #F48FB1 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 500; text-align: center; }
    .stButton>button { background-color: #FCE4EC !important; color: #C2185B !important; border: 1px solid #F8BBD0 !important; border-radius: 8px !important; padding: 12px 24px; font-weight: 600 !important; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #F8BBD0 !important; color: #880E4F !important; }
    [data-testid="stFileUploadDropzone"] { background-color: #FCFDFD; border: 1.5px dashed #F8BBD0; border-radius: 10px; }
    .subtext { text-align: center; color: #9E9E9E; font-size: 14px; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

# HÀM XỬ LÝ ĐỌC NHIỀU LOẠI FILE
def doc_noi_dung_file(uploaded_file):
    noi_dung = ""
    # Nếu là Word
    if uploaded_file.name.endswith('.docx'):
        doc = docx.Document(uploaded_file)
        noi_dung = '\n'.join([para.text for para in doc.paragraphs])
    # Nếu là PDF
    elif uploaded_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            noi_dung += page.extract_text() + "\n"
    # Nếu là Text
    elif uploaded_file.name.endswith('.txt'):
        noi_dung = uploaded_file.getvalue().decode("utf-8")
    return noi_dung

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.markdown("<h1>TÍCH HỢP NĂNG LỰC SỐ & AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Hệ thống tự động phân tích và lồng ghép chuẩn công nghệ vào Kế hoạch bài dạy<br>Hỗ trợ: .docx, .pdf, .txt</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mon_hoc = st.text_input("Môn học (VD: Toán, Ngữ văn)")
with col2:
    lop_hoc = st.text_input("Lớp học (VD: 9)")

# Cập nhật loại file cho phép tải lên
uploaded_file = st.file_uploader("Tải lên Kế hoạch bài dạy (Word, PDF, hoặc Text)", type=["docx", "pdf", "txt"])

document_text = ""
if uploaded_file is not None:
    with st.spinner('Đang đọc nội dung file...'):
        document_text = doc_noi_dung_file(uploaded_file)
        st.success(f"Đã đọc xong: {uploaded_file.name}")

st.write("") 
if st.button("Bắt Đầu Tích Hợp", use_container_width=True):
    if not document_text:
        st.error("Vui lòng tải tệp giáo án lên hệ thống.")
    else:
        with st.spinner('Trí tuệ nhân tạo đang phân tích và tái cấu trúc nội dung...'):
            try:
                # LẤY KHÓA TỪ KÉT SẮT CỦA STREAMLIT
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt_instructions = f"""
                Bạn là chuyên gia sư phạm và công nghệ giáo dục. Hãy nâng cấp Kế hoạch bài dạy môn {mon_hoc} lớp {lop_hoc} dưới đây bằng cách lồng ghép các hoạt động phát triển Năng lực số và Năng lực AI theo chuẩn Thông tư 02/2025/TT-BGDĐT và Công văn 3456/BGDĐT.
                
                QUY TẮC TÍCH HỢP:
                1. Năng lực số (Gợi ý theo môn):
                   - Toán: GeoGebra, vẽ hình, phần mềm mô phỏng.
                   - Ngữ văn: Padlet, Google Docs, PowerPoint.
                   - KHTN: PhET, Labster (thí nghiệm ảo).
                   - Tiếng Anh: Quizizz, Kahoot, Duolingo, Blooket.
                   - Các môn khác: Khai thác thông tin Internet, làm việc nhóm Online.
                
                2. Năng lực AI:
                   - Dùng AI làm công cụ hỗ trợ tìm ý tưởng, giải thích khái niệm.
                   - Giáo dục đạo đức AI.
                
                GIÁO ÁN GỐC:
                {document_text}
                
                YÊU CẦU TRÌNH BÀY (BẮT BUỘC):
                - Giữ nguyên toàn bộ cấu trúc gốc.
                - CHỈ BÔI ĐỎ bằng thẻ HTML: <span style="color:red; font-weight:bold;">[Nội dung tích hợp]</span>
                """
                
                response = model.generate_content(prompt_instructions)
                
                st.markdown("---")
                st.markdown("<h2>KẾT QUẢ GIÁO ÁN ĐÃ TÍCH HỢP</h2>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(response.text, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error("Hệ thống chưa tìm thấy mã API. Vui lòng cài đặt trong phần Secrets!")