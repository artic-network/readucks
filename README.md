# readucks 
<p align="center"><img src="images/readucks.png" alt="READUCKS" width="600"></p>
Nanopore read de-multiplexer (read demux -> readux -> readucks, innit).

This package is inspired by the demultiplexing options in [`porechop`](https://github.com/rrwick/Porechop) (by [Ryan Wick](https://github.com/rrwick)) but without the adapter trimming options - it just demuxes. It uses the [`parasail` library](https://github.com/jeffdaily/parasail) with its [Python bindings](https://github.com/jeffdaily/parasail-python) to do pairwise alignment which provides a considerable speed up over the [`seqan` library](https://github.com/seqan/seqan) used by `porechop` due to its low-level use of vector processor instructions.

Additional speed-ups come from specifying exactly which barcodes are present so it limits searching only to those (this is usually something you know, after all). 

There is also more flexibility with how double barcodes are called (i.e., when you only call a read's barcode if it has the matching barcode sequence at both ends to reduce the chance of mis-called reads). In `readucks` you can specify a lower identity threshold for the secondary barcode than the primary. The primary barcode is defined as the one with the highest match (either at the start or end of the read). The secondary barcode is then the other one. The secondary barcode must match the primary (i.e., be from the same pair) but may have more read errors. 

We are currently investigating the optimal settings for this to trade off between sensitivity and specificity for double barcoding.s

One source file `misc.py` is from `porechop` and is provided with its original licencing information.

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

#### Command line options:
```
usage: readucks -i INPUT_PATH [-o OUTPUT_DIR] [-b] [-a] [-e]
                [-p PREFIX] [-t THREADS] [-v VERBOSITY] [--single]
                [--native_barcodes] [--pcr_barcodes]
                [--rapid_barcodes]
                [--limit_barcodes_to LIMIT_BARCODES_TO [LIMIT_BARCODES_TO ...]]
                [--threshold THRESHOLD]
                [--secondary_threshold SECONDARY_THRESHOLD]
                [--scoring_scheme SCORING_SCHEME] [-h] [--version]
```

#### Main options:

> `-i INPUT_PATH`, `--input INPUT_PATH`

Provide a path to a input file or directory of input files to be processed. These should be either `FASTQ` or `FASTA` files with appropriate file extensions (`.fastq` or `.fasta`).                          
                          
> `-o OUTPUT_DIR`, `--output_dir OUTPUT_DIR`

Provide the path of a directory into which output files will be placed. If this is not specified then the output files will go into the current working directory (except for annotation CSV files - these will be placed along side their matching read files). 

> `-b`, `--bin_barcodes`

This option will bin reads into files according to their assigned barcodes. One file (either FASTQ or FASTA depending on the input file types) will be produced for each barcode that is called (and one for unassigned reads).

> `-a`, `--annotate_files`

This option writes a CSV file for each input file (with a corresponding file name) containing the barcode assignment for each read. 

> `-e`, `--extended_info`

When provided with the `-a` option, this writes much more detailed information about the barcode matches to the annotation (CSV) file.

> `-p PREFIX`, `--prefix PREFIX`

Give an optional prefix string that will be prepended to each output file.

> `-t THREADS`, `--threads THREADS`

The number of parallel threads to use (1 to turn off multithreading) (default: automatic)

> `-v VERBOSITY`, `--verbosity VERBOSITY`

Specify the level of output information: 0 = none, 1 = some, 2 = lots (default: 1)

#### Demuxing options:

> `--single`                

Only attempts to match a single barcode at one end (default double)

> `--native_barcodes`       

Only attempts to match the 24 native nanopore barcodes (default)

> `--pcr_barcodes`          

Only attempts to match the 96 PCR barcodes

> `--rapid_barcodes`        

Only attempts to match the 12 rapid barcodes
                        
> `--limit_barcodes_to LIMIT_BARCODES_TO [LIMIT_BARCODES_TO ...]`
                          
Specify a list of barcodes to look for (numbers, indexed from 1, refer to native, PCR or rapid barcodes as specified)

#### Barcode search settings:

> `--threshold THRESHOLD`   

A read must have at least this percent identity to a barcode (default: 90.0)

> `--secondary_threshold SECONDARY_THRESHOLD`

When double barcoding the second barcode (the one with the lower identity of the two) must have at least this percent identity (and match the first one) (default: 70.0)

> `--scoring_scheme SCORING_SCHEME`

Scoring scheme for the pairwise alignment. A comma-delimited string of alignment scores: match, mismatch, gap open, gap extend (default: 3,-6,-5,-2)

#### Example commands

```
readucks -i my_reads.fastq -o demuxed/ -b --native_barcodes --verbosity 1
```
This will demux the reads in `my_reads.fastq`, producing bin files in a directory called `demuxed` (which must already exist), giving some feedback information to the screen.
