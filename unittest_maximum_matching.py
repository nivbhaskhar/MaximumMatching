#!/usr/bin/env python


from collections import defaultdict, deque
from time import time
import pprint
import unittest
from  maximum_matching import *


class TestForestMethods(unittest.TestCase):
     """
     This class tests the methods of the class Forest defined in maximum_matching.py
     In particular, we test creating root nodes, adding edges to the forest, 
     finding the unique path from a given node to the root of its tree. 
     We also test extracting blooms (stem + blossom) given two appropriate nodes.
     """
      
     def setUp(self):
          """ sets up the forest"""
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
          """checks forest creation and modification by adding extra nodes and edges"""
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
         """checks path to root node"""
         
         self.forest.add_edge(5,12)
         #checking path to roots
         self.assertEqual(self.forest.path_to_root(12), [(12,5), (5,1)])
         self.assertEqual(self.forest.path_to_root(6), [(6,7)])
         self.assertEqual(self.forest.path_to_root(7), [])

     
     def test_bloom_without_stem(self):
          """checks extraction of blooms without stems"""
          
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
          """checks extraction of blooms with stems"""
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
     """
     This class tests the methods of the class Matching defined in maximum_matching.py
     """
     def setUp(self):
         """ sets up the matching"""
         initialmatching = {0:9 , 1:None , 2:4, 3: 12, 4:2 , 5:None ,
                            6:None , 7:None, 8:None , 9:0 ,10:11 ,11:10 ,12:3}
         self.matching = Matching(initialmatching)


     def tearDown(self):
         pass


     def test_matching_init(self):
         """checks creation of matching"""
         
         #checking if Matching object is set up correctly 
         self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 12), (10, 11), (0, 9), (4, 2), (2, 4), (12, 3)})
         self.assertEqual(self.matching.matchedvertices, {0, 2, 3, 4, 9, 10, 11, 12})
         self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: None, 2: 4, 3: 12, 4: 2, 5: None, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12: 3})         
         self.assertEqual(self.matching.cardinality, 4)
         


     def test_xor_even_path(self):
          """checks xor-ing of an even path from the root to the matching"""
          #xoring even path to test case
          self.matching.xor_even_path([(1,3),(3,12)])

          
          #checking xor_even_path on test case
          self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 1), (10, 11), (0, 9), (4, 2), (2, 4), (1, 3)})
          self.assertEqual(self.matching.matchedvertices, {0,1, 2, 3, 4, 9, 10, 11})
          self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: 3, 2: 4, 3: 1, 4: 2, 5: None, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12: None})         
          self.assertEqual(self.matching.cardinality, 4)
           

     def test_xor_aug_path(self):
         """checks xor-ing of an augmenting path to the matching"""
         #creating first test case
         self.matching.xor_aug_path([(1,2),(2,4),(4,5)])
         
         #checking xor_aug_path on first test case
         self.assertEqual(self.matching.matchededges,
                          {(9, 0), (11, 10), (3, 12), (10, 11), (0, 9), (1, 2), (2, 1), (12, 3), (4,5), (5,4)})
         self.assertEqual(self.matching.matchedvertices, {0,1, 2, 3, 4, 5, 9, 10, 11,12})
         self.assertEqual(self.matching.matchdict,
                          {0: 9, 1: 2, 2: 1, 3: 12, 4: 5, 5: 4, 6: None,
                           7: None, 8: None, 9: 0, 10: 11, 11: 10, 12:3})         
         self.assertEqual(self.matching.cardinality, 5)

         #creating second test case
         new_matching = Matching( {0: 9, 1: 2, 2: 1, 3: 12, 4: 5, 5: 4, 6: None,
                                   7: None, 8: None, 9: 0, 10: 11, 11: 10, 12:3, 13: None})
         new_matching.xor_aug_path([(13,5),(5,4),(4,2),(2,1),(1,8)])

         #checking xor_aug_path on second test case
         self.assertEqual(new_matching.matchededges,
                          {(1,8),(8,1),(2,4),(4,2),(5,13),(13,5),(0,9),(9,0),(11,10),(10,11),(3,12),(12,3)})
         self.assertEqual(new_matching.matchedvertices, {0,1, 2, 3, 4, 5,8, 9, 10, 11,12,13})
         self.assertEqual(new_matching.matchdict,
                          {0: 9, 1: 8, 2: 4, 3: 12, 4: 2, 5: 13, 6: None,
                           7: None, 8: 1, 9: 0, 10: 11, 11: 10, 12:3, 13: 5})
         self.assertEqual(new_matching.cardinality, 6)
         


class TestGraphCreation(unittest.TestCase):
     """ This class tests helper functions defined in maximum_matching.py 
         which create graphs/graph related data structures """
    
     def test_create_graph_adjacency_dict(self):
           """checks creation of an adjacency list (dictionary) representation from an adjacency matrix"""
           
           #checking adjacency matrix row length matches with number of vertices
           with self.assertRaises(AssertionError):
                create_graph_adjacency_dict([[0,1],[1,0]], [1,2,3])

           #checking adjacency matrix is symmetric
           adjacency_matrix = [[0,1,1,1,0],[1,0,1,1,0],[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,0]]
           with self.assertRaises(AssertionError):
                create_graph_adjacency_dict(adjacency_matrix, [1,5,7,2,3])
          
                
           #creating new adjacency matrix test case
           adjacency_matrix = [[0,1,1,1,0],[1,0,1,0,0],[1,1,0,0,0],[1,0,0,0,0],[0,0,0,0,0]]
           list_of_vertices = [1,5,7,2,3]
           graph_adjacency_dict = create_graph_adjacency_dict(adjacency_matrix, list_of_vertices)
           for v in graph_adjacency_dict:
                graph_adjacency_dict[v].sort()

           #checking new adjacency matrix test case
           self.assertEqual(graph_adjacency_dict, {1:[2,5,7] , 5: [1,7], 7: [1,5], 2:[1], 3:[]})

     

         
     def test_create_quotient(self):
          """checks quotienting of a graph modulo a blossom """
          
          vertices = set(range(12))
          graph_adj_dict = { 0:[1,2,3],
                        1:[0,2,4],
                        2:[0,1,5,8],
                        3:[0,5],
                        4:[1,6,7],
                        5:[2,3,7,8],
                        6:[4,9,10],
                        7:[4,5,10],
                        8:[2,5,11],
                        9:[6,10],
                        10:[6,7,9],
                        11:[8]}
          match_dict = {0:None, 1:4, 2:5, 3:None, 4:1, 5:2, 6:9, 7:10, 8:11, 9:6,10:7, 11:8}
          current_matching = Matching(match_dict)
          blossom_vertices = {4,6,9,10,7}
          least_common_ancestor = 4
          quotient_vertices, quotient_graph_adj_dict, quotient_matching, section = create_quotient(vertices,
                                                                                              graph_adj_dict,
                                                                                              current_matching,
                                                                                              blossom_vertices,
                                                                                              least_common_ancestor)
          for v in quotient_graph_adj_dict:
                quotient_graph_adj_dict[v].sort()
   
          self.assertEqual(quotient_vertices, {0, 1, 2, 3, 4, 5, 8, 11})
          self.assertEqual(quotient_graph_adj_dict, {0: [1, 2, 3], 1: [0, 2, 4],
                                                     4: [1, 5], 2: [0, 1, 5, 8],
                                                     3: [0, 5], 5: [2, 3, 4, 8],
                                                     8: [2, 5, 11], 11: [8]})
          self.assertEqual(quotient_matching.matchdict, {0: None, 1: 4, 2: 5,
                                                         3: None, 4: 1, 5: 2,
                                                         8: 11, 11: 8})
          for v,w in section:
               (a,b)= section[(v,w)]
               self.assertEqual(w, least_common_ancestor)
               self.assertEqual(v, a)
               self.assertFalse(a in blossom_vertices)
               self.assertTrue(b in blossom_vertices)
               self.assertTrue(b in graph_adj_dict[a])
               

     
     

class TestMaxMatchingComponentFunctions(unittest.TestCase):
     """ This class tests functions defined in maximum_matching.py 
         which find specific kind of paths inside a graph with a partial matching 
     """
     def test_find_even_path(self):
          """checks finding an even path from a node in a blossom to the tip of the blossom"""
          blossom_cycle = [(4,6), (6,9), (9,10), (10,7), (7,4)]
          self.assertEqual(find_even_path(9,blossom_cycle), [(9, 6), (6, 4)])
          self.assertEqual(find_even_path(4,blossom_cycle), [])
          self.assertEqual(find_even_path(10,blossom_cycle), [(10, 7), (7, 4)])
          self.assertEqual(find_even_path(6,blossom_cycle), [(6, 9), (9, 10), (10, 7), (7, 4)])
          self.assertEqual(find_even_path(7,blossom_cycle), [(7, 10), (10, 9), (9, 6), (6, 4)])


     def test_find_aug_path(self):
          """checks finding an augmenting path in a graph with a partial matching"""
          vertices = set(range(14))
          graph_adj_dict = { 0:[1,2,3],
                             1:[0,2,4],
                             2:[0,1,5,8],
                             3:[0,5,12],
                             4:[1,6,7],
                             5:[2,3,7,8],
                             6:[4,9,10],
                             7:[4,5,10],
                             8:[2,5,11],
                             9:[6,10,13],
                             10:[6,7,9,13],
                             11:[8],
                             12:[3],
                             13:[9,10]
                            }
          match_dict = {0:None, 1:4, 2:5, 3:12, 4:1, 5:2, 6:9, 7:10, 8:11, 9:6,10:7, 11:8, 12:3, 13: None}
          current_matching = Matching(match_dict)
          aug_path = find_aug_path(graph_adj_dict, current_matching, vertices)

          #checks if the path is an augmenting path
          self.assertNotEqual(aug_path, [])
          is_matched = False
          end_of_prev = aug_path[0][0]
          for edge in aug_path:
               self.assertEqual(end_of_prev, edge[0])
               if is_matched:
                    self.assertTrue(edge in current_matching.matchededges)
                    is_matched = False
               else:
                     self.assertTrue(edge not in current_matching.matchededges)
                     is_matched = True
               end_of_prev = edge[1]
          self.assertTrue(is_matched)
          
          
class TestMaxAndMaximalMatching(unittest.TestCase):
     """ This class tests functions defined in maximum_matching.py 
         which find a)maximal matchings in a graph b)maximum matching in a graph starting from a partial matching 
     """

     def setUp(self):
          self.vertices_list = [None, None, None, None, None]
          self.graph_adjacency_list = [None, None, None, None, None]
          self.match_dict_list = [None, None, None, None, None]

          #testcase 0
          self.vertices_list[0] = {0,1,2}
          self.graph_adjacency_list[0] = {0:[1,2], 1:[0,2], 2:[0,1]}
          self.match_dict_list[0]= {0:1 , 1:0 , 2:None } 

          #testcase 1
          self.vertices_list[1] = {0,1,2,3,4}
          self.graph_adjacency_list[1] = {0:[1,2,3], 1:[0,2], 2:[0,1], 3:[0,4], 4:[3]}
          self.match_dict_list[1]= {0:2, 1:None, 2:0, 3:None, 4:None}

          #testcase 2
          self.vertices_list[2] = {0,1,2,3,4,5,6}
          self.graph_adjacency_list[2] = {0:[1,3], 1:[0,2], 2:[1,3], 3:[0,2], 4:[4],5:[4], 6:[]}
          self.match_dict_list[2]= {0:None, 1:2, 2:1, 3: None, 4: None, 5:None, 6: None}

          #testcase 3
          self.vertices_list[3] = {0,1,2,3}
          self.graph_adjacency_list[3] = {0:[], 1:[], 2:[], 3:[]}
          self.match_dict_list[3]= {0: None, 1: None, 2:None, 3: None}

          #testcase 4
          self.vertices_list[4] = {0,1,2,3,4}
          self.graph_adjacency_list[4] = {0:[1,2,3], 1:[0,2], 2:[0,1], 3:[0,4], 4:[3]}
          self.match_dict_list[4]= {0:None, 1:None, 2:None, 3:None, 4:None}
          
   
     def tearDown(self):
         pass

     
     def test_find_a_maximal_matching(self):
          """manual check for finding a maximal matching in a graph"""
          for i in range(4):
               print(find_a_maximal_matching(self.graph_adjacency_list[i],self.vertices_list[i]).matchdict)

     
     def test_find_max_matching(self):
          """checks finding maximum matching in a graph starting with a partial matching"""
          answers = [1,2,3,0,2]          
          for i in range(5):
               max_matching_dict, max_matching_cardinality = find_max_matching(self.graph_adjacency_list[i],
                                                                               Matching(self.match_dict_list[i]),
                                                                               self.vertices_list[i])
               pprint.pprint(max_matching_dict)
               self.assertEqual(max_matching_cardinality,answers[i])

               

     

if __name__ == "__main__":
     unittest.main()
     
