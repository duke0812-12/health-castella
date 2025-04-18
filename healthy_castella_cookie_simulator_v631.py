# v6.3.1 修正版初始化：將補上 AI 建議模組、比例建議、平衡扣減邏輯

    # AI 建議與具體調整
    st.header("🧠 AI 健康建議與具體比例調整")
    notes = []
    optimized = {
        "蛋液": egg_pct,
        "糖": sugar_pct,
        "低筋麵粉": flour_pct,
        "麥芽漿": malt_pct,
        "水": water_pct
    }

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

    # 總和平衡處理
    total_opt = sum(optimized.values())
    if total_opt != 100:
        gap = round(total_opt - 100, 1)
        for source in ["水", "糖", "麥芽漿"]:
            if source in optimized and optimized[source] - gap >= 0:
                optimized[source] -= gap
                notes.append(f"🔧 自動從【{source}】中扣減 {gap}% 以平衡總和 = 100%")
                break

    # 顯示優化後配方
    st.subheader("📘 優化後推薦配方（總和 = 100%）")
    for k, v in optimized.items():
        st.markdown(f"- {k}: {round(v, 1)}%")

    if notes:
        st.info("🔎 AI 建議與比例說明")
        for n in notes:
            st.markdown(f"- {n}")
    else:
        st.success("✅ 配方已達成健康目標且總和正確！")
