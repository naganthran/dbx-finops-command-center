import streamlit as st
from databricks.connect import DatabricksSession

@st.cache_resource
def get_spark():
    return DatabricksSession.builder.getOrCreate()

@st.cache_data(ttl=1800)
def run_query(query: str):
    spark = get_spark()
    return spark.sql(query).toPandas()
