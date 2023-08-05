

canGoc = ["GIÁP", "ẤT", "BÍNH", "ĐINH",
          "MẬU", "KỶ", "CANH", "TÂN", "NHÂM", "QUÝ"]
chiGoc = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ",
          "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI"]
chixung = ["NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT",
           "HỢI", "TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ"]
chubichihinh = ["MÃO", "TUẤT", "TỊ", "TÝ", "THÌN",
                "THÂN", "NGỌ", "SỬU", "DẦN", "DẬU", "MÙI", "HỢI"]
danhsach24tietkhi = ["Lập xuân",
                     "Vũ Thủy",
                     "Kinh trập",
                     "Xuân phân",
                     "Thanh minh",
                     "Cốc vũ",
                     "Lập hạ",
                     "Tiểu mãn",
                     "Mang chủng",
                     "Hạ chí",
                     "Tiểu thử",
                     "Đại thử",
                     "Lập thu",
                     "Xử thử",
                     "Bạch lộ",
                     "Thu phân",
                     "Hàn lộ",
                     "Sương giáng",
                     "Lập đông",
                     "Tiểu tuyết",
                     "Đại tuyết",
                     "Đông chí",
                     "Tiểu hàn",
                     "Đại hàn"]
nguyetTuong = ["TÝ", "HỢI", "HỢI", "TUẤT", "TUẤT", "DẬU", "DẬU", "THÂN", "THÂN", "MÙI", "MÙI",
               "NGỌ", "NGỌ", "TỊ", "TỊ", "THÌN", "THÌN", "MÃO", "MÃO", "DẦN", "DẦN", "SỬU", "SỬU", "TÝ"]
skth = [["H",   "H",    "TS",   "TS",   "BK",   "BK",   "K",
         "K",    "TS",   "TS",   "BK",   "BK", "n"],
        ["H",   "H",    "TS",   "TS",   "BK",   "BK",   "K",
         "K",    "TS",   "TS",   "BK",   "BK", "n"],
        ["TS",  "TS",   "H",    "H",    "TS",   "TS",   "BK",
         "BK",   "K",    "K",    "TS",   "TS", "n"],
        ["TS",  "TS",   "H",    "H",    "TS",   "TS",   "BK",
         "BK",   "K",    "K",    "TS",   "TS", "n"],
        ["K",   "K",    "TS",   "TS",   "H",    "H",    "TS",
         "TS",   "BK",   "BK",   "H",    "H", "n"],
        ["K",   "K",    "TS",   "TS",   "H",    "H",    "TS",
         "TS",   "BK",   "BK",   "H",    "H", "n"],
        ["BK",  "BK",   "K",    "K",    "TS",   "TS",   "H",
         "H",    "TS",   "TS",   "TS",   "TS", "n"],
        ["BK",  "BK",   "K",    "K",    "TS",   "TS",   "H",
         "H",    "TS",   "TS",   "TS",   "TS", "n"],
        ["TS",  "TS",   "BK",   "BK",   "K",    "K",    "TS",
         "TS",   "H",    "H",    "K",    "K", "n"],
        ["TS",  "TS",   "BK",   "BK",   "K",    "K",    "TS",
         "TS",   "H",    "H",    "K",    "K", "n"]

        ]
tukhoa = ["DẦN", "MÃO", "TỊ", "NGỌ", "THÌN", "TUẤT",
          "THÂN", "DẬU", "HỢI", "TÝ", "SỬU", "MÙI"]

# Lưu ý: Hoán thần, Hoán tướng để Hoán quẻ
# Khi xây dựng app, cần thiết đưa một selector để lựa chọn Can Chi, Nguyệt tướng sẽ POST đến API
# Hoặc có thể xây dựng thêm 1 function trong API, để nhận yêu cầu Hoán tướng, Hoán thần và từ đó Hoán theo sách


def ThienBan(tietKhi, chiGio):
    sttnguyetuong = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sttchigio = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    doicung = ["", "", "", "", "", "", "", "", "", "", "", ""]
    giatricung = ["", "", "", "", "", "", "", "", "", "", "", ""]
    thientuong = ["", "", "", "", "", "", "", "", "", "", "", ""]
    a = danhsach24tietkhi.index(tietKhi)
    nguyettuong = nguyetTuong[a]
    sttnguyetuong[0] = chiGoc.index(nguyettuong)
    sttchigio[0] = chiGoc.index(chiGio)
    for i in range(1, len(sttnguyetuong)):
        sttnguyetuong[i] = (sttnguyetuong[i - 1] + 1) % 12
    for i in range(1, len(sttchigio)):
        sttchigio[i] = (sttchigio[i - 1] + 1) % 12
    for i in range(len(doicung)):
        doicung[i] = chiGoc[sttchigio[i]]
    for i in range(len(giatricung)):
        giatricung[i] = chiGoc[sttnguyetuong[i]]
    for i in range(12):
        thientuong[i] = giatricung[doicung.index(chiGoc[i])]
    return thientuong


def AnCanChi(canNgay, chiNgay):

    ancan = [2, 4, 5, 7, 5, 7, 8, 10, 11, 1]
    can = ['', '', '', '', '', '', '', '', '', '', '', '']
    chi = ['', '', '', '', '', '', '', '', '', '', '', '']
    can[ancan[canGoc.index(canNgay)]] = 'CAN'
    chi[chiGoc.index(chiNgay)] = 'CHI'
    return [can, chi]


def AnNienMenh(chiNamSinh, tuoiXem, intGioi):
    anchi = ["", "", "", "", "", "", "", "", "", "", "", ""]
    anchi[chiGoc.index(chiNamSinh)] = "Bản mệnh"

    hanhNien = ["", "", "", "", "", "", "", "", "", "", "", ""]
    lnnam = (tuoiXem+1) % 12
    lnnu = (tuoiXem + 7) % 12
    if (intGioi == 1):
        hanhNien[lnnam] = "Hành niên"
    else:
        hanhNien[lnnu] = "Hành niên"

    return [anchi, hanhNien]


def AnTrachMo(chiNgay):
    t = [7, 6, 6, 0, 9, 3, 7, 6, 6, 0, 9, 3]
    m = [4, 10, 10, 4, 1, 7, 4, 10, 10, 4, 1, 7]
    trach = ["", "", "", "", "", "", "", "", "", "", "", ""]
    mo = ["", "", "", "", "", "", "", "", "", "", "", ""]
    trach[t[chiGoc.index(chiNgay)]] = 'Trạch'
    mo[m[chiGoc.index(chiNgay)]] = 'Mộ'
    return [trach, mo]


def CanKy(canngay):
    canky = ["DẦN", "THÌN", "TỊ", "MÙI", "TỊ",
             "MÙI", "THÂN", "TUẤT", "HỢI", "SỬU"]
    return canky[canGoc.index(canngay)]


def TenThienBan(thienBan):
    namet = ["Thân hậu", "Đại cát", "Công tào", "Thái xung", "Thiên cương", "Thái ất",
             "Thắng quang", "Tiểu cát", "Truyền tống", "Tòng khôi", "Hà khôi", "Đăng minh"]
    return namet[chiGoc.index(thienBan)]


def TuKhoaSinhKhac(tk1, tk2, tk3, tk4, dk1, dk2, dk3, dk4):
    ss = [["H", "K", "S", "S", "K", "T", "T", "K", "S", "S", "K", "H"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["S", "T", "H", "H", "T", "S", "S", "T", "K", "K", "T", "S"],
          ["S", "T", "H", "H", "T", "S", "S", "T", "K", "K", "T", "S"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["K", "S", "S", "S", "S", "H", "H", "S", "T", "T", "S", "K"],
          ["K", "S", "S", "S", "S", "H", "H", "S", "T", "T", "S", "K"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["S", "S", "T", "T", "S", "K", "K", "S", "H", "H", "S", "S"],
          ["S", "S", "T", "T", "S", "K", "K", "S", "H", "H", "S", "S"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["H", "K", "S", "S", "K", "T", "T", "K", "S", "S", "K", "H"],
          ["S", "T", "H", "H", "T", "S", "S", "T", "K", "K", "T", "S"],
          ["S", "T", "H", "H", "T", "S", "S", "T", "K", "K", "T", "S"],
          ["K", "S", "S", "S", "S", "H", "H", "S", "T", "T", "S", "K"],
          ["K", "S", "S", "S", "S", "H", "H", "S", "T", "T", "S", "K"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["T", "H", "K", "K", "H", "S", "S", "H", "S", "S", "H", "T"],
          ["S", "S", "T", "T", "S", "K", "K", "S", "H", "H", "S", "S"],
          ["S", "S", "T", "T", "S", "K", "K", "S", "H", "H", "S", "S"],
          ["H", "K", "S", "S", "K", "T", "T", "K", "S", "S", "K", "H"],
          ["H", "K", "S", "S", "K", "T", "T", "K", "S", "S", "K", "H"]]
    tren = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ",
            "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI"]
    duoi = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT",
            "HỢI", "GIÁP", "ẤT", "BÍNH", "ĐINH", "MẬU", "KỶ", "CANH", "TÂN", "NHÂM", "QUÝ"]
    v = ["T", "K", "S", "H"]
    s = ["Tặc", "Khắc", "Sinh", "Tỷ"]
    ketQua1 = s[v.index(ss[duoi.index(dk1)][tren.index(tk1)])]
    ketQua2 = s[v.index(ss[duoi.index(dk2)][tren.index(tk2)])]
    ketQua3 = s[v.index(ss[duoi.index(dk3)][tren.index(tk3)])]
    ketQua4 = s[v.index(ss[duoi.index(dk4)][tren.index(tk4)])]

    return [ketQua1, ketQua2, ketQua3, ketQua4]


def ThienBanTuKhoa(tietKhi, chiGio, canNgay, chiNgay):
    thienBan = ThienBan(tietKhi, chiGio)
    tenThienBan = []
    for i in range(12):
        tenThienBan.append(TenThienBan(thienBan[i]))
    DK1 = canNgay
    TK1 = thienBan[chiGoc.index(CanKy(canNgay))]
    DK2 = TK1
    TK2 = thienBan[chiGoc.index(TK1)]
    DK3 = chiNgay
    TK3 = thienBan[chiGoc.index(chiNgay)]
    DK4 = TK3
    TK4 = thienBan[chiGoc.index(TK3)]
    return [thienBan, tenThienBan, [TK1, DK1], [TK2, DK2], [TK3, DK3], [TK4, DK4], TuKhoaSinhKhac(TK1, TK2, TK3, TK4, DK1, DK2, DK3, DK4)]


def ThienTuongQuyNhan(chiGio, canNgay, chiNgay, tietKhi):
    qn = ["Quý nhân", "Đằng xà", "Chu tước", "Thiên hợp", "Câu trận", "Thanh long",
          "Thiên không", "Bạch hổ", "Thái thường", "Huyền vũ", "Thái âm", "Thiên hậu"]
    ngay = ["SỬU", "TÝ", "HỢI", "HỢI", "SỬU", "TÝ", "SỬU", "NGỌ", "TỊ", "TỊ"]
    dem = ["MÙI", "THÂN", "DẬU", "DẬU", "MÙI",
           "THÂN", "MÙI", "DẦN", "MÃO", "MÃO"]
    qnThuanNghich = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1]
    gioNgayDem = [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    # xem vào giờ ban ngày lấy ngay, đêm lấy dem theo Can ngày
    if gioNgayDem[chiGoc.index(chiGio)] == 1:
        cungQn = ngay[canGoc.index(canNgay)]
    else:
        cungQn = dem[canGoc.index(canNgay)]

    # Đã có Qúy nhân đi cùng sao Thiên bàn, biết nó ở Địa bàn nào, từ đó phân ra Thuận Nghịch và đưa các sao vào một list thứ tự
    thienBan = ThienBan(tietKhi, chiGio)
    b = thienBan.index(cungQn)
    thuanNghich = qnThuanNghich[b]
    s = []
    for i in range(12):
        s.append((b + 12 + i*thuanNghich) % 12)
    # Sắp xếp
    p = []
    for i in range(12):
        p.append(s.index(i))
    k = []
    for i in range(12):
        k.append(qn[p[i]])

    return k


# region PHẦN CHUẨN BỊ CHO AN TAM TRUYỀN
def ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay):
    m = ThienBanTuKhoa(tietKhi, chiGio, canNgay, chiNgay)
    khoaTK = m[6]

    sK = [0, 0, 0, 0]
    sT = [0, 0, 0, 0]
    for i in range(len(khoaTK)):
        if khoaTK[i] == 'Khắc':
            sK[i] = 1
        elif khoaTK[i] == 'Tặc':
            sT[i] = 1
    soKhoaTac = sum(sT)
    soKhoaKhac = sum(sK)
    sttpa = 0
    canchidongcung = 0
    phucngam = 0
    phanngam = 0
    if (soKhoaTac == 1):
        sttpa = 2  # 2 là Trùng thẩm khóa
    elif ((soKhoaTac == 0) and (soKhoaKhac == 1)):
        sttpa = 1  # 1 là Nguyên thủ khóa
    elif ((soKhoaTac == 0) and (soKhoaKhac == 0)):
        sttpa = 3  # 3 là Giao khắc, Mão tinh, Biệt trách
    else:
        sttpa = 4  # 4 là Tri nhất Thiệp Hại
    # Ngoài ra các cách lấy khóa dư gồm có: Bát chuyên vô khắc, Phục ngậm và Phản ngậm khóa.
    if (chiNgay == CanKy(canNgay)):
        canchidongcung = 1
    else:
        canchidongcung = 0
    if m[0][0] == 'TÝ':
        phucngam = 1
    elif m[0][0] == 'NGỌ':
        phanngam = 1
    else:
        phucngam = 0
        phanngam = 0

        # Nguyên thủ trùng thẩm; giao mão biệt; tri thiệp; bát chuyên; phục ngâm; phản ngâm
    mode = [0, 0, 0, 0, 0, 0]
    if sttpa == 1 or sttpa == 2:
        mode[0] = 1  # Nguyên thủ trùng thẩm
    if sttpa == 3:
        mode[1] = 1  # giao khắc mão tinh biệt trách
    if sttpa == 4:
        mode[2] = 1  # Tri thiệp
    if canchidongcung == 1:
        mode[3] = 1  # Bát chuyên
    if phucngam == 1:
        mode[4] = 1
    if phanngam == 1:
        mode[5] = 1
# Các tham số cần thiết:
    if m[2][0] == m[3][0] or m[2][0] == m[4][0] or m[2][0] == m[5][0] or m[3][0] == m[4][0] or m[3][0] == m[5][0] or m[4][0] == m[5][0]:
        khoaKhacCungNhau = 0
    else:
        khoaKhacCungNhau = 1

    tukhoa = ["DẦN", "MÃO", "TỊ", "NGỌ", "THÌN", "TUẤT",
              "THÂN", "DẬU", "HỢI", "TÝ", "SỬU", "MÙI"]
    chudoi = ["H", "TS", "K", "BK"]
    sangso = [0, 0, 1, 10]
    sc = canGoc.index(canNgay)
    sk1 = tukhoa.index(m[2][0])
    sk2 = tukhoa.index(m[3][0])
    sk3 = tukhoa.index(m[4][0])
    sk4 = tukhoa.index(m[5][0])
    skth1 = skth[sc][sk1]
    skth2 = skth[sc][sk2]
    skth3 = skth[sc][sk3]
    skth4 = skth[sc][sk4]
    skth_number1 = sangso[chudoi.index(skth1)]
    skth_number2 = sangso[chudoi.index(skth2)]
    skth_number3 = sangso[chudoi.index(skth3)]
    skth_number4 = sangso[chudoi.index(skth4)]
    sum_skth = skth_number1 + skth_number2 + skth_number3 + skth_number4
    if (sum_skth != 0):
        tuKhoaTuongKhacCan = 1
    else:
        tuKhoaTuongKhacCan = 0
    soKhoaKhacCan = sum_skth % 10
    soKhoaBiCanKhac = sum_skth / 10
    if (soKhoaKhacCan != 0):
        coKhacCan = 1
    else:
        coKhacCan = 0

    if (sc % 2 == 0):
        ngayDuong = 1
    else:
        ngayDuong = 0

    chigocq = ["SỬU", "DẦN", "MÃO", "THÌN", "TỊ", "NGỌ",
               "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI", "TÝ"]
    k1 = khoaTK[0]
    k2 = khoaTK[1]
    k3 = khoaTK[2]
    k4 = khoaTK[3]
    k1amduong = chigocq.index(m[2][0]) % 2
    k2amduong = chigocq.index(m[3][0]) % 2
    k3amduong = chigocq.index(m[4][0]) % 2
    k4amduong = chigocq.index(m[5][0]) % 2
    tacduong = 0
    tacam = 0
    khacduong = 0
    khacam = 0
    if (k1amduong == 1):
        if (k1 == "Tặc"):
            tacduong += 1
        elif (k1 == "Khắc"):
            khacduong += 1
    elif (k1amduong == 0):
        if (k1 == "Tặc"):
            tacam += 1
        elif (k1 == "Khắc"):
            khacam += 1

    if (k2amduong == 1):
        if (k2 == "Tặc"):
            tacduong += 1
        elif (k2 == "Khắc"):
            khacduong += 1
    elif (k2amduong == 0):
        if (k2 == "Tặc"):
            tacam += 1
        elif (k2 == "Khắc"):
            khacam += 1

    if (k3amduong == 1):
        if (k3 == "Tặc"):
            tacduong += 1
        elif (k3 == "Khắc"):
            khacduong += 1
    elif (k3amduong == 0):
        if (k3 == "Tặc"):
            tacam += 1
        elif (k3 == "Khắc"):
            khacam += 1

    if (k4amduong == 1):
        if (k4 == "Tặc"):
            tacduong += 1
        elif (k4 == "Khắc"):
            khacduong += 1
    elif (k4amduong == 0):
        if (k4 == "Tặc"):
            tacam += 1
        elif (k4 == "Khắc"):
            khacam += 1
    return [mode, [soKhoaTac, soKhoaKhac, sttpa, tuKhoaTuongKhacCan, soKhoaKhacCan, soKhoaBiCanKhac, canchidongcung, ngayDuong, phucngam, phanngam, coKhacCan, khoaKhacCungNhau, tacduong, tacam, khacduong, khacam]]
# endregion

# region An Tam truyền theo các lựa chọn mode khác nhau, nếu không có, kết quả trả về [], sử dụng def NguyenThuTrungTham cho cả chức năng


def NguyenThuTrungTham(canNgay, chiNgay, tietKhi, chiGio):
    s = ThienBanTuKhoa(tietKhi, chiGio, canNgay, chiNgay)
    tenK1 = s[2][0]
    tenK2 = s[3][0]
    tenK3 = s[4][0]
    tenK4 = s[5][0]
    k1 = s[6][0]
    k2 = s[6][1]
    k3 = s[6][2]
    k4 = s[6][3]
    vo = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    ketQua = []
    if (vo[2] == 1):
        ketQua = AnTamTruyen_NguyenThuKhoa(
            tietKhi, chiGio, tenK1, tenK2, tenK3, tenK4, k1, k2, k3, k4)
    elif (vo[2] == 2):
        ketQua = AnTamTruyen_TrungThamKhoa(
            tietKhi, chiGio, tenK1, tenK2, tenK3, tenK4, k1, k2, k3, k4)
    else:
        ketQua = []
    ketQua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketQua[1], ketQua[2], ketQua[3]))
    return ketQua


def AnTamTruyen_NguyenThuKhoa(tietkhihientai, chigio, tk1, tk2, tk3, tk4, k1, k2, k3, k4):
    chutrenk1234 = [tk1, tk2, tk3, tk4]
    tkst1234 = [k1, k2, k3, k4]
    diaban = chiGoc
    thienban = ThienBan(tietkhihientai, chigio)
    a = 0
    for i in range(len(tkst1234)):
        if tkst1234[i] == 'Khắc':
            a = i
    soTruyen = chutrenk1234[a]
    b = diaban.index(chutrenk1234[a])
    trungTruyen = thienban[b]
    c = diaban.index(thienban[b])
    matTruyen = thienban[c]
    return ['Nguyên thủ khóa', soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_TrungThamKhoa(tietkhihientai, chigio, tk1, tk2, tk3, tk4, k1, k2, k3, k4):
    chutrenk1234 = [tk1, tk2, tk3, tk4]
    tkst1234 = [k1, k2, k3, k4]
    diaban = chiGoc
    thienban = ThienBan(tietkhihientai, chigio)
    a = 0
    for i in range(len(tkst1234)):
        if tkst1234[i] == 'Tặc':
            a = i
    soTruyen = chutrenk1234[a]
    b = diaban.index(chutrenk1234[a])
    trungTruyen = thienban[b]
    c = diaban.index(thienban[b])
    matTruyen = thienban[c]
    return ['Trùng thẩm khóa', soTruyen, trungTruyen, matTruyen]
# endregion

# region AN Tam truyền Bát chuyên khóa bằng def BatChuyen


def BatChuyen(tietKhi, chiGio, canNgay, chiNgay):
    s = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    ngayduong = s[7]
    sttpa = s[2]
    ketQua = []
    if (sttpa == 3):
        if (ngayduong == 1):
            ketQua = AnTamTruyen_BatChuyenTien(
                tietKhi, chiGio, canNgay)
        else:
            ketQua = AnTamTruyen_BatChuyenThoai(
                tietKhi, chiGio, canNgay, chiNgay)
    else:
        ketQua = ['Bát chuyên hữu khắc', '', '', ""]
    ketQua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketQua[1], ketQua[2], ketQua[3]))
    return ketQua


def AnTamTruyen_BatChuyenTien(tietkhihientai, chigio, canngay):
    diabantien = ["DẦN", "MÃO", "THÌN", "TỊ", "NGỌ",
                  "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI", "TÝ", "SỬU"]
    thienban = ThienBan(tietkhihientai, chigio)

    canky = CanKy(canngay)
    a = chiGoc.index(canky)
    tien = diabantien[a]
    b = chiGoc.index(tien)
    soTruyen = thienban[b]
    trungTruyen = thienban[a]
    matTruyen = thienban[a]
    name = 'Bát chuyên tiến'
    if soTruyen == trungTruyen or trungTruyen == matTruyen or soTruyen == matTruyen:
        name = 'Bát chuyên độc túc'
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_BatChuyenThoai(tietkhihientai, chigio, canNgay, chiNgay):
    diabanthoai = ["TUẤT", "HỢI", "TÝ", "SỬU", "DẦN",
                   "MÃO", "THÌN", "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU"]
    thienban = ThienBan(tietkhihientai, chigio)
    DK4 = ThienBanTuKhoa(tietkhihientai, chigio, canNgay, chiNgay)[5][1]
    chiAmThan = diabanthoai[chiGoc.index(DK4)]
    soTruyen = thienban[chiGoc.index(chiAmThan)]
    trungTruyen = thienban[chiGoc.index(CanKy(canNgay))]
    # mat = trung
    name = 'Bát chuyên thoái'
    if soTruyen == trungTruyen:
        name = 'Bát chuyên độc túc'
    return [name, soTruyen, trungTruyen, trungTruyen]
# endregion

# region An Tam truyền Phản ngâm khóa bằng def PhanNgam


def PhanNgam(tietKhi, chiGio, canNgay, chiNgay):
    s = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    sttpa = s[2]
    ketqua = []
    if (sttpa == 3):
        ketqua = AnTamTruyen_PhanNgamKhoa(
            tietKhi, chiGio, canNgay, chiNgay)  # "Phản ngậm vô khắc"
    else:
        ketqua = ["Phản ngậm tương khắc", '', '', '']
    ketqua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketqua[1], ketqua[2], ketqua[3]))
    return ketqua


def AnTamTruyen_PhanNgamKhoa(tietkhihientai, chigio, canngay, chingay):
    chitien5 = ["THÌN", "TỊ", "NGỌ", "MÙI", "THÂN",
                "DẬU", "TUẤT", "HỢI", "TÝ", "SỬU", "DẦN", "MÃO"]
    thienban = ThienBan(tietkhihientai, chigio)
    ketqua = ["Phản ngâm vô khắc", "Sơ", "Trung", "Mạt"]
    # Cung 1 có an Chi, tiến đến 5, lấy thiên bàn đó làm sơ
    ketqua[1] = thienban[chiGoc.index(chitien5[chiGoc.index(chingay)])]
    ketqua[2] = thienban[chiGoc.index(chingay)]
    ketqua[3] = thienban[chiGoc.index(CanKy(canngay))]

    return ketqua


# endregion

# region An Tam truyền Phục ngâm khóa bằng def PhucNgam

def PhucNgam(canNgay, chiNgay, tietKhi, chiGio):
    s = ThienBanTuKhoa(tietKhi, chiGio, canNgay, chiNgay)
    tenK1 = s[2][0]
    tenK2 = s[3][0]
    tenK3 = s[4][0]
    tenK4 = s[5][0]
    k1 = s[6][0]
    k2 = s[6][1]
    k3 = s[6][2]
    k4 = s[6][3]
    vo = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    sttpa = vo[2]
    ngayduong = vo[7]
    ketQua = []

    if (sttpa != 3):
        ketQua = AnTamTruyen_PhucNgamKhoa_PhucNgamTuongKhac_DoTruyen(
            tietKhi, chiGio, chiNgay, tenK1, tenK2, tenK3, tenK4, k1, k2, k3, k4)
    else:
        if (ngayduong == 1):
            ketQua = AnTamTruyen_PhucNgamKhoa_PhucNgamTuNham_DoTruyen(
                tietKhi, chiGio, canNgay, chiNgay)
        else:
            ketQua = AnTamTruyen_PhucNgamKhoa_PhucNgamTuTin_DoTruyen(
                tietKhi, chiGio, canNgay, chiNgay)
    ketQua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketQua[1], ketQua[2], ketQua[3]))
    return ketQua


def AnTamTruyen_PhucNgamKhoa_PhucNgamTuongKhac_DoTruyen(tietkhihientai, chigio, chingay, tk1, tk2, tk3, tk4, k1, k2, k3, k4):

    # Nếu là Phục ngậm tương khắc, lấy chữ trên khóa khắc làm sơ truyền, nếu sơ truyền tự hình thì là Phục ngậm đô truyền,
    # lúc này trung truyền là chữ Thiên bàn trên cung Chi.
    chutrenk1234 = [tk1, tk2, tk3, tk4]
    tkst1234 = [k1, k2, k3, k4]

    thienban = ThienBan(tietkhihientai, chigio)
    ketqua = ["Phục ngậm tương khắc", "Sơ", "Trung", "Mạt"]
    a = 0
    for i in range(len(tkst1234)):
        if ((tkst1234[i] == "Tặc") or (tkst1234[i] == "Khắc")):
            a = i
    ketqua[1] = chutrenk1234[a]  # Sơ truyền

    # Trung truyền là chữ bị sơ truyền hình, nếu sơ tự hình thì đổi sang cung Chi làm trung truyền
    ketqua[2] = chubichihinh[chiGoc.index(ketqua[1])]
    if ketqua[2] == ketqua[1]:
        ketqua[0] = "Phục ngậm đô truyền tương khắc"
        ketqua[2] = thienban[chiGoc.index(chingay)]
    # Mạt truyền là chữ bị trung truyền hình, nếu trung tự hình thì đổi sang chữ bị trung truyền xung
    ketqua[3] = chubichihinh[chiGoc.index(ketqua[2])]
    if ketqua[3] == ketqua[2]:
        ketqua[3] = chixung[chiGoc.index(ketqua[2])]

    return ketqua


def AnTamTruyen_PhucNgamKhoa_PhucNgamTuNham_DoTruyen(tietkhihientai, chigio, canngay, chingay):

    thienban = ThienBan(tietkhihientai, chigio)
    ketqua = ["Phục ngậm tự nhậm", "Sơ", "Trung", "Mạt"]
    # Sơ truyền là chữ thiên bàn trên cung Can
    ketqua[1] = thienban[chiGoc.index(CanKy(canngay))]
    # Lấy trung truyền: chữ bị sơ hình, nếu sơ tự hình thì lấy ở cung Chi
    ketqua[2] = chubichihinh[chiGoc.index(ketqua[1])]
    if ketqua[2] == ketqua[1]:
        ketqua[0] = "Phục ngậm đô truyền tự nhậm"
        ketqua[2] = thienban[chiGoc.index(chingay)]
    # Lấy mạt truyền, chữ bị trung hình, nếu trung tự hình thì lấy ở cung xung với trung truyền
    ketqua[3] = chubichihinh[chiGoc.index(ketqua[2])]
    if ketqua[3] == ketqua[2]:
        ketqua[3] = chixung[chiGoc.index(ketqua[2])]
    return ketqua


def AnTamTruyen_PhucNgamKhoa_PhucNgamTuTin_DoTruyen(tietkhihientai, chigio, canngay, chingay):
    thienban = ThienBan(tietkhihientai, chigio)
    ketqua = ["Phục ngậm tự tín", "Sơ", "Trung", "Mạt"]
    # SƠ truyền trên cung Chi
    ketqua[1] = thienban[chiGoc.index(chingay)]

    # Nếu sơ truyền là tự hình thì Trung truyền lấy ở cung Can, không thì trung là sơ hình
    ketqua[2] = chubichihinh[chiGoc.index(ketqua[1])]
    if ketqua[2] == ketqua[1]:
        ketqua[0] = "Phục ngậm đô truyền tự tín"
        ketqua[2] = thienban[chiGoc.index(CanKy(canngay))]
    ketqua[3] = chubichihinh[chiGoc.index(ketqua[2])]
    if ketqua[3] == ketqua[2]:
        ketqua[3] = chixung[chiGoc.index(ketqua[2])]
    return ketqua


# endregion
# region an Giao khắc, mão tinh, biệt trách
def GiaoKhacMaoTinhBietTrach(canNgay, chiNgay, tietKhi, chiGio):
    s = ThienBanTuKhoa(tietKhi, chiGio, canNgay, chiNgay)
    tenK1 = s[2][0]
    tenK2 = s[3][0]
    tenK3 = s[4][0]
    tenK4 = s[5][0]

    vo = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    k = KiemTraGiaoKhacMaoTinhBietTrach(
        vo[4], vo[5], vo[7], vo[11], canNgay, tenK1, tenK2, tenK3, tenK4)
    ketQua = []
    if (k == "Giao khắc khóa - Cao thỉ cách"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_CaoThiCach(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Giao khắc khóa - Đạn xạ cách"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_DanXaCach(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Giao khắc khóa - Cao thỉ cách dương nhật"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_CaoThiCachDuongNhat(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Giao khắc khóa - Cao thỉ cách âm nhật"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_CaoThiCachAmNhat(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Giao khắc khóa - Đạn xạ cách dương nhật"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_DanXaCachDuongNhat(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Giao khắc khóa - Đạn xạ cách âm nhật"):
        ketQua = AnTamTruyen_GiaoKhacKhoa_DanXaCachAmNhat(
            tietKhi, chiGio, canNgay, chiNgay, tenK1, tenK2, tenK3, tenK4)
    elif (k == "Mão tinh dương nhật"):
        ketQua = AnTamTruyen_MaoTinhDuongNhat(
            tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Mão tinh âm nhật"):
        ketQua = AnTamTruyen_MaoTinhAmNhat(tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Biệt trách dương nhật"):
        ketQua = AnTamTruyen_BietTrachDuongNhat(
            tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Biệt trách âm nhật"):
        ketQua = AnTamTruyen_BietTrachAmNhat(tietKhi, chiGio, canNgay, chiNgay)
    ketQua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketQua[1], ketQua[2], ketQua[3]))
    return ketQua


def KiemTraGiaoKhacMaoTinhBietTrach(sokhoakhaccan, sokhoabicankhac, ngayduong, khoakhaccung, canngay, tk1, tk2, tk3, tk4):
    ketqua = ""
    sokhoakhaccanthuocduong = SoKhoaDuongKhacCan(canngay, tk1, tk2, tk3, tk4)
    sokhoakhaccanthuocam = SoKhoaAmKhacCan(canngay, tk1, tk2, tk3, tk4)
    sokhoaambicankhac = SoKhoaAmBiCanKhac(canngay, tk1, tk2, tk3, tk4)
    sokhoaduongbicankhac = SoKhoaDuongBiCanKhac(canngay, tk1, tk2, tk3, tk4)
    if (sokhoakhaccan == 1):
        ketqua = "Giao khắc khóa - Cao thỉ cách"
    elif (sokhoabicankhac == 1):
        ketqua = "Giao khắc khóa - Đạn xạ cách"
    elif ((sokhoakhaccan > 1) and (ngayduong == 1) and (sokhoakhaccanthuocduong <= 1)):
        ketqua = "Giao khắc khóa - Cao thỉ cách dương nhật"
    elif ((sokhoakhaccan > 1) and (ngayduong == 0) and (sokhoakhaccanthuocam <= 1)):
        ketqua = "Giao khắc khóa - Cao thỉ cách âm nhật"
    elif ((sokhoabicankhac > 1) and (ngayduong == 1) and (sokhoaduongbicankhac <= 1)):
        ketqua = "Giao khắc khóa - Đạn xạ cách dương nhật"
    elif ((sokhoabicankhac > 1) and (ngayduong == 0) and (sokhoaambicankhac <= 1)):
        ketqua = "Giao khắc khóa - Đạn xạ cách âm nhật"
    elif ((khoakhaccung == 1) and (ngayduong == 1)):
        ketqua = "Mão tinh dương nhật"
    elif ((khoakhaccung == 1) and (ngayduong == 0)):
        ketqua = "Mão tinh âm nhật"
    elif ((khoakhaccung == 0) and (ngayduong == 1)):
        ketqua = "Biệt trách dương nhật"
    elif ((khoakhaccung == 0) and (ngayduong == 0)):
        ketqua = "Biệt trách âm nhật"
    return ketqua


def AnTamTruyen_GiaoKhacKhoa_CaoThiCach(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    chutrenk1234 = [tk1, tk2, tk3, tk4]
    thienban = ThienBan(tietkhihientai, chigio)
    tukhoa = ["DẦN", "MÃO", "TỊ", "NGỌ", "THÌN", "TUẤT",
              "THÂN", "DẬU", "HỢI", "TÝ", "SỬU", "MÙI"]

    sc = canGoc.index(canngay)
    sk1 = tukhoa.index(chutrenk1234[0])
    sk2 = tukhoa.index(chutrenk1234[1])
    sk3 = tukhoa.index(chutrenk1234[2])
    sk4 = tukhoa.index(chutrenk1234[3])
    skthoa = [skth[sc][sk1], skth[sc][sk2], skth[sc][sk3], skth[sc][sk4]]
    a = 0
    for i in range(len(skthoa)):
        if skthoa[i] == "K":
            a = i
    name = "Giao khắc khóa - Cao thỉ cách"
    soTruyen = chutrenk1234[a]
    b = chiGoc.index(chutrenk1234[a])
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_GiaoKhacKhoa_DanXaCach(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    chutrenk1234 = [tk1, tk2, tk3, tk4]
    thienban = ThienBan(tietkhihientai, chigio)
    tukhoa = ["DẦN", "MÃO", "TỊ", "NGỌ", "THÌN", "TUẤT",
              "THÂN", "DẬU", "HỢI", "TÝ", "SỬU", "MÙI"]

    sc = canGoc.index(canngay)
    sk1 = tukhoa.index(chutrenk1234[0])
    sk2 = tukhoa.index(chutrenk1234[1])
    sk3 = tukhoa.index(chutrenk1234[2])
    sk4 = tukhoa.index(chutrenk1234[3])
    skthoa = [skth[sc, sk1], skth[sc, sk2], skth[sc, sk3], skth[sc, sk4]]
    a = 0
    for i in range(len(skthoa)):
        if (skthoa[i] == "BK"):
            a = i
    name = "Giao khắc khóa - Đạn xạ cách"
    soTruyen = chutrenk1234[a]
    b = chiGoc.index(chutrenk1234[a])
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_GiaoKhacKhoa_CaoThiCachDuongNhat(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    thienban = ThienBan(tietkhihientai, chigio)
    sochukhaccanthuocduong = SoKhoaDuongKhacCan(canngay, tk1, tk2, tk3, tk4)
    sochukhaccanthuocam = SoKhoaAmKhacCan(canngay, tk1, tk2, tk3, tk4)
    if (sochukhaccanthuocduong == 1):
        soTruyen = KhoaDuongKhacCanDuyNhat(canngay, tk1, tk2, tk3, tk4)
    elif (sochukhaccanthuocduong == 0):
        if (sochukhaccanthuocam > 0):
            soTruyen = KhoaAmKhacCanDauTien(canngay, tk1, tk2, tk3, tk4)
    b = chiGoc.index(soTruyen)
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    name = "Giao khắc khóa - Cao thỉ cách Dương nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_GiaoKhacKhoa_CaoThiCachAmNhat(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    thienban = ThienBan(tietkhihientai, chigio)
    sochukhaccanthuocduong = SoKhoaDuongKhacCan(canngay, tk1, tk2, tk3, tk4)
    sochukhaccanthuocam = SoKhoaAmKhacCan(canngay, tk1, tk2, tk3, tk4)
    if (sochukhaccanthuocam == 1):
        soTruyen = KhoaAmKhacCanDauTien(
            canngay, tk1, tk2, tk3, tk4)
    elif (sochukhaccanthuocam == 0):
        if (sochukhaccanthuocduong > 0):
            soTruyen = KhoaDuongKhacCanDuyNhat(
                canngay, tk1, tk2, tk3, tk4)
    # Lưu ý: đoạn Khóa duong khắc can duy nhất cũng dùng để tính cho khóa dương khắc can đầu tiên được
    b = chiGoc.index(soTruyen)
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    name = "Giao khắc khóa - Cao thỉ cách Âm nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_GiaoKhacKhoa_DanXaCachDuongNhat(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    thienban = ThienBan(tietkhihientai, chigio)
    soTruyen = KhoaDuongBiCanKhac(
        canngay, tk1, tk2, tk3, tk4)

    b = chiGoc.index(soTruyen)
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    name = "Giao khắc khóa - Đạn xạ cách Dương nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_GiaoKhacKhoa_DanXaCachAmNhat(tietkhihientai, chigio, canngay, chingay, tk1, tk2, tk3, tk4):
    thienban = ThienBan(tietkhihientai, chigio)
    soTruyen = KhoaAmBiCanKhac(
        canngay, tk1, tk2, tk3, tk4)

    b = chiGoc.index(soTruyen)
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    name = "Giao khắc khóa - Đạn xạ cách Âm nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_MaoTinhDuongNhat(tietkhihientai, chigio, canngay, chingay):
    thienban = ThienBan(tietkhihientai, chigio)
    a = chiGoc.index("DẬU")
    soTruyen = thienban[a]

    b = chiGoc.index(chingay)
    trungTruyen = thienban[b]

    c = chiGoc.index(CanKy(canngay))
    matTruyen = thienban[c]
    name = "Mão tinh Dương nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_MaoTinhAmNhat(tietkhihientai, chigio, canngay, chingay):
    thienban = ThienBan(tietkhihientai, chigio)
    a = thienban.index("DẬU")
    soTruyen = chiGoc[a]

    b = chiGoc.index(CanKy(canngay))
    trungTruyen = thienban[b]

    c = chiGoc.index(chingay)
    matTruyen = thienban[c]
    name = "Mão tinh Âm nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_BietTrachDuongNhat(tietkhihientai, chigio, canngay, chingay):
    thienban = ThienBan(tietkhihientai, chigio)
    canhopxuongdiaban = ["MÙI", "THÂN", "TUẤT", "HỢI",
                         "SỬU", "DẦN", "THÌN", "TỊ", "MÙI", "TỊ"]
    cungancan = ["DẦN", "THÌN", "TỊ", "MÙI",
                 "TỊ", "MÙI", "THÂN", "TUẤT", "HỢI", "SỬU"]
    a = canGoc.index(canngay)
    b = canhopxuongdiaban[a]
    c = chiGoc.index(b)
    soTruyen = thienban[c]
    e = cungancan[a]
    d = chiGoc.index(e)
    trungTruyen = thienban[d]
    matTruyen = thienban[d]
    name = "Biệt trách Dương nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def AnTamTruyen_BietTrachAmNhat(tietkhihientai, chigio, canngay, chingay):
    thienban = ThienBan(tietkhihientai, chigio)
    chingayam = ["TỊ", "DẬU", "SỬU", "HỢI", "MÃO", "MÙI"]
    tienchitamhop = ["DẬU", "SỬU", "TỊ", "MÃO", "MÙI", "HỢI"]
    cungancan = ["DẦN", "THÌN", "TỊ", "MÙI",
                 "TỊ", "MÙI", "THÂN", "TUẤT", "HỢI", "SỬU"]
    soTruyen = tienchitamhop[chingayam.index(chingay)]
    a = canGoc.index(canngay)
    e = cungancan[a]
    d = chiGoc.index(e)
    trungTruyen = thienban[d]
    matTruyen = thienban[d]
    name = "Biệt trách Âm nhật"
    return [name, soTruyen, trungTruyen, matTruyen]


def Temp(canNgay, tk1, tk2, tk3, tk4, val):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoa = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == val:
            khoa[i] = khoatinh[i]
    a = canGoc.index(canNgay)
    try:
        b = tukhoa.index(khoa[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoa[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoa[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoa[3])
    except:
        e = 12

    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    return khac


def SoKhoaDuongKhacCan(canNgay, tk1, tk2, tk3, tk4):

    khac = Temp(canNgay, tk1, tk2, tk3, tk4, 0)
    so = [0, 0, 0, 0]
    for i in range(len(so)):
        if khac[i] == "K":
            so[i] = 1
        else:
            so[i] = 0
    return sum(so)


def KhoaDuongKhacCanDuyNhat(canNgay, tk1, tk2, tk3,  tk4):

    khac = Temp(canNgay, tk1, tk2, tk3, tk4, 0)
    khoa = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 0:
            khoa[i] = khoatinh[i]
    f = ""
    if (khac[0] == "K"):
        f = khoa[0]
    elif (khac[1] == "K"):
        f = khoa[1]
    elif (khac[2] == "K"):
        f = khoa[2]
    elif (khac[3] == "K"):
        f = khoa[3]
    return f


def SoKhoaAmKhacCan(canNgay, tk1, tk2, tk3, tk4):
    khac = Temp(canNgay, tk1, tk2, tk3, tk4, 1)
    so = [0, 0, 0, 0]
    f = 0
    for i in range(len(so)):
        if khac[i] == 'K':
            so[i] = 1
        else:
            so[i] = 0
    f = sum(so)
    return f


def KhoaAmKhacCanDauTien(canngay, tk1, tk2, tk3, tk4):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoaam = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 1:
            khoaam[i] = khoatinh[i]
    a = canGoc.index(canngay)
    try:
        b = tukhoa.index(khoaam[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoaam[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoaam[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoaam[3])
    except:
        e = 12
    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    f = ""
    if (khac[0] == "K"):
        f = khoaam[0]
    elif (khac[1] == "K"):
        f = khoaam[1]
    elif (khac[2] == "K"):
        f = khoaam[2]
    elif (khac[3] == "K"):
        f = khoaam[3]
    return f


def KhoaDuongBiCanKhac(canngay, tk1, tk2, tk3, tk4):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoaduong = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 0:
            khoaduong[i] = khoatinh[i]
    a = canGoc.index(canngay)
    try:
        b = tukhoa.index(khoaduong[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoaduong[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoaduong[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoaduong[3])
    except:
        e = 12
    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    f = ""
    if (khac[0] == "BK"):
        f = khoaduong[0]
    elif (khac[1] == "BK"):
        f = khoaduong[1]
    elif (khac[2] == "BK"):
        f = khoaduong[2]
    elif (khac[3] == "BK"):
        f = khoaduong[3]
    return f


def KhoaAmBiCanKhac(canngay, tk1, tk2, tk3, tk4):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoaam = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 1:
            khoaam[i] = khoatinh[i]
    a = canGoc.index(canngay)
    try:
        b = tukhoa.index(khoaam[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoaam[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoaam[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoaam[3])
    except:
        e = 12
    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    if (khac[0] == "BK"):
        f = khoaam[0]
    elif (khac[1] == "BK"):
        f = khoaam[1]
    elif (khac[2] == "BK"):
        f = khoaam[2]
    elif (khac[3] == "BK"):
        f = khoaam[3]
    return f


def SoKhoaDuongBiCanKhac(canngay, tk1, tk2, tk3, tk4):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoaduong = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 0:
            khoaduong[i] = khoatinh[i]
    a = canGoc.index(canngay)
    try:
        b = tukhoa.index(khoaduong[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoaduong[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoaduong[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoaduong[3])
    except:
        e = 12
    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    f = 0
    so = [0, 0, 0, 0]
    for i in range(len(so)):
        if khac[i] == 'BK':
            so[i] = 1
        else:
            so[i] = 0
    f = sum(so)
    return f


def SoKhoaAmBiCanKhac(canngay, tk1, tk2, tk3, tk4):
    khac = ["", "", "", ""]
    khoatinh = [tk1, tk2, tk3, tk4]
    khoaduong = ["", "", "", ""]
    for i in range(len(khoatinh)):
        if chiGoc.index(khoatinh[i]) % 2 == 1:
            khoaduong[i] = khoatinh[i]
    a = canGoc.index(canngay)
    try:
        b = tukhoa.index(khoaduong[0])
    except:
        b = 12
    try:
        c = tukhoa.index(khoaduong[1])
    except:
        c = 12
    try:
        d = tukhoa.index(khoaduong[2])
    except:
        d = 12
    try:
        e = tukhoa.index(khoaduong[3])
    except:
        e = 12
    khac[0] = skth[a][b]
    khac[1] = skth[a][c]
    khac[2] = skth[a][d]
    khac[3] = skth[a][e]
    f = 0
    so = [0, 0, 0, 0]
    for i in range(len(so)):
        if khac[i] == 'BK':
            so[i] = 1
        else:
            so[i] = 0
    f = sum(so)
    return f


# endregion

# region Tri nhất và def chung Tri nhất thiệp hại
def TriNhatThiepHai(canNgay, chiNgay, tietKhi, chiGio):

    vo = ChonTamTruyen(tietKhi, chiGio, canNgay, chiNgay)[1]
    ngayduong = vo[7]
    ketQua = []
    k = KiemTraTriNhatThiepHai(
        vo[0], vo[1], vo[7], vo[12], vo[13], vo[14], vo[15])
    if (k == "Tri nhất khóa - Âm nhật Nhất Tặc"):
        ketQua = AnTamTruyen_TriNhatKhoa(
            0, "Tặc", tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Tri nhất khóa - Âm nhật Vô Tặc Đa Khắc"):
        ketQua = AnTamTruyen_TriNhatKhoa(
            0, "Khắc", tietKhi, chiGio,  canNgay, chiNgay)
    elif (k == "Tri nhất khóa - Dương nhật Nhất Tặc"):
        ketQua = AnTamTruyen_TriNhatKhoa(
            1, "Tặc", tietKhi, chiGio,  canNgay, chiNgay)
    elif (k == "Tri nhất khóa - Dương nhật Vô tặc Đa khắc"):
        ketQua = AnTamTruyen_TriNhatKhoa(
            1, "Khắc", tietKhi, chiGio,  canNgay, chiNgay)
    elif (k == "Thiệp hại khóa - Thiệp tặc cách dương"):
        ketQua = AnTamTruyen_ThiepHaiKhoa(
            1, "Tặc", tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Thiệp hại khóa - Thiệp tặc cách âm"):
        ketQua = AnTamTruyen_ThiepHaiKhoa(
            0, "Tặc", tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Thiệp hại khóa - Thiệp khắc cách dương"):
        ketQua = AnTamTruyen_ThiepHaiKhoa(
            1, "Khắc", tietKhi, chiGio, canNgay, chiNgay)
    elif (k == "Thiệp hại khóa - Thiệp khắc cách âm"):
        ketQua = AnTamTruyen_ThiepHaiKhoa(
            0, "Khắc", tietKhi, chiGio, canNgay, chiNgay)
    ketQua.append(AnThienTuongChoTamTruyen(tietKhi, chiGio,
                                           canNgay, chiNgay, ketQua[1], ketQua[2], ketQua[3]))
    return ketQua


def KiemTraTriNhatThiepHai(sotac, sokhac, ngayduong, tacduong, tacam, khacduong, khacam):
    ketqua = ""
    if ((sotac > 1) and (tacam == 1) and (ngayduong == 0)):
        ketqua = "Tri nhất khóa - Âm nhật Nhất Tặc"
    elif ((sotac == 0) and (khacam == 1) and (sokhac > 1) and (ngayduong == 0)):
        ketqua = "Tri nhất khóa - Âm nhật Vô Tặc Đa Khắc"
    elif ((sotac > 1) and (tacduong == 1) and (ngayduong == 1)):
        ketqua = "Tri nhất khóa - Dương nhật Nhất Tặc"
    elif ((sotac == 0) and (khacduong == 1) and (sokhac > 1) and (ngayduong == 1)):
        ketqua = "Tri nhất khóa - Dương nhật Vô tặc Đa khắc"

    elif ((sotac > 1) and (tacam == 0)):
        ketqua = "Thiệp hại khóa - Thiệp tặc cách dương"
    elif ((sotac > 1) and (tacduong == 0)):
        ketqua = "Thiệp hại khóa - Thiệp tặc cách âm"
    elif ((sotac > 1) and (tacam != 0) and (ngayduong == 0)):
        ketqua = "Thiệp hại khóa - Thiệp tặc cách âm"
    elif ((sotac > 1) and (tacduong != 0) and (ngayduong == 1)):
        ketqua = "Thiệp hại khóa - Thiệp tặc cách dương"

    elif ((sotac == 0) and (sokhac > 1) and (khacam == 0)):
        ketqua = "Thiệp hại khóa - Thiệp khắc cách dương"
    elif ((sotac == 0) and (sokhac > 1) and (khacduong == 0)):
        ketqua = "Thiệp hại khóa - Thiệp khắc cách âm"
    elif ((sotac == 0) and (sokhac > 1) and (khacduong != 0) and (ngayduong == 1)):
        ketqua = "Thiệp hại khóa - Thiệp khắc cách dương"
    elif ((sotac == 0) and (sokhac > 1) and (khacam != 0) and (ngayduong == 0)):
        ketqua = "Thiệp hại khóa - Thiệp khắc cách âm"

    return ketqua


def AnTamTruyen_TriNhatKhoa(amduong, tackhac, tietkhihientai, chigio, canNgay, chiNgay):
    s = ThienBanTuKhoa(tietkhihientai, chigio, canNgay, chiNgay)
    chutrenk1234 = [s[2][0], s[3][0], s[4][0], s[5][0]]
    tkst1234 = s[6]
    thienban = ThienBan(tietkhihientai, chigio)
    a = 0
    ad = 0
    if (amduong == 1):
        ad = 0
    else:
        ad = 1
    for i in range(len(tkst1234)):
        if ((tkst1234[i] == tackhac) and (chiGoc.index(chutrenk1234[i]) % 2 == ad)):
            a = i

    soTruyen = chutrenk1234[a]
    b = chiGoc.index(chutrenk1234[a])
    trungTruyen = thienban[b]
    c = chiGoc.index(thienban[b])
    matTruyen = thienban[c]
    if ((amduong == 0) and (tackhac == "Tặc")):
        name = "Tri nhất khóa - Âm nhật nhất Tặc"
    elif ((amduong == 0) and (tackhac == "Khắc")):
        name = "Tri nhất khóa - Âm nhật vô tặc đa khắc"
    elif ((amduong == 1) and (tackhac == "Tặc")):
        name = "Tri nhất khóa - Dương nhật nhất Tặc"
    elif ((amduong == 1) and (tackhac == "Khắc")):
        name = "Tri nhất khóa - Dương nhật vô tặc đa khắc"
    # AnThienTuongChoTamTruyen(tietkhihientai, chigio, canngay, chingay)
    return [name, soTruyen, trungTruyen, matTruyen]
# endregion
# region Thiệp hại


def TinhThiepKhac(chutren, chuduoi):
    thiepkhac = [[0, 1,  1,  1,  1,  0,  0,  1,  4,  4,  1,  4],
                 [4, 0,  0,  0,  0,  0,  0,  0,  4,  4,  0,  4],
                 [4, 4,  0,  0,  0,  0,  0,  0,  2,  2,  0,  4],
                 [4, 4,  6,  0,  0,  0,  0,  0,  1,  1,  0,  4],
                 [4, 4,  5,  5,  0,  0,  0,  0,  0,  0,  0,  4],
                 [2, 4,  4,  4,  4,  0,  0,  0,  0,  0,  0,  2],
                 [1, 4,  4,  4,  4,  4,  0,  0,  0,  0,  0,  1],
                 [0, 4,  2,  2,  4,  4,  4,  0,  0,  0,  0,  0],
                 [0, 4,  2,  2,  4,  2,  2,  4,  0,  0,  0,  0],
                 [0, 4,  2,  2,  4,  1,  1,  4,  4,  0,  0,  0],
                 [0, 4,  1,  1,  4,  0,  0,  4,  4,  4,  0,  0],
                 [0, 2,  1,  1,  2,  0,  0,  2,  4,  4,  2,  0],
                 [4, 4,  0,  0,  0,  0,  0,  0,  2,  2,  0,  4],
                 [4, 4,  5,  5,  0,  0,  0,  0,  0,  0,  0,  4],
                 [2, 4,  4,  4,  4,  0,  0,  0,  0,  0,  0,  2],
                 [0, 4,  2,  2,  4,  4,  0,  0,  0,  0,  0,  0],
                 [2, 4,  4,  4,  4,  0,  0,  0,  0,  0,  0,  2],
                 [0, 4,  2,  2,  4,  4,  0,  0,  0,  0,  0,  0],
                 [0, 4,  2,  2,  4,  2,  2,  4,  0,  0,  0,  0],
                 [0, 4,  1,  1,  4,  0,  0,  4,  4,  0,  0,  0],
                 [0, 2,  1,  1,  2,  0,  0,  2,  4,  4,  2,  0],
                 [4, 0,  0,  0,  0,  0,  0,  0,  4,  4,  0,  4]]
    chutrenar = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN",
                 "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI"]
    chuduoiar = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT",
                 "HỢI", "GIÁP", "ẤT", "BÍNH", "ĐINH", "MẬU", "KỶ", "CANH", "TÂN", "NHÂM", "QUÝ"]
    try:
        duoi = chuduoiar.index(chuduoi)
    except:
        duoi = -1
    try:
        tren = chutrenar.index(chutren)
    except:
        tren = -1
    ketqua = 0
    if (tren == -1):
        ketqua = -1
    else:
        ketqua = thiepkhac[duoi][tren]
    return ketqua


def TinhThiepTac(chutren, chuduoi):
    thieptac = [[0, 0,  0,  0,  3,  1,  1,  4,  4,  4,  4,  6],
                [5, 0,  0,  0,  3,  0,  0,  4,  4,  4,  4,  5],
                [5, 2,  0,  0,  1,  0,  0,  2,  4,  4,  2,  5],
                [5, 1,  4,  0,  1,  0,  0,  1,  4,  4,  1,  5],
                [4, 0,  4,  4,  0,  0,  0,  0,  4,  4,  0,  4],
                [3, 0,  4,  4,  3,  0,  0,  0,  2,  2,  0,  3],
                [3, 0,  4,  4,  3,  4,  0,  0,  1,  1,  0,  3],
                [1, 0,  4,  4,  3,  4,  4,  0,  0,  0,  0,  1],
                [1, 0,  2,  2,  3,  4,  4,  4,  0,  0,  0,  1],
                [1, 0,  1,  1,  3,  4,  4,  4,  4,  0,  0,  1],
                [0, 0,  0,  0,  3,  4,  4,  4,  4,  4,  0,  0],
                [0, 0,  0,  0,  3,  2,  2,  4,  4,  4,  4,  0],
                [5, 2,  0,  0,  1,  0,  0,  2,  4,  4,  2,  5],
                [4, 0,  4,  4,  0,  0,  0,  0,  4,  4,  0,  4],
                [3, 0,  4,  4,  3,  0,  0,  0,  2,  2,  0,  3],
                [1, 0,  4,  4,  3,  4,  4,  0,  0,  0,  0,  1],
                [3, 0,  4,  4,  3,  0,  0,  0,  2,  2,  0,  3],
                [1, 0,  4,  4,  3,  4,  4,  0,  0,  0,  0,  1],
                [1, 0,  2,  2,  3,  4,  4,  4,  0,  0,  0,  1],
                [0, 0,  0,  0,  3,  4,  4,  4,  4,  4,  0,  0],
                [0, 0,  0,  0,  3,  2,  2,  4,  4,  4,  4,  0],
                [5, 0,  0,  0,  3,  0,  0,  4,  4,  4,  4,  5]]
    chutrenar = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN",
                 "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI"]
    chuduoiar = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ", "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT",
                 "HỢI", "GIÁP", "ẤT", "BÍNH", "ĐINH", "MẬU", "KỶ", "CANH", "TÂN", "NHÂM", "QUÝ"]
    try:
        duoi = chuduoiar.index(chuduoi)
    except:
        duoi = -1
    try:
        tren = chutrenar.index(chutren)
    except:
        tren = -1
    ketqua = 0
    if (tren == -1):
        ketqua = -1
    else:
        ketqua = thieptac[duoi][tren]
    return ketqua


def ManhDiaBan(chucankiemtra):
    manh = ["DẦN", "THÂN", "TỊ", "HỢI", "GIÁP", "BÍNH", "MẬU", "CANH", "NHÂM"]
    ketqua = 0
    if chucankiemtra in manh:
        ketqua = 1

    return ketqua


def TrongDiaBan(chucankiemtra):
    trong = ["TÝ", "NGỌ", "MÃO", "DẬU"]
    ketqua = 0
    if chucankiemtra in trong:
        ketqua = 1
    return ketqua


def QuyDiaBan(chucankiemtra):
    quy = ["THÌN", "TUẤT", "SỬU", "MÙI", "ẤT", "ĐINH", "KỶ", "TÂN", "QUÝ"]
    ketqua = 0
    if chucankiemtra in quy:
        ketqua = 1
    return ketqua


def SinhKhacCan(canNgay, khoaTinh):
    toCan = [
        [0, 1, 2, 2, 1, 3, 3, 1, 4, 4, 1, 0],
        [0, 1, 2, 2, 1, 3, 3, 1, 4, 4, 1, 0],
        [4, 3, 0, 0, 3, 2, 2, 3, 1, 1, 3, 4],
        [4, 3, 0, 0, 3, 2, 2, 3, 1, 1, 3, 4],
        [1, 2, 4, 4, 2, 0, 0, 2, 3, 3, 2, 1],
        [1, 2, 4, 4, 2, 0, 0, 2, 3, 3, 2, 1],
        [3, 0, 1, 1, 0, 4, 4, 0, 2, 2, 0, 3],
        [3, 0, 1, 1, 0, 4, 4, 0, 2, 2, 0, 3],
        [2, 4, 3, 3, 4, 1, 1, 4, 0, 0, 4, 2],
        [2, 4, 3, 3, 4, 1, 1, 4, 0, 0, 4, 2]]

    # 0 là sinh Can, 1 là bị can khắc, 2 là tỷ hòa, 3 là Can sinh, 4 là khắc Can
    sCan = canGoc.index(canNgay)
    sKhoaTinh = chiGoc.index(khoaTinh)
    ketQua = toCan[sCan][sKhoaTinh]
    return ketQua


def AnTamTruyen_ThiepHaiKhoa(amduong, tackhac, tietkhihientai, chigio, canngay, chingay):
    # THỨ TỰ ƯU TIÊN CÁC CÁCH TRONG THIỆP HẠI KHÓA KHI VIẾT CHƯƠNG TRÌNH TÍNH
    # Tỷ dụng cách
    # Kiến cơ cách
    # Sát vi cách
    # Xuyết hà cách
    # Thiệp hại (tặc - khắc) cách
    soTruyen = ''
    trungTruyen = ''
    matTruyen = ''
    name = ''
    vo = ChonTamTruyen(tietkhihientai, chigio, canngay, chingay)[1]
    ngayduong = vo[7]
    s = ThienBanTuKhoa(tietkhihientai, chigio, canngay, chingay)
    thienban = s[0]
    tk = [s[2][0], s[3][0], s[4][0], s[5][0]]
    dk = [s[2][1], s[3][1], s[4][1], s[5][1]]
    kn = s[6]
    dk[0] = CanKy(dk[0])
    # Chọn ra mảng các khóa dương hoặc âm theo yêu cầu của biến amduong
    chonkhoa1 = [0, 0, 0, 0]
    if (amduong == 1):
        for i in range(len(tk)):
            if chiGoc.index(tk[i]) % 2 == 0:
                chonkhoa1[i] = 1
            else:
                chonkhoa1[i] = 0
    else:
        for i in range(len(tk)):
            if chiGoc.index(tk[i]) % 2 != 0:
                chonkhoa1[i] = 1
            else:
                chonkhoa1[i] = 0

    # Chọn ra mảng các khóa Tặc hoặc khóa Khắc theo yêu cầu cua biến tackhac
    chonkhoa2 = [0, 0, 0, 0]
    if (tackhac == "Tặc"):
        for i in range(len(tk)):
            if (kn[i] == "Tặc"):
                chonkhoa2[i] = 1
            else:
                chonkhoa2[i] = 0
    else:
        for i in range(len(tk)):
            if (kn[i] == "Khắc"):
                chonkhoa2[i] = 1
            else:
                chonkhoa2[i] = 0
    # Tổng hợp: chọn ra mảng chứa các khóa cần tính thiệp
    chonkhoa = [0, 0, 0, 0]
    for i in range(len(chonkhoa)):
        chonkhoa[i] = chonkhoa1[i] * chonkhoa2[i]
    khoatinhthiep = ["", "", "", ""]
    khoaduoitinhthiep = ['', '', '', '']
    for i in range(len(khoatinhthiep)):
        if (chonkhoa[i] == 1):
            khoatinhthiep[i] = tk[i]
            khoaduoitinhthiep[i] = dk[i]
        else:
            khoatinhthiep[i] = "nothing"
            khoaduoitinhthiep[i] = "nothing"
    # Tính Thiệp theo yêu cầu Tặc hay Khắc, sau đó tìm ra max trong kết quả tính
    ketquatinhthiep = [0, 0, 0, 0]
    if (tackhac == "Tặc"):
        for i in range(len(khoatinhthiep)):
            ketquatinhthiep[i] = TinhThiepTac(khoatinhthiep[i], dk[i])
    else:
        for i in range(len(khoatinhthiep)):
            ketquatinhthiep[i] = TinhThiepKhac(khoatinhthiep[i], dk[i])
    maxr = max(ketquatinhthiep)

    # Chọn sơ truyền: Tại đây, nếu có chữ tương khắc Can mà cũng có chữ sinh Can (tính với các chữ đang dùng tính thiệp) thì
    # dùng ngay chữ sinh Can làm sơ, gọi là Tỷ dụng cách, trước hết cần phải kiểm tra xem có phải Tỷ dụng cách hay không
    mangtinh = []
    m = []
    tkCan = 0
    sCan = 0
    isTyDung = 0
    for i in range(len(ketquatinhthiep)):
        if ketquatinhthiep[i] != -1:
            mangtinh.append(khoatinhthiep[i])
    for i in range(len(mangtinh)):
        m.append(SinhKhacCan(canngay, mangtinh[i]))
    if 0 in m:
        sCan = 1
    if (1 in m) or (4 in m):
        tkCan = 1
    if sCan == 1 and tkCan == 1:
        isTyDung = 1
    # Kiểm tra xem có phải kiến cơ cách hay không
    test = []
    isCanBeKienCo = 0
    for i in range(len(ketquatinhthiep)):
        if maxr == ketquatinhthiep[i]:
            test.append(i)
    if len(test) > 1:
        isCanBeKienCo = 1
    else:
        isCanBeKienCo = 0
    ##############################################################################################
    ###### AN TỶ DỤNG CÁCH ĐẦU TIÊN NẾU XUẤT HIỆN ##################################################
    ##############################################################################################
    if isTyDung == 1:
        for i in range(len(ketquatinhthiep)):
            if ketquatinhthiep[i] != -1 and (SinhKhacCan(canngay, khoatinhthiep[i]) == 0):
                soTruyen = khoatinhthiep[i]
        trungTruyen = thienban[chiGoc.index(soTruyen)]
        matTruyen = thienban[chiGoc.index(trungTruyen)]
        name = "Thiệp hại khóa - Tỷ dụng cách"
    ###############################################################################################
    ### tiếp theo kiểm tra kiến cơ, sát vi và xuyết hà cách #######################################
    ###############################################################################################
    elif isCanBeKienCo == 1:
        # Chú ý: Cần chú ý chỗ này, khi có thể là kiến cơ cách, phải xét nếu chỉ có 1 chữ gia mạnh thì là kiến cơ
        # nếu chỉ một chữ gia trọng là sát vi, nếu cùng gia mạnh, trọng, quý thì mới xét đến Xuyết hà
        testm = []
        testt = []
        for i in range(len(khoatinhthiep)):
            if ManhDiaBan(khoaduoitinhthiep[i]) == 1:
                testm.append(i)
            if TrongDiaBan(khoaduoitinhthiep[i]) == 1:
                testt.append(i)
        if len(testm) == 1:
            for i in range(len(khoatinhthiep)):
                if ManhDiaBan(khoaduoitinhthiep[i]) == 1:
                    soTruyen = khoatinhthiep[i]
                    trungTruyen = thienban[chiGoc.index(soTruyen)]
                    matTruyen = thienban[chiGoc.index(trungTruyen)]
                    name = "Thiệp hại khóa - Kiến cơ cách"
        elif len(testt) == 1:
            for i in range(len(khoatinhthiep)):
                if TrongDiaBan(khoaduoitinhthiep[i]) == 1:
                    soTruyen = khoatinhthiep[i]
                    trungTruyen = thienban[chiGoc.index(soTruyen)]
                    matTruyen = thienban[chiGoc.index(trungTruyen)]
                    name = "Thiệp hại khóa - Sát vi cách"
        else:
            name = 'Thiệp hại khóa - Xuyết hà cách'
            if ngayduong == 1:
                for i in range(2):
                    if khoatinhthiep[i] != 'nothing':
                        soTruyen = khoatinhthiep[i]
            elif ngayduong == 0:
                for i in range(2):
                    if khoaduoitinhthiep[i+2] != 'nothing':
                        soTruyen = khoatinhthiep[i+2]
            trungTruyen = thienban[chiGoc.index(soTruyen)]
            matTruyen = thienban[chiGoc.index(trungTruyen)]
    else:
        # Không phải tỷ dụng, không phải kiến cơ, sát vi, xuyết hà cách thì chỉ lấy thiệp tặc - thiệp khắc cơ bản
        for i in range(len(ketquatinhthiep)):
            if maxr == ketquatinhthiep[i]:
                soTruyen = khoatinhthiep[i]
        trungTruyen = thienban[chiGoc.index(soTruyen)]
        matTruyen = thienban[chiGoc.index(trungTruyen)]

        if ((amduong == 0) and (tackhac == "Tặc")):
            name = "Thiệp hại khóa - Thiệp tặc cách âm"
        elif ((amduong == 0) and (tackhac == "Khắc")):
            name = "Thiệp hại khóa - Thiệp khắc cách âm"
        elif ((amduong == 1) and (tackhac == "Tặc")):
            name = "Thiệp hại khóa - Thiệp tặc cách dương"
        elif ((amduong == 1) and (tackhac == "Khắc")):
            name = "Thiệp hại khóa - Thiệp khắc cách dương"

    return [name, soTruyen, trungTruyen, matTruyen]
# endregion

# region An tHIÊN TƯỚNG CHO 3 TRUYỀN


def AnThienTuongChoTamTruyen(tietkhihientai, chigio, canngay, chingay, soTruyen, trungTruyen, matTruyen):
    thientuong = ThienTuongQuyNhan(chigio, canngay, chingay, tietkhihientai)
    thienban = ThienBan(tietkhihientai, chigio)
    a = thienban.index(soTruyen)
    soTuong = thientuong[a]
    a = thienban.index(trungTruyen)
    trungTuong = thientuong[a]
    a = thienban.index(matTruyen)
    matTuong = thientuong[a]
    diabancholucthan = ["DẦN", "MÃO", "TỊ", "NGỌ", "THÌN",
                        "TUẤT", "THÂN", "DẬU", "HỢI", "TÝ", "SỬU", "MÙI"]
    lucthancanngay = [
        ["Huynh đệ",    "Huynh đệ", "Tử tôn",   "Tử tôn",   "Thê tài",  "Thê tài",
         "Quan quỷ", "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",  "Thê tài",  "Thê tài", ],
        ["Huynh đệ",    "Huynh đệ", "Tử tôn",   "Tử tôn",   "Thê tài",  "Thê tài",
         "Quan quỷ", "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",  "Thê tài",  "Thê tài", ],
        ["Phụ mẫu", "Phụ mẫu",  "Huynh đệ", "Huynh đệ", "Tử tôn",   "Tử tôn",
         "Thê tài",  "Thê tài",  "Quan quỷ", "Quan quỷ", "Tử tôn",   "Tử tôn", ],
        ["Phụ mẫu", "Phụ mẫu",  "Huynh đệ", "Huynh đệ", "Tử tôn",   "Tử tôn",
         "Thê tài",  "Thê tài",  "Quan quỷ", "Quan quỷ", "Tử tôn",   "Tử tôn", ],
        ["Quan quỷ",    "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",  "Huynh đệ", "Huynh đệ",
         "Tử tôn",   "Tử tôn",   "Thê tài",  "Thê tài",  "Huynh đệ", "Huynh đệ", ],
        ["Quan quỷ",    "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",  "Huynh đệ", "Huynh đệ",
         "Tử tôn",   "Tử tôn",   "Thê tài",  "Thê tài",  "Huynh đệ", "Huynh đệ", ],
        ["Thê tài", "Thê tài",  "Quan quỷ", "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",
         "Huynh đệ", "Huynh đệ", "Tử tôn",   "Tử tôn",   "Phụ mẫu",  "Phụ mẫu", ],
        ["Thê tài", "Thê tài",  "Quan quỷ", "Quan quỷ", "Phụ mẫu",  "Phụ mẫu",
         "Huynh đệ", "Huynh đệ", "Tử tôn",   "Tử tôn",   "Phụ mẫu",  "Phụ mẫu", ],
        ["Tử tôn",  "Tử tôn",   "Thê tài",  "Thê tài",  "Quan quỷ", "Quan quỷ",
         "Phụ mẫu",  "Phụ mẫu",  "Huynh đệ", "Huynh đệ", "Quan quỷ", "Quan quỷ", ],
        ["Tử tôn",  "Tử tôn",   "Thê tài",  "Thê tài",  "Quan quỷ", "Quan quỷ",
         "Phụ mẫu",  "Phụ mẫu",  "Huynh đệ", "Huynh đệ", "Quan quỷ", "Quan quỷ", ]

    ]
    b = canGoc.index(canngay)
    c = diabancholucthan.index(soTruyen)
    d = diabancholucthan.index(trungTruyen)
    e = diabancholucthan.index(matTruyen)
    soLucThan = lucthancanngay[b][c]
    trungLucThan = lucthancanngay[b][d]
    matLucThan = lucthancanngay[b][e]
    return [[soTuong, trungTuong, matTuong], [soLucThan, trungLucThan, matLucThan]]
# endregion
