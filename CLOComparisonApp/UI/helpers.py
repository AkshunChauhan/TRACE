def update_label(slider, label, prefix):
    value = slider.value() / 100
    label.setText(f"{prefix}: {value:.2f}")


def update_progress(parent, value):
    parent.progressbar.setValue(value)


def display_results(parent, results, avg_similarity_threshold):
    overall_result_text = ""
    match_result_text = ""
    no_match_result_text = ""

    for sheet_name, average_similarity, highest_similarity_pairs in results:
        overall_result_text += (
            f"Course: {sheet_name}, Average Similarity: {average_similarity:.2f}\n"
        )
        if average_similarity >= avg_similarity_threshold:
            match_result_text += f"\nMatching Course: {sheet_name}\n"
            for existing_clo, new_clo, score in highest_similarity_pairs:
                match_result_text += f"  Existing CLO: {existing_clo}\n  New CLO: {new_clo}\n  Similarity Score: {score:.2f}\n"
        else:
            no_match_result_text += f"No match found for course: {sheet_name}\n"

    parent.result_tab.setPlainText(overall_result_text)
    parent.match_tab.setPlainText(match_result_text)
    parent.no_match_tab.setPlainText(no_match_result_text)
