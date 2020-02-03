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
from collections import defaultdict
from datetime import datetime
from multiprocessing.pool import ThreadPool
from functools import partial

from Bio import SeqIO
import parasail

from .demuxer import set_alignment_settings, demux_read, print_result
from .barcodes import NATIVE_BARCODES, PCR_BARCODES, RAPID_BARCODES
from .misc import bold_underline, MyHelpFormatter, output_progress_line
from .version import __version__


def main():
    '''
    Entry point for Readucks. Gets arguments, processes them and then calls process_files function
    to do the actual work.
    :return:
    '''
    args = get_arguments()

    barcode_set = 'native'
    # if args.native_barcodes:
    #     barcode_set = 'native'
    if args.pcr_barcodes:
        barcode_set = 'pcr'
    if args.rapid_barcodes:
        barcode_set = 'rapid'

    settings = {
        'barcode_set': "native",
        'single_barcode': args.single,
        'threshold': args.threshold / 100.0,
        'secondary_threshold': None,
        'mode': args.mode,
        'additional_info': args.summary_info,
        'verbosity': args.verbosity
    }

    if args.secondary_threshold:
        settings['secondary_threshold'] = args.secondary_threshold / 100.0

    # set_alignment_settings( 10,
    #                         1,
    #                         parasail.matrix_create("ACGT", 3, -2))
    set_alignment_settings( -args.scoring_scheme_vals[2],
                            -args.scoring_scheme_vals[3],
                            parasail.matrix_create("ACGT", args.scoring_scheme_vals[0], args.scoring_scheme_vals[1]))
    output_path = None
    if args.output_dir:
        if os.path.isdir(args.output_dir):
            output_path = args.output_dir.rstrip("/") + "/"

    output = {
        'path': output_path,
        'prefix': args.prefix,
        'bin_barcodes': args.bin_barcodes,
        'annotate_files': args.annotate_files,
        'extended_info': args.extended_info,
        'summary_info': args.summary_info,
        'bin_files': {}
    }

    process_files(args.input_path, output, barcode_set, args.limit_barcodes_to, settings, args.verbosity, args.threads, args.num_reads_in_batch)

def process_files(input_path, output, barcode_set, limit_barcodes_to, settings, verbosity, threads, batch_size):
    """
    Core function to process one or more input files and create the required output files.

    Iterates through the reads in one or more input files and bins or filters them into the
    output files as required.
    """

    start_time = datetime.now()

    read_files = get_input_files(input_path)

    if verbosity > 0:
        print(bold_underline('\n' + str(len(read_files)) + " read {} found".format('files' if len(read_files) > 1 else 'file')), flush=True)

    # if verbosity > 1:
        for read_file in read_files:
            print(read_file, flush=True)

    barcode_counts = defaultdict(int)

    if barcode_set == 'native':
        barcodes = NATIVE_BARCODES
    elif barcode_set == 'pcr':
        barcodes = PCR_BARCODES
    elif barcode_set == 'rapid':
        barcodes = RAPID_BARCODES
    else:
        sys.exit(
            'Unrecognised barcode_set: ' + barcode_set)

    barcode_list = {}
    if limit_barcodes_to:
        for index, barcode in enumerate(barcodes):
            if (index + 1) in limit_barcodes_to:
                barcode_list[barcode] = barcodes[barcode]

    if verbosity > 0:
        print(bold_underline('\nBarcode set: ' + barcode_set), flush=True)
        if limit_barcodes_to:
            print('limited to: ', end =' ')
            for barcode in barcode_list:
                print(barcode, end = ' ')
            print()

    output['file_type'] = get_output_file_type(read_files)

    if verbosity > 0:
        print(bold_underline("\nProcessing files"), flush=True)
        output_progress_line(0, len(read_files))


    for index, read_file in enumerate(read_files):

        process_read_file(read_file, output, barcodes, settings, barcode_counts, verbosity, threads, batch_size)

        if verbosity > 0:
            output_progress_line(index, len(read_files))

    if verbosity > 0:
        output_progress_line(len(read_files), len(read_files))

    time = datetime.now() - start_time

    if verbosity > 0:
        print("\n\nTime taken: " + str(time.total_seconds()) + " secs")

        if output['bin_barcodes']:
            if verbosity > 0:
                print(bold_underline("\nBinned reads by barcode"), flush=True)

        for f in output['bin_files'].values():
            if verbosity > 0:
                print(f.name, flush=True)
            f.close()

    if verbosity > 0:
        print(bold_underline('\nBarcodes called:'), flush=True)
        barcode_names = []
        for barcode_id in barcode_counts:
            barcode_names.append(barcode_id)

        barcode_names.sort()

        for barcode_name in barcode_names:
            print(barcode_name + ": " + str(barcode_counts[barcode_name]), flush=True)


def get_input_files(input_path):
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
                              if f.lower().endswith('.fastq') or #f.lower().endswith('.fastq.gz') or
                              f.lower().endswith('.fasta') # or f.lower().endswith('.fasta.gz')
                              ])
        if not input_files:
            sys.exit('Error: could not find FASTQ/FASTA files in ' + input_path)

    else:
        sys.exit('Error: could not find ' + input_path)

    return input_files


def get_output_file_type(read_files):
    """
    returns the output file type. This will be 'fastq' unless one of the
    input files is a 'fasta'
    :param read_files:
    :return: the file type
    """
    file_type = 'fastq'

    for read_file in read_files:
        if read_file.lower().endswith('.fasta'):
            file_type = 'fasta'

    return file_type


def process_read_file(read_file, output, barcodes, settings, barcode_counts, verbosity, threads = 1, batch_size = 200):
    """
    Iterates through the reads in an input files and bins or filters them into the
    output files as required.
    """
    demux_func = partial(demux_read,
                         barcodes = barcodes,
                         single_barcode = settings['single_barcode'],
                         threshold = settings['threshold'],
                         secondary_threshold = settings['secondary_threshold'],
                         mode = settings['mode'],
                         additional_info = settings['additional_info'],
                         verbosity = settings['verbosity'])

    file_type = 'fastq'
    if read_file.lower().endswith('.fasta'):
        file_type = 'fasta'

    records = SeqIO.index(read_file, file_type)
    read_names = list(records.keys())
    n_reads = len(records)

    results = []
    for i in range(0, n_reads, batch_size):
        reads = [records[r] for r in read_names[i:i + batch_size]]

        if threads == 1: # if single threading then don't use a thread pool
            for read in reads:
                results.append(demux_func(read))
        else:
            with ThreadPool(threads) as pool:
                results.extend(pool.map(demux_func, reads))

    print("Reads length: ", n_reads, " and results length: ", len(results))

    annotation_file = None
    summary_file = None
    if output['annotate_files'] or output['summary_info']:
        # strip extensions off
        path_stem = read_file.rstrip(".gz") \
            .rstrip(".fastq").rstrip(".fasta") \
            .rstrip(".FASTQ").rstrip(".FASTA")

        if output['path']:
            name_stem = path_stem.split('/')[-1]
            path_stem = output['path']
            path_stem += output['prefix'] if output['prefix'] else ""
            path_stem += name_stem

        annotation_file = open(path_stem + ".csv", 'wt')
        # if verbosity > 1:
        #     print("\nWriting annotation file: " + annotation_file.name)

        if output['extended_info']:
            print('name', 'barcode',
                  'primary_barcode', 'primary_is_start', 'primary_score', 'primary_identity', 'primary_matches', 'primary_length',
                  'secondary_barcode', 'secondary_is_start', 'secondary_score', 'secondary_identity', 'secondary_matches', 'secondary_length',
                  file=annotation_file, sep=',')
        else:
            print('name', 'barcode', file=annotation_file, sep=',')

        if output['summary_info']:
            summary_file = open(path_stem + ".summary.csv", 'wt')
            print('name', 'barcode',
                  'primary_barcode', 'primary_is_start', 'primary_start_score', 'primary_start_identity',
                  'primary_start_matches', 'primary_start_length', 'primary_end_score', 'primary_end_identity',
                  'primary_end_matches', 'primary_end_length', 'secondary_barcode', 'secondary_is_start',
                  'secondary_start_score', 'secondary_start_identity', 'secondary_start_matches',
                  'secondary_start_length', 'secondary_end_score', 'secondary_end_identity',
                  'secondary_end_matches', 'secondary_end_length',
                  file=summary_file, sep=',')

    # threadpool map function maintains the same order as the input data
    for result in results:
        barcode_counts[result['call']] += 1

        if annotation_file:
            if output['extended_info']:
                print(result['name'], result['call'],
                      result['primary']['id'], result['primary']['start'], result['primary']['score'],
                      result['primary']['identity'], result['primary']['matches'], result['primary']['length'],
                      result['secondary']['id'], result['secondary']['start'], result['secondary']['score'],
                      result['secondary']['identity'], result['secondary']['matches'], result['secondary']['length'],
                      file=annotation_file, sep=',')
            else:
                print(result['name'], result['call'], file=annotation_file, sep=',')

        if output['summary_info']:
            print(result['name'], result['call'],
                  result['primary']['id'], result['primary']['start'], result['primary']['start_score'],
                  result['primary']['start_identity'], result['primary']['start_matches'],
                  result['primary']['start_length'], result['primary']['end_score'], result['primary']['end_identity'],
                  result['primary']['end_matches'], result['primary']['end_length'],
                  result['secondary']['id'], result['secondary']['start'], result['secondary']['start_score'],
                  result['secondary']['start_identity'], result['secondary']['start_matches'],
                  result['secondary']['start_length'], result['secondary']['end_score'],
                  result['secondary']['end_identity'], result['secondary']['end_matches'],
                  result['secondary']['end_length'],
                  file=summary_file, sep=',')

        if output['bin_barcodes']:
            read = records[result['name']]
            bin_read(read, result, output)

        if verbosity > 1:
            print_result(result)

    if annotation_file:
        annotation_file.close()

    if summary_file:
        summary_file.close()

    records.close()

def bin_read(read, result, output):
    """
    Bins a read into the appropriate file (creating it if necessary).
    """

    if result['call'] not in output['bin_files']:
        filename = output['path'] if output['path'] else ""
        filename += output['prefix'] if output['prefix'] else ""

        filename += result['call'] + "." + output['file_type']
        output['bin_files'][result['call']] = open(filename, "wt")

    SeqIO.write(read, output['bin_files'][result['call']], output['file_type'])

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
    main_group.add_argument('-o', '--output_dir',
                            help='Output directory (default: working directory)')
    main_group.add_argument('-b', '--bin_barcodes', action='store_true',
                            help='Reads will be binned based on their barcode and saved to '
                                 'separate files.')
    main_group.add_argument('-a', '--annotate_files', action='store_true',
                            help='Writes a CSV file for each input file containing barcode calls '
                                 'for each read. ')
    main_group.add_argument('-e', '--extended_info', action='store_true',
                            help='Writes extended information about barcode calls. ')
    main_group.add_argument('-s', '--summary_info', action='store_true',
                            help='Writes another file with information about barcode calls. ')
    main_group.add_argument('-m', '--mode', default='precision',
                            help='Demuxing mode, maximizing either ["precision","recall"].')
    main_group.add_argument('-p', '--prefix',
                            help='Optional prefix to file names')
    main_group.add_argument('-t', '--threads', type=int, default=2,
                            help='The number of threads to use (1 to turn off multithreading)')
    main_group.add_argument('-n', '--num_reads_in_batch', type=int, default=200,
                            help='The number of reads to process (and hold in memory) at a time')
    main_group.add_argument('-v', '--verbosity', type=int, default=1,
                            help='Level of output information: 0 = none, 1 = some, 2 = lots')

    barcode_group = parser.add_argument_group('Demuxing options')
    barcode_group.add_argument('--single', action='store_true',
                               help='Only attempts to match a single barcode at one end (default double)')
    barcode_group.add_argument('--native_barcodes', action='store_true',
                               help='Only attempts to match the 24 native barcodes (default)')
    barcode_group.add_argument('--pcr_barcodes', action='store_true',
                               help='Only attempts to match the 96 PCR barcodes')
    barcode_group.add_argument('--rapid_barcodes', action='store_true',
                               help='Only attempts to match the 12 rapid barcodes')
    barcode_group.add_argument('--limit_barcodes_to', nargs='+', type=int, required=False,
                               help='Specify a list of barcodes to look for (numbers refer to native, PCR or rapid)')
    # barcode_group.add_argument('--custom_barcodes',
    #                            help='CSV file containing custom barcode sequences')

    barcode_search_group = parser.add_argument_group('Barcode search settings',
                                                     'Settings for how to search for and call barcodes')
    barcode_search_group.add_argument('--threshold', type=float, default=90.0,
                                      help='A read must have at least this percent identity to a barcode')
    barcode_search_group.add_argument('--secondary_threshold', type=float, default=70.0,
                                      help='The second barcode must have at least this percent identity (and match the first one)')
    barcode_search_group.add_argument('--scoring_scheme', type=str, default='3,-6,-5,-2',
                                      help='Comma-delimited string of alignment scores: match, '
                                           'mismatch, gap open, gap extend')

    help_args = parser.add_argument_group('Help')
    help_args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                           help='Show this help message and exit')
    help_args.add_argument('--version', action='version', version=__version__,
                           help="Show program's version number and exit")

    args = parser.parse_args()

    if (args.native_barcodes and args.pcr_barcodes) or (args.native_barcodes and args.rapid_barcodes) or (args.pcr_barcodes and args.rapid_barcodes):
        sys.exit(
            'Error: only one of the following options may be used: --native_barcodes, --pcr_barcodes or --rapid_barcodes')

    if (args.single and args.secondary_threshold):
        args.secondary_threshold = None

    if (args.threshold > 0.0 and args.threshold < 1.0):
        sys.exit(
            'Error: the option --threshold should be given as a percentage')

    if (args.secondary_threshold is not None and args.secondary_threshold > 0.0 and args.secondary_threshold < 1.0):
        sys.exit(
            'Error: the option --secondary_threshold should be given as a percentage')

    try:
        scoring_scheme = [int(x) for x in args.scoring_scheme.split(',')]
    except ValueError:
        sys.exit('Error: incorrectly formatted scoring scheme')
    if len(scoring_scheme) != 4:
        sys.exit('Error: incorrectly formatted scoring scheme')
    args.scoring_scheme_vals = scoring_scheme

    return args

