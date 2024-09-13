import streamlit as st
import pandas as pd
from io import BytesIO
import hashlib


USERNAME = "trang"
PASSWORD_HASH = "46db32ea0fc4ced928035124401df8625512638e9ba4f6fc4bc946bf6d3b764b"

if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'output_file' not in st.session_state:
    st.session_state.output_file = 'output.xlsx'
if 'output' not in st.session_state:
    st.session_state.output = None

# Hàm mã hóa mật khẩu nhập vào
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def extract_numbers(s):
    return ''.join(char for char in s if char.isdigit())

# Hàm đăng nhập
def login():
    st.sidebar.title("Đăng nhập")
    username = st.sidebar.text_input("Tên đăng nhập")
    password = st.sidebar.text_input("Mật khẩu", type="password")
    
    if st.sidebar.button("Đăng nhập"):
        password_hash = hash_password(password)
        if username == USERNAME and password_hash == PASSWORD_HASH:
            st.session_state.logged_in = True
            st.sidebar.success("Đăng nhập thành công!")
        else:
            st.sidebar.error("Tên đăng nhập hoặc mật khẩu không chính xác!")


if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    login()
else:
    st.title("Tìm giá trị trong file Excel")
    st.header("Upload files")

    # Upload các file nguồn và file đích
    src_file = st.file_uploader("Upload file nguồn", type=['xlsx', 'xls'])
    target_file = st.file_uploader("Upload file đích", type=['xlsx', 'xls'])

    if target_file is not None and src_file is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            target_sheet = st.text_input("Tên sheet của file đích", value='T07.24')
        with col2:
            src_col = st.text_input("Tên cột của file nguồn (A, B, C, ...)", value='B>J')  # Cột để tìm kiếm trong file nguồn
        with col3:
            target_col = st.text_input("Tên cột của file đích (A, B, C, ...)", value='D>G')  # Cột cần kiểm tra trong file đích

        # Tách giá trị cột nguồn và giá trị từ cột
        temp = src_col.split('>')
        src_col = temp[0]
        value_of_src_col = temp[1]
        temp = target_col.split('>')
        target_col = temp[0]
        value_of_target_col = temp[1]
        del temp

        # Các giá trị mặc định của nợ 702 và 704
        default_702_values = ['453101', '702', '- 702016', '+ 790005', '+ 790006', '+ 711026', '-711052', '+ 719009']
        default_704_values = ['+ 704', '+ 714009', '- 702010']

        # Nhập các giá trị cần tìm của nợ 702 và nợ 704
        user_input_702 = st.text_area("Nhập các giá trị cần tìm của nợ 702, mỗi giá trị trên một dòng", value="\n".join(default_702_values))
        user_input_704 = st.text_area("Nhập các giá trị cần tìm của nợ 704, mỗi giá trị trên một dòng", value="\n".join(default_704_values))

        if st.button("Tiến hành xử lý!"):
            # Đọc file đích với tất cả các sheet
            all_sheets = pd.read_excel(target_file, sheet_name=None)
            target_df = all_sheets[target_sheet]
            
            target_col_idx = ord(target_col.upper()) - ord('A')
            target_values = target_df.iloc[:, target_col_idx].tolist()

            # Lấy các giá trị tìm kiếm từ input người dùng
            search_values_702 = [line.strip() for line in user_input_702.split('\n') if line.strip()]
            search_values_704 = [line.strip() for line in user_input_704.split('\n') if line.strip()]
            search_values = search_values_702 + search_values_704

            # Làm sạch các giá trị để chỉ còn số
            filtered_values = [extract_numbers(value) for value in search_values if extract_numbers(value)]

            # Đọc file nguồn và lấy cột nguồn
            src_df = pd.read_excel(src_file)
            src_col_idx = ord(src_col.upper()) - ord('A')  # Chỉ số cột nguồn để tìm giá trị
            src_values = src_df.iloc[:, src_col_idx].tolist()
            src_values_cleaned = [str(int(value)) if isinstance(value, float) and value.is_integer() else str(value) for value in src_values]

            # Tìm vị trí của các giá trị trong file nguồn
            positions_in_src = []
            for value in filtered_values:
                position = [i+1 for i, v in enumerate(src_values_cleaned) if v == value]
                positions_in_src.append(position[0] if position else None)

            # Tìm vị trí của các giá trị trong file đích
            positions_in_target = []
            for value in filtered_values:
                position = [i+1 for i, v in enumerate(target_values) if extract_numbers(str(v)) == value]
                positions_in_target.append(position[0] if position else None)

            # Lấy giá trị từ cột J trong file nguồn
            src_col_j_idx = ord(value_of_src_col) - ord('A')  # Cột J trong file nguồn
            values_in_col_j = []
            for pos in positions_in_src:
                if pos is not None:
                    values_in_col_j.append(src_df.iloc[pos - 1, src_col_j_idx])  # Lấy giá trị tại cột J
                else:
                    values_in_col_j.append(None)

            # Cập nhật giá trị vào cột G trong file đích chỉ nếu có giá trị hợp lệ trong file nguồn
            target_col_g_idx = ord(value_of_target_col) - ord('A')  # Cột G trong file đích
            for i, pos in enumerate(positions_in_target):
                if positions_in_src[i] is not None:  # Chỉ cập nhật nếu có vị trí hợp lệ trong file nguồn
                    if pos is not None:
                        target_df.iloc[pos - 1, target_col_g_idx] = values_in_col_j[i]  # Gán giá trị từ file nguồn vào cột G

            # Lưu kết quả thành danh sách
            results = []
            for i, value in enumerate(filtered_values):
                result = {
                    'value': value,
                    'src_position': positions_in_src[i],
                    'target_position': positions_in_target[i],
                    'value_in_col_j': values_in_col_j[i]
                }
                results.append(result)
            
            # Hiển thị kết quả
            st.write("Kết quả tìm kiếm:")
            for result in results:
                src_info = f"Nguồn (hàng {result['src_position']}, giá trị cột J: {result['value_in_col_j']} )" if result['src_position'] else "Nguồn (không tìm thấy)"
                target_info = f"Đích (hàng {result['target_position']})" if result['target_position'] else "Đích (không tìm thấy)"
                st.write(f"Giá trị '{result['value']}': {src_info}, {target_info}")
            
            all_sheets[target_sheet] = target_df
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in all_sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            output.seek(0)
            st.session_state.processing_done = True
            st.session_state.output = output
        
        if st.session_state.processing_done:
            output_file = st.text_input("Nhập tên file để lưu kết quả", value=st.session_state.output_file)
            
            # Cập nhật session state với tên file nhập vào
            st.session_state.output_file = output_file
            
            # Tạo nút tải xuống nếu có tên file hợp lệ
            if output_file:
                st.download_button(
                    label="Tải file kết quả về",
                    data=st.session_state.output,
                    file_name=st.session_state.output_file,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )