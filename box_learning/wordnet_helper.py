from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import math
import numpy as np
import sys

class wordnet_helper:
    # Parameters to the algorithm. Currently set to values that was reported
    # in the paper to produce "best" results.
    ALPHA = 0.2
    BETA = 0.45
    N = 0

    def get_best_synset_pair(self, word_1, word_2):
        """ 
        Choose the pair with highest path similarity among all pairs. 
        Mimics pattern-seeking behavior of humans.
        """
        max_sim = -1.0
        synsets_1 = wn.synsets(word_1)
        synsets_2 = wn.synsets(word_2)
        if len(synsets_1) == 0 or len(synsets_2) == 0:
            return None, None
        else:
            max_sim = -1.0
            best_pair = None, None
            for synset_1 in synsets_1:
                for synset_2 in synsets_2:
                   sim = wn.path_similarity(synset_1, synset_2)
                   if sim > max_sim:
                       max_sim = sim
                       best_pair = synset_1, synset_2
            return best_pair

    def get_best_synset_pair_similarity(self, word_1, word_2):
        """ 
        Choose the pair with highest path similarity among all pairs. 
        Mimics pattern-seeking behavior of humans.
        """
        max_sim = -1.0
        synsets_1 = wn.synsets(word_1)
        synsets_2 = wn.synsets(word_2)
        if len(synsets_1) == 0 or len(synsets_2) == 0:
            return None, None
        else:
            max_sim = -1.0
            best_pair = None, None
            for synset_1 in synsets_1:
                for synset_2 in synsets_2:
                   sim = wn.path_similarity(synset_1, synset_2)
                   if sim > max_sim:
                       max_sim = sim
                       best_pair = synset_1, synset_2
            return wn.path_similarity(best_pair[0], best_pair[1])

    def length_dist(self, synset_1, synset_2):
        """
        Return a measure of the length of the shortest path in the semantic 
        ontology (Wordnet in our case as well as the paper's) between two 
        synsets.
        """
        l_dist = sys.maxint
        if synset_1 is None or synset_2 is None: 
            return 0.0
        if synset_1 == synset_2:
            # if synset_1 and synset_2 are the same synset return 0
            l_dist = 0.0
        else:
            wset_1 = set([str(x.name()) for x in synset_1.lemmas()])        
            wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
            if len(wset_1.intersection(wset_2)) > 0:
                # if synset_1 != synset_2 but there is word overlap, return 1.0
                l_dist = 1.0
            else:
                # just compute the shortest path between the two
                l_dist = synset_1.shortest_path_distance(synset_2)
                if l_dist is None:
                    l_dist = 0.0
        # normalize path length to the range [0,1]
        return math.exp(-self.ALPHA * l_dist)

    def hierarchy_dist(self, synset_1, synset_2):
        """
        Return a measure of depth in the ontology to model the fact that 
        nodes closer to the root are broader and have less semantic similarity
        than nodes further away from the root.
        """
        h_dist = sys.maxint
        if synset_1 is None or synset_2 is None: 
            return h_dist
        if synset_1 == synset_2:
            # return the depth of one of synset_1 or synset_2
            h_dist = max([x[1] for x in synset_1.hypernym_distances()])
        else:
            # find the max depth of least common subsumer
            hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
            hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
            lcs_candidates = set(hypernyms_1.keys()).intersection(
                set(hypernyms_2.keys()))
            if len(lcs_candidates) > 0:
                lcs_dists = []
                for lcs_candidate in lcs_candidates:
                    lcs_d1 = 0
                    if hypernyms_1.has_key(lcs_candidate):
                        lcs_d1 = hypernyms_1[lcs_candidate]
                    lcs_d2 = 0
                    if hypernyms_2.has_key(lcs_candidate):
                        lcs_d2 = hypernyms_2[lcs_candidate]
                    lcs_dists.append(max([lcs_d1, lcs_d2]))
                h_dist = max(lcs_dists)
            else:
                h_dist = 0
        return ((math.exp(self.BETA * h_dist) - math.exp(-self.BETA * h_dist)) / 
            (math.exp(self.BETA * h_dist) + math.exp(-self.BETA * h_dist)))
        
    def word_similarity(self, word_1, word_2):
        synset_pair = self.get_best_synset_pair(word_1, word_2)
        return (self.length_dist(synset_pair[0], synset_pair[1]) * 
            self.hierarchy_dist(synset_pair[0], synset_pair[1]))

