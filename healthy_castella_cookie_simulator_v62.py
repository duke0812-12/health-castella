
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.2 🍪（全功能整合）")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔧 原始配方輸入（總和 = 100%）")
egg_pct = st.slider("蛋液 (%)", 0, 100, 10)
sugar_pct = st.slider("糖總量 (%)", 0, 100, 36)
flour_pct = st.slider("低筋麵粉 (%)", 0, 100, 36)
malt_pct = st.slider("麥芽漿 (%)", 0, 100, 9)
water_pct = st.slider("水 (%)", 0, 100, 9)

total_pct = egg_pct + sugar_pct + flour_pct + malt_pct + water_pct
if total_pct != 100:
    st.error(f"⚠️ 原料總和為 {total_pct}%，請調整為100%")
    st.stop()

# 糖系模組
st.header("🍬 糖系調配模組（糖總量的組成）")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sucrose_ratio = st.number_input("蔗糖 %", 0, 100, 70)
with col2:
    erythritol_ratio = st.number_input("赤藻糖醇 %", 0, 100, 20)
with col3:
    monk_ratio = st.number_input("羅漢果糖 %", 0, 100, 5)
with col4:
    syrup_ratio = st.number_input("轉化糖漿 %", 0, 100, 5)

sugar_blend_total = sucrose_ratio + erythritol_ratio + monk_ratio + syrup_ratio
if sugar_blend_total != 100:
    st.error("⚠️ 糖系組成總和需為100%")
    st.stop()

cookie_weight = st.number_input("每片餅乾重量 (g)", min_value=1.0, max_value=50.0, value=10.0)
target_goals = st.multiselect(
    "🎯 想達成的健康訴求",
    ["高蛋白", "減糖", "高纖", "低GI", "熱量控制"]
)

if st.button("🚀 執行模擬"):

    # 營養參數定義
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

    # 模擬營養計算
    protein_g = round(cookie_weight * ((egg_pct/100)*egg_protein_rate + (flour_pct/100)*flour_protein_rate), 2)
    fiber_g = round(cookie_weight * ((flour_pct/100)*flour_fiber_rate), 2)
    sugar_g = round(cookie_weight * (sugar_pct/100) * ((sucrose_ratio + syrup_ratio)/100), 2)
    fat_g = round(cookie_weight * ((egg_pct/100)*egg_fat_rate), 2)
    sat_fat_g = round(fat_g * 0.3, 2)
    sodium_mg = round(cookie_weight * (7 / 8.2), 1)

    kcal_total = round(cookie_weight * (
        (egg_pct/100)*kcal_egg +
        (flour_pct/100)*kcal_flour +
        (sugar_pct/100)*(sucrose_ratio/100*kcal_sugar + erythritol_ratio/100*kcal_erythritol + monk_ratio/100*kcal_monk + syrup_ratio/100*kcal_syrup) +
        (egg_pct/100)*egg_fat_rate*kcal_fat
    ), 1)

    # 顯示營養標示
    st.header("📊 營養標示模擬結果")
    st.markdown(f'''
- 熱量：{kcal_total} kcal  
- 蛋白質：{protein_g} g  
- 脂肪：{fat_g} g（飽和脂肪：{sat_fat_g} g）  
- 碳水化合物：{round(sugar_g + fiber_g, 2)} g  
   糖：{sugar_g} g  
   膳食纖維：{fiber_g} g  
- 鈉：{sodium_mg} mg
''')

    # 感官預測
    st.subheader("🌟 感官預測指數（★）")
    hardness = min(5, max(1, round((flour_pct + malt_pct) / 20)))
    sweetness = min(5, max(1, round(sugar_pct * (sucrose_ratio/100 + 0.7*erythritol_ratio/100 + 1.5*monk_ratio/100) / 15)))
    aroma = min(5, max(1, round(egg_pct / 20)))
    color = min(5, max(1, round(sugar_pct * (sucrose_ratio + syrup_ratio) / 100 / 10)))
    moist = min(5, max(1, round((egg_pct + syrup_ratio*sugar_pct/100) / 15)))
    grain = min(5, max(1, round((flour_pct + malt_pct) / 20)))

    st.markdown(f'''
- 硬度：{'★'*hardness + '☆'*(5-hardness)}  
- 甜味：{'★'*sweetness + '☆'*(5-sweetness)}  
- 奶香：{'★'*aroma + '☆'*(5-aroma)}  
- 上色：{'★'*color + '☆'*(5-color)}  
- 潤口感：{'★'*moist + '☆'*(5-moist)}  
- 穀香：{'★'*grain + '☆'*(5-grain)}  
''')

    # 優化建議（具體比例 + 扣減來源）
    st.header("🧠 AI 健康建議與具體比例調整")

    original = {
        "蛋液": egg_pct,
        "糖": sugar_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct
    }
    optimized = original.copy()
    notes = []

    def adjust_and_note(name, new_value, reduce_from=["水", "糖"]):
        delta = new_value - optimized[name]
        if delta <= 0:
            return
        optimized[name] = new_value
        for source in reduce_from:
            if source != name and optimized[source] > 0:
                deduct = min(delta, optimized[source])
                optimized[source] -= deduct
                delta -= deduct
                notes.append(f"建議將【{name}】由 {original[name]}% ➜ **{new_value}%**，"
                             f"將【{source}】由 {original[source]}% ➜ **{optimized[source]}%**")
                if delta <= 0:
                    break
        if delta > 0:
            notes.append(f"⚠️ 尚缺 {delta}% 來提升【{name}】，請手動調整")

    if "減糖" in target_goals and sugar_pct > 30:
        adjust_and_note("糖", 30)

    if "高蛋白" in target_goals and protein_g < 1.0:
        adjust_and_note("蛋液", 15)

    if "高纖" in target_goals and fiber_g < 1.0:
        adjust_and_note("低筋麵粉", flour_pct + 5)

    if "熱量控制" in target_goals and kcal_total > 45:
        adjust_and_note("水", water_pct + 5)

    if "低GI" in target_goals and sucrose_ratio > 50:
        notes.append("建議降低蔗糖比例，增加赤藻糖醇／羅漢果糖以降低GI值")

    # 優化後平衡處理
    total_opt = sum(optimized.values())
    if total_opt != 100:
        diff = round(total_opt - 100, 1)
        for source in ["水", "糖", "麥芽漿"]:
            if source in optimized and optimized[source] - diff >= 0:
                optimized[source] -= diff
                notes.append(f"總和為 {total_opt}% ➜ 自動從【{source}】扣除 {diff}% 以平衡")
                break

    # 顯示優化後配方
    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {round(v,1)}%")

    if notes:
        st.info("🔎 系統具體建議")
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方符合所有健康目標！")

    # 儲存歷史紀錄
    record = {
        "原_蛋液": egg_pct, "原_糖": sugar_pct, "原_低筋麵粉": flour_pct,
        "原_麥芽漿": malt_pct, "原_水": water_pct,
        "優_蛋液": optimized["蛋液"], "優_糖": optimized["糖"],
        "優_低筋麵粉": optimized["低筋麵粉"], "優_麥芽漿": optimized["麥芽漿"], "優_水": optimized["水"],
        "熱量": kcal_total, "蛋白質": protein_g, "纖維": fiber_g, "糖": sugar_g,
        "脂肪": fat_g, "飽和脂肪": sat_fat_g, "鈉": sodium_mg
    }
    st.session_state.history.append(record)

# 顯示歷史紀錄
if st.session_state.history:
    st.subheader("📂 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
