
import streamlit as st
import pandas as pd

st.title("健康長崎蛋糕片模擬器 v6.0 🍰（原產品 + 升級建議客製版）")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("📦 現有產品初始值（已自動載入）")

st.markdown("### 🥚 現有產品原配方預估（每片 8.2g）")
st.markdown("""
- 雞蛋：約 20%
- 蔗糖：約 50%
- 低筋麵粉：約 28%
- 麥芽漿：約 2%
- 豌豆蛋白 / 膳食纖維 / 代糖：未添加
""")

st.markdown("### 💡 系統建議健康升級版配方（每片 10g 計算）")

default_values = {
    "主粉體": 35,
    "全麥粉": 10,
    "豌豆蛋白": 10,
    "蔗糖": 6,
    "赤藻糖醇": 6,
    "羅漢果糖": 3,
    "膳食纖維": 8,
    "蛋液": 12,
    "麥芽漿": 5,
    "水": 5
}

total = sum(default_values.values())
if total != 100:
    st.warning(f"⚠️ 預設比例總和為 {total}%，建議調整")

df = pd.DataFrame({
    "原料": list(default_values.keys()),
    "比例 (%)": list(default_values.values())
})

st.dataframe(df.set_index("原料"))

# 營養推估簡表
protein = round(10 * (default_values["豌豆蛋白"]/100*0.82 + default_values["蛋液"]/100*0.125 + default_values["主粉體"]/100*0.1 + default_values["全麥粉"]/100*0.12), 2)
fiber = round(10 * (default_values["主粉體"]/100*0.08 + default_values["全麥粉"]/100*0.10 + default_values["膳食纖維"]/100*0.9), 2)
sugar = round(10 * (default_values["蔗糖"]/100 + default_values["羅漢果糖"]/100 + default_values["麥芽漿"]/100*0.4), 2)
fat = round(10 * (default_values["蛋液"]/100*0.1), 2)
sat_fat = round(fat * 0.3, 2)
kcal = round(
    10 * (
        default_values["蛋液"]/100*1.4 +
        default_values["主粉體"]/100*3.6 +
        default_values["全麥粉"]/100*3.5 +
        default_values["豌豆蛋白"]/100*0.82*3.5 +
        default_values["蔗糖"]/100*4 +
        default_values["赤藻糖醇"]/100*0.2 +
        default_values["羅漢果糖"]/100*0 +
        default_values["膳食纖維"]/100*2 +
        default_values["麥芽漿"]/100*3.2
    ), 1)

st.markdown("### 🧾 預估營養標示（每片 10g）")
st.markdown(f'''
- 熱量: {kcal} kcal  
- 蛋白質: {protein} g  
- 脂肪: {fat} g（飽和脂肪: {sat_fat} g）  
- 碳水化合物: {round(sugar + fiber, 2)} g  
      糖: {sugar} g  
      膳食纖維: {fiber} g  
- 鈉: 15 mg
''')
