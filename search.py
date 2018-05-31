#!/usr/bin/python3

import requests
import os
import sys
import json

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

class Guesser:
    def guess(self, question, options):
        raise NotImplementedError()

class Searcher:
    def search(self, query):
        raise NotImplementedError()

class Aggregator(Guesser):
    """
    Combine the result of multiple guessers
    """
    def __init__(self, guessers):
        self.guessers = guessers

    def guess(self, question, options):
        #TODO: parallelize
        pass

    def get_final_result(self, question, results):
        if question.contains('NOT'):
            return worst(results)
        else:
            return best(results)


class BingSearcher(Searcher):

    url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'

    def __init__(self, token):
        self.headers = {'Ocp-Apim-Subscription-Key': token}

    def search(self, query):
        params  = {"q": query, "textDecorations":True, "textFormat":"HTML"}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

class ResultsGuesser(Guesser):
    """
    Search web for:
        question + "option"
    Return the number of results for each search
    """

    def __init__(self, searcher):
        self.searcher = searcher

    def guess(self, question, options):
        #TODO parallelize
#        options = [options[0]]
        results = {}
        for i,opt in enumerate(options):

            answer = self.searcher.search(question+ ' ' + _q(opt))
            try:
                results[opt] = answer['webPages']['totalEstimatedMatches']
            except:
                print(json.dumps(answer, indent=4))
                print('--------------')

        return results

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
    return '"' + string + '"'

def main():
    try:
        data = json.load(sys.stdin)
    except:
        raise ValueError("Non ho ottenuto il json di input correttamente")

    try:
        s = BingSearcher(os.environ['BING_API_KEY'])
    except:
        raise ValueError("Non è stata impostata la key di bing correttamente")

    g = ResultsGuesser(s)

    print(json.dumps(data, indent=4))
    print("\n")

    guess = g.guess(data['question'], [data['a_1'], data['a_2'], data['a_3']])
    print(guess)
    guess = best(guess)
    print(guess)
    if guess == data['a_1']:
        print('0')
    if guess == data['a_2']:
        print('1')
    if guess == data['a_3']:
        print('2')

    return

if __name__ == '__main__':
    main()
