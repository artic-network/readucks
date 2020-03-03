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

read_fragment_length = 100

def set_alignment_settings(open, extend, matrix):
    global gap_open, gap_extend, nuc_matrix

    gap_open = open
    gap_extend = extend
    nuc_matrix = matrix

def best_read_identity(reads, barcodes, barcode_set):
    start_identities = {}
    end_identities = {}

    for barcode_id in barcodes:
        start_identities[barcode_id] = 0
        end_identities[barcode_id] = 0

        # Look at alignment of just the barcode, not the extended adapter sequence
        start_adapter_seq = barcodes[barcode_id]['start']
        end_adapter_seq = barcodes[barcode_id]['end']

        for read in reads:
            query_start = str(read.seq)[:read_fragment_length]
            result_start = get_all(barcode_id, query_start, start_adapter_seq, gap_open, gap_extend, nuc_matrix)
            if result_start['identity'] > start_identities[barcode_id]:
                start_identities[barcode_id] = result_start['identity']

            query_end = str(read.seq)[-read_fragment_length:]
            result_end = get_all(barcode_id, query_end, end_adapter_seq, gap_open, gap_extend, nuc_matrix)
            if result_end['identity'] > end_identities[barcode_id]:
                end_identities[barcode_id] = result_end['identity']

    return start_identities, end_identities


def demux_read(read, barcodes, barcode_set, single_barcode, threshold, secondary_threshold, score_diff, mode, additional_info, verbosity):
    '''
    Processes a read to find barcodes and returns the results
    :param name: The name of the read
    :param read:  The sequence
    '''
    query_start = str(read.seq)[:read_fragment_length]
    query_end = str(read.seq)[-read_fragment_length:]

    results = []

    for barcode_id in barcodes:
        start_adapter_seq = get_start_adapter_seq(barcode_id, barcode_set)
        end_adapter_seq = get_end_adapter_seq(barcode_id, barcode_set)

        if mode == 'porechop':
            result_start = get_identity(barcode_id, query_start, start_adapter_seq, gap_open, gap_extend,
                                     nuc_matrix)
            result_end = get_identity(barcode_id, query_end, end_adapter_seq, gap_open, gap_extend, nuc_matrix)
        else:
            result_start = get_score(barcode_id, query_start, start_adapter_seq, gap_open, gap_extend, nuc_matrix)
            result_end = get_score(barcode_id, query_end, end_adapter_seq, gap_open, gap_extend, nuc_matrix)
        results.append(combine_results(result_start, result_end))

    if mode == 'porechop':
        results.sort(key=lambda k: (-k['start_identity'], -k['end_identity']))
    else:
        results.sort(key=lambda k: (-k['start_score'], -k['end_score']))
    start_best = get_all(results[0]['id'], query_start, get_start_adapter_seq(results[0]['id'], barcode_set), gap_open,
                         gap_extend, nuc_matrix)
    if additional_info or mode == "lenient":
        start_best_end = get_all(results[0]['id'], query_end, get_end_adapter_seq(results[0]['id'], barcode_set), gap_open,
                                 gap_extend, nuc_matrix)
        start_best = combine_results(start_best, start_best_end, start_best)
    start_second_best = None
    if mode == 'porechop' and len(results) > 1:
        start_second_best = get_all(results[1]['id'], query_start, get_start_adapter_seq(results[1]['id'], barcode_set), gap_open,
                         gap_extend, nuc_matrix)

    if mode == 'porechop':
        results.sort(key=lambda k: (-k['end_identity'], -k['start_identity']))
    else:
        results.sort(key=lambda k: (-k['end_score'], -k['start_score']))
    end_best = get_all(results[0]['id'], query_end, get_end_adapter_seq(results[0]['id'], barcode_set), gap_open, gap_extend,
                       nuc_matrix)
    if additional_info or mode == "lenient":
        end_best_start = get_all(results[0]['id'], query_start, get_start_adapter_seq(results[0]['id'], barcode_set), gap_open,
                                 gap_extend, nuc_matrix)
        end_best = combine_results(end_best_start, end_best, end_best)
    end_second_best = None
    if mode == 'porechop' and len(results) > 1:
        end_second_best = get_all(results[1]['id'], query_end, get_end_adapter_seq(results[1]['id'], barcode_set), gap_open,
                         gap_extend, nuc_matrix)

    #if verbosity > 2:
    #    print(read.name + ": ")
    #    print_alignment(start_best, end_best)
    #    print("\n\n")

    if start_best['identity'] >= end_best['identity']:
        primary = start_best
        primary['start'] = 1
        primary_second = start_second_best
        secondary = end_best
        secondary['start'] = 0
        secondary_second = end_second_best
    else:
        primary = end_best
        primary['start'] = 0
        primary_second = end_second_best
        secondary = start_best
        secondary['start'] = 1
        secondary_second = start_second_best

    if mode == 'lenient':
        primary['dominant'] = 1
    else:
        primary['dominant'] = 0

    call = call_barcode(primary, secondary, primary_second, secondary_second, single_barcode, threshold, secondary_threshold, score_diff, mode, verbosity)

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

def call_barcode_porechop_mode(primary, secondary, primary_second, secondary_second, single_barcode, threshold, score_diff, verbosity):

    primary_over_threshold = (primary['identity'] >= threshold)
    primary_good_diff = (primary_second is None or primary['identity'] >= primary_second['identity'] + score_diff)
    secondary_over_threshold = (secondary['identity'] >= threshold)
    secondary_good_diff = (secondary_second is None or secondary['identity'] >= secondary_second['identity'] + score_diff)
    ids_match = (primary['id'] == secondary['id'])

    if single_barcode:
        if primary_over_threshold and primary_good_diff:
            return primary['id']

        elif verbosity > 2:
            if not primary_over_threshold:
                return 'low_primary_identity'
            elif not primary_good_diff:
                return 'bad_primary_diff'
    else:
        if ids_match and primary_over_threshold and primary_good_diff and secondary_over_threshold and secondary_good_diff:
            return primary['id']

        elif verbosity > 2:
            if not ids_match:
                return 'mismatched_barcode'
            elif not primary_over_threshold:
                return 'low_primary_identity'
            elif not primary_good_diff:
                return 'bad_primary_diff'
            elif not secondary_over_threshold:
                return 'low_secondary_identity'
            elif not secondary_good_diff:
                return 'bad_secondary_diff'

    return 'unassigned'

def call_barcode(primary, secondary, primary_second, secondary_second, single_barcode, threshold, secondary_threshold,
                 score_diff, mode, verbosity):

    if mode == 'porechop':
        return call_barcode_porechop_mode(primary, secondary, primary_second, secondary_second, single_barcode,
                                          threshold, score_diff, verbosity)

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
    if reference is None:
        result = {
            'id': id,
            'score': 0,
        }

        return result

    # score = parasail.sw_striped_8(query, reference, open, extend, matrix)
    score = parasail.sg_qx_striped_sat(query, reference, open, extend, matrix)
    result = {
        'id': id,
        'score': score.score,
    }

    del score

    return result

def get_identity(id, query, reference, open, extend, matrix):
    if reference is None:
        result = {
            'id': id,
            'score': 0,
            'identity': 0,
        }

        return result

    stats = parasail.sg_qx_stats_striped_sat(query, reference, open, extend, matrix)

    result = {
        'id': id,
        'score': stats.score,
        'identity': stats.matches / stats.length
    }

    del stats

    return result


def get_stats(id, query, reference, open, extend, matrix):
    if reference is None:
        result = {
            'id': id,
            'matches': 0,
            'length': 0,
            'score': 0,
            'identity': 0
        }
        return result

    # stats = parasail.sw_stats_striped_8(query, reference, open, extend, matrix)
    stats = parasail.sg_qx_stats_striped_sat(query, reference, open, extend, matrix)

    result = {
        'id': id,
        'matches': stats.matches,
        'length': stats.length,
        'score': stats.score,
        'identity': stats.matches / stats.length
    }

    del stats

    return result


def get_all(id, query, reference, open, extend, matrix):
    if reference is None:
        result = {
            'id': id,
            'matches': 0,
            'score': 0,
            'identity': 0,
            'length': 0,
            'mismatches': 0,
            'similarity': 0,
            'trace': {
                'cigar': '',
                'ref': '',
                'comp': '',
                'query': '',
                'query_start': 0,
                'query_end': 0,
                'ref_start': 0,
                'ref_end': 0
            }
        }
        return result

    # stats = parasail.sw_stats(query, reference, open, extend, matrix)
    stats = parasail.sg_qx_stats_striped_sat(query, reference, open, extend, matrix)

    result = {
        'id': id,
        'matches': stats.matches,
        'score': stats.score,
        'length': stats.length,
        'identity': stats.matches / stats.length
    }

    del stats

    # trace = parasail.sw_trace(query, reference, open, extend, matrix)
    trace = parasail.sg_qx_trace_striped_sat(query, reference, open, extend, matrix)
    traceback = trace.get_traceback()
    cigar = trace.get_cigar()

    #result['length'] = len(traceback.comp)
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

def get_start_adapter_seq(barcode_id, barcode_set):
    if barcode_set == 'native':
        start_SQK_NSK007 = "AATGTACTTCGTTCAGTTACGTATTGCT"
        start_barcode_seq = NATIVE_BARCODES[barcode_id]['start']
        start_full_seq = start_SQK_NSK007 + "AAGGTTAA" + start_barcode_seq + "CAGCACCT"
    elif barcode_set == 'rapid':
        rapid_adapter = "GTTTTCGCATTTATCGTGAAACGCTTTCGCGTTTTTCGTGCGCCGCTTCA"
        start_barcode_seq = RAPID_BARCODES[barcode_id]['start']
        start_full_seq = 'AATGTACTTCGTTCAGTTACGTATTGCT' + start_barcode_seq + rapid_adapter
    elif barcode_set == 'pcr':
        start_full_seq = PCR_BARCODES[barcode_id]['start']
    else:
        start_full_seq = None
    return start_full_seq

def get_end_adapter_seq(barcode_id, barcode_set):
    if barcode_set == 'native':
        end_SQK_NSK007 = "GCAATACGTAACTGAACGAAGT"
        end_barcode_seq = NATIVE_BARCODES[barcode_id]['end']
        end_full_seq = "AGGTGCTG" + end_barcode_seq + "TTAACCTTA" + end_SQK_NSK007
    elif barcode_set == 'pcr':
        end_full_seq = PCR_BARCODES[barcode_id]['end']
    else:
        end_full_seq = None
    return end_full_seq