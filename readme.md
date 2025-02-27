# Export Data Correlation Analysis

This project analyzes the correlation between exported item values using data from an SQLite database. It includes:
- **Correlation Analysis (`corelation.py`)**: A Streamlit app for selecting two items and analyzing their correlation.
- **Heatmap (`heatmap.py`)**: A Python script to generate a correlation heatmap for multiple export items.

## 📌 Installation & Setup

### 1️⃣ Create & Activate Virtual Environment  
**For Windows:**  
`python -m venv venv && venv\Scripts\activate`  

**For macOS/Linux:**  
`python3 -m venv venv && source venv/bin/activate`  

### 2️⃣ Install Dependencies  
Ensure you have Python installed, then install the required packages:  
`pip install sqlite3 pandas matplotlib seaborn streamlit numpy`  

### 3️⃣ Setup Database  
Make sure the SQLite database (`trade_data_raw.db`) exists in the same directory.

### 4️⃣ Run the Applications  
Run **Correlation Analysis (Streamlit App)**:  
`streamlit run corelation.py`  

Run **Heatmap Analysis (Standalone Script)**:  
`python heatmap.py`

## 📂 Project Files  
- **`corelation.py`** - Streamlit app for selecting two export items and analyzing their correlation.  
- **`heatmap.py`** - Generates a heatmap of correlations between multiple export items.  
- **`trade_data_raw.db`** - SQLite database containing export data.  

## ✅ Requirements  
- Python 3.x  
- SQLite database (`trade_data_raw.db`)  
- Required Python libraries: `pandas`, `matplotlib`, `seaborn`, `streamlit`, `numpy`  

## 🔗 License  
This project is open-source and free to use.  

---  
Happy Coding! 🚀
