
#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  extract_entities.py
#
# Description:
#               Extract entities from HC example data
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import os
import os.path as op
import stanza
import pandas as pd
from stanza.server import CoreNLPClient
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
# Create text pipeline
nlp = stanza.Pipeline(processors="tokenize,mwt,lemma,pos")

data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
f = open(op.join(data_dir, 'Kings',
                 'Prolific_pilot_all_transcripts', '3138838-TAT13.txt'), 'r')
text = f.read()
f.close()

with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(text)
# --> The CoreNLP server will be automatically started in the background upon the instantiation of the client.

# get the first sentence
sentence = ann.sentence[0]


# get the constituency parse of the first sentence
constituency_parse = sentence.parseTree
print(constituency_parse)
constituency_parse.child[0].value

print(sentence.basicDependencies)


# get the first token of the first sentence
token = sentence.token[8]
print(token.value, token.pos, token.ner)

# get an entity mention from the first sentence
print(sentence.mentions[1].entityMentionText)

# access the coref chain in the input text
print(ann.corefChain)


hild {
    child {
        child {
            child {
                value: "Well"
            }
            value: "UH"
            score: -2.3202738761901855
        }
        value: "INTJ"
        score: -2.370940923690796
    }
    child {
        child {
            value: ","
        }
        value: ","
        score: -0.00916041899472475
    }
    child {
        child {
            child {
                child {
                    value: "on"
                }
                value: "IN"
                score: -3.775491714477539
            }
            child {
                child {
                    child {
                        value: "the"
                    }
                    value: "DT"
                    score: -0.5893369317054749
                }
                child {
                    child {
                        value: "picture"
                    }
                    value: "NN"
                    score: -7.971802711486816
                }
                value: "NP"
                score: -10.600319862365723
            }
            value: "PP"
            score: -14.832088470458984
        }
        child {
            child {
                child {
                    value: "I"
                }
                value: "PRP"
                score: -1.959579586982727
            }
            value: "NP"
            score: -2.821143627166748
        }
        child {
            child {
                child {
                    value: "see"
                }
                value: "VBP"
                score: -4.33377742767334
            }
            child {
                child {
                    child {
                        child {
                            value: "four"
                        }
                        value: "CD"
                        score: -4.341630458831787
                    }
                    child {
                        child {
                            value: "men"
                        }
                        value: "NNS"
                        score: -5.355259895324707
                    }
                    value: "NP"
                    score: -13.7655029296875
                }
                child {
                    child {
                        child {
                            value: "lying"
                        }
                        value: "VBG"
                        score: -6.755360126495361
                    }
                    child {
                        child {
                            child {
                                value: "on"
                            }
                            value: "IN"
                            score: -2.73764967918396
                        }
                        child {
                            child {
                                child {
                                    value: "the"
                                }
                                value: "DT"
                                score: -0.5893369317054749
                            }
                            child {
                                child {
                                    value: "field"
                                }
                                value: "NN"
                                score: -7.400427341461182
                            }
                            value: "NP"
                            score: -10.028943061828613
                        }
                        value: "PP"
                        score: -13.28922176361084
                    }
                    value: "VP"
                    score: -22.177703857421875
                }
                value: "NP"
                score: -39.381553649902344
            }
            value: "VP"
            score: -49.26670837402344
        }
        value: "S"
        score: -71.37034606933594
    }
    child {
        child {
            value: ","
        }
        value: ","
        score: -0.00916041899472475
    }
    child {
        child {
            child {
                child {
                    value: "they"
                }
                value: "PRP"
                score: -2.4822897911071777
            }
            value: "NP"
            score: -3.3438539505004883
        }
        child {
            child {
                child {
                    value: "seem"
                }
                value: "VBP"
                score: -5.168150901794434
            }
            child {
                child {
                    child {
                        child {
                            value: "to"
                        }
                        value: "TO"
                        score: -0.015242991037666798
                    }
                    child {
                        child {
                            child {
                                value: "be"
                            }
                            value: "VB"
                            score: -0.009304866194725037
                        }
                        child {
                            child {
                                child {
                                    child {
                                        value: "some"
                                    }
                                    value: "DT"
                                    score: -4.490752696990967
                                }
                                child {
                                    child {
                                        value: "sort"
                                    }
                                    value: "NN"
                                    score: -7.978192329406738
                                }
                                value: "NP"
                                score: -14.067277908325195
                            }
                            child {
                                child {
                                    child {
                                        value: "of"
                                    }
                                    value: "IN"
                                    score: -0.6558045148849487
                                }
                                child {
                                    child {
                                        child {
                                            value: "workers"
                                        }
                                        value: "NNS"
                                        score: -5.933518886566162
                                    }
                                    value: "NP"
                                    score: -8.974897384643555
                                }
                                value: "PP"
                                score: -10.051775932312012
                            }
                            value: "NP"
                            score: -24.541553497314453
                        }
                        value: "VP"
                        score: -29.694377899169922
                    }
                    value: "VP"
                    score: -29.740581512451172
                }
                value: "S"
                score: -30.0257625579834
            }
            value: "VP"
            score: -40.008262634277344
        }
        value: "S"
        score: -43.91356658935547
    }
    child {
        child {
            value: "and"
        }
        value: "CC"
        score: -0.0193919874727726
    }
    child {
        child {
            child {
                child {
                    child {
                        value: "they"
                    }
                    value: "PRP"
                    score: -2.4822897911071777
                }
                value: "NP"
                score: -3.3438539505004883
            }
            child {
                child {
                    child {
                        value: "seem"
                    }
                    value: "VBP"
                    score: -5.168150901794434
                }
                child {
                    child {
                        child {
                            child {
                                value: "to"
                            }
                            value: "TO"
                            score: -0.015242991037666798
                        }
                        child {
                            child {
                                child {
                                    value: "be"
                                }
                                value: "VB"
                                score: -0.009304866194725037
                            }
                            child {
                                child {
                                    child {
                                        value: "tired"
                                    }
                                    value: "JJ"
                                    score: -6.965800762176514
                                }
                                value: "ADJP"
                                score: -7.669890403747559
                            }
                            value: "VP"
                            score: -11.859903335571289
                        }
                        value: "VP"
                        score: -11.906106948852539
                    }
                    value: "S"
                    score: -12.19128704071045
                }
                value: "VP"
                score: -22.173786163330078
            }
            value: "S"
            score: -26.07908821105957
        }
        child {
            child {
                value: "and"
            }
            value: "CC"
            score: -0.0193919874727726
        }
        child {
            child {
                child {
                    child {
                        value: "presumably"
                    }
                    value: "RB"
                    score: -8.037413597106934
                }
                value: "ADVP"
                score: -8.128385543823242
            }
            child {
                child {
                    value: ","
                }
                value: ","
                score: -0.00916041899472475
            }
            child {
                child {
                    child {
                        value: "maybe"
                    }
                    value: "RB"
                    score: -5.9769463539123535
                }
                value: "ADVP"
                score: -6.067918300628662
            }
            child {
                child {
                    child {
                        value: "it"
                    }
                    value: "PRP"
                    score: -1.8175901174545288
                }
                value: "NP"
                score: -2.67915415763855
            }
            child {
                child {
                    child {
                        value: "\342\200\231s"
                    }
                    value: "VBZ"
                    score: -3.821916341781616
                }
                child {
                    child {
                        child {
                            value: "during"
                        }
                        value: "IN"
                        score: -5.040411472320557
                    }
                    child {
                        child {
                            child {
                                value: "midday"
                            }
                            value: "NN"
                            score: -10.264880180358887
                        }
                        value: "NP"
                        score: -12.358820915222168
                    }
                    value: "PP"
                    score: -17.92186164855957
                }
                child {
                    child {
                        value: ","
                    }
                    value: ","
                    score: -0.009031965397298336
                }
                child {
                    child {
                        child {
                            value: "because"
                        }
                        value: "IN"
                        score: -2.622575521469116
                    }
                    child {
                        child {
                            child {
                                child {
                                    value: "their"
                                }
                                value: "PRP$"
                                score: -1.6789374351501465
                            }
                            child {
                                child {
                                    value: "hats"
                                }
                                value: "NNS"
                                score: -9.01156997680664
                            }
                            value: "NP"
                            score: -15.767658233642578
                        }
                        child {
                            child {
                                child {
                                    value: "are"
                                }
                                value: "VBP"
                                score: -0.22139421105384827
                            }
                            child {
                                child {
                                    child {
                                        value: "covering"
                                    }
                                    value: "VBG"
                                    score: -6.0886406898498535
                                }
                                child {
                                    child {
                                        child {
                                            value: "their"
                                        }
                                        value: "PRP$"
                                        score: -1.6789374351501465
                                    }
                                    child {
                                        child {
                                            value: "heads"
                                        }
                                        value: "NNS"
                                        score: -7.7458977699279785
                                    }
                                    value: "NP"
                                    score: -13.24549674987793
                                }
                                value: "VP"
                                score: -21.4462890625
                            }
                            value: "VP"
                            score: -25.915287017822266
                        }
                        value: "S"
                        score: -42.019474029541016
                    }
                    value: "SBAR"
                    score: -45.034141540527344
                }
                value: "VP"
                score: -76.01790618896484
            }
            value: "S"
            score: -102.61265563964844
        }
        value: "S"
        score: -133.54824829101562
    }
    child {
        child {
            value: "."
        }
        value: "."
        score: -0.0575326532125473
    }
    value: "S"
    score: -265.03729248046875
}
value: "ROOT"
score: -265.2088317871094
