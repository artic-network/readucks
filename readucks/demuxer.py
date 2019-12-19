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

import parasail

DEBUG = True

def demux_read(read, barcodes, single_barcode, threshold, secondary_threshold, open, extend, matrix, store_alignments):
    '''
    Processes a read to find barcodes and returns the results
    :param name: The name of the read
    :param read:  The sequence
    '''

    query_start = str(read.seq)[:100]
    query_end = str(read.seq)[-100:]

    start_results = []
    end_results = []

    for barcode_id in barcodes:
        result_start = get_score(barcode_id, query_start, barcodes[barcode_id]['start'], open, extend, matrix)
        result_end = get_score(barcode_id, query_end, barcodes[barcode_id]['end'], open, extend, matrix)

        if DEBUG:
            result_start = get_stats(barcode_id, query_start, barcodes[barcode_id]['start'], open, extend, matrix)
            result_end = get_stats(barcode_id, query_end, barcodes[barcode_id]['end'], open, extend, matrix)
            result_start = get_alignment(query_start, barcodes[barcode_id]['start'], open, extend, matrix, result_start)
            result_end = get_alignment(query_end, barcodes[barcode_id]['end'], open, extend, matrix, result_end)

        start_results.append(result_start)
        end_results.append(result_end)

    start_results.sort(key=lambda k: -k['score'])
    end_results.sort(key=lambda k: -k['score'])

    if DEBUG:
        print(read.name + ": ")
        for index, start in enumerate(start_results):
            end = end_results[index]
            print_alignment(start, end)
        print("\n\n")

    start_best = get_stats(start_results[0]['id'], query_start, barcodes[start_results[0]['id']]['start'], open, extend, matrix)
    end_best = get_stats(end_results[0]['id'], query_end, barcodes[end_results[0]['id']]['end'], open, extend, matrix)

    if store_alignments:
        start_best = get_alignment(query_start, barcodes[start_best['id']]['start'], open, extend, matrix, start_best)
        end_best = get_alignment(query_end, barcodes[end_best['id']]['end'], open, extend, matrix, end_best)

    if start_best['identity'] >= end_best['identity']:
        primary = start_best
        primary['start'] = 1
        secondary = end_best
        secondary['start'] = 0
    else:
        primary = end_best
        primary['start'] = 0
        secondary = start_best
        secondary['start'] = 1

    call = call_barcode(primary, secondary, single_barcode, threshold, secondary_threshold)

    return {
        'name': read.name,
        'call': call,
        'primary': primary,
        'secondary': secondary
    }

def call_barcode(primary, secondary, single_barcode, threshold, secondary_threshold):

    if single_barcode:
        if primary['identity'] >= threshold:
            return primary['id']

    if primary['identity'] >= threshold and secondary['identity'] >= secondary_threshold and primary['id'] == secondary['id']:
        return primary['id']

    return "none"


def print_result(result):
    start = result['primary'] if result['primary']['start'] == 1 else result['secondary']
    end = result['secondary'] if result['secondary']['start'] == 0 else result['primary']

    print(result['name'] + ": ")
    print_alignment(start, end)


def print_alignment(start, end):
    print(start['id'], start['score'], start['identity'], " .... ", end['id'], end['score'], end['identity'])
    print(start['trace']['ref'] + " .... " + end['trace']['ref'] + "\n" +
          start['trace']['comp'] + " .... " + end['trace']['comp'] + "\n" +
          start['trace']['query'] + " .... " + end['trace']['query'] + "\n")


def get_score(id, query, reference, open, extend, matrix):
    result = parasail.sw_striped_8(query, reference, open, extend, matrix)
    return {
        'id': id,
        'score': result.score
    }

def get_stats(id, query, reference, open, extend, matrix):

    result = parasail.sw_stats_striped_8(query, reference, open, extend, matrix)

    return {
        'id': id,
        'matches': result.matches,
        'length': result.len_ref,
        'score': result.score,
        'identity': result.matches / result.len_ref,
    }

def get_alignment(query, reference, open, extend, matrix, results):

    result = parasail.sw_trace_striped_8(query, reference, open, extend, matrix)
    traceback = result.get_traceback('|', '.', ' ')
    cigar = result.get_cigar().decode

    # add traceback to results object
    results['trace'] = {
        'cigar': cigar,
        'ref': traceback.ref,
        'comp': traceback.comp,
        'query': traceback.query
    }

    return results

