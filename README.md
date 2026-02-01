# X-Ray Image Search Interface

This project is a prototype for searching X-ray images using both **Text Queries** and **Image-Based (Reverse) Search**. It utilizes the **CLIP (Contrastive Language-Image Pre-training)** model to understand the semantic similarity between text and images.

## 📂 Project Structure

```text
code/
│
├── app.py                 # Main Streamlit application
├── search_engine.py       # Core logic (CLIP model & Search)
├── data_prep.py           # Script to generate metadata.csv
├── requirements.txt       # Python dependencies
├── metadata.csv           # Generated metadata file (must be present)
└── dataset/               # Folder containing image subfolders (chest, spine, etc.)

🚀 Setup Instructions
1. Install Dependencies
Ensure you have Python installed (3.8+ recommended). Open your terminal/command prompt in this folder and run:

Bash
pip install -r requirements.txt
2. Prepare the Data
The project requires a metadata.csv file to map images to their categories.

Ensure your images are in the dataset/ folder, organized by category subfolders (e.g., dataset/chest/).

Run the preparation script:

Bash
python data_prep.py
This will generate the metadata.csv file.

3. Run the Application
Launch the web interface using Streamlit:

Bash
streamlit run app.py
The app will open automatically in your browser (usually at http://localhost:8501).

Note: The first run may take a few minutes to download the CLIP model and compute image embeddings. Subsequent runs will be instant.

🛠️ Features
Text Search: Enter terms like "fracture" or "dental" to find relevant X-rays.

Image Search: Upload an X-ray image to find visually similar cases.

Filtering: Filter results by category (Chest, Spine, Dental, etc.).

📝 Notes for Reviewer
The embeddings.pkl file is generated automatically to cache search vectors for performance.

If you add new images to the dataset, delete embeddings.pkl and restart the app to re-index them.


### **One Final Check**
Before zipping your folder, make sure your folder looks **exactly** like the structure in the README above.
1.  Is `metadata.csv` there? (If not, run `python data_prep.py` one last time).
2.  Did you include the `dataset` folder inside `code` or at the root?
    * *Correction:* In the README above, I assumed `dataset/` is inside `code/`. If your submission structure has `dataset/` *outside* the `code/` folder (as we discussed in the "Final Packaging" step), you might need to adjust the path in `data_prep.py` or just move the dataset folder into `code/` to keep it simple and self-contained for the reviewer. **Moving it inside `code/` is usually safer** so the scripts run without path errors.

**Would you like me to help you verify your final folder structure before you zip it?**