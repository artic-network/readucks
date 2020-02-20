NATIVE_BARCODES = {
    # The native barcodes use the rev comp barcode at the start
    # of the read and the forward barcode at the end of the read.
    'NB01': {
		'name': "Native Barcode 1",
        'start': "CACAAAGACACCGACAACTTTCTT",
        'end': "AAGAAAGTTGTCGGTGTCTTTGTG"
    },
    'NB02': {
		'name': "Native Barcode 2",
        'start': "ACAGACGACTACAAACGGAATCGA",
        'end': "TCGATTCCGTTTGTAGTCGTCTGT"
    },
    'NB03': {
		'name': "Native Barcode 3",
        'start': "CCTGGTAACTGGGACACAAGACTC",
        'end': "GAGTCTTGTGTCCCAGTTACCAGG"
    },
    'NB04': {
		'name': "Native Barcode 4",
        'start': "TAGGGAAACACGATAGAATCCGAA",
        'end': "TTCGGATTCTATCGTGTTTCCCTA"
    },
    'NB05': {
		'name': "Native Barcode 5",
        'start': "AAGGTTACACAAACCCTGGACAAG",
        'end': "CTTGTCCAGGGTTTGTGTAACCTT"
    },
    'NB06': {
		'name': "Native Barcode 6",
        'start': "GACTACTTTCTGCCTTTGCGAGAA",
        'end': "TTCTCGCAAAGGCAGAAAGTAGTC"
    },
    'NB07': {
		'name': "Native Barcode 7",
        'start': "AAGGATTCATTCCCACGGTAACAC",
        'end': "GTGTTACCGTGGGAATGAATCCTT"
    },
    'NB08': {
		'name': "Native Barcode 8",
        'start': "ACGTAACTTGGTTTGTTCCCTGAA",
        'end': "TTCAGGGAACAAACCAAGTTACGT"
    },
    'NB09': {
		'name': "Native Barcode 9",
        'start': "AACCAAGACTCGCTGTGCCTAGTT",
        'end': "AACTAGGCACAGCGAGTCTTGGTT"
    },
    'NB10': {
		'name': "Native Barcode 10",
        'start': "GAGAGGACAAAGGTTTCAACGCTT",
        'end': "AAGCGTTGAAACCTTTGTCCTCTC"
    },
    'NB11': {
		'name': "Native Barcode 11",
        'start': "TCCATTCCCTCCGATAGATGAAAC",
        'end': "GTTTCATCTATCGGAGGGAATGGA"
    },
    'NB12': {
		'name': "Native Barcode 12",
        'start': "TCCGATTCTGCTTCTTTCTACCTG",
        'end': "CAGGTAGAAAGAAGCAGAATCGGA"
    },

    'NB13': {
		'name': "Native Barcode 13",
        'start': "AGAACGACTTCCATACTCGTGTGA",
        'end': "TCACACGAGTATGGAAGTCGTTCT"
    },
    'NB14': {
		'name': "Native Barcode 14",
        'start': "AACGAGTCTCTTGGGACCCATAGA",
        'end': "TCTATGGGTCCCAAGAGACTCGTT"
    },
    'NB15': {
		'name': "Native Barcode 15",
        'start': "AGGTCTACCTCGCTAACACCACTG",
        'end': "CAGTGGTGTTAGCGAGGTAGACCT"
    },
    'NB16': {
		'name': "Native Barcode 16",
        'start': "CGTCAACTGACAGTGGTTCGTACT",
        'end': "AGTACGAACCACTGTCAGTTGACG"
    },
    'NB17': {
		'name': "Native Barcode 17",
        'start': "ACCCTCCAGGAAAGTACCTCTGAT",
        'end': "ATCAGAGGTACTTTCCTGGAGGGT"
    },
    'NB18': {
		'name': "Native Barcode 18",
        'start': "CCAAACCCAACAACCTAGATAGGC",
        'end': "GCCTATCTAGGTTGTTGGGTTTGG"
    },
    'NB19': {
		'name': "Native Barcode 19",
        'start': "GTTCCTCGTGCAGTGTCAAGAGAT",
        'end': "ATCTCTTGACACTGCACGAGGAAC"
    },
    'NB20': {
		'name': "Native Barcode 20",
        'start': "TTGCGTCCTGTTACGAGAACTCAT",
        'end': "ATGAGTTCTCGTAACAGGACGCAA"
    },
    'NB21': {
		'name': "Native Barcode 21",
        'start': "GAGCCTCTCATTGTCCGTTCTCTA",
        'end': "TAGAGAACGGACAATGAGAGGCTC"
    },
    'NB22': {
		'name': "Native Barcode 22",
        'start': "ACCACTGCCATGTATCAAAGTACG",
        'end': "CGTACTTTGATACATGGCAGTGGT"
    },
    'NB23': {
		'name': "Native Barcode 23",
        'start': "CTTACTACCCAGTGAACCTCCTCG",
        'end': "CGAGGAGGTTCACTGGGTAGTAAG"
    },
    'NB24': {
		'name': "Native Barcode 24",
        'start': "GCATAGTTCTGCATGATGGGTTAG",
        'end': "CTAACCCATCATGCAGAACTATGC"
    }
}

PCR_BARCODES = {
    'BC01': {
		'name': "PCR Barcode 1",
        'start': "AAGAAAGTTGTCGGTGTCTTTGTG",
        'end': "CACAAAGACACCGACAACTTTCTT"
    },
    'BC02': {
		'name': "PCR Barcode 2",
        'start': "TCGATTCCGTTTGTAGTCGTCTGT",
        'end': "ACAGACGACTACAAACGGAATCGA"
    },
    'BC03': {
		'name': "PCR Barcode 3",
        'start': "GAGTCTTGTGTCCCAGTTACCAGG",
        'end': "CCTGGTAACTGGGACACAAGACTC"
    },
    'BC04': {
		'name': "PCR Barcode 4",
        'start': "TTCGGATTCTATCGTGTTTCCCTA",
        'end': "TAGGGAAACACGATAGAATCCGAA"
    },
    'BC05': {
		'name': "PCR Barcode 5",
        'start': "CTTGTCCAGGGTTTGTGTAACCTT",
        'end': "AAGGTTACACAAACCCTGGACAAG"
    },
    'BC06': {
		'name': "PCR Barcode 6",
        'start': "TTCTCGCAAAGGCAGAAAGTAGTC",
        'end': "GACTACTTTCTGCCTTTGCGAGAA"
    },
    'BC07': {
		'name': "PCR Barcode 7",
        'start': "GTGTTACCGTGGGAATGAATCCTT",
        'end': "AAGGATTCATTCCCACGGTAACAC"
    },
    'BC08': {
		'name': "PCR Barcode 8",
        'start': "TTCAGGGAACAAACCAAGTTACGT",
        'end': "ACGTAACTTGGTTTGTTCCCTGAA"
    },
    'BC09': {
		'name': "PCR Barcode 9",
        'start': "AACTAGGCACAGCGAGTCTTGGTT",
        'end': "AACCAAGACTCGCTGTGCCTAGTT"
    },
    'BC10': {
		'name': "PCR Barcode 10",
        'start': "AAGCGTTGAAACCTTTGTCCTCTC",
        'end': "GAGAGGACAAAGGTTTCAACGCTT"
    },
    'BC11': {
		'name': "PCR Barcode 11",
        'start': "GTTTCATCTATCGGAGGGAATGGA",
        'end': "TCCATTCCCTCCGATAGATGAAAC"
    },
    'BC12': {
		'name': "PCR Barcode 12",
        'start': "CAGGTAGAAAGAAGCAGAATCGGA",
        'end': "TCCGATTCTGCTTCTTTCTACCTG"
    },
    'BC13': {
		'name': "PCR Barcode 13",
        'start': "AGAACGACTTCCATACTCGTGTGA",
        'end': "TCACACGAGTATGGAAGTCGTTCT"
    },
    'BC14': {
		'name': "PCR Barcode 14",
        'start': "AACGAGTCTCTTGGGACCCATAGA",
        'end': "TCTATGGGTCCCAAGAGACTCGTT"
    },
    'BC15': {
		'name': "PCR Barcode 15",
        'start': "AGGTCTACCTCGCTAACACCACTG",
        'end': "CAGTGGTGTTAGCGAGGTAGACCT"
    },
    'BC16': {
		'name': "PCR Barcode 16",
        'start': "CGTCAACTGACAGTGGTTCGTACT",
        'end': "AGTACGAACCACTGTCAGTTGACG"
    },
    'BC17': {
		'name': "PCR Barcode 17",
        'start': "ACCCTCCAGGAAAGTACCTCTGAT",
        'end': "ATCAGAGGTACTTTCCTGGAGGGT"
    },
    'BC18': {
		'name': "PCR Barcode 18",
        'start': "CCAAACCCAACAACCTAGATAGGC",
        'end': "GCCTATCTAGGTTGTTGGGTTTGG"
    },
    'BC19': {
		'name': "PCR Barcode 19",
        'start': "GTTCCTCGTGCAGTGTCAAGAGAT",
        'end': "ATCTCTTGACACTGCACGAGGAAC"
    },
    'BC20': {
		'name': "PCR Barcode 20",
        'start': "TTGCGTCCTGTTACGAGAACTCAT",
        'end': "ATGAGTTCTCGTAACAGGACGCAA"
    },
    'BC21': {
		'name': "PCR Barcode 21",
        'start': "GAGCCTCTCATTGTCCGTTCTCTA",
        'end': "TAGAGAACGGACAATGAGAGGCTC"
    },
    'BC22': {
		'name': "PCR Barcode 22",
        'start': "ACCACTGCCATGTATCAAAGTACG",
        'end': "CGTACTTTGATACATGGCAGTGGT"
    },
    'BC23': {
		'name': "PCR Barcode 23",
        'start': "CTTACTACCCAGTGAACCTCCTCG",
        'end': "CGAGGAGGTTCACTGGGTAGTAAG"
    },
    'BC24': {
		'name': "PCR Barcode 24",
        'start': "GCATAGTTCTGCATGATGGGTTAG",
        'end': "CTAACCCATCATGCAGAACTATGC"
    },
    'BC25': {
		'name': "PCR Barcode 25",
        'start': "GTAAGTTGGGTATGCAACGCAATG",
        'end': "CATTGCGTTGCATACCCAACTTAC"
    },
    'BC26': {
		'name': "PCR Barcode 26",
        'start': "CATACAGCGACTACGCATTCTCAT",
        'end': "ATGAGAATGCGTAGTCGCTGTATG"
    },
    'BC27': {
		'name': "PCR Barcode 27",
        'start': "CGACGGTTAGATTCACCTCTTACA",
        'end': "TGTAAGAGGTGAATCTAACCGTCG"
    },
    'BC28': {
		'name': "PCR Barcode 28",
        'start': "TGAAACCTAAGAAGGCACCGTATC",
        'end': "GATACGGTGCCTTCTTAGGTTTCA"
    },
    'BC29': {
		'name': "PCR Barcode 29",
        'start': "CTAGACACCTTGGGTTGACAGACC",
        'end': "GGTCTGTCAACCCAAGGTGTCTAG"
    },
    'BC30': {
		'name': "PCR Barcode 30",
        'start': "TCAGTGAGGATCTACTTCGACCCA",
        'end': "TGGGTCGAAGTAGATCCTCACTGA"
    },
    'BC31': {
		'name': "PCR Barcode 31",
        'start': "TGCGTACAGCAATCAGTTACATTG",
        'end': "CAATGTAACTGATTGCTGTACGCA"
    },
    'BC32': {
		'name': "PCR Barcode 32",
        'start': "CCAGTAGAAGTCCGACAACGTCAT",
        'end': "ATGACGTTGTCGGACTTCTACTGG"
    },
    'BC33': {
		'name': "PCR Barcode 33",
        'start': "CAGACTTGGTACGGTTGGGTAACT",
        'end': "AGTTACCCAACCGTACCAAGTCTG"
    },
    'BC34': {
		'name': "PCR Barcode 34",
        'start': "GGACGAAGAACTCAAGTCAAAGGC",
        'end': "GCCTTTGACTTGAGTTCTTCGTCC"
    },
    'BC35': {
		'name': "PCR Barcode 35",
        'start': "CTACTTACGAAGCTGAGGGACTGC",
        'end': "GCAGTCCCTCAGCTTCGTAAGTAG"
    },
    'BC36': {
		'name': "PCR Barcode 36",
        'start': "ATGTCCCAGTTAGAGGAGGAAACA",
        'end': "TGTTTCCTCCTCTAACTGGGACAT"
    },
    'BC37': {
		'name': "PCR Barcode 37",
        'start': "GCTTGCGATTGATGCTTAGTATCA",
        'end': "TGATACTAAGCATCAATCGCAAGC"
    },
    'BC38': {
		'name': "PCR Barcode 38",
        'start': "ACCACAGGAGGACGATACAGAGAA",
        'end': "TTCTCTGTATCGTCCTCCTGTGGT"
    },
    'BC39': {
		'name': "PCR Barcode 39",
        'start': "CCACAGTGTCAACTAGAGCCTCTC",
        'end': "GAGAGGCTCTAGTTGACACTGTGG"
    },
    'BC40': {
		'name': "PCR Barcode 40",
        'start': "TAGTTTGGATGACCAAGGATAGCC",
        'end': "GGCTATCCTTGGTCATCCAAACTA"
    },
    'BC41': {
		'name': "PCR Barcode 41",
        'start': "GGAGTTCGTCCAGAGAAGTACACG",
        'end': "CGTGTACTTCTCTGGACGAACTCC"
    },
    'BC42': {
		'name': "PCR Barcode 42",
        'start': "CTACGTGTAAGGCATACCTGCCAG",
        'end': "CTGGCAGGTATGCCTTACACGTAG"
    },
    'BC43': {
		'name': "PCR Barcode 43",
        'start': "CTTTCGTTGTTGACTCGACGGTAG",
        'end': "CTACCGTCGAGTCAACAACGAAAG"
    },
    'BC44': {
		'name': "PCR Barcode 44",
        'start': "AGTAGAAAGGGTTCCTTCCCACTC",
        'end': "GAGTGGGAAGGAACCCTTTCTACT"
    },
    'BC45': {
		'name': "PCR Barcode 45",
        'start': "GATCCAACAGAGATGCCTTCAGTG",
        'end': "CACTGAAGGCATCTCTGTTGGATC"
    },
    'BC46': {
		'name': "PCR Barcode 46",
        'start': "GCTGTGTTCCACTTCATTCTCCTG",
        'end': "CAGGAGAATGAAGTGGAACACAGC"
    },
    'BC47': {
		'name': "PCR Barcode 47",
        'start': "GTGCAACTTTCCCACAGGTAGTTC",
        'end': "GAACTACCTGTGGGAAAGTTGCAC"
    },
    'BC48': {
		'name': "PCR Barcode 48",
        'start': "CATCTGGAACGTGGTACACCTGTA",
        'end': "TACAGGTGTACCACGTTCCAGATG"
    },
    'BC49': {
		'name': "PCR Barcode 49",
        'start': "ACTGGTGCAGCTTTGAACATCTAG",
        'end': "CTAGATGTTCAAAGCTGCACCAGT"
    },
    'BC50': {
		'name': "PCR Barcode 50",
        'start': "ATGGACTTTGGTAACTTCCTGCGT",
        'end': "ACGCAGGAAGTTACCAAAGTCCAT"
    },
    'BC51': {
		'name': "PCR Barcode 51",
        'start': "GTTGAATGAGCCTACTGGGTCCTC",
        'end': "GAGGACCCAGTAGGCTCATTCAAC"
    },
    'BC52': {
		'name': "PCR Barcode 52",
        'start': "TGAGAGACAAGATTGTTCGTGGAC",
        'end': "GTCCACGAACAATCTTGTCTCTCA"
    },
    'BC53': {
		'name': "PCR Barcode 53",
        'start': "AGATTCAGACCGTCTCATGCAAAG",
        'end': "CTTTGCATGAGACGGTCTGAATCT"
    },
    'BC54': {
		'name': "PCR Barcode 54",
        'start': "CAAGAGCTTTGACTAAGGAGCATG",
        'end': "CATGCTCCTTAGTCAAAGCTCTTG"
    },
    'BC55': {
		'name': "PCR Barcode 55",
        'start': "TGGAAGATGAGACCCTGATCTACG",
        'end': "CGTAGATCAGGGTCTCATCTTCCA"
    },
    'BC56': {
		'name': "PCR Barcode 56",
        'start': "TCACTACTCAACAGGTGGCATGAA",
        'end': "TTCATGCCACCTGTTGAGTAGTGA"
    },
    'BC57': {
		'name': "PCR Barcode 57",
        'start': "GCTAGGTCAATCTCCTTCGGAAGT",
        'end': "ACTTCCGAAGGAGATTGACCTAGC"
    },
    'BC58': {
		'name': "PCR Barcode 58",
        'start': "CAGGTTACTCCTCCGTGAGTCTGA",
        'end': "TCAGACTCACGGAGGAGTAACCTG"
    },
    'BC59': {
		'name': "PCR Barcode 59",
        'start': "TCAATCAAGAAGGGAAAGCAAGGT",
        'end': "ACCTTGCTTTCCCTTCTTGATTGA"
    },
    'BC60': {
		'name': "PCR Barcode 60",
        'start': "CATGTTCAACCAAGGCTTCTATGG",
        'end': "CCATAGAAGCCTTGGTTGAACATG"
    },
    'BC61': {
		'name': "PCR Barcode 61",
        'start': "AGAGGGTACTATGTGCCTCAGCAC",
        'end': "GTGCTGAGGCACATAGTACCCTCT"
    },
    'BC62': {
		'name': "PCR Barcode 62",
        'start': "CACCCACACTTACTTCAGGACGTA",
        'end': "TACGTCCTGAAGTAAGTGTGGGTG"
    },
    'BC63': {
		'name': "PCR Barcode 63",
        'start': "TTCTGAAGTTCCTGGGTCTTGAAC",
        'end': "GTTCAAGACCCAGGAACTTCAGAA"
    },
    'BC64': {
		'name': "PCR Barcode 64",
        'start': "GACAGACACCGTTCATCGACTTTC",
        'end': "GAAAGTCGATGAACGGTGTCTGTC"
    },
    'BC65': {
		'name': "PCR Barcode 65",
        'start': "TTCTCAGTCTTCCTCCAGACAAGG",
        'end': "CCTTGTCTGGAGGAAGACTGAGAA"
    },
    'BC66': {
		'name': "PCR Barcode 66",
        'start': "CCGATCCTTGTGGCTTCTAACTTC",
        'end': "GAAGTTAGAAGCCACAAGGATCGG"
    },
    'BC67': {
		'name': "PCR Barcode 67",
        'start': "GTTTGTCATACTCGTGTGCTCACC",
        'end': "GGTGAGCACACGAGTATGACAAAC"
    },
    'BC68': {
		'name': "PCR Barcode 68",
        'start': "GAATCTAAGCAAACACGAAGGTGG",
        'end': "CCACCTTCGTGTTTGCTTAGATTC"
    },
    'BC69': {
		'name': "PCR Barcode 69",
        'start': "TACAGTCCGAGCCTCATGTGATCT",
        'end': "AGATCACATGAGGCTCGGACTGTA"
    },
    'BC70': {
		'name': "PCR Barcode 70",
        'start': "ACCGAGATCCTACGAATGGAGTGT",
        'end': "ACACTCCATTCGTAGGATCTCGGT"
    },
    'BC71': {
		'name': "PCR Barcode 71",
        'start': "CCTGGGAGCATCAGGTAGTAACAG",
        'end': "CTGTTACTACCTGATGCTCCCAGG"
    },
    'BC72': {
		'name': "PCR Barcode 72",
        'start': "TAGCTGACTGTCTTCCATACCGAC",
        'end': "GTCGGTATGGAAGACAGTCAGCTA"
    },
    'BC73': {
		'name': "PCR Barcode 73",
        'start': "AAGAAACAGGATGACAGAACCCTC",
        'end': "GAGGGTTCTGTCATCCTGTTTCTT"
    },
    'BC74': {
		'name': "PCR Barcode 74",
        'start': "TACAAGCATCCCAACACTTCCACT",
        'end': "AGTGGAAGTGTTGGGATGCTTGTA"
    },
    'BC75': {
		'name': "PCR Barcode 75",
        'start': "GACCATTGTGATGAACCCTGTTGT",
        'end': "ACAACAGGGTTCATCACAATGGTC"
    },
    'BC76': {
		'name': "PCR Barcode 76",
        'start': "ATGCTTGTTACATCAACCCTGGAC",
        'end': "GTCCAGGGTTGATGTAACAAGCAT"
    },
    'BC77': {
		'name': "PCR Barcode 77",
        'start': "CGACCTGTTTCTCAGGGATACAAC",
        'end': "GTTGTATCCCTGAGAAACAGGTCG"
    },
    'BC78': {
		'name': "PCR Barcode 78",
        'start': "AACAACCGAACCTTTGAATCAGAA",
        'end': "TTCTGATTCAAAGGTTCGGTTGTT"
    },
    'BC79': {
		'name': "PCR Barcode 79",
        'start': "TCTCGGAGATAGTTCTCACTGCTG",
        'end': "CAGCAGTGAGAACTATCTCCGAGA"
    },
    'BC80': {
		'name': "PCR Barcode 80",
        'start': "CGGATGAACATAGGATAGCGATTC",
        'end': "GAATCGCTATCCTATGTTCATCCG"
    },
    'BC81': {
		'name': "PCR Barcode 81",
        'start': "CCTCATCTTGTGAAGTTGTTTCGG",
        'end': "CCGAAACAACTTCACAAGATGAGG"
    },
    'BC82': {
		'name': "PCR Barcode 82",
        'start': "ACGGTATGTCGAGTTCCAGGACTA",
        'end': "TAGTCCTGGAACTCGACATACCGT"
    },
    'BC83': {
		'name': "PCR Barcode 83",
        'start': "TGGCTTGATCTAGGTAAGGTCGAA",
        'end': "TTCGACCTTACCTAGATCAAGCCA"
    },
    'BC84': {
		'name': "PCR Barcode 84",
        'start': "GTAGTGGACCTAGAACCTGTGCCA",
        'end': "TGGCACAGGTTCTAGGTCCACTAC"
    },
    'BC85': {
		'name': "PCR Barcode 85",
        'start': "AACGGAGGAGTTAGTTGGATGATC",
        'end': "GATCATCCAACTAACTCCTCCGTT"
    },
    'BC86': {
		'name': "PCR Barcode 86",
        'start': "AGGTGATCCCAACAAGCGTAAGTA",
        'end': "TACTTACGCTTGTTGGGATCACCT"
    },
    'BC87': {
		'name': "PCR Barcode 87",
        'start': "TACATGCTCCTGTTGTTAGGGAGG",
        'end': "CCTCCCTAACAACAGGAGCATGTA"
    },
    'BC88': {
		'name': "PCR Barcode 88",
        'start': "TCTTCTACTACCGATCCGAAGCAG",
        'end': "CTGCTTCGGATCGGTAGTAGAAGA"
    },
    'BC89': {
		'name': "PCR Barcode 89",
        'start': "ACAGCATCAATGTTTGGCTAGTTG",
        'end': "CAACTAGCCAAACATTGATGCTGT"
    },
    'BC90': {
		'name': "PCR Barcode 90",
        'start': "GATGTAGAGGGTACGGTTTGAGGC",
        'end': "GCCTCAAACCGTACCCTCTACATC"
    },
    'BC91': {
		'name': "PCR Barcode 91",
        'start': "GGCTCCATAGGAACTCACGCTACT",
        'end': "AGTAGCGTGAGTTCCTATGGAGCC"
    },
    'BC92': {
		'name': "PCR Barcode 92",
        'start': "TTGTGAGTGGAAAGATACAGGACC",
        'end': "GGTCCTGTATCTTTCCACTCACAA"
    },
    'BC93': {
		'name': "PCR Barcode 93",
        'start': "AGTTTCCATCACTTCAGACTTGGG",
        'end': "CCCAAGTCTGAAGTGATGGAAACT"
    },
    'BC94': {
		'name': "PCR Barcode 94",
        'start': "GATTGTCCTCAAACTGCCACCTAC",
        'end': "GTAGGTGGCAGTTTGAGGACAATC"
    },
    'BC95': {
		'name': "PCR Barcode 95",
        'start': "CCTGTCTGGAAGAAGAATGGACTT",
        'end': "AAGTCCATTCTTCTTCCAGACAGG"
    },
    'BC96': {
		'name': "PCR Barcode 96",
        'start': "CTGAACGGTCATAGAGTCCACCAT",
        'end': "ATGGTGGACTCTATGACCGTTCAG"
    }
}

RAPID_BARCODES = {
    'BC01': {
		'name': "Rapid Barcode 1",
        'start': "AAGAAAGTTGTCGGTGTCTTTGTG",
        'end': None
    },
    'BC02': {
		'name': "Rapid Barcode 2",
        'start': "TCGATTCCGTTTGTAGTCGTCTGT",
        'end': None
    },
    'BC03': {
		'name': "Rapid Barcode 3",
        'start': "GAGTCTTGTGTCCCAGTTACCAGG",
        'end': None
    },
    'BC04': {
		'name': "Rapid Barcode 4",
        'start': "TTCGGATTCTATCGTGTTTCCCTA",
        'end': None
    },
    'BC05': {
		'name': "Rapid Barcode 5",
        'start': "CTTGTCCAGGGTTTGTGTAACCTT",
        'end': None
    },
    'BC06': {
		'name': "Rapid Barcode 6",
        'start': "TTCTCGCAAAGGCAGAAAGTAGTC",
        'end': None
    },
    'BC07': {
		'name': "Rapid Barcode 7",
        'start': "GTGTTACCGTGGGAATGAATCCTT",
        'end': None
    },
    'BC08': {
		'name': "Rapid Barcode 8",
        'start': "TTCAGGGAACAAACCAAGTTACGT",
        'end': None
    },
    'BC09': {
		'name': "Rapid Barcode 9",
        'start': "AACTAGGCACAGCGAGTCTTGGTT",
        'end': None
    },
    'BC10': {
		'name': "Rapid Barcode 10",
        'start': "AAGCGTTGAAACCTTTGTCCTCTC",
        'end': None
    },
    'BC11': {
		'name': "Rapid Barcode 11",
        'start': "GTTTCATCTATCGGAGGGAATGGA",
        'end': None
    },
    'BC12': {
		'name': "Rapid Barcode 12",
        'start': "CAGGTAGAAAGAAGCAGAATCGGA",
        'end': None
    }
}


