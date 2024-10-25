from PyQt5.QtCore import QThread, pyqtSignal
from models import model
from utils import jaccard_similarity
from sentence_transformers import util


class CLOComparisonThread(QThread):
    update_progress = pyqtSignal(int)
    comparison_done = pyqtSignal(list)

    def __init__(self, existing_clo_dict, new_clo_list, batches):
        super().__init__()
        self.existing_clo_dict = existing_clo_dict
        self.new_clo_list = new_clo_list
        self.batches = batches

    def run(self):
        results = []
        for batch_index, batch in enumerate(self.batches):
            results.extend(
                self.process_batch(batch, self.existing_clo_dict, self.new_clo_list)
            )
            self.update_progress.emit(int((batch_index + 1) / len(self.batches) * 100))
        self.comparison_done.emit(results)

    def process_batch(self, batch, existing_clo_dict, new_clo_list):
        results = []
        for sheet_name, existing_clo_set in batch:
            existing_clo_embeddings = model.encode(
                existing_clo_set, batch_size=8, convert_to_tensor=True
            )
            new_clo_embeddings = model.encode(
                new_clo_list, batch_size=8, convert_to_tensor=True
            )
            semantic_similarities = util.cos_sim(
                existing_clo_embeddings, new_clo_embeddings
            )
            threshold = 0.7
            highest_similarity_pairs = []
            for i, existing_clo in enumerate(existing_clo_set):
                for j, new_clo in enumerate(new_clo_list):
                    similarity_score = semantic_similarities[i][j].item()
                    if similarity_score > threshold:
                        highest_similarity_pairs.append(
                            (existing_clo, new_clo, similarity_score)
                        )
            average_semantic_similarity = (
                (semantic_similarities > threshold).float().mean().item()
            )
            existing_clo_set = set(existing_clo_set)
            new_clo_set = set(new_clo_list)
            average_jaccard_similarity = jaccard_similarity(
                existing_clo_set, new_clo_set
            )
            average_similarity = (
                average_semantic_similarity + average_jaccard_similarity
            ) / 2
            results.append((sheet_name, average_similarity, highest_similarity_pairs))
        return results
