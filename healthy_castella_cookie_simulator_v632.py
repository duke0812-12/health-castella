
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.3.2 🍪（修正縮排 + AI建議 + 營養映射）")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔧 原始配方輸入（總和 = 100%）")
egg_pct = st.slider("蛋液 (%)", 0, 100, 45)
sugar_pct = st.slider("糖 (%)", 0, 100, 40)
flour_pct = st.slider("低筋麵粉 (%)", 0, 100, 10)
malt_pct = st.slider("麥芽漿 (%)", 0, 100, 3)
water_pct = st.slider("水 (%)", 0, 100, 2)

total_pct = egg_pct + sugar_pct + flour_pct + malt_pct + water_pct
if total_pct != 100:
    st.error(f"⚠️ 原料總和為 {total_pct}%，請調整為100%")
    st.stop()

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

    # 使用者產品組成比例（總和100%）
    reference_ratio = {
        "蛋液": 45,
        "糖": 40,
        "低筋麵粉": 10,
        "麥芽漿": 3,
        "水": 2
    }

    # 使用者產品營養標示（每8.2g）
    actual_nutrition = {
        "熱量": 35.4,
        "蛋白質": 0.7,
        "脂肪": 0.7,
        "糖": 4.1,
        "鈉": 7
    }

    unit_nutrition = {k: v / 8.2 for k, v in actual_nutrition.items()}
    per_ingredient = {k: {n: (unit_nutrition[n] * (reference_ratio[k] / 100)) for n in unit_nutrition} for k in reference_ratio}

    def estimate_nutrition(weight, ratio_dict):
        result = {k: 0 for k in actual_nutrition}
        for ing, pct in ratio_dict.items():
            for nutrient in result:
                result[nutrient] += per_ingredient[ing][nutrient] * pct / 100 * weight
        return {k: round(v, 2) for k, v in result.items()}

    predicted = estimate_nutrition(cookie_weight, {
        "蛋液": egg_pct,
        "糖": sugar_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct
    })

    st.header(f"📊 模擬營養標示（每片 {cookie_weight}g）")
    for k, v in predicted.items():
        st.markdown(f"- {k}：{v} {'kcal' if k=='熱量' else 'g' if k!='鈉' else 'mg'}")

    # AI 建議與比例調整
    st.header("🧠 AI 建議與具體比例調整")
    optimized = {
        "蛋液": egg_pct,
        "糖": sugar_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct
    }
    notes = []

    def apply_adjustment(target_name, new_value, reduce_from=["糖", "水", "麥芽漿"]):
        original = optimized[target_name]
        delta = new_value - original
        if delta <= 0:
            return
        optimized[target_name] = new_value
        notes.append(f"✅ 將【{target_name}】由 {original}% ➜ 提升至 {new_value}%")
        for source in reduce_from:
            if source != target_name and optimized[source] > 0:
                deduction = min(delta, optimized[source])
                optimized[source] -= deduction
                delta -= deduction
                notes.append(f"  ⮕ 從【{source}】扣減 {deduction}%")
                if delta <= 0:
                    break
        if delta > 0:
            notes.append(f"⚠️ 尚需補足 {delta}% 來完成【{target_name}】的比例提升")

    if "減糖" in target_goals and optimized["糖"] > 25:
        apply_adjustment("糖", 25)
    if "高蛋白" in target_goals and predicted["蛋白質"] < 1.2:
        apply_adjustment("蛋液", egg_pct + 5)
    if "高纖" in target_goals and optimized["低筋麵粉"] < 15:
        apply_adjustment("低筋麵粉", flour_pct + 5)
    if "熱量控制" in target_goals and predicted["熱量"] > 45:
        apply_adjustment("水", water_pct + 5)
    if "低GI" in target_goals and sucrose_ratio > 50:
        notes.append("🔁 建議降低蔗糖比例至50%以下，提升赤藻糖醇／羅漢果糖比例")

    total_opt = sum(optimized.values())
    if total_opt != 100:
        gap = round(total_opt - 100, 1)
        for s in ["水", "糖", "麥芽漿"]:
            if optimized[s] - gap >= 0:
                optimized[s] -= gap
                notes.append(f"🔧 自動從【{s}】扣減 {gap}% 以平衡總和")
                break

    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {round(v, 1)}%")
    if notes:
        st.info("🔎 調整建議")
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方已符合健康目標！")
