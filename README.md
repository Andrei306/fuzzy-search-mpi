# Fuzzy Search MPI

## Descriere

Acest proiect implementează o aplicație de căutare fuzzy a numelor într-o listă de dimensiune mare, utilizând algoritmul Jaro-Winkler și paradigma de programare paralel-distribuită MPI.

Aplicația primește ca date de intrare un nume de căutat, un prag de similaritate și o listă de nume. Lista este împărțită în mai multe chunk-uri, distribuite către procese MPI distincte. Fiecare proces calculează local similaritatea dintre numele căutat și numele din chunk-ul primit, iar rezultatele sunt colectate de procesul root, sortate descrescător după scorul de similaritate și afișate.

Proiectul a fost realizat pentru disciplina **Algoritmi Paraleli și Distribuiți 2**.

## Tehnologii utilizate

- Python 3
- MPI
- mpi4py
- jellyfish

## Structura proiectului

```text
fuzzy-search-mpi/
│
├── data/
│   └── names.txt
│
├── results/
│   └── benchmark.csv
│
├── src/
│   ├── generate_dataset.py
│   ├── sequential.py
│   ├── mpi_search.py
│   ├── benchmark.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalare

Se recomandă utilizarea unui mediu virtual Python.

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Instalarea dependențelor:
```
pip install -r requirements.txt
```
Pentru rularea aplicației MPI este necesară instalarea unei implementări MPI. Pe Windows s-a utilizat Microsoft MPI.

## Generarea datasetului

Pentru generarea listei de nume:
```
python src/generate_dataset.py
```
Această comandă generează fișierul: `data/names.txt` cu 1.000.000 de nume generate aleator.

## Rulare secvențială

Pentru rularea variantei secvențiale:
```
python src/sequential.py
```
Aceasta este folosită ca bază de comparație pentru implementarea paralelă.

## Rulare paralel-distribuită MPI

Pentru rularea aplicației cu 4 procese MPI:
```
mpiexec -np 4 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85
```
Pentru afișarea doar a primelor 20 de rezultate:
```
mpiexec -np 4 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 20
```
## Exemple de rulare cu număr diferit de procese:
```
mpiexec -np 1 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 20
mpiexec -np 2 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 20
mpiexec -np 4 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 20
mpiexec -np 8 python src/mpi_search.py --query "Andrei Popescu" --threshold 0.85 --top-k 20
```
## Benchmark

Pentru rularea automată a testelor de performanță:
```
python src/benchmark.py
```
Scriptul rulează aplicația pentru mai multe valori ale numărului de procese MPI și calculează:

- timpul mediu de execuție;
- speedup;
- eficiența;
- throughput-ul exprimat în nume procesate pe secundă.

Rezultatele sunt salvate în directorul:
`
results/
`
sub formă de fișier `.csv`.