#!/usr/bin/env python


from collections import defaultdict, deque
from time import time
import pprint
import unittest
from  maximum_matching import *



# class Matching:
#     #match_dict = {v: match[v] for all v in vertex_list}
#     #Note: If no match, match[v] is set to  None
#     def __init__(self, match_dict):
#          self.matchededges = set()
#          self.matchedvertices = set()
#          cardinality = 0
#          for v in match_dict:
#              if match_dict[v]!= None:
#                  self.matchedvertices.add(v)
#                  cardinality += 1
#                  self.matchededges.add((v,match_dict[v]))

    
#          self.cardinality = (cardinality//2)
#          self.matchdict = match_dict
         
         
         
#     def xor_even_path(self, even_path):
#          #even_path = [(v_0,v_1), (v_1,v_2),...,(v_{2n-1}, v_2n)]
         

#     def xor_aug_path(self, aug_path):
#          #aug_path = [(v_0,v_1), (v_1,v_2),...,(v_{n-1}, v_n)]
     


class TestForestMethods(unittest.TestCase):
     def setUp(self):
          self.forest = Forest()
          f = self.forest
          f.add_root(1)
          f.add_edge(1,5)
          f.add_edge(1,4)
          f.add_edge(1,2)
          f.add_edge(1,3)
          f.add_root(7)
          f.add_edge(7,6)
          f.add_edge(6,8)
     

     def tearDown(self):
         pass

     def test_forest_addition(self):
          #checking initial forest set up
          self.assertEqual(self.forest.rootnodes, {1,7})
          self.assertEqual(self.forest.allnodes, {5,4,2,1,7,6,8,3})
          self.assertEqual(self.forest.parentdict, {1: None, 4:1, 2:1, 5:1, 7:None, 6:7, 8:6, 3:1})
          self.assertEqual(self.forest.rootdict, {5:1, 4:1, 2:1, 1:1, 7:7, 3:1, 6:7, 8:7})

          #checking adding root nodes
          self.forest.add_root(9)
          
          self.assertEqual(self.forest.rootnodes, {1,7,9})
          self.assertEqual(self.forest.allnodes, {5,4,2,1,7,6,8,3,9})
          self.assertEqual(self.forest.parentdict, {1: None, 4:1, 2:1, 5:1, 7:None, 6:7, 8:6, 3:1, 9:None})
          self.assertEqual(self.forest.rootdict, {5:1, 4:1, 2:1, 1:1, 7:7, 3:1, 6:7, 8:7, 9:9})

          #checking adding edges
          self.forest.add_edge(9,10)
          self.forest.add_edge(9,11)
          self.forest.add_edge(5,12)

          self.assertEqual(self.forest.rootnodes, {1,7,9})
          self.assertEqual(self.forest.allnodes, {5,4,2,1,7,6,8,3,9,10,11,12})
          self.assertEqual(self.forest.parentdict,
                           {1: None, 4:1, 2:1, 5:1, 7:None,6:7, 8:6, 3:1, 9:None, 12:5, 10:9, 11:9})
          self.assertEqual(self.forest.rootdict,
                           {5:1, 4:1, 2:1, 1:1, 7:7, 3:1, 6:7, 8:7, 9:9, 10:9, 11:9, 12:1})
          

     def test_path_to_root(self):
         self.forest.add_edge(5,12)

         #checking path to roots
         self.assertEqual(self.forest.path_to_root(12), [(12,5), (5,1)])
         self.assertEqual(self.forest.path_to_root(6), [(6,7)])
         self.assertEqual(self.forest.path_to_root(7), [])

     
     def test_bloom_without_stem(self):
          #creating bloom without stem
          self.forest.add_edge(7,9)
          self.forest.add_edge(9,10)

          #checking bloom with stem
          stem, blossom_vertices, blossom_cycle, least_common_ancestor, has_stem = self.forest.bloom(8,10)
          self.assertEqual(stem, [])
          self.assertEqual(blossom_vertices, {6,7,8,9,10})
          self.assertEqual(least_common_ancestor, 7)
          self.assertEqual(has_stem, False)
          self.assertEqual(blossom_cycle, [(7, 6), (6, 8), (8, 10), (10, 9), (9, 7)])
          
     
     def test_bloom_with_stem(self):
          #creating bloom with stem
          self.forest.add_edge(3,12)
          self.forest.add_edge(12,0)
          self.forest.add_edge(12,11)
          self.forest.add_edge(0,9)
          self.forest.add_edge(11,10)
          
          #checking bloom with stem
          stem, blossom_vertices, blossom_cycle, least_common_ancestor, has_stem = self.forest.bloom(10,9)
          self.assertEqual(stem, [(1,3),(3,12)])
          self.assertEqual(blossom_vertices, {12,0,9,10,11})
          self.assertEqual(least_common_ancestor, 12)
          self.assertEqual(has_stem, True)
          self.assertEqual(blossom_cycle, [(12,11), (11, 10), (10,9), (9, 0), (0, 12)])
          

class TestMatchingMethods(unittest.TestCase):
     def setUp(self):
         initialmatching = {0:9 , 1:None , 2:4, 3: 12, 4:2 , 5:None ,
                            6:None , 7:None, 8:None , 9:0 ,10:11 ,11:10 ,12:3}
         self.matching = Matching(initialmatching)


     def tearDown(self):
         pass


     def test_matching_init(self):
         self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 12), (10, 11), (0, 9), (4, 2), (2, 4), (12, 3)})
         self.assertEqual(self.matching.matchedvertices, {0, 2, 3, 4, 9, 10, 11, 12})
         self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: None, 2: 4, 3: 12, 4: 2, 5: None, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12: 3})         
         self.assertEqual(self.matching.cardinality, 4)
         


     def test_xor_even_path(self):
          self.matching.xor_even_path([(1,3),(3,12)])

          self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 1), (10, 11), (0, 9), (4, 2), (2, 4), (1, 3)})
          self.assertEqual(self.matching.matchedvertices, {0,1, 2, 3, 4, 9, 10, 11})
          self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: 3, 2: 4, 3: 1, 4: 2, 5: None, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12: None})         
          self.assertEqual(self.matching.cardinality, 4)
           

     def test_xor_aug_path(self):
         self.matching.xor_aug_path([(1,2),(2,4),(4,5)])

         self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 12), (10, 11), (0, 9), (1, 2), (2, 1), (12, 3), (4,5), (5,4)})
         self.assertEqual(self.matching.matchedvertices, {0,1, 2, 3, 4, 5, 9, 10, 11,12})
         self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: 2, 2: 1, 3: 12, 4: 5, 5: 4, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12:3})         
         self.assertEqual(self.matching.cardinality, 5)
          
     
          
#TODO
class TestMaxMatchingComponentFunctions(unittest.TestCase):
     def setUp(self):
         pass


     def tearDown(self):
         pass


    
     def test_create_graph_adjacency_dict(self):
     #(adjacency_matrix, list_of_vertices):
          pass

         
     def test_create_quotient(self):
     #(vertices, graph_adj_dict, current_matching, blossom_vertices, least_common_ancestor):
          pass

     def test_find_even_path(self):
     #(node, blossom_cycle)
          pass

     def test_find_aug_path(self):
     #(graph_adjacency_dict, current_matching, vertices):
          pass

     def test_find_max_matching(self):
     #(graph_adjacency_dict, current_matching, vertices):
          pass

     def test_find_a_maximal_matching(self):
     #(graph_adjacency_dict,vertices):
          pass


     def test_run_blossoms_algorithm(self):
     #(adjacency_matrix, list_of_vertices = None):
          pass

if __name__ == "__main__":
     unittest.main()
     
