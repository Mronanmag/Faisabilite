def reverse(query) :
   return ''.join(reversed(query))

def complement(query,dict) :
    seq_comp = ""
    for nucl in query : 
        try :
            seq_comp += dict[nucl]
        except :
            seq_comp += nucl
    return seq_comp

def rev_function(query) :   
    dict_complement  = {"A":"T",
                        "G":"C",
                        "C":"G",
                        "T":"A",
                        "U":"A",
                        "R":"Y",
                        "Y":"R",
                        "S":"S",
                        "W":"W",
                        "K":"M",
                        "B":"V",
                        "V":"B",
                        "D":"H",
                        "H":"D",
                        "-":"-",
                        "I":"N"
                        }

    query_reverse = reverse(query)
    query_reverseComplement = complement(query_reverse,dict_complement)
    return query_reverseComplement
