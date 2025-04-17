
import streamlit as st

st.title("長崎蛋糕餅乾健康模擬器 🍪")

st.header("🔧 配方比例輸入（總和為100%）")
base_flour_pct = st.slider("主粉體比例（低筋/全麥/裸麥/杏仁粉）", 10, 80, 40, step=1)
pea_protein_pct = st.slider("豌豆蛋白比例", 0, 30, 0, step=1)
fat_pct = st.slider("油脂比例", 0, 30, 15, step=1)
sweetener_pct = st.slider("甜味劑比例", 0, 30, 20, step=1)
egg_pct = st.slider("蛋液比例", 0, 30, 15, step=1)
fiber_pct = st.slider("膳食纖維添加比例", 0, 15, 0, step=1)

# 計算總和
total_pct = base_flour_pct + pea_protein_pct + fat_pct + sweetener_pct + egg_pct + fiber_pct
st.markdown(f"**目前總配方比例：{total_pct}%**")
if total_pct != 100:
    st.error("⚠️ 原料總比例必須為100%，請調整比例")
    st.stop()

# 原料類型選擇
st.header("🧂 原料種類選擇")
flour_type = st.selectbox("主粉體種類", ["低筋麵粉", "全麥粉", "裸麥粉", "杏仁粉"])
sweetener_type = st.selectbox("甜味劑類型", ["蔗糖", "赤藻糖醇", "阿洛酮糖", "甜菊糖"])
fiber_added = fiber_pct > 0
vitamin_fortified = st.multiselect("添加機能營養素", ["維生素D", "B群", "鈣", "鐵", "Omega-3"])

# 📊 模擬結果預測
st.header("📊 模擬結果預測")
protein_g = round(1.5 + pea_protein_pct * 0.25, 1)
texture = "鬆軟"
color = "金黃色"
sweetness = "標準甜感"

if pea_protein_pct > 10:
    texture = "偏硬"
if pea_protein_pct > 20:
    texture = "明顯偏硬、易乾裂"
if sweetener_type != "蔗糖":
    sweetness = "甜感下降"
if sweetener_type == "阿洛酮糖":
    color = "上色稍淡"

st.markdown(f'''
- **每片蛋白質含量**: {protein_g} g  
- **預測質地**: {texture}  
- **預測色澤**: {color}  
- **甜味表現**: {sweetness}  
- **膳食纖維**: {"有添加" if fiber_added else "未添加"}  
- **營養素強化**: {", ".join(vitamin_fortified) if vitamin_fortified else "未添加"}  
''')

# 💡 智慧建議模組（具體版）
st.header("💡 智慧建議模組")

suggestions = []

if pea_protein_pct > 10:
    suggestions.append("📌 質地偏硬：可將豌豆蛋白減少至10%，並將油脂從15%增加至20%以改善口感。")
if pea_protein_pct > 20:
    suggestions.append("📌 容易乾裂：建議保留20%蛋白，增加蛋液比例至20%，或添加2%甘油或麥芽糊精保濕。")
if sweetener_type != "蔗糖":
    suggestions.append("📌 甜味不足：可將甜味劑提高5%，或將赤藻糖醇改為阿洛酮糖，並增加烘焙上色時間。")
if flour_type in ["裸麥粉", "杏仁粉"]:
    suggestions.append(f"📌 {flour_type} 吸水性強：建議減少其比例至30%，增加蛋液或油脂3-5%調整黏稠度。")

if not suggestions:
    st.success("✅ 配方參數合理，無需額外調整，可進行試作。")
else:
    for s in suggestions:
        st.warning(s)
