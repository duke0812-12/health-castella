
import streamlit as st
import pandas as pd

st.title("長崎蛋糕餅乾健康模擬器 v6.1 🍪（具體比例建議 + 扣減來源 + 總和100%）")

if "history" not in st.session_state:
    st.session_state.history = []

# === 原始配方輸入 ===
st.header("🔧 原始配方輸入（總和 = 100%）")
egg_pct = st.slider("蛋液 (%)", 0, 100, 10)
sugar_pct = st.slider("糖 (%)", 0, 100, 36)
flour_pct = st.slider("低筋麵粉 (%)", 0, 100, 36)
malt_pct = st.slider("麥芽漿 (%)", 0, 100, 9)
water_pct = st.slider("水 (%)", 0, 100, 9)

total_pct = egg_pct + sugar_pct + flour_pct + malt_pct + water_pct
if total_pct != 100:
    st.error(f"⚠️ 原料總和為 {total_pct}%，請調整為100%")
    st.stop()

# === 模擬與建議 ===
if st.button("🚀 模擬並給出具體建議"):

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
            return  # 不需調整
        optimized[name] = new_value
        # 從指定來源依序扣除
        for source in reduce_from:
            if source != name and optimized[source] > 0:
                deduct = min(delta, optimized[source])
                optimized[source] -= deduct
                delta -= deduct
                notes.append(f"建議將【{name}】由 {original[name]}% ➜ **{new_value}%**，"
                             f"並將【{source}】由 {original[source]}% ➜ **{optimized[source]}%**")
                if delta <= 0:
                    break
        if delta > 0:
            notes.append(f"⚠️ 無法完全補足【{name}】的增加比例 {new_value}%（尚缺 {delta}%）")

    # === 建議模組（具體值） ===
    if sugar_pct > 30:
        adjust_and_note("糖", 30)

    if flour_pct < 35:
        adjust_and_note("低筋麵粉", 38)

    if water_pct > 5:
        notes.append(f"建議將【水】由 {water_pct}% ➜ **5%**，以避免過濕影響質地")
        optimized["水"] = 5
        notes.append(f"已將【水】比例下修至 5%，騰出 {water_pct - 5}% 供其他原料使用")

    if malt_pct < 10:
        adjust_and_note("麥芽漿", 10)

    # 最終修正總和
    total_final = sum(optimized.values())
    if total_final != 100:
        gap = round(total_final - 100, 1)
        # 自動從水或糖中微調補差
        for k in ["水", "糖"]:
            if k in optimized and optimized[k] - gap >= 0:
                optimized[k] -= gap
                notes.append(f"總和為 {total_final}%，系統自動從【{k}】中扣除 {gap}%")
                break

    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {round(v, 1)}%")

    st.info("🔎 系統具體建議：")
    for n in notes:
        st.markdown(f"- {n}")

    # 儲存紀錄
    record = {f"原始_{k}": v for k, v in original.items()}
    record.update({f"優化_{k}": round(v, 1) for k, v in optimized.items()})
    st.session_state.history.append(record)

# === 模擬紀錄 ===
if st.session_state.history:
    st.subheader("📊 模擬紀錄")
    st.dataframe(pd.DataFrame(st.session_state.history))
