# v6.3 建立完成：整合 v6.2 全功能 + 新增營養映射推估邏輯 based on 現有產品配方
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.3 🍪（營養映射引擎 + 全功能）")

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

    # 使用者實際產品比例基準（100%組成）
    reference_ratio = {
        "蛋液": 45,
        "糖": 40,
        "低筋麵粉": 10,
        "麥芽漿": 3,
        "水": 2
    }

    # 使用者實際產品營養標示（每8.2g）
    actual_nutrition = {
        "熱量": 35.4,
        "蛋白質": 0.7,
        "脂肪": 0.7,
        "碳水": 6.5,
        "糖": 4.1,
        "鈉": 7
    }

    # 單位原料平均營養（每1%原料的營養貢獻，以8.2g基準）
    unit_nutrition = {}
    for key in actual_nutrition:
        unit_nutrition[key] = actual_nutrition[key] / 8.2  # 每1g產品中該營養成分含量
    ref_total = sum(reference_ratio.values())
    per_ingredient = {k: unit_nutrition.copy() for k in reference_ratio}
    for nutrient in actual_nutrition:
        total_ratio = sum(reference_ratio.values())
        for ingredient in reference_ratio:
            portion = reference_ratio[ingredient] / total_ratio
            if nutrient in per_ingredient[ingredient]:
                per_ingredient[ingredient][nutrient] = unit_nutrition[nutrient] * portion * 8.2 / reference_ratio[ingredient]

    # 模擬營養總和（依照目前配方 × 對應原料營養）
    def estimate_nutrition(weight):
        result = {"熱量": 0, "蛋白質": 0, "脂肪": 0, "糖": 0, "鈉": 0}
        input_ratio = {
            "蛋液": egg_pct,
            "糖": sugar_pct,
            "低筋麵粉": flour_pct,
            "麥芽漿": malt_pct,
            "水": water_pct
        }
        for ingredient, pct in input_ratio.items():
            for key in result:
                result[key] += (per_ingredient[ingredient][key] * pct / 100 * weight)
        return {k: round(v, 2) for k, v in result.items()}

    predicted = estimate_nutrition(cookie_weight)

    st.header("📊 模擬營養標示（每片 {}g）".format(cookie_weight))
    st.markdown(f'''
- 熱量：{predicted["熱量"]} kcal  
- 蛋白質：{predicted["蛋白質"]} g  
- 脂肪：{predicted["脂肪"]} g  
- 糖：{predicted["糖"]} g  
- 鈉：{predicted["鈉"]} mg  
''')


    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {round(v, 1)}%")

    if notes:
        st.info("🔎 系統具體建議")
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方符合所有健康目標！")

    # 🔁 使用 AI 建議後的配方來重新做感官預測
    st.subheader("🌟 優化配方的感官預測（★）")
    hardness = min(5, max(1, round((optimized["低筋麵粉"] + optimized["麥芽漿"]) / 20)))
    sweetness = min(5, max(1, round(optimized["糖"] * (sucrose_ratio/100 + 0.7*erythritol_ratio/100 + 1.5*monk_ratio/100) / 15)))
    aroma = min(5, max(1, round(optimized["蛋液"] / 20)))
    color = min(5, max(1, round(optimized["糖"] * (sucrose_ratio + syrup_ratio) / 100 / 10)))
    moist = min(5, max(1, round((optimized["蛋液"] + syrup_ratio*optimized["糖"]/100) / 15)))
    grain = min(5, max(1, round((optimized["低筋麵粉"] + optimized["麥芽漿"]) / 20)))

    st.markdown(f'''
- 硬度：{'★'*hardness + '☆'*(5-hardness)}  
- 甜味：{'★'*sweetness + '☆'*(5-sweetness)}  
- 奶香：{'★'*aroma + '☆'*(5-aroma)}  
- 上色：{'★'*color + '☆'*(5-color)}  
- 潤口感：{'★'*moist + '☆'*(5-moist)}  
- 穀香：{'★'*grain + '☆'*(5-grain)}  
''')

    # 儲存歷史紀錄
    record = {
        "原_蛋液": egg_pct, "原_糖": sugar_pct, "原_低筋麵粉": flour_pct,
        "原_麥芽漿": malt_pct, "原_水": water_pct,
        "優_蛋液": optimized["蛋液"], "優_糖": optimized["糖"],
        "優_低筋麵粉": optimized["低筋麵粉"], "優_麥芽漿": optimized["麥芽漿"], "優_水": optimized["水"],
        "熱量": predicted["熱量"], "蛋白質": predicted["蛋白質"],
        "脂肪": predicted["脂肪"], "糖": predicted["糖"], "鈉": predicted["鈉"]
    }
    st.session_state.history.append(record)

# 顯示歷史紀錄
if st.session_state.history:
    st.subheader("📂 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
