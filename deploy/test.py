import pandas as pd


def calcualte_earnings(LP_702_co, LP_702_no, thu_lai_702, LP_thu_lai_702, mark_704, LP_704_co, LP_704_no, thu_lai_704, LP_thu_lai_704):
    result = LP_702_co - LP_702_no
    for i in range(len(thu_lai_702)):
        if (thu_lai_702[i][0] == '-'):
            result = result - LP_thu_lai_702[i]
        else:
            result = result + LP_thu_lai_702[i]

    if(mark_704[0] == '-'):
        result = result - LP_704_co
    else:
        result = result + LP_704_co
    result = result - LP_704_no

    for j in range(len(thu_lai_704)):
        if (thu_lai_704[j][0] == '-'):
            result = result - LP_thu_lai_704[j]
        else:
            result = result + LP_thu_lai_704[j]
    
    return result

len26_empty = [''] * 26
len8_empty = [''] * 8
len18_empty = [''] * 18
tong_thue  = 20122061
number_EV = 42906634
chenh_lech = tong_thue - number_EV

thu_lai_702 = ['- 702016', '+ 790005', '+ 790006', '+ 711026', '- 711052', '+ 719009']
LP_thu_lai_702 = [0, 0, 0, 0, 50000, 11583750]
DN_thu_lai_702 = [0, 0, 0, 0, 0, 7152200]
mark_704 = '+ 704'
thu_lai_704 = ['+ 714009', '- 702010']
LP_thu_lai_704 = [437504, 2359318821]
DN_thu_lai_704 = [4126380, 0]

D_col = ['TONG THUE', tong_thue, 'EV', number_EV, 'CHENH LECH', chenh_lech, '', '', 702, ''] + thu_lai_702 + ['704', ''] +  thu_lai_704 + ['', '', '', '', '', '']
l104 = 1831549
subtraction_chenhlech_l104 = chenh_lech - l104
E_col = ['', '', '', '', '', l104, subtraction_chenhlech_l104, '', 'Có', 'Nợ', '', '', '', '', '', '', 'Có', 'Nợ'] + len8_empty

LP = 24667832
LP_702_co = 6932177284
LP_702_no = 10609130
LP_704_co = 35971036
LP_704_no = 0
LP_result = calcualte_earnings(LP_702_co, LP_702_no, thu_lai_702, LP_thu_lai_702, mark_704, LP_704_co, LP_704_no, thu_lai_704, LP_thu_lai_704)
F_col = ['LP (453101)(cuối kỳ)', LP, '', '', 'LAP THEM', '', '', '', LP_702_co, LP_702_no] + LP_thu_lai_702 + [LP_704_co, LP_704_no] + LP_thu_lai_704 + [LP_result] + [2985868391, '', '', '', '']

DN = 20122061
DN_702_co = 1830497534
DN_702_no = 5133223
DN_704_co = 0
DN_704_no = 0
DN_result = calcualte_earnings(DN_702_co, DN_702_no, thu_lai_702, DN_thu_lai_702, mark_704, DN_704_co, DN_704_no, thu_lai_704, DN_thu_lai_704)
# G_col = ['DN', DN, '', '', '', '', '', '', DN_702_co, DN_702_no] + DN_thu_lai_702 + [DN_704_co, DN_704_no] + DN_thu_lai_704 + [DN_result] + [3089317721, '', '', '', '']

# H_col = len18_empty + [(LP_thu_lai_704[0] + DN_thu_lai_704[0]), '', (LP_result + DN_result), 6432754649, '', '', (LP_result + DN_result - 6432754649), (LP_result + DN_result - 6432754649 - 0)]

# I_col = len18_empty + ['', '', 'TONG', 'EV', 7603, 7614, 'LAP THEM', '']

print(LP_result)
print(DN_result)

# data = {
#     'A': ['CÂN ĐỐI THÁNG TRƯỚC DỒN TÍCH', '', '', '', '', '', '', '', '', '', 'Thu lãi ĐCV', 'Thu lãi nợ ngắn hạn đã XLRR', 'Thu lãi nợ trung hạn đã XLRR', 'Phí thường niên thẻ TD (glcb06 lấy mã 1000)', '', '', 'Thu từ ng.vụ BL', '', '', 'TN bán vốn', '', '', '', '', '', ''],
#     'B': len26_empty,
#     'C': len26_empty,
#     'D': D_col,
#     'E': E_col,
#     'F': F_col,
#     'G': G_col,
#     'H': H_col,
#     'I': I_col
# }


# for key in data.keys():
#     print(len(data[key]))