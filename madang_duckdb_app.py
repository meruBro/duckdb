import streamlit as st
import duckdb
import pandas as pd

st.title("마당 서점 조회 (DuckDB 버전)")

@st.cache_resource
def get_connection():
    # Streamlit Cloud에서는 이 파일이 앱과 같은 폴더에 있어야 함
    return duckdb.connect(database="madang.duckdb", read_only=True)

conn = get_connection()

name = st.text_input("고객명 입력 (예: 박지성)")

if name:
    query = """
        SELECT c.name,
               b.bookname,
               o.orderdate,
               o.saleprice
        FROM Customer c
        JOIN Orders o ON c.custid = o.custid
        JOIN Book   b ON o.bookid = b.bookid
        WHERE c.name = ?
        ORDER BY o.orderdate
    """
    df = conn.execute(query, [name]).df()

    if df.empty:
        st.info("해당 고객의 주문 기록이 없습니다.")
    else:
        st.subheader(f"'{name}' 고객의 구매 내역")
        st.dataframe(df)
