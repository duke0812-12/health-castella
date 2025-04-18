# v6.3.3 模擬紀錄版本初始化：將加入歷史記錄功能

    # ⏺ 模擬紀錄儲存
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

# 顯示模擬歷史紀錄
if st.session_state.history:
    st.subheader("📂 模擬紀錄")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)
