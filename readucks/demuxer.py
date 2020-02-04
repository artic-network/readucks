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

from .barcodes import NATIVE_BARCODES, PCR_BARCODES, RAPID_BARCODES

# these need to be globals as the c object in matrix cannot be passed to a thread pool function
nuc_matrix = None
gap_open = 10
gap_extend = 1

def set_alignment_settings(open, extend, matrix):
    global gap_open, gap_extend, nuc_matrix

    gap_open = open
    gap_extend = extend
    nuc_matrix = matrix


def demux_read(read, barcodes, single_barcode, threshold, secondary_threshold, mode, additional_info, verbosity):
    '''
    Processes a read to find barcodes and returns the results
    :param name: The name of the read
    :param read:  The sequence
    '''
    query_start = str(read.seq)[:100]
    query_end = str(read.seq)[-100:]

    results = []

    for barcode_id in barcodes:
        result_start = get_score(barcode_id, query_start, barcodes[barcode_id]['start'], gap_open, gap_extend, nuc_matrix)
        result_end = get_score(barcode_id, query_end, barcodes[barcode_id]['end'], gap_open, gap_extend, nuc_matrix)
        results.append(combine_results(result_start, result_end))

    results.sort(key=lambda k: (-k['start_score'], -k['end_score']))
    start_best = get_all(results[0]['id'], query_start, barcodes[results[0]['id']]['start'], gap_open,
                         gap_extend, nuc_matrix)
    if additional_info or mode == "lenient":
        start_best_end = get_all(results[0]['id'], query_end, barcodes[results[0]['id']]['end'], gap_open,
                                 gap_extend, nuc_matrix)
        start_best = combine_results(start_best, start_best_end, start_best)

    results.sort(key=lambda k: (-k['end_score'], -k['start_score']))
    end_best = get_all(results[0]['id'], query_end, barcodes[results[0]['id']]['end'], gap_open, gap_extend,
                       nuc_matrix)
    if additional_info or mode == "lenient":
        end_best_start = get_all(results[0]['id'], query_start, barcodes[results[0]['id']]['start'], gap_open,
                                 gap_extend, nuc_matrix)
        end_best = combine_results(end_best_start, end_best, end_best)

    #if verbosity > 2:
    #    print(read.name + ": ")
    #    print_alignment(start_best, end_best)
    #    print("\n\n")

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

    if mode == 'lenient':
        primary['dominant'] = 1
    else:
        primary['dominant'] = 0

    call = call_barcode(primary, secondary, single_barcode, threshold, secondary_threshold, mode, verbosity)

    return {
        'name': read.name,
        'call': call,
        'primary': primary,
        'secondary': secondary
    }


def combine_results(start_result, end_result, primary_result=None):
    all_results = {}
    if primary_result:
        for key in primary_result:
            all_results[key] = primary_result[key]

    all_results['id'] = start_result['id']
    for key in start_result:
        all_results["start_%s" %key] = start_result[key]
    for key in end_result:
        all_results["end_%s" %key] = end_result[key]

    return all_results

def call_barcode_stringent_mode(primary, secondary, threshold, secondary_threshold, verbosity):

    if primary['identity'] >= threshold and secondary['identity'] >= secondary_threshold \
            and primary['id'] == secondary['id']:
        return primary['id']

    elif verbosity > 2:
        if primary['identity'] >= threshold and primary['start'] == 1 \
            and primary['end_identity'] >= secondary_threshold:
            return 'mismatched_barcode'
        elif primary['identity'] >= threshold and primary['start'] == 0 \
                and primary['start_identity'] >= secondary_threshold:
            return 'mismatched_barcode'
        elif primary['identity'] >= threshold:
            return 'low_secondary_identity'
        else:
            return 'low_primary_identity'

    return 'unassigned'

def call_barcode_lenient_mode(primary, secondary, threshold, secondary_threshold, verbosity):

    if primary['start'] == 1 and primary['start_identity'] >= threshold and secondary['end_identity'] >= secondary_threshold:
        return primary['id']
    elif primary['start'] == 0 and primary['end_identity'] >= threshold and secondary['start_identity'] >= secondary_threshold:
        return primary['id']

    elif verbosity > 2:
        if primary['start'] == 1 and primary['start_identity'] >= threshold:
            return 'low_secondary_identity'
        elif primary['start'] == 0 and primary['end_identity'] >= threshold:
            return 'low_secondary_identity'
        elif primary['start'] == 1 and primary['end_identity'] >= secondary_threshold:
            return 'low_primary_identity'
        elif primary['start'] == 0 and primary['end_identity'] >= secondary_threshold:
            return 'low_primary_identity'

    return 'unassigned'


def call_barcode(primary, secondary, single_barcode, threshold, secondary_threshold, mode, verbosity):

    if single_barcode:
        if primary['identity'] >= threshold:
            return primary['id']

    if mode == "stringent":
        return call_barcode_stringent_mode(primary, secondary, threshold, secondary_threshold, verbosity)
    elif mode == "lenient":
        return call_barcode_lenient_mode(primary, secondary, threshold, secondary_threshold, verbosity)

    return 'unassigned'


def print_result(result):
    start = result['primary'] if result['primary']['start'] == 1 else result['secondary']
    print(result['primary']['dominant'])
    end = result['secondary'] if result['secondary']['start'] == 0 and result['primary']['dominant'] == 0 else result['primary']

    print(result['name'] + ": " + result['call'])
    print_alignment(start, end)



def print_alignment(start, end):
    print("Start: " + start['id'], "| score:", start['score'], "| identity:", "{:.2f}".format(start['identity']),
          "| similarity:", "{:.2f}".format(start['similarity']), "| matches:", start['matches'],
          "| mismatches:", start['mismatches'], "| length:", start['length'])
    print("  End: " + end['id'], "| score:", end['score'], "| identity:", "{:.2f}".format(end['identity']),
          "| similarity:", "{:.2f}".format(end['similarity']), "| matches:", end['matches'],
          "| mismatches:", end['mismatches'], "| length:", end['length'])
    print(start['trace']['ref'] + " .... " + end['trace']['ref'] + "\n" +
          start['trace']['comp'] + " .... " + end['trace']['comp'] + "\n" +
          start['trace']['query'] + " .... " + end['trace']['query'] + "\n")


def get_score(id, query, reference, open, extend, matrix):
    # score = parasail.sw_striped_8(query, reference, open, extend, matrix)
    score = parasail.sg_qx_striped_sat(query, reference, open, extend, matrix)
    result = {
        'id': id,
        'score': score.score,
    }

    del score

    return result


def get_stats(id, query, reference, open, extend, matrix):

    # stats = parasail.sw_stats_striped_8(query, reference, open, extend, matrix)
    stats = parasail.sg_qx_stats_striped_sat(query, reference, open, extend, matrix)

    result = {
        'id': id,
        'matches': stats.matches,
        'length': stats.len_ref,
        'score': stats.score,
        'identity': stats.matches / stats.len_ref
    }

    del stats

    return result


def get_all(id, query, reference, open, extend, matrix):

    # stats = parasail.sw_stats(query, reference, open, extend, matrix)
    stats = parasail.sg_qx_stats_striped_sat(query, reference, open, extend, matrix)

    result = {
        'id': id,
        'matches': stats.matches,
        'score': stats.score,
        'identity': stats.matches / stats.len_ref
    }

    del stats

    # trace = parasail.sw_trace(query, reference, open, extend, matrix)
    trace = parasail.sg_qx_trace_striped_sat(query, reference, open, extend, matrix)
    traceback = trace.get_traceback()
    cigar = trace.get_cigar()

    result['length'] = len(traceback.comp)
    result['mismatches'] = traceback.comp.count('.')
    result['similarity'] = result['matches'] / (result['matches'] + result['mismatches'])

    result['trace'] = {
            'cigar': cigar.decode,
            'ref': traceback.ref,
            'comp': traceback.comp,
            'query': traceback.query,
            'query_start': cigar.beg_query,
            'query_end': trace.end_query,
            'ref_start': cigar.beg_ref,
            'ref_end': trace.end_ref,
    }

    del trace

    return result

def native_barcode_adapter(barcode_id):
    start_SQK_NSK007 = "AATGTACTTCGTTCAGTTACGTATTGCT"
    end_SQK_NSK007 = "GCAATACGTAACTGAACGAAGT"

    start_barcode_seq = NATIVE_BARCODES[barcode_id]['start']
    end_barcode_seq = NATIVE_BARCODES[barcode_id]['end']

    start_full_seq = start_SQK_NSK007 + "AAGGTTAA" + start_barcode_seq + "CAGCACCT"
    end_full_seq = "AGGTGCTG" + end_barcode_seq + "TTAACCTTA" + end_SQK_NSK007

    return start_full_seq, end_full_seq

def rapid_barcode_adapter(barcode_id):
    rapid_adapter = "GTTTTCGCATTTATCGTGAAACGCTTTCGCGTTTTTCGTGCGCCGCTTCA"

    start_barcode_seq = RAPID_BARCODES[barcode_id]['start']
    start_full_seq = 'AATGTACTTCGTTCAGTTACGTATTGCT' + start_barcode_seq + rapid_adapter

    return start_full_seq
