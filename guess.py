#!/usr/bin/python3 

import json

class Guesser:
    """
    Abstract class that defines a strategy to guess which of the given options
    correctly answers the given question

    Args:
        question: A string
        options: An array of strings

    Returns:
        A list of indexes corresponding to the given options, from best to worst.
    """
    def guess(self, question, options):
        raise NotImplementedError()

class ResultsGuesser(Guesser):
    """
    Search web for:
        question + "option"

    Return the number of results for each search
    """

    def __init__(self, searcher):
        self.searcher = searcher

    def guess(self, question, options):
        scores = self.get_scores(question, options)
        return scores

    def get_scores(self, question, options, out='index'):
        #TODO parallelize
        scores = {}

        for i, opt in enumerate(options):

            answer = self.searcher.search(question+ ' ' + _q(opt))
            try:
                if out == 'scores':
                    scores[opt] = answer['webPages']['totalEstimatedMatches']
                else:
                    scores[i] = answer['webPages']['totalEstimatedMatches']
            except:
                print(json.dumps(answer, indent=4))
                print('--------------')
        return scores


class FrequencyGuesser(Guesser):
    """
    Search for question
    Count the number of times each option appears.

    TODO: Find a way to treat multi-word options 
    """
    def __init__(self, searcher):
        self.searcher = searcher

    def guess(self, question, options):
        results = {}

        answer = self.searcher.search(question)

        for opt in options:
            results[opt] = 0

        for a in answer['webPages']['value']:
            for opt in options:
                results[opt] += a['snippet'].count(min(opt.split(' '), key=(lambda x: a['snippet'].count(x))))

        return results



def _q(string):
    """ Quote a string """
    return '"' + string + '"'

def scores_to_indexes(options, scores, reverse=False):
    idx = []
    for k, v in sorted(scores, key=lambda key: scores[key], reverse=reverse):
        idx += options.index(k)
    return idx

def best(results):
    """
    Return best score
    """
    return max(results, key=(lambda key: results[key]))

def worst(results):
    """
    Return worst score
    """
    return min(results, key=(lambda key: results[key]))

def main():
    import search
    import extract
    import os
    import sys

    guessers = {
        'results':  ResultsGuesser(search.BingSearcher(os.environ['BING_API_KEY']))
    }

    if len(sys.argv) == 1:
        print("Usage: guess.py [guesser=results] image")
        return

    if len(sys.argv) == 2:
        if sys.argv[1] != "--help":
            img = sys.argv[1]
            g = "results"
        else:
            print("Usage: guess.py [guesser=results] image")

    if len(sys.argv) == 3:
        img = sys.argv[2]
        g = sys.argv[1]


    data = extract.run_extraction(img)
    print(json.dumps(data, indent=4))
    out = guessers[g].guess(data['question'], [data['a_1'], data['a_2'], data['a_3']])
    print(out)
    print(best(out))

if __name__ == '__main__':
    main()
