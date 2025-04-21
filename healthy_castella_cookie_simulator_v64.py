# v6.4 智慧替代建議引擎版初始化：將新增針對健康訴求的多樣化原料替代建議

    st.header("📘 智慧替代建議模組")
    st.markdown("根據您的健康目標，以下是可考慮的配方替代建議：")

    if "高蛋白" in target_goals:
        st.markdown("- ✅ 建議以 **豌豆蛋白粉取代 10% 麵粉或麥芽漿**，可顯著提升蛋白質含量")
        st.markdown("- ✅ 蛋液比例若高於 30%，建議再加入乳清蛋白或大豆分離蛋白增補")

    if "減糖" in target_goals:
        st.markdown("- ✅ 建議將蔗糖比例從目前數值降至 25% 以下")
        st.markdown("- ✅ 可改為：赤藻糖醇（50%）、羅漢果糖（30%）、轉化糖漿（20%）組合")

    if "高纖" in target_goals:
        st.markdown("- ✅ 建議添加 **5% 菊苣纖維或燕麥纖維**，以取代相同比例糖或麵粉")
        st.markdown("- ✅ 也可加入難消化性麥芽糊精來提升可溶性膳食纖維含量")

    if "低GI" in target_goals:
        st.markdown("- ✅ 建議以羅漢果糖與赤藻糖醇搭配使用，降低甜味來源GI")
        st.markdown("- ✅ 建議以難消化性麥芽糊精或全穀粉替代部份低筋麵粉")

