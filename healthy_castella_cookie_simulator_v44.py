
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v4.4 🍪")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔧 原始配方輸入（總和為100%）")
base_flour_pct = st.slider("主粉體比例（低筋/全麥/裸麥/杏仁粉）", 10, 80, 40, step=1)
pea_protein_pct = st.slider("豌豆蛋白比例", 0, 30, 5, step=1)
fat_pct = st.slider("油脂比例", 0, 30, 18, step=1)
sugar_total_pct = st.slider("糖總比例", 0, 50, 25, step=1)
egg_pct = st.slider("蛋液比例", 0, 30, 10, step=1)
fiber_pct = st.slider("膳食纖維比例", 0, 15, 2, step=1)

flour_type = st.selectbox("主粉體種類", ["低筋麵粉", "全麥粉", "裸麥粉", "杏仁粉"])
add_vitamins = st.checkbox("加入維生素強化")
target_goals = st.multiselect("🎯 想達成的健康訴求", ["高蛋白", "減糖", "高纖", "低GI", "營養素強化"])

# 糖系調配模組
st.header("🍬 糖系調配模組（糖總量的組成比例）")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sucrose_ratio = st.number_input("蔗糖 %", 0, 100, 50)
with col2:
    erythritol_ratio = st.number_input("赤藻糖醇 %", 0, 100, 20)
with col3:
    monk_ratio = st.number_input("羅漢果糖 %", 0, 100, 20)
with col4:
    syrup_ratio = st.number_input("轉化糖漿 %", 0, 100, 10)

sugar_blend_total = sucrose_ratio + erythritol_ratio + monk_ratio + syrup_ratio
if sugar_blend_total != 100:
    st.error("⚠️ 糖系組成比例總和需為100%")
    st.stop()

# 每片餅乾重量（固定10g）
cookie_weight = 10

if st.button("🚀 一鍵執行模擬"):
    total_pct = base_flour_pct + pea_protein_pct + fat_pct + sugar_total_pct + egg_pct + fiber_pct
    if total_pct != 100:
        st.error("⚠️ 原料總比例必須為100%，請調整比例")
        st.stop()

    st.header("📊 模擬結果預測")
    protein_g = round(cookie_weight * (pea_protein_pct / 100) * 0.3, 2)
    fiber_g = round(cookie_weight * (fiber_pct / 100) * 0.2, 2)
    sugar_level = "高糖配方" if sugar_total_pct > 30 else "正常或減糖配方"
    texture = "標準偏軟"
    if pea_protein_pct > 10:
        texture = "偏硬"
    if pea_protein_pct > 20:
        texture = "硬脆"

    st.markdown(f'''
    - **每片餅乾重量**: {cookie_weight} g  
    - **每片蛋白質含量**: {protein_g} g  
    - **每片膳食纖維**: {fiber_g} g  
    - **糖分水平**: {sugar_level}  
    - **預測質地**: {texture}  
    - **添加維生素**: {"是" if add_vitamins else "否"}  
    ''')

    st.subheader("🍬 糖系組成分析")
    st.markdown(f'''
    - 蔗糖：{round(sugar_total_pct * sucrose_ratio / 100, 1)}%  
    - 赤藻糖醇：{round(sugar_total_pct * erythritol_ratio / 100, 1)}%  
    - 羅漢果糖：{round(sugar_total_pct * monk_ratio / 100, 1)}%  
    - 轉化糖漿：{round(sugar_total_pct * syrup_ratio / 100, 1)}%  
    ''')

    st.header("🧠 健康配方優化建議（比例總和 = 100%）")
    optimized = {
        "base_flour": 35,
        "pea_protein": 10,
        "fat": 18,
        "sugar": 15,
        "egg": 15,
        "fiber": 7
    }
    opt_total = sum(optimized.values())
    optimized = {k: round(v / opt_total * 100, 1) for k, v in optimized.items()}

    for k, v in optimized.items():
        st.markdown(f"- {k}：{v}%")

    if "營養素強化" in target_goals and add_vitamins:
        st.markdown(f'''
        - ✅ 建議添加以下維生素量（每100g成品）:
          - **維生素D**: 0.005g（5mg）
          - **維生素B群（綜合）**: 0.015g（15mg）
        ''')

    st.subheader("📘 優化後配方比例統整（自動調整為100%）")
    for k, v in optimized.items():
        label = {
            "base_flour": "主粉體",
            "pea_protein": "豌豆蛋白",
            "fat": "油脂",
            "sugar": "糖",
            "egg": "蛋液",
            "fiber": "膳食纖維"
        }[k]
        st.markdown(f"- {label}: {v}%")

    # 儲存模擬紀錄
    st.session_state.history.append({
        "主粉體": base_flour_pct,
        "豌豆蛋白": pea_protein_pct,
        "油脂": fat_pct,
        "糖": sugar_total_pct,
        "蛋液": egg_pct,
        "膳食纖維": fiber_pct,
        "蛋白g": protein_g,
        "纖維g": fiber_g,
        "糖分": sugar_level,
        "質地": texture,
        "糖_蔗糖": round(sugar_total_pct * sucrose_ratio / 100, 1),
        "糖_赤藻糖醇": round(sugar_total_pct * erythritol_ratio / 100, 1),
        "糖_羅漢果糖": round(sugar_total_pct * monk_ratio / 100, 1),
        "糖_轉化糖漿": round(sugar_total_pct * syrup_ratio / 100, 1),
        "優化後_主粉體": optimized["base_flour"],
        "優化後_豌豆蛋白": optimized["pea_protein"],
        "優化後_油脂": optimized["fat"],
        "優化後_糖": optimized["sugar"],
        "優化後_蛋液": optimized["egg"],
        "優化後_膳食纖維": optimized["fiber"]
    })

# 顯示紀錄表格
if st.session_state.history:
    st.subheader("🗂️ 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
