import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# เชื่อมต่อกับฐานข้อมูล SQLite
db_path = "trade_data_raw.db"
conn = sqlite3.connect(db_path)

# คำสั่ง SQL สำหรับดึงข้อมูล
query = """
    SELECT 
        year_month,
        SUM(CASE WHEN items_name = 'กระเป๋าหนังและเข็มขัดหนัง' THEN items_baht_amnt_export ELSE 0 END) AS leather_bag_belt,
        SUM(CASE WHEN items_name = 'กล้องถ่ายรูปและอุปกรณ์' THEN items_baht_amnt_export ELSE 0 END) AS camera,
        SUM(CASE WHEN items_name = 'ดอกไม้' THEN items_baht_amnt_export ELSE 0 END) AS flower,
        SUM(CASE WHEN items_name = 'นาฬิกาและอุปกรณ์' THEN items_baht_amnt_export ELSE 0 END) AS watch,
        SUM(CASE WHEN items_name = 'น้ำหอมและเครื่องสำอางค์' THEN items_baht_amnt_export ELSE 0 END) AS perfume,
        SUM(CASE WHEN items_name = 'ปากกาและอุปกรณ์' THEN items_baht_amnt_export ELSE 0 END) AS pen,
        SUM(CASE WHEN items_name = 'ผ้าทอทำด้วยขนสัตว์' THEN items_baht_amnt_export ELSE 0 END) AS wool_textile,
        SUM(CASE WHEN items_name = 'รองเท้าหนังและรองเท้าผ้าใบ' THEN items_baht_amnt_export ELSE 0 END) AS shoes,
        SUM(CASE WHEN items_name = 'สุราต่างประเทศ' THEN items_baht_amnt_export ELSE 0 END) AS liquor,
        SUM(CASE WHEN items_name = 'สูท เสื้อ กระโปรง กางเกง สำหรับบุรุษ สตรี เด็กชาย และเด็กหญิง และเนคไท' THEN items_baht_amnt_export ELSE 0 END) AS clothing,
        SUM(CASE WHEN items_name = 'เครื่องประดับที่ทำด้วยคริสตัล' THEN items_baht_amnt_export ELSE 0 END) AS crystal_jewelry,
        SUM(CASE WHEN items_name = 'เครื่องแก้วชนิดใช้บนโต๊ะอาหาร หรือใช้ตกแต่งภายในที่ทำด้วยคริสตัล' THEN items_baht_amnt_export ELSE 0 END) AS crystal_glass,
        SUM(CASE WHEN items_name = 'เลนส์' THEN items_baht_amnt_export ELSE 0 END) AS lens,
        SUM(CASE WHEN items_name = 'แว่นตา' THEN items_baht_amnt_export ELSE 0 END) AS glasses,
        SUM(CASE WHEN items_name = 'ไฟแช็คและอุปกรณ์' THEN items_baht_amnt_export ELSE 0 END) AS lighter,
        SUM(CASE WHEN items_name = 'ไวน์' THEN items_baht_amnt_export ELSE 0 END) AS wine
    FROM cleaned_data
    GROUP BY year_month
    ORDER BY year_month DESC;
"""

# โหลดข้อมูลลง DataFrame
df = pd.read_sql_query(query, conn)

# ปิดการเชื่อมต่อฐานข้อมูล
conn.close()

# ลบคอลัมน์ year_month ออกเพื่อให้เหลือแต่ข้อมูลตัวเลขสำหรับคำนวณ correlation
df_numeric = df.drop(columns=["year_month"])

# คำนวณ correlation matrix
correlation_matrix = df_numeric.corr()

# สร้าง mask เพื่อตัดค่าครึ่งล่างออก (เก็บเฉพาะค่าครึ่งบน)
mask = np.tril(np.ones_like(correlation_matrix, dtype=bool))  # ตัดค่าครึ่งล่างออก

# วาด heatmap พร้อมแก้ปัญหาตัวอักษรซ้อนกัน และย้าย Color Bar ไปด้านซ้าย
plt.figure(figsize=(8.4, 6))  # Zoom ออก 0.6 เท่า จาก (14,10) → (8.4,6)
ax = sns.heatmap(
    correlation_matrix, 
    mask=mask,  # ใช้ mask เพื่อตัดค่าครึ่งล่างออก
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    linewidths=0.5,
    cbar_kws={"location": "left"}  # ย้าย Color Bar ไปด้านซ้าย
)

# ย้ายชื่อประเภทสินค้าจากแกน X ด้านล่างไปด้านบน
ax.xaxis.tick_top()  # ย้าย label ของ X ไปด้านบน
ax.xaxis.set_label_position('top')  # กำหนดตำแหน่ง label ด้านบน

# ย้าย Y-label (ชื่อประเภทสินค้า) จากด้านซ้ายไปด้านขวา
ax.yaxis.tick_right()  # ย้าย tick marks ไปด้านขวา
ax.yaxis.set_label_position("right")  # ย้าย label แกน Y ไปด้านขวา

# ตั้งค่าให้ตัวหนังสือบนแกน X เป็นแนวตั้ง (90 องศา)
plt.xticks(rotation=90, ha="center", fontsize=8)  

# ตั้งค่าให้ตัวหนังสือบนแกน Y เป็นแนวนอน
plt.yticks(rotation=0, ha="left", fontsize=8)  

# ปรับระยะห่างของ heatmap ให้ชิดซ้ายมากที่สุด
ax.figure.subplots_adjust(left=0.05, right=0.75, top=0.85, bottom=0.2)

# เลื่อน Label แกน Y ให้ออกจาก Heatmap เพิ่มเติม
ax.yaxis.set_label_coords(1.15, 0.5)

plt.title("Correlation Matrix of Export Items", fontsize=12)
plt.show()
