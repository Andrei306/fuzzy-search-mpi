import subprocess
import csv
import re
import os


PROCESS_COUNTS = [1, 2, 4, 8]
REPEATS = 3

MPIEXEC = "mpiexec"
SCRIPT = "src/mpi_search.py"
OUTPUT_FILE = "results/benchmark.csv"


def run_benchmark(processes):
    command = [
        MPIEXEC,
        "-np",
        str(processes),
        "python",
        SCRIPT
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = completed.stdout

    time_match = re.search(r"METRIC_TIME=([0-9.]+)", output)
    names_match = re.search(r"METRIC_NAMES=([0-9]+)", output)

    if not time_match or not names_match:
        print(output)
        print(completed.stderr)
        raise RuntimeError("Could not parse benchmark output.")

    elapsed = float(time_match.group(1))
    names_count = int(names_match.group(1))

    return elapsed, names_count


def main():
    os.makedirs("results", exist_ok=True)

    rows = []

    baseline_time = None

    for processes in PROCESS_COUNTS:
        times = []

        for repeat in range(REPEATS):
            print(f"Running np={processes}, repeat={repeat + 1}/{REPEATS}")

            elapsed, names_count = run_benchmark(processes)
            times.append(elapsed)

        avg_time = sum(times) / len(times)

        if processes == 1:
            baseline_time = avg_time

        speedup = baseline_time / avg_time
        efficiency = speedup / processes
        throughput = names_count / avg_time

        rows.append({
            "processes": processes,
            "avg_time_seconds": avg_time,
            "speedup": speedup,
            "efficiency": efficiency,
            "throughput_names_per_second": throughput
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "processes",
                "avg_time_seconds",
                "speedup",
                "efficiency",
                "throughput_names_per_second"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nBenchmark saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()