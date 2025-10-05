import streamlit as st
import pandas as pd

st.set_page_config(page_title="Phân tích dữ liệu nhà đất", layout="wide")
st.title("📊 Phân tích dữ liệu nhà đất từ file data.csv")

df = pd.read_csv('data.csv')

required_columns = ['Giá', 'Diện tích', 'Quận', 'Loại hình nhà ở']
missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"❌ Các cột sau không tồn tại trong dữ liệu: {missing}")
    st.write("📌 Các cột hiện có trong file:")
    st.write(df.columns.tolist())
else:
    df.dropna(subset=required_columns, inplace=True)
    df = df[df['Diện tích'] > 0]
    df.drop_duplicates(inplace=True)
    df['Giá_m2'] = df['Giá'] / df['Diện tích']

    st.subheader("📌 Tổng quan dữ liệu")
    st.dataframe(df.head())

    st.subheader("🏠 Các ngôi nhà có giá > 100 triệu/m²")
    expensive_homes = df[df['Giá_m2'] > 100_000_000]
    st.dataframe(expensive_homes[['Địa chỉ', 'Giá', 'Diện tích', 'Giá_m2']])

    st.subheader("📍 Quận có giá nhà cao nhất và thấp nhất")
    avg_price_by_district = df.groupby('Quận')['Giá_m2'].mean().sort_values(ascending=False)
    st.write(f"🔺 Quận đắt nhất: **{avg_price_by_district.idxmax()}** ({avg_price_by_district.max():,.0f} đ/m²)")
    st.write(f"🔻 Quận rẻ nhất: **{avg_price_by_district.idxmin()}** ({avg_price_by_district.min():,.0f} đ/m²)")
    st.dataframe(avg_price_by_district.reset_index().rename(columns={'Giá_m2': 'Giá trung bình (đ/m²)'}))

    st.subheader("🏘️ Giá trung bình theo loại hình nhà ở")
    avg_price