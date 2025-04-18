
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.0 🍪（升級：推薦原料 + 優化配方記錄）")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔧 原始配方輸入（比例總和必須為100%）")
egg_pct = st.slider("蛋液比例 (%)", 0, 100, 10, step=1)
sugar_total_pct = st.slider("總糖比例 (%)（含蔗糖與麥芽漿）", 0, 100, 30, step=1)
flour_pct = st.slider("低筋麵粉比例 (%)", 0, 100, 40, step=1)
malt_pct = st.slider("麥芽漿比例 (%)", 0, 100, 10, step=1)
water_pct = st.slider("水比例 (%)", 0, 100, 10, step=1)

target_goals = st.multiselect(
    "🎯 想達成的健康訴求",
    ["高蛋白", "減糖", "高纖", "低GI", "熱量控制"]
)

total_pct = egg_pct + sugar_total_pct + flour_pct + malt_pct + water_pct
if total_pct != 100:
    st.error(f"⚠️ 原料總比例為 {total_pct}%，請調整為100%")
    st.stop()

st.header("🍬 糖系調配模組（糖總量組成比例）")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sucrose_ratio = st.number_input("蔗糖 (%)", 0, 100, 70)
with col2:
    erythritol_ratio = st.number_input("赤藻糖醇 (%)", 0, 100, 20)
with col3:
    monk_ratio = st.number_input("羅漢果糖 (%)", 0, 100, 5)
with col4:
    syrup_ratio = st.number_input("轉化糖漿 (%)", 0, 100, 5)

sugar_blend_total = sucrose_ratio + erythritol_ratio + monk_ratio + syrup_ratio
if sugar_blend_total != 100:
    st.error("⚠️ 糖系組成比例總和需為100%")
    st.stop()

cookie_weight = st.number_input("每片餅乾重量 (g)", min_value=1.0, max_value=50.0, value=8.2)

if st.button("🚀 執行模擬與優化"):
    # 營養參數
    egg_protein_rate = 0.125
    egg_fat_rate = 0.10
    flour_protein_rate = 0.10
    flour_fiber_rate = 0.08

    kcal_fat = 9
    kcal_sugar = 4
    kcal_erythritol = 0.2
    kcal_monk = 0
    kcal_protein = 3.5
    kcal_flour = 3.6
    kcal_fiber = 2
    kcal_egg = 1.4
    kcal_syrup = 3.2

    protein_g = round(cookie_weight * ((egg_pct/100)*egg_protein_rate + (flour_pct/100)*flour_protein_rate), 2)
    fiber_g = round(cookie_weight * ((flour_pct/100)*flour_fiber_rate), 2)
    sugar_g = round(cookie_weight * (sugar_total_pct/100) * ((sucrose_ratio + syrup_ratio)/100), 2)
    fat_g = round(cookie_weight * ((egg_pct/100)*egg_fat_rate), 2)
    sat_fat_g = round(fat_g * 0.3, 2)
    sodium_mg = round(cookie_weight * (7 / 8.2), 1)

    kcal_total = round(cookie_weight * (
        (egg_pct/100)*kcal_egg +
        (flour_pct/100)*kcal_flour +
        (sugar_total_pct/100)*(sucrose_ratio/100*kcal_sugar + erythritol_ratio/100*kcal_erythritol + monk_ratio/100*kcal_monk + syrup_ratio/100*kcal_syrup) +
        (egg_pct/100)*egg_fat_rate*kcal_fat
    ), 1)

    st.header("📊 模擬結果（含營養標示）")
    st.markdown(f'''
- 每片重量: {cookie_weight} g  
- 蛋白質: {protein_g} g  
- 膳食纖維: {fiber_g} g  
- 總糖: {sugar_g} g  
- 脂肪: {fat_g} g (飽和脂肪: {sat_fat_g} g)  
- 熱量: {kcal_total} kcal  
- 鈉: {sodium_mg} mg
''')

    st.subheader("🍬 糖系組成分析")
    st.markdown(f'''
- 蔗糖: {round(sugar_total_pct * sucrose_ratio / 100, 1)}%  
- 赤藻糖醇: {round(sugar_total_pct * erythritol_ratio / 100, 1)}%  
- 羅漢果糖: {round(sugar_total_pct * monk_ratio / 100, 1)}%  
- 轉化糖漿: {round(sugar_total_pct * syrup_ratio / 100, 1)}%
''')

    st.subheader("🎯 感官預測指數（1～5★）")
    hardness = min(5, max(1, round((flour_pct + malt_pct) / 20)))
    sweetness = min(5, max(1, round(sugar_total_pct * (sucrose_ratio/100 + 0.7*erythritol_ratio/100 + 1.5*monk_ratio/100) / 15)))
    aroma = min(5, max(1, round(egg_pct / 20)))
    color = min(5, max(1, round(sugar_total_pct * (sucrose_ratio + syrup_ratio) / 100 / 10)))
    moist = min(5, max(1, round((egg_pct + syrup_ratio*sugar_total_pct/100) / 15)))
    grain = min(5, max(1, round((flour_pct + malt_pct) / 20)))

    st.markdown(f'''
- 硬度: {'★'*hardness + '☆'*(5-hardness)}  
- 甜味: {'★'*sweetness + '☆'*(5-sweetness)}  
- 奶油香氣: {'★'*aroma + '☆'*(5-aroma)}  
- 上色: {'★'*color + '☆'*(5-color)}  
- 潤口度: {'★'*moist + '☆'*(5-moist)}  
- 穀物香: {'★'*grain + '☆'*(5-grain)}  
''')

    st.header("🧠 AI 健康優化建議與推薦原料")

    notes = []
    optimized = {"蛋液": egg_pct, "糖": sugar_total_pct, "低筋麵粉": flour_pct, "麥芽漿": malt_pct, "水": water_pct}

    if "減糖" in target_goals and sugar_total_pct > 20:
        optimized["糖"] = 20
        notes.append(f"建議將總糖從 {sugar_total_pct}% 降至 20%，並搭配赤藻糖醇與羅漢果糖調整甜度")

    if "高蛋白" in target_goals and protein_g < 1.0:
        new_egg = min(30, round((1.0 / cookie_weight) / egg_protein_rate * 100, 1))
        optimized["蛋液"] = new_egg
        notes.append(f"蛋白質過低，建議蛋液提高至 {new_egg}%，或添加豌豆蛋白 5–10%")

    if "高纖" in target_goals and fiber_g < 1.0:
        optimized["低筋麵粉"] = min(optimized["低筋麵粉"] + 10, 80)
        notes.append("膳食纖維偏低，建議添加 5–7% 難消化麥芽糊精或全麥粉")

    if "熱量控制" in target_goals and kcal_total > 40:
        notes.append("熱量偏高，建議減少糖與油脂來源")

    if "低GI" in target_goals and sucrose_ratio > 50:
        notes.append("蔗糖比例偏高，建議提高赤藻糖醇與羅漢果糖比例")

    total_opt = sum(optimized.values())
    optimized = {k: round(v/total_opt*100,1) for k,v in optimized.items()}

    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {v}%")

    if notes:
        st.info("🔎 系統建議：")
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方符合所有健康目標！")

    st.session_state.history.append({
        "蛋液": egg_pct,
        "糖": sugar_total_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct,
        "蛋白質 (g)": protein_g,
        "膳食纖維 (g)": fiber_g,
        "總糖 (g)": sugar_g,
        "脂肪 (g)": fat_g,
        "飽和脂肪 (g)": sat_fat_g,
        "熱量 (kcal)": kcal_total,
        "鈉 (mg)": sodium_mg,
        "優化_蛋液": optimized["蛋液"],
        "優化_糖": optimized["糖"],
        "優化_低筋麵粉": optimized["低筋麵粉"],
        "優化_麥芽漿": optimized["麥芽漿"],
        "優化_水": optimized["水"]
    })

if st.session_state.history:
    st.subheader("🗂️ 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
