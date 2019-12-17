"""
Copyright 2019 Andrew Rambaut (a.rambaut@ed.ac.uk)
https://github.com/rambaut/readucks

This module contains the main script for Readucks. It is executed when a user runs `readucks`
(after installation) or `readucks-runner.py` (directly from the source directory).

This file is part of Readucks. Readucks is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Readucks is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Readucks. If
not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
import sys

from Bio import SeqIO
import parasail

from .misc import bold_underline, MyHelpFormatter
from .version import __version__

read = "CAGTGTACTTCGTTCGGTACGTATTGCTAAGGTTAAAGGTTGCACAAACCCTGGACAAGCAACACCTACACAATGAATACAAAGTTTGATTCTTGAATTCAATAGCTCTCTTGCTATCTAACTAGATGGAATACTTCATATTGGGCTAACTCTTATATGCTGACTCAATAGTTAACTTGACATCTCTGCCTTCATAATCAGATATATAAGCATAATAAATAAATACTCATATTTCTTGATAATTTGTTTAACCACAGATAAATCCTCACTGTAAGCCAGGCTTTCAAGTTGACACCCTTACAAAAACCAGGACTCAGAATCCCTCAAATAAGAGATTCCAAGACAACATCCTTAAATTGCTTTATTATATTAATAAGCATTTTATCACTAGAAATCAATGAAATGGTTAATTGTAACTAAACCCGCAGGTCACGTGTGTTAGGTTTCCAGGTGCTAGCGTCAGGGTTTGTAACCTTTCCAACCTTAACCAATACGTGGC"

native_barcodes = {
    'NB05': {
        'start': "AAGGTTACACAAACCCTGGACAAG",
        'start_r': "GAACAGGTCCCAAACACATTGGAA", # reversed
        'end': "CTTGTCCAGGGTTTGTGTAACCTT",
        'end_r': "TTCCAATGTGTTTGGGACCTGTTC" # reversed
    }
}


def main():
    '''
    Entry point for Chorepop. Gets arguments, processes them and then calls process_files function
    to do the actual work.
    :return:
    '''
    args = get_arguments()

    process_files(args.input_path, args.output, args.verbosity, args.print_dest)


def process_files(input_path, output_path, verbosity, print_dest):
    """
    Core function to process one or more input files and create the required output files.

    Iterates through the reads in one or more input files and bins or filters them into the
    output files as required.
    """

    read_files = get_input_files(input_path, verbosity, print_dest)

    if verbosity > 0:
        print(bold_underline('\nRead files found:'), flush=True, file=print_dest)
        for read_file in read_files:
            print(read_file, flush=True, file=print_dest)

    for read_file in read_files:
        process_read_file(read_file, verbosity, print_dest)

    if verbosity > 0:
        print(bold_underline('\nRead files found:'), flush=True, file=print_dest)
        for read_file in read_files:
            print(read_file, flush=True, file=print_dest)


def get_input_files(input_path, verbosity, print_dest):
    '''
    Takes a path to a single file or a directory and returns a list of file paths to be processed.
    :param input_file_or_directory: The input path
    :param verbosity: Verbosity level to report
    :param print_dest: Where to report (stdout or stderr)
    :return: An array of file paths to process
    '''
    input_files = []

    if os.path.isfile(input_path):
        input_files.append(input_path)

    # If the input is a directory, search it recursively for fastq files.
    elif os.path.isdir(input_path):
        input_files = sorted([os.path.join(dir_path, f)
                              for dir_path, _, filenames in os.walk(input_path)
                              for f in filenames
                              if f.lower().endswith('.fastq') or f.lower().endswith('.fastq.gz') or
                              f.lower().endswith('.fasta') or f.lower().endswith('.fasta.gz')])
        if not input_files:
            sys.exit('Error: could not find FASTQ/FASTA files in ' + input_path)

    else:
        sys.exit('Error: could not find ' + input_path)

    return input_files


def process_read_file(read_file, verbosity, print_dest):
    """
    Iterates through the reads in an input files and bins or filters them into the
    output files as required.
    """

    for read in SeqIO.parse(read_file, "fastq"):
        process_read(read, print_dest)

def process_read(read, print_dest):
    '''
    Processes a read to find barcodes and returns the results
    :param name: The name of the read
    :param read:  The sequence
    '''

    nuc_matrix = parasail.matrix_create("ACGT", 2, -1)

    call_barcode(read, native_barcodes, 10, 0, nuc_matrix)

def call_barcode(read, barcodes, open, extend, matrix):

    name = read.id

    query_start = str(read.seq)
    query_end = str(read.seq)

    for barcode_id in barcodes:
        # result_start = align_barcode(query_start, barcodes[barcode_id]['start'], open, extend, matrix)
        # result_end = align_barcode(query_end, barcodes[barcode_id]['end'], open, extend, matrix)
        #
        # print(name, result_start['identity'], result_end['identity'])
        # print(result_start['ref'] + " .... " + result_end['ref'] + "\n" +
        #       result_start['comp'] + " .... " + result_end['comp'] + "\n" +
        #       result_start['query'] + " .... " + result_end['ref'] + "\n")

        result_all = align_barcode(str(read.seq), barcodes[barcode_id]['start'] + "---" + barcodes[barcode_id]['end'], open, extend, matrix)

        print(name, result_all['identity'], result_all['cigar'])
        print(result_all['ref'] + "\n" +
              result_all['comp'] + "\n" +
              result_all['query'] + "\n")

def align_barcode(query, reference, open, extend, matrix):

    result = parasail.sw_trace_striped_8(query, reference, open, extend, matrix)
    traceback = result.get_traceback('|', '.', ' ')
    cigar = result.get_cigar().decode

    result = parasail.sw_stats_striped_8(query, reference, open, extend, matrix)

    return {
        "matches": result.matches,
        "length": result.len_ref,
        "score": result.score,
        "identity": result.matches / result.len_ref,
        "cigar": cigar,
        "ref": traceback.ref,
        "comp": traceback.comp,
        "query": traceback.query
    }




def get_arguments():
    '''
    Parse the command line arguments.
    '''
    parser = argparse.ArgumentParser(description='Readucks: a simple demuxing tool for nanopore data.',
                                     formatter_class=MyHelpFormatter, add_help=False)

    main_group = parser.add_argument_group('Main options')
    main_group.add_argument('-i', '--input', dest='input_path', required=True,
                            help='FASTQ of input reads or a directory which will be '
                                 'recursively searched for FASTQ files (required).')
    main_group.add_argument('-o', '--output', required=True,
                            help='Output filename (or filename prefix)')
    main_group.add_argument('-v', '--verbosity', type=int, default=1,
                            help='Level of output information: 0 = none, 1 = some, 2 = lots')

    help_args = parser.add_argument_group('Help')
    help_args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                           help='Show this help message and exit')
    help_args.add_argument('--version', action='version', version=__version__,
                           help="Show program's version number and exit")

    args = parser.parse_args()

    if args.output is None:
        # output is to stdout so print messages to stderr
        args.print_dest = sys.stderr
    else:
        args.print_dest = sys.stdout

    return args


