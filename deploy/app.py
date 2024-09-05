import streamlit as st
import pandas as pd

def extract_numbers(s):
    return ''.join(char for char in s if char.isdigit())

st.title("Tìm giá trị trong file Excel")
st.header("Upload files")

src_file = st.file_uploader("Upload file nguồn", type=['xlsx', 'xls'])
target_file = st.file_uploader("Upload file đích", type=['xlsx', 'xls'])

if target_file is not None and src_file is not None:
    col1, col2, col3 = st.columns(3)
    with col1:
        target_sheet = st.text_input("Tên sheet của file đích", value='T07.24')
    with col2:
        src_col = st.text_input("Tên cột của file nguồn (A, B, C, ...)", value='B')
    with col3:
        target_col = st.text_input("Tên cột của file đích (A, B, C, ...)", value='D')
    
    default_search_values = ['702', '', '- 702016', '+ 790005', '+ 790006', '+ 711026', '-711052', '+ 719009', '+ 704', '', '+ 714009', '- 702010']
    user_input = st.text_area("Nhập các giá trị cần tìm, mỗi giá trị trên một dòng", value="\n".join(default_search_values))

    target_df = pd.read_excel(target_file, sheet_name=target_sheet)
    target_col_idx = ord(target_col.upper()) - ord('A')
    target_values = target_df.iloc[:, target_col_idx].tolist()

    search_values = [line.strip() for line in user_input.split('\n') if line.strip()]
    filtered_values = [extract_numbers(value) for value in search_values if extract_numbers(value)]

    src_df = pd.read_excel(src_file)
    src_col_idx = ord(src_col.upper()) - ord('A')
    src_values = src_df.iloc[:, src_col_idx].tolist()
    src_values_cleaned = [str(int(value)) if isinstance(value, float) and value.is_integer() else str(value) for value in src_values]

    positions_in_src = []

    for value in filtered_values:
        # Tìm các vị trí của giá trị trong src_values_cleaned
        position = [i+1 for i, v in enumerate(src_values_cleaned) if v == value]
        # Nếu tìm thấy, thêm vị trí vào danh sách, nếu không thì thêm None
        positions_in_src.append(position[0] if position else None)

    # Hiển thị kết quả vị trí trong file nguồn
    st.write("Vị trí của các giá trị trong cột nguồn:")
    for i, value in enumerate(filtered_values):
        st.write(f"Giá trị '{value}': Hàng {positions_in_src[i]}")
