# HE THONG PHAN TICH VA DU BAO NGUY CO CHAY RUNG
## ALGERIAN FOREST FIRE ANALYTICS AND EARLY WARNING SYSTEM

He thong phan tich, canh bao som nguy co chay rung va mo phong kich ban khi hau dua tren du lieu khi tuong Algerian Forest Fires Dataset (2012). Ung dung tich hop hai dong co hoc may doc lap: **Decision Tree (Cay quyet dinh)** va **Random Forest (Rung ngau nhien)** nham toi uu giua kha nang giai thich truc quan va do chinh xac du bao.

---

## 1. TONG QUAN DU AN

Du an tap trung xu ly va mo hinh hoa du lieu quan trac tai hai khu vuc khi hau dac trung cua Algeria:
- **Vung Bejaia**: Khu vuc duyen hai phia Dong Bac, chiu anh huong boi gio bien va do am cao tu Dia Trung Hai.
- **Vung Sidi-Bel Abbes**: Khu vuc cao nguyen noi dia phia Tay Bac, khi hau ban kho han, nhiet do cao va do am thap.

### Tap du lieu (Dataset)
- **Tong so ban ghi**: 244 ngay quan trac (122 ngay tai Bejaia, 122 ngay tai Sidi-Bel Abbes).
- **Thoi gian thu thap**: Tu thang 06/2012 den thang 09/2012.
- **Cac nhom thuoc tinh**:
  - *Khi tuong thuc dia*: Temperature (Nhiet do), RH (Do am tuong doi), Ws (Toc do gio), Rain (Luong mua).
  - *He thong chi so FWI (Canadian Forest Fire Weather Index)*:
    - FFMC (Fine Fuel Moisture Code): Do am vat lieu chay min tren be mat.
    - DMC (Duff Moisture Code): Do am tang mun huu co trung binh.
    - DC (Drought Code): Chi so kho han tang sau va re cay muc.
    - ISI (Initial Spread Index): Chi so toc do lan truyen lua ban dau.
    - BUI (Buildup Index): Tong luong vat lieu chay san sang bat lua.
    - FWI (Fire Weather Index): Chi so thoi tiet nguy co chay rung tong hop.

---

## 2. KIEN TRUC THU MUC DU AN

```text
TTCS/
|-- data/
|   `-- Algerian_forest_fires_dataset_UPDATE.csv   # Tap du lieu nguon da lam sach
|-- models/
|   |-- __init__.py                               # Package exports cho module hoc may
|   |-- decision_tree_model.py                    # Dong co Cay quyet dinh & trich xuat bo luat
|   |-- random_forest_model.py                    # Dong co Rung ngau nhien & do dong thuan
|   `-- model_evaluator.py                        # Danh gia benchmark, Confusion Matrix, ROC-AUC
|-- views/
|   |-- __init__.py                               # Package exports cho cac man hinh chuc nang
|   |-- alert_view.py                             # Chuc nang 1: Canh bao nguy co tuc thoi
|   |-- climate_view.py                           # Chuc nang 2: Mo phong kich ban khi hau 2D
|   |-- regional_view.py                          # Chuc nang 3: Phan tich doi chieu vung mien
|   |-- seasonal_view.py                          # Chuc nang 4: Truy vet rui ro theo mua vu
|   `-- explainability_view.py                    # Chuc nang 5: Giai ma trong so & cay suy luan
|-- .streamlit/
|   `-- config.toml                               # Cau hinh may chu Streamlit
|-- .vscode/
|   `-- settings.json                             # Cau hinh moi truong Pylance/Python IDE
|-- app.py                                        # Entry point chinh cua ung dung Streamlit
|-- config.py                                     # Cau hinh he thong, bang mau, nguong canh bao
|-- data_loader.py                                # Module doc, lam sach va tien xu ly du lieu
|-- pyrightconfig.json                            # Cau hinh type-checking va import resolution
|-- requirements.txt                              # Danh muc thu vien phu thuoc
|-- run_app.bat                                   # Script khoi chay ung dung 1-click tren Windows
|-- setup_env.bat                                 # Script khoi tao moi truong ao tu dong
|-- test_pipeline.py                              # Bo kiem thu tu dong (Unit Tests)
|-- .gitignore                                    # Danh muc loai tru cho Git
`-- README.md                                     # Tai lieu huong dan du an
```

---

## 3. YEU CAU HE THONG

- **Python**: Phien ban 3.10 tro len (khuyen nghi Python 3.10 hoac 3.11).
- **Git**: Phien ban 2.30 tro len.
- **Trinh duyet**: Chrome, Edge, Firefox, Safari ho tro HTML5 / WebGL.
- **He dieu hanh**: Windows 10/11, macOS, hoac Linux (Ubuntu 20.04+).

---

## 4. HUONG DAN CAI DAT VA KHOI CHAY

### Cach 1: Khoi chay nhanh tren Windows (Khuyen nghi)

Doi voi he dieu hanh Windows da cai dat Python, ban co the su dung cac file script co san trong thu muc:

1. **Buoc 1: Khoi tao moi truong ao va cai dat thu vien**
   Nhan dup chuot vao file `setup_env.bat` hoac chay trong Terminal:
   ```cmd
   setup_env.bat
   ```
   Script se tu dong tao moi truong ao `.venv` va cai dat toan bo thu vien tu `requirements.txt`.

2. **Buoc 2: Chay ung dung**
   Nhan dup chuot vao file `run_app.bat` hoac chay trong Terminal:
   ```cmd
   run_app.bat
   ```
   Trinh duyet se tu dong mo dia chi: `http://localhost:8501`.

---

### Cach 2: Cai dat thu cong (Tat ca he dieu hanh)

1. **Clone repository ve may:**
   ```bash
   git clone https://github.com/zeddiewannabexrdev/Algerian_forest_fires_demo.git
   cd Algerian_forest_fires_demo
   ```

2. **Tao va kich hoat moi truong ao (Virtual Environment):**
   - Tren Windows (Command Prompt / PowerShell):
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - Tren macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Nang cap pip va cai dat danh muc thu vien:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Khoi chay ung dung Streamlit:**
   ```bash
   streamlit run app.py
   ```
   He thong se thong bao dia chi truy cap tai dia phuong:
   ```text
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

---

## 5. KIEM THU HE THONG (UNIT TESTS)

Du an di kem bo kiem thu tu dong kiem tra toan dien pipeline tien xu ly, huan luyen mo hinh va xuat luat. De thuc hien kiem thu:

```bash
python test_pipeline.py
```

Ket qua kiem thu tieu chuan:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.200s

OK
```

Danh sach cac test case:
1. `test_data_loader_shape_and_clean`: Kiem tra tinh toan ven du lieu (du 244 dong, 15 cot, khong co gia tri thieu).
2. `test_decision_tree_manager`: Kiem tra huan luyen va du bao cua dong co Decision Tree.
3. `test_random_forest_manager`: Kiem tra huan luyen, OOB score va phan tich do dong thuan cua Random Forest.
4. `test_model_evaluator`: Kiem tra phan chia Stratified 80/20 va bang so sanh benchmark.
5. `test_rule_extraction`: Kiem tra chuc nang trich xuat luat quyet dinh If-Else bang ngon ngu tu nhien.

---

## 6. CHI TIET CAC MODULE CHUC NANG

### Module 1: Giam Sat Tuc Thoi & Canh Bao Nguy Co
- Nhan dau vao la cac thong so khi tuong thuc dia (Nhiet do, Do am, Toc do gio, Luong mua) va chi so FWI.
- Tinh toan xac suat bat lua doc lap tu Decision Tree va Random Forest.
- Tinh chi so rui ro tong hop Ensemble, phan cap 4 cap do canh bao (Cap 1 - Thap, Cap 2 - Trung binh, Cap 3 - Nguy hiem, Cap 4 - Cuc ky nguy hiem).
- Dua ra chi thi tac chien ro rang danh cho luc luong kiem lam tai hien truong.

### Module 2: Mo Phong Kich Ban Khi Hau 2D
- Cung cap 4 kich ban khi hau gia lap (Thoi tiet thong thuong, Song nhiet El Nino, Bien doi khi hau 2050 RCP 8.5, Mua dong giai nhiet).
- Duong cong phan ung do nhay nhiet do tu 20°C den 45°C.
- Ma tran ranh gioi chuyen pha bat lua 2D (Nhiet do x Do am) su dung ky thuat Vectorized Batch Prediction giup render tuc thi khong gay tre he thong.

### Module 3: Phan Tich Doi Chieu Vung Mien
- So sanh truc quan giua Bejaia (Duyen hai) va Sidi-Bel Abbes (Noi dia).
- Bieu do Radar Profile chuan hoa 6 chi so FWI.
- Bieu do Boxplot phan bo tung tham so khi tuong theo hien trang chay / khong chay.
- Thong ke tan suat chay theo tung thang giua hai khu vuc.

### Module 4: Truy Vet Rui Ro Theo Mua Vu
- Chuoi thoi gian quan trac lien tuc tu thang 6 den thang 9 nam 2012.
- Phan tich co che tich luy kho han tang sau qua chi so Drought Code (DC), giai thich tai sao thang 8 la cao diem chay dien rong.
- Ma tran lich rui ro theo tung ngay (Calendar Heatmap).

### Module 5: Giai Ma Mo Hinh & Bo Luat Suy Luan
- Bang ma tran so sanh hieu nang do luong (Accuracy, Precision, Recall, F1-Score, ROC-AUC).
- Bieu do so sanh Feature Importance giua Decision Tree va Random Forest.
- So do cay phan nhanh Decision Tree ho tro phong to thu nho.
- Bo luat suy luan If-Else duoc phien dich truc quan kem theo xac suat va do tin cay.

---

## 7. CHE DO GIAO DIEN (THEME CONFIGURATION)

Ung dung tich hop san bo chuyen doi giao dien tren thanh dieu khien ben trai (Sidebar):
- **Toi (Dark Mode)**: Bieu dien phong cach may tram chi huy ban dem voi bang mau Slate sẫm (`#0b0f19`, `#131b2e`), do tuong phan cao, chu trang ro net (`#f8fafc`), khong gay moi mat khi lam viec lau.
- **Sang (Light Mode)**: Bieu dien phong cach phong thi nghiem toi gian voi nen trang (`#ffffff`), vien hairline ro net (`#cbd5e1`), chu mau than chi dam (`#090d16`).

Toan bo bieu do Plotly va Matplotlib deu tu dong dong bo mau nen va truc toa do theo theme duoc chon.

---

## 8. THU VIEN SU DUNG CHINH

| Thu vien | Phien ban | Muc dich su dung |
| :--- | :--- | :--- |
| `streamlit` | >= 1.28.0 | Khung giao dien nguoi dung dang may tram chuyen dung |
| `pandas` | >= 2.0.0 | Xu ly cau truc va bien doi du lieu bang |
| `numpy` | >= 1.24.0 | Tinh toan vector hoa va ma tran luoi 2D |
| `scikit-learn` | >= 1.3.0 | Xay dung, huan luyen va danh gia Decision Tree, Random Forest |
| `plotly` | >= 5.15.0 | Bieu do tuong tac cao: Gauge, Radar, Contour, Boxplot, ROC |
| `matplotlib` | >= 3.7.0 | Ket xuat so do phan nhanh cay quyet dinh |
