
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v5.7 🍪（營養標示模擬引擎）")

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

    # 萃取營養係數（平均估值）
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

    # 蛋白質與膳食纖維
    protein_g = round(cookie_weight * (
        (pea_protein_pct / 100) * pea_protein_rate +
        (egg_pct / 100) * egg_protein_rate +
        (base_flour_pct / 100) * flour_protein_rate
    ), 2)
    fiber_g = round(cookie_weight * (
        (base_flour_pct / 100) * flour_fiber_rate +
        (fiber_pct / 100) * fiber_fiber_rate
    ), 2)

    # 糖類含量（不含赤藻糖醇與羅漢果糖）
    sugar_g = round(cookie_weight * (sugar_total_pct / 100) *
        (sucrose_ratio + syrup_ratio) / 100, 2)

    # 熱量計算
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

    # 脂肪與飽和脂肪估算
    fat_g = round(cookie_weight * ((fat_pct / 100) + (egg_pct / 100 * 0.10)), 2)
    sat_fat_g = round(fat_g * 0.3, 2)

    # 鈉含量估值（預設每10g含鹽0.1g = 鈉約 40mg）
    sodium_mg = 40

    st.header("📊 營養標示模擬結果（每片 10g）")
    st.markdown(f'''
    熱量：**{kcal_total} kcal**  
    蛋白質：**{protein_g} g**  
    脂肪：**{fat_g} g**（飽和脂肪：**{sat_fat_g} g**）  
    碳水化合物：**{round(sugar_g + fiber_g, 2)} g**  
      糖：**{sugar_g} g**  
      膳食纖維：**{fiber_g} g**  
    鈉：**{sodium_mg} mg**
    ''')

    st.success("✅ 成功模擬每片餅乾完整營養標示資訊！")
