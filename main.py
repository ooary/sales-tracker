import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except FileNotFoundError:
        st.error("File data.csv tidak ditemukan!")
        return pd.DataFrame(columns=["nama", "area", "sales", "bulan", "tahun"])

# Save data
def save_data(df):
    df.to_csv("data.csv", index=False)

# Main App
def main():
    st.title("Sales Tracker")
    df = load_data()
    
    if df.empty:
        st.warning("Data tidak ditemukan! Silakan tambahkan data penjualan baru.")
        return
    
    # Add new sales entry
    st.subheader("Tambah Penjualan")
    with st.form("add_sales"):
        nama = st.text_input("Nama Sales")
        area = st.text_input("Area")
        sales = st.number_input("Jumlah Penjualan", min_value=0)
        bulan = st.selectbox("Bulan", list(range(1, 13)))
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100, step=1)
        submitted = st.form_submit_button("Tambah")
        
        if submitted:
            new_data = pd.DataFrame([[nama, area, sales, bulan, tahun]], columns=["nama", "area", "sales", "bulan", "tahun"])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Data berhasil ditambahkan!")
            st.rerun()

    # Sidebar filters
    area_list = df["area"].unique().tolist()
    tahun_list = df["tahun"].unique().tolist()
    
    area_filter = st.sidebar.multiselect("Pilih Area", area_list, default=area_list)
    tahun_filter = st.sidebar.multiselect("Pilih Tahun", tahun_list, default=tahun_list)
    
    # Filter data
    filtered_df = df[(df["area"].isin(area_filter)) & (df["tahun"].isin(tahun_filter))]
    
    # Show data
    st.subheader("Data Penjualan")
    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    else:
        st.dataframe(filtered_df)
    
    # Sales summary
    total_sales = filtered_df["sales"].sum()
    st.subheader(f"Total Penjualan: {total_sales}")
    
    # Sales per area
    st.subheader("Penjualan per Area")
    if not filtered_df.empty:
        sales_per_area = filtered_df.groupby("area")["sales"].sum().reset_index()
        fig = px.bar(sales_per_area, x="area", y="sales", title="Total Penjualan per Area")
        st.plotly_chart(fig)
    
    # Sales per month
    st.subheader("Penjualan per Bulan")
    if not filtered_df.empty:
        sales_per_month = filtered_df.groupby("bulan")["sales"].sum().reset_index()
        fig = px.line(sales_per_month, x="bulan", y="sales", title="Tren Penjualan per Bulan")
        st.plotly_chart(fig)
    
    
  
if __name__ == "__main__":
    main()
