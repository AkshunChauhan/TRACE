import torch
from sentence_transformers import SentenceTransformer, util

# Initialize Sentence-BERT model
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('bert-large-nli-mean-tokens')
model.to(device)

def jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity between two sets."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0
    return intersection / union

def calculate_semantic_similarity(existing_clo_set, new_clo_list):
    """Calculate semantic similarity using Sentence-BERT."""
    existing_clo_embeddings = model.encode(existing_clo_set, batch_size=8, convert_to_tensor=True)
    new_clo_embeddings = model.encode(new_clo_list, batch_size=8, convert_to_tensor=True)

    semantic_similarities = util.cos_sim(existing_clo_embeddings, new_clo_embeddings)
    return semantic_similarities
