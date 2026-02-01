import pandas as pd
import torch
import os
import pickle
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from tqdm import tqdm  # Progress bar

class XRaySearchEngine:
    def __init__(self, metadata_path='metadata.csv', embeddings_path='embeddings.pkl'):
        self.metadata_path = metadata_path
        self.embeddings_path = embeddings_path
        self.df = pd.read_csv(metadata_path)
        
        # Load CLIP model
        print("Loading CLIP model...")
        self.model = SentenceTransformer('clip-ViT-B-32')
        
        # Check if we already have saved embeddings
        if os.path.exists(self.embeddings_path):
            print(f"Loading pre-computed embeddings from {self.embeddings_path}...")
            with open(self.embeddings_path, 'rb') as f:
                self.image_embeddings = pickle.load(f)
            print("Embeddings loaded instantly!")
        else:
            print("Computing embeddings for the first time (this takes a while)...")
            self.image_embeddings = self._encode_dataset_images()
            
            # Save them for next time
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(self.image_embeddings, f)
            print(f"Embeddings saved to {self.embeddings_path}")

    def _encode_dataset_images(self):
        images = []
        valid_indices = []
        
        # Use tqdm to show a progress bar
        print(f"Found {len(self.df)} images. Processing...")
        
        for idx, row in tqdm(self.df.iterrows(), total=len(self.df)):
            try:
                img = Image.open(row['file_path'])
                images.append(img)
                valid_indices.append(idx)
            except Exception as e:
                print(f"Error loading {row['file_path']}: {e}")
        
        # Update dataframe to only include valid images
        self.df = self.df.iloc[valid_indices].reset_index(drop=True)
        
        # Compute embeddings in batches
        return self.model.encode(images, convert_to_tensor=True, show_progress_bar=True)

    def search_by_text(self, query_text, top_k=5):
        text_emb = self.model.encode([query_text], convert_to_tensor=True)
        hits = util.semantic_search(text_emb, self.image_embeddings, top_k=top_k)[0]
        return self._format_results(hits)

    def search_by_image(self, query_image, top_k=5):
        img_emb = self.model.encode([query_image], convert_to_tensor=True)
        hits = util.semantic_search(img_emb, self.image_embeddings, top_k=top_k)[0]
        return self._format_results(hits)

    def _format_results(self, hits):
        results = []
        for hit in hits:
            idx = hit['corpus_id']
            score = hit['score']
            result_row = self.df.iloc[idx].to_dict()
            result_row['score'] = score
            results.append(result_row)
        return results