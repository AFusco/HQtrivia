#!/usr/bin/python3

import requests
import os
import sys
import json

class Guesser:
    def guess(self, question, options):
        raise NotImplementedError()

class Searcher:
    def search(self, query):
        raise NotImplementedError()


class BingSearcher:

    url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    headers = {'Ocp-Apim-Subscription-Key': ''}

    def __init__(self, token):
        self.headers = {'Ocp-Apim-Subscription-Key': token}

    def search(self, query):
        params  = {"q": query, "textDecorations":True, "textFormat":"HTML"}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

class ResultsGuesser(Guesser):
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

def best(results):
    return max(results, key=(lambda key: results[key]))

def _q(string):
    return '"' + string + '"'

def main():
    data = json.load(sys.stdin)
    s = BingSearcher(os.environ['BING_API_KEY'])
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
