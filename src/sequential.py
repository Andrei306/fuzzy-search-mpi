import time
from utils import load_names, compute_similarity


FILE_PATH = "data/names.txt"
QUERY = "Andrei Popescu"
THRESHOLD = 0.85


def main():
    names = load_names(FILE_PATH)

    start = time.time()

    results = []

    for name in names:
        score = compute_similarity(QUERY, name)

        if score >= THRESHOLD:
            results.append((name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    end = time.time()

    print("\nResults:\n")

    for name, score in results[:20]:
        print(f"{name} -> {score:.4f}")

    print(f"\nExecution time: {end - start:.4f} seconds")


if __name__ == "__main__":
    main()