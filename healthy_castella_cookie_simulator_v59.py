
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v5.8 🍪（全功能整合版）")

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔧 原始配方輸入（總和為100%）")
base_flour_pct = st.slider("主粉體比例", 10, 80, 40, step=1)
pea_protein_pct = st.slider("豌豆蛋白比例", 0, 30, 5, step=1)
fat_pct = st.slider("油脂比例", 0, 30, 18, step=1)
sugar_total_pct = st.slider("糖總比例", 0, 50, 25, step=1)
egg_pct = st.slider("蛋液比例", 0, 30, 10, step=1)
fiber_pct = st.slider("膳食纖維比例", 0, 15, 2, step=1)

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

cookie_weight = 10

if st.button("🚀 一鍵執行模擬"):
    total_pct = base_flour_pct + pea_protein_pct + fat_pct + sugar_total_pct + egg_pct + fiber_pct
    if total_pct != 100:
        st.error("⚠️ 原料總比例必須為100%，請調整比例")
        st.stop()

    # 營養參數（可擴充為資料庫）
    pea_protein_rate = 0.82
    egg_protein_rate = 0.125
    flour_protein_rate = 0.10
    flour_fiber_rate = 0.08
    fiber_fiber_rate = 0.90

    kcal_fat = 9
    kcal_sugar = 4
    kcal_erythritol = 0.2
    kcal_monk = 0
    kcal_protein = 3.5
    kcal_flour = 3.6
    kcal_fiber = 2
    kcal_egg = 1.4
    kcal_syrup = 3.2

    # 營養成分預測
    protein_g = round(cookie_weight * (
        (pea_protein_pct / 100) * pea_protein_rate +
        (egg_pct / 100) * egg_protein_rate +
        (base_flour_pct / 100) * flour_protein_rate
    ), 2)

    fiber_g = round(cookie_weight * (
        (base_flour_pct / 100) * flour_fiber_rate +
        (fiber_pct / 100) * fiber_fiber_rate
    ), 2)

    sugar_g = round(cookie_weight * (sugar_total_pct / 100) *
        (sucrose_ratio + syrup_ratio) / 100, 2)

    fat_g = round(cookie_weight * ((fat_pct / 100) + (egg_pct / 100 * 0.10)), 2)
    sat_fat_g = round(fat_g * 0.3, 2)
    sodium_mg = 40

    kcal_total = round(cookie_weight * (
        (fat_pct / 100) * kcal_fat +
        (pea_protein_pct / 100) * pea_protein_rate * kcal_protein +
        (egg_pct / 100) * kcal_egg +
        (base_flour_pct / 100) * kcal_flour +
        (fiber_pct / 100) * kcal_fiber +
        (sugar_total_pct / 100) * (
            sucrose_ratio / 100 * kcal_sugar +
            erythritol_ratio / 100 * kcal_erythritol +
            monk_ratio / 100 * kcal_monk +
            syrup_ratio / 100 * kcal_syrup
        )
    ), 1)

    st.header("📊 模擬結果預測（含營養標示）")
    st.markdown(f'''
    - **每片餅乾重量**: {cookie_weight} g  
    - **蛋白質含量（綜合）**: {protein_g} g  
    - **膳食纖維（綜合）**: {fiber_g} g  
    - **總糖（不含代糖）**: {sugar_g} g  
    - **脂肪：{fat_g} g（飽和脂肪：{sat_fat_g} g）**  
    - **熱量：{kcal_total} kcal**  
    - **鈉含量：{sodium_mg} mg**
    ''')

    st.subheader("🍬 糖系組成分析")
    st.markdown(f'''
    - 蔗糖：{round(sugar_total_pct * sucrose_ratio / 100, 1)}%  
    - 赤藻糖醇：{round(sugar_total_pct * erythritol_ratio / 100, 1)}%  
    - 羅漢果糖：{round(sugar_total_pct * monk_ratio / 100, 1)}%  
    - 轉化糖漿：{round(sugar_total_pct * syrup_ratio / 100, 1)}%  
    ''')

    # 感官預測
    st.subheader("🎯 感官預測指數（1～5★）")
    hardness = min(5, max(1, round((pea_protein_pct + fiber_pct) / 6)))
    sweetness = min(5, max(1, round((sugar_total_pct * (sucrose_ratio/100 + 0.7 * erythritol_ratio/100 + 1.5 * monk_ratio/100)) / 10)))
    aroma = min(5, max(1, round(fat_pct / 6)))
    color = min(5, max(1, round((sugar_total_pct * (sucrose_ratio + syrup_ratio) / 100) / 6)))
    moist = min(5, max(1, round((egg_pct + syrup_ratio * sugar_total_pct / 100) / 6)))
    grain = min(5, max(1, round((base_flour_pct + fiber_pct) / 20)))

    st.markdown(f'''
    - 硬度：{"★"*hardness + "☆"*(5-hardness)}  
    - 甜味強度：{"★"*sweetness + "☆"*(5-sweetness)}  
    - 奶油香氣：{"★"*aroma + "☆"*(5-aroma)}  
    - 上色程度：{"★"*color + "☆"*(5-color)}  
    - 潤口保濕感：{"★"*moist + "☆"*(5-moist)}  
    - 穀物香味：{"★"*grain + "☆"*(5-grain)}  
    ''')

    # 智慧建議
    st.header("🧠 AI 動態健康優化建議")
    notes = []
    optimized = {
        "base_flour": base_flour_pct,
        "pea_protein": pea_protein_pct,
        "fat": fat_pct,
        "sugar": sugar_total_pct,
        "egg": egg_pct,
        "fiber": fiber_pct
    }

    if "減糖" in target_goals and sugar_total_pct > 20:
        optimized["sugar"] = 15
        notes.append(f"建議將糖分從 {sugar_total_pct}% 降至 15%，可改用赤藻糖醇與羅漢果糖調和。")
    if "高蛋白" in target_goals and protein_g < 5:
        optimized["pea_protein"] = min(30, round((5 / cookie_weight) / pea_protein_rate * 100, 1))
        notes.append(f"目前蛋白質 {protein_g}g，建議豌豆蛋白提高至 {optimized['pea_protein']}%。")
    if "高纖" in target_goals and fiber_g < 1.5:
        optimized["fiber"] = max(optimized["fiber"], 5)
        notes.append("膳食纖維偏低，建議膳食纖維提升至 5%。")
    if "低GI" in target_goals and sucrose_ratio > 50:
        notes.append("蔗糖比例高，建議提升赤藻糖醇與羅漢果糖比例以降低GI。")
    if moist <= 2:
        optimized["egg"] = min(optimized["egg"] + 3, 20)
        notes.append(f"潤口度偏低，建議提升蛋液至 {optimized['egg']}%。")

    # 總和調整至100%
    total_opt = sum(optimized.values())
    optimized = {k: round(v / total_opt * 100, 1) for k, v in optimized.items()}

    st.subheader("📘 優化後推薦配方（比例總和 = 100%）")
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

    if notes:
        st.info("🔎 系統建議：")
        for note in notes:
            st.markdown(f"- {note}")
    else:
        st.success("✅ 您目前的配方已符合設定目標！")

    # 儲存紀錄（包含所有參數與預測結果）
    st.session_state.history.append({
        "主粉體": base_flour_pct,
        "豌豆蛋白": pea_protein_pct,
        "油脂": fat_pct,
        "糖": sugar_total_pct,
        "蛋液": egg_pct,
        "膳食纖維": fiber_pct,
        "蛋白g": protein_g,
        "纖維g": fiber_g,
        "脂肪g": fat_g,
        "飽和脂肪g": sat_fat_g,
        "總糖g": sugar_g,
        "熱量kcal": kcal_total,
        "鈉mg": sodium_mg,
        "糖_蔗糖": round(sugar_total_pct * sucrose_ratio / 100, 1),
        "糖_赤藻糖醇": round(sugar_total_pct * erythritol_ratio / 100, 1),
        "糖_羅漢果糖": round(sugar_total_pct * monk_ratio / 100, 1),
        "糖_轉化糖漿": round(sugar_total_pct * syrup_ratio / 100, 1),
        "硬度": hardness,
        "甜感": sweetness,
        "奶香": aroma,
        "上色": color,
        "保濕": moist,
        "穀香": grain
    })

# 顯示模擬紀錄表格
if st.session_state.history:
    st.subheader("🗂️ 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
