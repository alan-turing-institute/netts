sentence = ex_stanza.sentence[0]
idx_sentence = 0


.token[mention.beginIndex: mention.endIndex]
sentence.enhancedDependencies.edge
[source: 2
 target: 1
 dep: "nsubj"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 2
 target: 4
 dep: "obj"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 2
 target: 13
 dep: "punct"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 4
 target: 3
 dep: "det"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish,

 source: 4
 target: 8
 dep: "nmod:in"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish,

 source: 4
 target: 12
 dep: "nmod:against"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish,

 source: 8
 target: 5
 dep: "case"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 8
 target: 6
 dep: "det"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 8
 target: 7
 dep: "amod"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 12
 target: 9
 dep: "case"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 12
 target: 10
 dep: "det"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish, source: 12
 target: 11
 dep: "amod"
 isExtra: false
 sourceCopy: 0
 targetCopy: 0
 language: UniversalEnglish
 ]

# ----------------------------------- Save workspace ------------------------------
import shelve

del CoreNLPClient, client, __setitem__, __builtins__
# T = 'Hiya'
# val = [1, 2, 3]
filename = op.join(data_dir, 'extractions', file)
my_shelf = shelve.open(filename, 'n')  # 'n' for new

for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))

my_shelf.close()

# ----------------------------------- Restore workspace ------------------------------
my_shelf = shelve.open(filename)
for key in my_shelf:
    globals()[key] = my_shelf[key]

my_shelf.close()

print(extractions)
# Hiya
print(annotations)
# [1, 2, 3]


('it', 'distinctive'): 'is not', ('it', 'it'): 'is not', ('it', 'i'): 'think', ('it', 'clear'): 'is not',
