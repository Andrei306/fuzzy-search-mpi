from mpi4py import MPI
import argparse
import time
from utils import load_names, compute_similarity
import sys

sys.stdout.reconfigure(encoding="utf-8")

def split_list(data, num_chunks):
    chunk_size = len(data) // num_chunks
    chunks = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = len(data) if i == num_chunks - 1 else start + chunk_size
        chunks.append(data[start:end])

    return chunks


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", default="data/names.txt")
    parser.add_argument("--query", default="Andrei Popescu")
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("--top-k", type=int, default=0)

    return parser.parse_args()


def main():
    args = parse_args()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    names = None
    chunks = None

    if rank == 0:
        names = load_names(args.file)
        chunks = split_list(names, size)

    local_names = comm.scatter(chunks, root=0)

    comm.Barrier()
    start = time.time()

    local_results = []

    for name in local_names:
        if abs(len(name) - len(args.query)) > 8:
            continue

        score = compute_similarity(args.query, name)

        if score >= args.threshold:
            local_results.append((name, score))

    all_results = comm.gather(local_results, root=0)

    if rank == 0:
        results = []

        for partial in all_results:
            results.extend(partial)

        results.sort(key=lambda x: x[1], reverse=True)

        if args.top_k > 0:
            results_to_print = results[:args.top_k]
        else:
            results_to_print = results

        end = time.time()
        elapsed = end - start

        print("\nResults:\n")

        for name, score in results_to_print:
            print(f"{name} -> {score:.4f}")

        print(f"\nTotal matches: {len(results)}")
        print(f"Processes: {size}")
        print(f"Execution time: {elapsed:.6f} seconds")

        print(f"METRIC_TIME={elapsed:.6f}")
        print(f"METRIC_NAMES={len(names)}")


if __name__ == "__main__":
    main()

### To run: mpiexec -np 4 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 30
### --top-k is optional