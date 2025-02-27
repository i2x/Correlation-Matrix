import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# === Database Config ===
db_path = "trade_data_raw.db"
table_name = "cleaned_data"

# === Item Dictionary ===
item_mapping = {
    "Leather Bag & Belt": "กระเป๋าหนังและเข็มขัดหนัง",
    "Camera": "กล้องถ่ายรูปและอุปกรณ์",
    "Flower": "ดอกไม้",
    "Watch": "นาฬิกาและอุปกรณ์",
    "Perfume": "น้ำหอมและเครื่องสำอางค์",
    "Pen": "ปากกาและอุปกรณ์",
    "Wool Textile": "ผ้าทอทำด้วยขนสัตว์",
    "Shoes": "รองเท้าหนังและรองเท้าผ้าใบ",
    "Liquor": "สุราต่างประเทศ",
    "Clothing": "สูท เสื้อ กระโปรง กางเกง สำหรับบุรุษ สตรี เด็กชาย และเด็กหญิง และเนคไท",
    "Crystal Jewelry": "เครื่องประดับที่ทำด้วยคริสตัล",
    "Crystal Glass": "เครื่องแก้วชนิดใช้บนโต๊ะอาหาร หรือใช้ตกแต่งภายในที่ทำด้วยคริสตัล",
    "Lens": "เลนส์",
    "Glasses": "แว่นตา",
    "Lighter": "ไฟแช็คและอุปกรณ์",
    "Wine": "ไวน์",
}

# === Streamlit UI ===
st.title("Export Data Correlation Analysis")

# Dropdowns
item_options = list(item_mapping.keys())
item1 = st.selectbox("Select first item:", item_options)
item2 = st.selectbox("Select second item:", item_options)

if item1 != item2:
    # Get Thai names
    item1_thai = item_mapping[item1]
    item2_thai = item_mapping[item2]

    # Fetch Data
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT 
            year_month,
            SUM(CASE WHEN items_name = '{item1_thai}' THEN items_baht_amnt_export ELSE 0 END) AS item1_value,
            SUM(CASE WHEN items_name = '{item2_thai}' THEN items_baht_amnt_export ELSE 0 END) AS item2_value
        FROM {table_name}
        GROUP BY year_month
        ORDER BY year_month DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Compute correlation
    correlation_value = df["item1_value"].corr(df["item2_value"])

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=df["item1_value"], y=df["item2_value"], color="steelblue", alpha=0.7, ax=ax)
    sns.regplot(x=df["item1_value"], y=df["item2_value"], scatter=False, color="red", line_kws={"linewidth": 2}, ax=ax)

    ax.set_xlabel(f"{item1} Export Value (Baht)")
    ax.set_ylabel(f"{item2} Export Value (Baht)")
    ax.set_title(f"Correlation between {item1} and {item2}\nCorrelation: {correlation_value:.2f}")

    # Display results
    st.pyplot(fig)
    st.write(f"**Correlation Coefficient ({item1} & {item2}): {correlation_value:.2f}**")

else:
    st.warning("Please select two different items for comparison.")
