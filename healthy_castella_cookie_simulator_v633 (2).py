
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.3.3 🍪")

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

st.header("🍬 糖系調配模組")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sucrose_ratio = st.number_input("蔗糖 %", 0, 100, 70)
with col2:
    erythritol_ratio = st.number_input("赤藻糖醇 %", 0, 100, 20)
with col3:
    monk_ratio = st.number_input("羅漢果糖 %", 0, 100, 5)
with col4:
    syrup_ratio = st.number_input("轉化糖漿 %", 0, 100, 5)

if sucrose_ratio + erythritol_ratio + monk_ratio + syrup_ratio != 100:
    st.error("⚠️ 糖系比例總和需為100%")
    st.stop()

cookie_weight = st.number_input("餅乾單片重量 (g)", 1.0, 50.0, 10.0)
target_goals = st.multiselect("🎯 想達成的健康訴求", ["高蛋白", "減糖", "高纖", "低GI", "熱量控制"])

if st.button("🚀 執行模擬"):

    ref_ratio = {"蛋液": 45, "糖": 40, "低筋麵粉": 10, "麥芽漿": 3, "水": 2}
    ref_nutrition = {"熱量": 35.4, "蛋白質": 0.7, "脂肪": 0.7, "糖": 4.1, "鈉": 7}
    unit_nutrition = {k: v / 8.2 for k, v in ref_nutrition.items()}
    per_ingredient = {k: {n: unit_nutrition[n] * (ref_ratio[k]/100) for n in unit_nutrition} for k in ref_ratio}

    def estimate_nutrition(weight, ratio_dict):
        result = {k: 0 for k in ref_nutrition}
        for ing, pct in ratio_dict.items():
            for nutrient in result:
                result[nutrient] += per_ingredient[ing][nutrient] * pct / 100 * weight
        return {k: round(v, 2) for k, v in result.items()}

    input_ratio = {
        "蛋液": egg_pct,
        "糖": sugar_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct
    }

    predicted = estimate_nutrition(cookie_weight, input_ratio)

    st.header("📊 模擬營養標示（每片 {}g）".format(cookie_weight))
    for k, v in predicted.items():
        st.markdown(f"- {k}：{v}{' kcal' if k=='熱量' else ' g' if k!='鈉' else ' mg'}")

    st.header("🧠 AI 建議與調整")
    optimized = input_ratio.copy()
    notes = []

    def apply_adjust(name, new_val, from_sources=["糖", "水", "麥芽漿"]):
        delta = new_val - optimized[name]
        if delta <= 0: return
        optimized[name] = new_val
        notes.append(f"✅ 將【{name}】提升至 {new_val}%")
        for src in from_sources:
            if src != name and optimized[src] > 0:
                cut = min(delta, optimized[src])
                optimized[src] -= cut
                notes.append(f"  ⮕ 從【{src}】扣減 {cut}%")
                delta -= cut
                if delta <= 0: break

    if "減糖" in target_goals and optimized["糖"] > 25:
        apply_adjust("糖", 25)
    if "高蛋白" in target_goals and predicted["蛋白質"] < 1.2:
        apply_adjust("蛋液", optimized["蛋液"] + 5)
    if "高纖" in target_goals and optimized["低筋麵粉"] < 15:
        apply_adjust("低筋麵粉", optimized["低筋麵粉"] + 5)
    if "熱量控制" in target_goals and predicted["熱量"] > 45:
        apply_adjust("水", optimized["水"] + 5)

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
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方已符合健康目標")

    # 📋 模擬紀錄
    record = {
        "目標": ", ".join(target_goals),
        "原_蛋液": egg_pct, "原_糖": sugar_pct,
        "原_低筋麵粉": flour_pct, "原_麥芽漿": malt_pct, "原_水": water_pct,
        "優_蛋液": optimized["蛋液"], "優_糖": optimized["糖"],
        "優_低筋麵粉": optimized["低筋麵粉"], "優_麥芽漿": optimized["麥芽漿"], "優_水": optimized["水"],
        "熱量": predicted["熱量"], "蛋白質": predicted["蛋白質"],
        "脂肪": predicted["脂肪"], "糖": predicted["糖"], "鈉": predicted["鈉"]
    }
    st.session_state.history.append(record)

if st.session_state.history:
    st.subheader("📂 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
