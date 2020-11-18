subject: "boy"
relation: "is sitting in"
object: "barn"
confidence: 1.0
tree {
    node {
        sentenceIndex: 0
        index: 2
    }
    node {
        sentenceIndex: 0
        index: 3
    }
    node {
        sentenceIndex: 0
        index: 4
    }
    node {
        sentenceIndex: 0
        index: 5
    }
    node {
        sentenceIndex: 0
        index: 7
    }
    edge {
        source: 4
        target: 2
        dep: "nsubj"
        isExtra: false
        sourceCopy: 0
        targetCopy: 0
        language: UniversalEnglish
    }
    edge {
        source: 4
        target: 3
        dep: "aux"
        isExtra: false
        sourceCopy: 0
        targetCopy: 0
        language: UniversalEnglish
    }
    edge {
        source: 4
        target: 7
        dep: "obl:in"
        isExtra: false
        sourceCopy: 0
        targetCopy: 0
        language: UniversalEnglish
    }
    edge {
        source: 7
        target: 5
        dep: "case"
        isExtra: false
        sourceCopy: 0
        targetCopy: 0
        language: UniversalEnglish
    }
    root: 4
}
subjectTokens {
    sentenceIndex: 0
    tokenIndex: 1
}
relationTokens {
    sentenceIndex: 0
    tokenIndex: 2
}
relationTokens {
    sentenceIndex: 0
    tokenIndex: 3
}
relationTokens {
    sentenceIndex: 0
    tokenIndex: 4
}
objectTokens {
    sentenceIndex: 0
    tokenIndex: 6
}
