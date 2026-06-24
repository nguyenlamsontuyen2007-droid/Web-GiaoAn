import streamlit as st
import docx
import google.generativeai as genai

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

# ==========================================
# GIAO DIỆN CHÍNH (ĐÃ BỎ THANH SIDEBAR)
# ==========================================
st.markdown("<h1>TÍCH HỢP NĂNG LỰC SỐ & AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Hệ thống tự động phân tích và lồng ghép chuẩn công nghệ vào Kế hoạch bài dạy<br>Phát triển bởi Nguyễn Lâm Sơn Tuyền</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mon_hoc = st.text_input("Môn học (VD: Toán, Ngữ văn)")
with col2:
    lop_hoc = st.text_input("Lớp học (VD: 9)")

uploaded_file = st.file_uploader("Tải lên Kế hoạch bài dạy (.docx)", type=["docx"])

document_text = ""
if uploaded_file is not None:
    doc = docx.Document(uploaded_file)
    document_text = '\n'.join([para.text for para in doc.paragraphs])
    st.success("Tải tệp thành công. Sẵn sàng xử lý!")

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
                   - Ngữ văn: Padlet, Google Docs (làm việc nhóm), PowerPoint.
                   - KHTN: PhET, Labster (thí nghiệm ảo), ứng dụng đo lường.
                   - Tiếng Anh: Quizizz, Kahoot, Duolingo, Blooket.
                   - Lịch sử/Địa lý: Google Earth, Google Maps, bảo tàng ảo 3D.
                   - Công nghệ: Tinkercad, thiết kế 3D.
                   - Kỹ năng chung: Khai thác thông tin, đánh giá độ tin cậy của dữ liệu trên Internet.
                
                2. Năng lực AI:
                   - Dùng AI (ChatGPT, Gemini) làm công cụ hỗ trợ tìm kiếm ý tưởng, giải thích khái niệm.
                   - Hướng dẫn học sinh nhận diện thông tin do AI tạo ra, kiểm chứng kết quả.
                   - Giáo dục đạo đức: Không dùng AI để gian lận.
                
                GIÁO ÁN GỐC:
                {document_text}
                
                YÊU CẦU TRÌNH BÀY (BẮT BUỘC):
                - Giữ nguyên toàn bộ cấu trúc, tiến trình và nội dung gốc của giáo án (chữ màu đen bình thường).
                - CHỈ BÔI ĐỎ những câu từ, hoạt động mà bạn VỪA THÊM VÀO bằng thẻ HTML sau: <span style="color:red; font-weight:bold;">[Nội dung tích hợp]</span>
                - Tuyệt đối không dùng dấu sao (**) để in đậm cho phần thêm mới.
                """
                
                response = model.generate_content(prompt_instructions)
                
                st.markdown("---")
                st.markdown("<h2>KẾT QUẢ GIÁO ÁN ĐĐ TÍCH HỢP</h2>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(response.text, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error("Hệ thống chưa tìm thấy mã API. Vui lòng cài đặt trong phần Secrets!")