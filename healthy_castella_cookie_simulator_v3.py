
import streamlit as st

st.title("長崎蛋糕餅乾健康模擬器 v3 🍪")

st.header("🔧 原始配方輸入（總和為100%）")
base_flour_pct = st.slider("主粉體比例（低筋/全麥/裸麥/杏仁粉）", 10, 80, 40, step=1)
pea_protein_pct = st.slider("豌豆蛋白比例", 0, 30, 5, step=1)
fat_pct = st.slider("油脂比例", 0, 30, 18, step=1)
sweetener_pct = st.slider("甜味劑比例", 0, 30, 25, step=1)
egg_pct = st.slider("蛋液比例", 0, 30, 10, step=1)
fiber_pct = st.slider("膳食纖維比例", 0, 15, 2, step=1)

# 總量檢查
total_pct = base_flour_pct + pea_protein_pct + fat_pct + sweetener_pct + egg_pct + fiber_pct
st.markdown(f"**目前總配方比例：{total_pct}%**")
if total_pct != 100:
    st.error("⚠️ 原料總比例必須為100%，請調整比例")
    st.stop()

flour_type = st.selectbox("主粉體種類", ["低筋麵粉", "全麥粉", "裸麥粉", "杏仁粉"])
sweetener_type = st.selectbox("甜味劑種類", ["蔗糖", "赤藻糖醇", "阿洛酮糖", "甜菊糖"])
add_vitamins = st.checkbox("加入維生素強化")
target_goals = st.multiselect("🎯 想達成的健康訴求", ["高蛋白", "減糖", "高纖", "低GI", "營養素強化"])

# 預估營養與結果
st.header("📊 模擬結果預測")
protein_g = round(1.2 + pea_protein_pct * 0.3, 1)
fiber_g = round(fiber_pct * 0.2, 1)
sugar_level = "正常甜度" if sweetener_pct >= 20 else "減糖配方"
texture = "標準偏軟"
if pea_protein_pct > 10:
    texture = "偏硬"
if pea_protein_pct > 20:
    texture = "硬脆"

st.markdown(f'''
- **預測蛋白質含量**: {protein_g} g／片  
- **預測膳食纖維**: {fiber_g} g／片  
- **糖分水平**: {sugar_level}  
- **預測質地**: {texture}  
- **添加維生素**: {"是" if add_vitamins else "否"}  
''')

# 💡 優化建議區塊
st.header("🧠 健康配方優化建議")

# 初始建議列表
optimized = {
    "base_flour": "全麥粉 20% + 低筋麵粉 20%",
    "pea_protein": "10%",
    "fat": f"{fat_pct}%",
    "sweetener": "阿洛酮糖 10% + 赤藻糖醇 5%",
    "egg": "15%",
    "fiber": "5%",
    "vitamin_d": "0.005g（5mg）／100g",
    "vitamin_b": "0.015g（15mg）／100g"
}

if "減糖" in target_goals:
    st.markdown("- ✅ 建議將甜味劑由蔗糖25%降至 **阿洛酮糖10% + 赤藻糖醇5%**")
if "高蛋白" in target_goals:
    st.markdown("- ✅ 建議豌豆蛋白提升至 **10%**，以達到每片 >5g 蛋白")
if "高纖" in target_goals:
    st.markdown("- ✅ 建議膳食纖維添加至 **5%**，並選用 **β-葡聚醣、抗性糊精**")
if "低GI" in target_goals:
    st.markdown("- ✅ 建議選用低GI主粉（如 **全麥粉、裸麥粉**），減糖並加纖")
if "營養素強化" in target_goals and add_vitamins:
    st.markdown(f'''
- ✅ 建議添加以下維生素量（每100g成品）:
  - **維生素D**: {optimized["vitamin_d"]}
  - **維生素B群（綜合）**: {optimized["vitamin_b"]}
  - 建議依功能食品規範進行實驗驗證與營養標示。
''')

# 差異比較總結
st.subheader("📘 優化後推薦配方建議（總合100%）")
st.markdown(f'''
- 主粉體: {optimized["base_flour"]}  
- 豌豆蛋白: {optimized["pea_protein"]}  
- 油脂: {optimized["fat"]}  
- 甜味劑: {optimized["sweetener"]}  
- 蛋液: {optimized["egg"]}  
- 膳食纖維: {optimized["fiber"]}  
''')
if "營養素強化" in target_goals and add_vitamins:
    st.markdown("- 維生素D、B群強化已納入")
