"""
Legacy entry point — use the multipage app instead.

Run: streamlit run app.py
Then open "Continuous Monitoring" from the sidebar.
"""

import streamlit as st

st.set_page_config(page_title="Redirecting…", page_icon="📈")
st.warning("This file is deprecated. Use `streamlit run app.py` and open **Continuous Monitoring** from the sidebar.")
st.page_link("pages/2_Continuous_Monitoring.py", label="Go to Continuous Monitoring →")
