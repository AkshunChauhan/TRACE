from PyQt5.QtCore import QThread, pyqtSignal
from app.services.similarity import calculate_semantic_similarity, jaccard_similarity

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
            results.extend(self.process_batch(batch, self.existing_clo_dict, self.new_clo_list))
            self.update_progress.emit(int((batch_index + 1) / len(self.batches) * 100))
        self.comparison_done.emit(results)

    def process_batch(self, batch, existing_clo_dict, new_clo_list):
        results = []
        for sheet_name, existing_clo_set in batch:
            semantic_similarities = calculate_semantic_similarity(existing_clo_set, new_clo_list)

            highest_similarity_pairs = []
            for i, existing_clo in enumerate(existing_clo_set):
                for j, new_clo in enumerate(new_clo_list):
                    score = semantic_similarities[i][j].item()
                    highest_similarity_pairs.append((existing_clo, new_clo, score))

            highest_similarity_pairs = sorted(highest_similarity_pairs, key=lambda x: x[2], reverse=True)[:3]
            average_similarity = sum(score for _, _, score in highest_similarity_pairs) / len(highest_similarity_pairs)
            results.append((sheet_name, average_similarity, highest_similarity_pairs))

        return results
