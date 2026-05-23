import jellyfish


def load_names(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]


def compute_similarity(query, name):
    return jellyfish.jaro_winkler_similarity(
        query.lower(),
        name.lower()
    )