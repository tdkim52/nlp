#############################################################
# Timothy Kim - W01011895
# February 28, 2015
# CSCI 404 @ 11am
#
# vtag.py - Homework #3
#
#
# See report.pdf for full details
#
#
#############################################################

import math

def vtag(train, test):

    tag_dict = {'###': ['###']}  # key: word, value: tag
    tag_count = {'###': 0}  # key: tag, value: count
    tagtag_count = {'######': 0}  # key: tag2tag3, value: count
    word_count = {'###': 0}  # key: word, value: count
    wordtag_count = {'###/###': 0}  # key: word/tag, value: count
    test_string = []
    test_tags = []
    num_sents = 0

    raw = open('enraw.txt', "r")
    vocab = []

    # causes '######' to appear in tagtag dictionary with a count of
    # 1 but does not actually appear in data
    prevtag = '###'

    # in one passage through training data, obtains words, tags
    # and all relevant counts
    print "Parsing training file..."
    for line in train:
        line = line[:-1]  # eliminates newline character
        tmp = line.split('/')
        # creates dictionary of word/tag combination counts
        if line in wordtag_count:
            count = wordtag_count[line] + 1
            wordtag_count.update({line: count})
        else:
            wordtag_count.update({line: 1})
        #tmp = line.split('/')
        # tmp[0] = word , tmp[1] =  tag
        # creates dictionary of possible tags for each unique word
        # and dictionary of word counts
        if tmp[0] in tag_dict:
            count = word_count[tmp[0]] + 1
            word_count.update({tmp[0]: count})
            tlist = tag_dict[tmp[0]]
            if not tmp[1] in tlist:
                tlist.append(tmp[1])
                tag_dict.update({tmp[0]: tlist})
        else:
            tag_dict.update({tmp[0]: list(tmp[1])})
            word_count.update({tmp[0]: 1})
        # creates dictionary of tag counts
        if tmp[1] in tag_count:
            count = tag_count[tmp[1]] + 1
            tag_count.update({tmp[1]: count})
        else:
            tag_count.update({tmp[1]: 1})
        # creates dictionary of tagtag keys with their counts
        # tagtag: prev tag followed by current tag
        tagtag = prevtag + tmp[1]
        prevtag = tmp[1]
        if tagtag in tagtag_count:
            count = tagtag_count[tagtag] + 1
            tagtag_count.update({tagtag: count})
        else:
            tagtag_count.update({tagtag: 1})

    print "Parsing testing file..."
    for line in test:
        line = line[:-1]
        tmp = line.split('/')
        test_string.append(tmp[0])
        test_tags.append(tmp[1])
        if tmp[0] == '###':
            num_sents = num_sents + 1

    print "Parsing enraw.txt file..."
    for line in raw:
        line = line[:-1]
        if not line in vocab:
            vocab.append(line)
    vocab = list(set(vocab) | set(word_count.keys()))

    vv = len(word_count.keys())

    # Maximum Likelihood Estimate functions
    # calculates probability of P(ti|ti-1)
    def ttMLE(tag3, tag2):
        if (tag2+tag3) not in tagtag_count:
            num = 0
        else:
            num = tagtag_count[tag2+tag3]
        denom = tag_count[tag2]
        #prob = float(num + 1) / (denom + vv)
        prob = float(num + 1) / (denom + len(vocab))
        prob = math.log(prob)
        return prob

    # calculates probability P(wi|ti)
    def wtMLE(word, tag):
        if not word+'/'+tag in wordtag_count:
            num = 0
        else:
            num = wordtag_count[word+'/'+tag]
        denom = tag_count[tag]
        if word == '###' and tag == '###':
            prob = 1.0
        else:
            #prob = float(num + 1) / (denom + vv)
            prob = float(num + 1) / (denom + len(vocab))
            prob = math.log(prob)
        return prob

    viterbi = []
    backpointer = []
    first_viterbi = {}
    first_backpointer = {}

    for tag in tag_dict[test_string[1]]:
        if tag == '###':
            continue
        first_viterbi[tag] = ttMLE(tag, '###') + wtMLE(test_string[1],tag)
        first_backpointer[tag] = '###'

    viterbi.append(first_viterbi)
    backpointer.append(first_backpointer)

    print "Determining Viterbi best tag sequence..."
    for i in range(2, len(test_string)-1):
        this_viterbi = {}
        this_backpointer = {}
        prev_viterbi = viterbi[-1]
        if not test_string[i] in tag_dict:
            temp = tag_count.keys()
            temp.remove('###')
            tag_dict.update({test_string[i]: temp})
        for tag in tag_dict[test_string[i]]:
            best_previous = max(prev_viterbi.keys(),
                                key = lambda prevtag: \
                                    prev_viterbi[prevtag] + ttMLE(tag, prevtag) + wtMLE(test_string[i], tag))
            this_viterbi[tag] = prev_viterbi[best_previous] + \
                                ttMLE(tag, best_previous) + wtMLE(test_string[i], tag)
            this_backpointer[tag] = best_previous
        viterbi.append(this_viterbi)
        backpointer.append(this_backpointer)

    prev_viterbi = viterbi[-1]
    best_previous = max(prev_viterbi.keys(),
                        key = lambda prevtag: \
                            prev_viterbi[prevtag] + ttMLE('###', prevtag))
    prob_tagsequence = prev_viterbi[best_previous] + ttMLE('###', best_previous)
    best_tagsequence = ['###', best_previous]
    backpointer.reverse()
    current_best = best_previous

    for bp in backpointer:
        best_tagsequence.append(bp[current_best])
        current_best = bp[current_best]
    best_tagsequence.reverse()

    overall = 0
    known = 0
    unknown = 0
    novel = 0
    for i in range(0, len(test_tags)):
        if test_tags[i] == best_tagsequence[i]:
            if test_tags[i] != '###':
                overall =  overall + 1
        if test_string[i] in word_count:
            if test_tags[i] == best_tagsequence[i]:
                if test_tags[i] != '###':
                    known =  known + 1
        if not test_string[i] in word_count:
            unknown = unknown + 1
            if test_tags[i] == best_tagsequence[i]:
                if test_tags[i] != '###':
                    novel = novel + 1

    print  "test sequence:", test_tags
    print "best sequence:" , best_tagsequence
    print "log prob:" , prob_tagsequence
    print ""

    # overall accuracy (not counting '###' tag matches)
    o = 100 * (float(overall) / (len(test_tags) - num_sents))
    k = 100 * (float(known) / (len(test_tags) - num_sents - unknown))
    if unknown == 0:
        print "Tagging accuracy (Viterbi decoding): {:.2f}% (known: {:.2f}% novel: N/A)".format(o,k)
    else:
        n = 100 * (float(novel) / unknown)
        print "Tagging accuracy (Viterbi decoding): {:.2f}% (known: {:.2f}% novel: {:.2f}%)".format(o,k,n)










if __name__ == "__main__":
    from sys import argv
    if len(argv) != 3:
        print "Usage: vtag.py [train filename] [test filename]"
    else:
        trainfd = open(argv[1], "r")
        testfd = open(argv[2], "r")
        vtag(trainfd, testfd)