import streamlit as st

# =========================================================
# CẤU HÌNH
# =========================================================
st.set_page_config(
    page_title="trân lét",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 trân lét")
st.caption("Nhập món ăn, số lượng và đơn giá để tính tổng tiền khách phải thanh toán.")

# =========================================================
# DANH SÁCH MÓN MẶC ĐỊNH
# =========================================================
MENU = {
    "Phở bò": 50000,
    "Phở gà": 45000,
    "Cơm tấm": 55000,
    "Bún bò": 50000,
    "Mì xào": 45000,
    "Cơm chiên": 50000,
    "Gà rán": 35000,
    "Khoai tây chiên": 30000,
    "Trà đào": 25000,
    "Trà tắc": 15000,
    "Cà phê": 25000,
    "Nước suối": 10000
    "Chí Linh hấp bia": 2000
    "bà trân 7 màu": 299000
}

# =========================================================
# NHẬP THÔNG TIN
# =========================================================
st.subheader("1. Thông tin món ăn")

num_items = st.number_input(
    "Số lượng món trong hóa đơn",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

items = []

for i in range(num_items):

    st.markdown(f"### 🍽️ Món {i + 1}")

    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

    with col1:
        item_name = st.selectbox(
            "Tên món",
            options=list(MENU.keys()) + ["Món khác"],
            key=f"name_{i}"
        )

    with col2:
        if item_name == "Món khác":
            price = st.number_input(
                "Đơn giá (VNĐ)",
                min_value=0,
                value=0,
                step=1000,
                key=f"price_{i}"
            )
        else:
            price = MENU[item_name]
            st.number_input(
                "Đơn giá (VNĐ)",
                value=price,
                disabled=True,
                format="%d",
                key=f"price_display_{i}"
            )

    with col3:
        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            value=1,
            step=1,
            key=f"quantity_{i}"
        )

    with col4:
        subtotal = price * quantity
        st.metric(
            "Thành tiền",
            f"{subtotal:,.0f} VNĐ"
        )

    items.append({
        "Tên món": item_name,
        "Đơn giá": price,
        "Số lượng": quantity,
        "Thành tiền": subtotal
    })

# =========================================================
# GIẢM GIÁ + VAT
# =========================================================
st.divider()
st.subheader("2. Khuyến mãi và thuế")

col1, col2 = st.columns(2)

with col1:
    discount_percent = st.number_input(
        "Giảm giá (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

with col2:
    vat_percent = st.number_input(
        "VAT (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

# =========================================================
# TÍNH TIỀN
# =========================================================
if st.button("🧮 TÍNH TIỀN", type="primary", use_container_width=True):

    subtotal = sum(item["Thành tiền"] for item in items)

    discount_amount = subtotal * discount_percent / 100

    after_discount = subtotal - discount_amount

    vat_amount = after_discount * vat_percent / 100

    total = after_discount + vat_amount

    # -----------------------------------------------------
    # KẾT QUẢ
    # -----------------------------------------------------
    st.subheader("📊 HÓA ĐƠN")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Tiền hàng",
        f"{subtotal:,.0f} VNĐ"
    )

    c2.metric(
        "Giảm giá",
        f"-{discount_amount:,.0f} VNĐ"
    )

    c3.metric(
        "VAT",
        f"{vat_amount:,.0f} VNĐ"
    )

    c4.metric(
        "TỔNG THANH TOÁN",
        f"{total:,.0f} VNĐ"
    )

    # -----------------------------------------------------
    # CHI TIẾT HÓA ĐƠN
    # -----------------------------------------------------
    st.write("### 🧾 Chi tiết hóa đơn")

    st.dataframe(
        items,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # TÓM TẮT
    # -----------------------------------------------------
    st.write("### 💰 Tổng kết")

    st.write(
        f"*Tiền hàng:* {subtotal:,.0f} VNĐ"
    )

    st.write(
        f"*Giảm giá ({discount_percent:.0f}%):* "
        f"-{discount_amount:,.0f} VNĐ"
    )

    st.write(
        f"*Tiền sau giảm:* {after_discount:,.0f} VNĐ"
    )

    st.write(
        f"*VAT ({vat_percent:.0f}%):* "
        f"{vat_amount:,.0f} VNĐ"
    )

    st.success(
        f"### 🎉 KHÁCH CẦN THANH TOÁN: {total:,.0f} VNĐ"
    )

    # -----------------------------------------------------
    # TIỀN KHÁCH ĐƯA
    # -----------------------------------------------------
    st.divider()

    customer_money = st.number_input(
        "💵 Tiền khách đưa (VNĐ)",
        min_value=0,
        value=0,
        step=1000,
        format="%d"
    )

    if customer_money > 0:

        change = customer_money - total

        if change >= 0:
            st.success(
                f"💵 Tiền thối lại: *{change:,.0f} VNĐ*"
            )
        else:
            st.error(
                f"⚠️ Khách đưa thiếu: *{-change:,.0f} VNĐ*"
            )

# =========================================================
# GHI CHÚ
# =========================================================
st.divider()

st.caption(
    "Công thức: Thành tiền = Đơn giá × Số lượng. "
    "Tiền sau giảm = Tiền hàng − Tiền giảm giá. "
    "Tổng thanh toán = Tiền sau giảm + VAT."
)
