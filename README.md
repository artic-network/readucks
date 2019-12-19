# readucks
Nanopore read de-multiplexer

## Installation

```
git clone https://github.com/rambaut/readucks.git
```

Install dependencies
```
pip install biopython
pip install parasail
```

Install Readucks
```
cd readucks
python setup.py install
```

Run Readucks
```
readucks --help
```

## Running

```
readucks -i my_reads.fastq -o my_output.tsv --native_barcodes --verbosity 1
```
