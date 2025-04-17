
import streamlit as st

# 頁面標題
st.title("長崎蛋糕餅乾健康模擬器 🍪")

# 🧁 輸入區塊
st.header("🔧 配方參數設定")

pea_protein_pct = st.slider("豌豆蛋白添加比例 (%)", 0, 30, 0, step=1)
fat_pct = st.slider("油脂總量 (%)", 0, 30, 15, step=1)
sweetener_type = st.selectbox("甜味劑類型", ["蔗糖", "赤藻糖醇", "阿洛酮糖", "甜菊糖"])
flour_type = st.selectbox("粉體種類", ["低筋麵粉", "全麥粉", "裸麥粉", "杏仁粉"])
fiber_added = st.checkbox("添加膳食纖維（如燕麥β-葡聚醣）")
vitamin_fortified = st.multiselect("添加機能營養素", ["維生素D", "B群", "鈣", "鐵", "Omega-3"])

# 📊 模擬結果預測
st.header("📊 模擬結果預測")

# 預估值（簡化處理）
protein_g = round(1.5 + pea_protein_pct * 0.25, 1)
texture = "鬆軟"
color = "金黃色"
sweetness = "標準甜感"

# 質地變化邏輯
if pea_protein_pct > 10:
    texture = "偏硬"
if pea_protein_pct > 20:
    texture = "明顯偏硬、易乾裂"

if sweetener_type != "蔗糖":
    sweetness = "甜感下降"

if sweetener_type == "阿洛酮糖":
    color = "上色稍淡"

# 結果顯示
st.markdown(f"""
- **每片蛋白質含量**：{protein_g} g  
- **預測質地**：{texture}  
- **預測色澤**：{color}  
- **甜味表現**：{sweetness}  
- **膳食纖維**：{"有添加" if fiber_added else "未添加"}  
- **營養素強化**：{", ".join(vitamin_fortified) if vitamin_fortified else "未添加"}  
""")

# 💡 智慧建議模組
st.header("💡 智慧建議模組")

suggestions = []

if pea_protein_pct > 10:
    suggestions.append("📌 豌豆蛋白超過10%，質地可能偏硬：建議增加油脂或加蛋黃調整口感。")
if pea_protein_pct > 20:
    suggestions.append("📌 蛋白超過20%時，建議搭配膳食纖維（如β-葡聚醣）改善乾裂。")
if sweetener_type != "蔗糖":
    suggestions.append("📌 使用代糖會降低甜感與焦糖化：可適量添加天然還原糖或焦糖粉提升風味。")
if flour_type in ["裸麥粉", "杏仁粉"]:
    suggestions.append("📌 使用高纖粉體時，需注意吸水性，建議調整含水比例或添加甘油調和。")

if not suggestions:
    st.success("✅ 目前參數組合無顯著問題，歡迎進一步調整配方。")
else:
    for s in suggestions:
        st.warning(s)
