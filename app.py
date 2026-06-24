import streamlit as st
import docx
import google.generativeai as genai

# ==========================================
# CẤU HÌNH GIAO DIỆN & BẢO MẬT BẢN QUYỀN
# ==========================================
st.set_page_config(page_title="App Tích hợp AI Giáo án", page_icon="📚", layout="wide")

# Tên đăng nhập được thiết lập độc quyền cho bạn
AUTHORIZED_USER = "SonTuyen" 
SECRET_PASSWORD = "123"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

st.sidebar.title("🔒 Xác thực Bản quyền")

if not st.session_state['logged_in']:
    username = st.sidebar.text_input("Tên đăng nhập")
    password = st.sidebar.text_input("Mật khẩu", type="password")
    
    if st.sidebar.button("Đăng nhập", type="primary"):
        if username == AUTHORIZED_USER and password == SECRET_PASSWORD:
            st.session_state['logged_in'] = True
            st.sidebar.success(f"Xin chào {username}! Truy cập thành công.")
            st.rerun()
        else:
            st.sidebar.error("🚫 Truy cập bị từ chối! Sai tên đăng nhập hoặc mật khẩu.")
            st.stop()
else:
    st.sidebar.success(f"Đã đăng nhập dưới quyền: **{AUTHORIZED_USER}**")
    if st.sidebar.button("Đăng xuất"):
        st.session_state['logged_in'] = False
        st.rerun()

# ==========================================
# TÍNH NĂNG CHÍNH: TÍCH HỢP NĂNG LỰC SỐ & AI
# ==========================================
if st.session_state['logged_in']:
    st.title("📚 Công cụ Nâng cấp Giáo án (Bản quyền của Sơn Tuyền)")
    st.markdown("Hệ thống sử dụng Gemini AI. **Các nội dung tích hợp mới sẽ được bôi màu đỏ để dễ phân biệt.**")
    
    # 1. Nhập chìa khóa AI
    api_key = st.text_input("Nhập Gemini API Key của bạn (Lấy tại aistudio.google.com):", type="password")
    
    st.markdown("---")
    
    # 2. Nạp tài liệu làm kim chỉ nam cho AI
    st.subheader("Bước 1: Cung cấp Tài liệu Tham chiếu")
    st.info("Mở các file tài liệu tập huấn của bạn, copy những nội dung/định nghĩa quan trọng nhất và dán vào 2 ô dưới đây để AI có cơ sở làm việc.")
    
    col1, col2 = st.columns(2)
    with col1:
        tai_lieu_so = st.text_area("📋 Dán nội dung 'Tài liệu tập huấn Năng lực số' vào đây:", height=200)
    with col2:
        tai_lieu_ai = st.text_area("🤖 Dán nội dung 'Năng lực AI' vào đây:", height=200)
    
    st.markdown("---")
    
    # 3. Tải giáo án gốc
    st.subheader("Bước 2: Tải Giáo án gốc lên")
    uploaded_file = st.file_uploader("Chọn file giáo án của bạn (Định dạng .docx)", type=["docx"])

    if uploaded_file is not None:
        doc = docx.Document(uploaded_file)
        document_text = '\n'.join([para.text for para in doc.paragraphs])
        st.success("Đã đọc nội dung giáo án gốc thành công!")
        
        # 4. Thực thi AI
        if st.button("🚀 Bắt đầu Phân tích & Tích hợp", type="primary"):
            if not api_key:
                st.warning("Vui lòng nhập Gemini API Key ở phía trên!")
            elif not tai_lieu_so or not tai_lieu_ai:
                st.warning("Vui lòng dán nội dung tài liệu tham chiếu ở Bước 1 để AI biết cần tích hợp điều gì.")
            else:
                with st.spinner('AI đang đọc tài liệu và tiến hành nâng cấp giáo án. Vui lòng đợi...'):
                    try:
                        genai.configure(api_key=api_key)
                        # Sử dụng model flash để tốc độ phản hồi nhanh nhất
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt_instructions = f"""
                        Bạn là một chuyên gia công nghệ giáo dục (EdTech). 
                        Nhiệm vụ của bạn là viết lại giáo án gốc, lồng ghép thêm các hoạt động phát triển Năng lực số và Năng lực AI cho học sinh.
                        
                        CƠ SỞ LÝ LUẬN BẮT BUỘC PHẢI BÁM SÁT ĐỂ TÍCH HỢP:
                        1. Tài liệu Năng lực số: {tai_lieu_so}
                        2. Tài liệu Năng lực AI: {tai_lieu_ai}
                        
                        GIÁO ÁN GỐC:
                        {document_text}
                        
                        YÊU CẦU QUAN TRỌNG VỀ ĐỊNH DẠNG ĐẦU RA:
                        - Giữ nguyên cấu trúc, bố cục và nội dung cũ của giáo án gốc (chữ màu đen bình thường).
                        - BẤT KỲ CÂU HOẶC ĐOẠN VĂN NÀO BẠN THÊM VÀO HOẶC CHỈNH SỬA LẠI (để đáp ứng năng lực số và AI), BẮT BUỘC phải được bọc trong thẻ HTML sau để bôi đỏ: <span style="color:red; font-weight:bold;">nội dung thêm vào</span>
                        - Tuyệt đối không dùng dấu sao (**) để in đậm cho các phần màu đỏ, chỉ dùng thẻ HTML.
                        """
                        
                        response = model.generate_content(prompt_instructions)
                        result_text = response.text
                        
                        st.markdown("---")
                        st.subheader("💡 GIÁO ÁN MỚI ĐÃ ĐƯỢC TÍCH HỢP")
                        st.markdown("*(Lưu ý: Các phần chữ màu đỏ là các hoạt động Năng lực số / AI đã được AI chèn thêm vào bài)*")
                        
                        # unsafe_allow_html=True để trình duyệt hiểu được thẻ màu đỏ
                        st.markdown(result_text, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Đã xảy ra lỗi kết nối với Google: {e}")