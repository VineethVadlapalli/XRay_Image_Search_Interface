import streamlit as st
from PIL import Image
from search_engine import XRaySearchEngine
import os

# Page Config
st.set_page_config(page_title="X-Ray Search", layout="wide")
st.title("🩻 X-Ray Image Search Interface")
st.markdown("Search via text or upload an image to find similar X-rays.")

# Initialize Search Engine (Cached to avoid reloading model)
@st.cache_resource
def load_engine():
    if not os.path.exists('metadata.csv'):
        return None
    return XRaySearchEngine()

engine = load_engine()

if engine is None:
    st.error("Error: 'metadata.csv' not found. Please run 'data_prep.py' first.")
    st.stop()

# --- Sidebar: Search Options ---
st.sidebar.header("Search Mode")
search_mode = st.sidebar.radio("Choose Input Type:", ["Text Query", "Image Upload"])

# Bonus: Category Filter [cite: 26]
categories = ["All"] + list(engine.df['category'].unique())
selected_category = st.sidebar.selectbox("Filter by Category (Optional)", categories)

# --- Main Interface ---
results = []

if search_mode == "Text Query":
    # Requirements: [cite: 9, 17]
    query = st.text_input("Enter search terms (e.g., 'fractured', 'dental x-ray'):")
    if st.button("Search Text"):
        if query:
            with st.spinner("Searching..."):
                results = engine.search_by_text(query, top_k=10)
        else:
            st.warning("Please enter a text query.")

elif search_mode == "Image Upload":
    # Requirements: [cite: 13, 17]
    uploaded_file = st.file_uploader("Upload an X-ray image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        query_img = Image.open(uploaded_file)
        st.image(query_img, caption="Query Image", width=200)
        
        if st.button("Search Image"):
            with st.spinner("Analyzing image..."):
                results = engine.search_by_image(query_img, top_k=10)

# --- Results Display ---
# Requirements: [cite: 11, 15, 17]
if results:
    st.subheader(f"Top Matches Found")
    
    # Apply Category Filter if selected
    if selected_category != "All":
        results = [r for r in results if r['category'] == selected_category]
        if not results:
            st.warning(f"No results found in category '{selected_category}'.")

    # Display Grid
    cols = st.columns(5) # 5 columns for grid
    for i, res in enumerate(results):
        with cols[i % 5]:
            try:
                img = Image.open(res['file_path'])
                st.image(img, use_container_width=True)
                # Display metadata and Score [cite: 25]
                st.caption(f"**{res['category']}**")
                st.caption(f"Score: {res['score']:.4f}")
                st.text(res['image_name'])
            except Exception as e:
                st.error("Image load error")

# Error Handling [cite: 18]
elif search_mode == "Text Query" and not results:
    st.info("Enter a query to see results.")