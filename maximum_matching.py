#!/usr/bin/env python


from collections import defaultdict, deque
from time import time
import pprint


class Forest:
     def __init__(self):
          self.rootnodes = set()
          self.allnodes = set()
          self.parentdict = {}
          self.rootdict = {}
          

     def add_root(self, root):
          self.rootnodes.add(root)
          self.allnodes.add(root)
          self.parentdict[root] = None
          self.rootdict[root] = root


     def add_edge(self, beg_node, end_node):
          #beg_node in forest already
          #end_node not in forest

          self.allnodes.add(end_node)
          self.parentdict[end_node] = beg_node
          self.rootdict[end_node] = self.rootdict[beg_node]

     def path_to_root(self, node):
          path = []
          root = self.rootdict[node]
          current_node = node
          while(current_node != root):
               parent = self.parentdict[current_node]
               path.append((current_node,parent))
               current_node = parent
          return path
               

     def bloom(self, node_1, node_2):
          root = self.rootdict[node_1] #same root for node_2 as well
          blossom_vertices = set()
          stem = []
          has_stem = False
          path_1 = self.path_to_root(node_1)
          path_2 = self.path_to_root(node_2)
          least_common_ancestor = root
          blossom_cycle = []
     
          while(path_1 and path_2):
               (v_1,w_1) = path_1[-1]
               (v_2,w_2) = path_2[-1]
               if v_1 == v_2 and w_1 == w_2:
                    stem.append((w_1,v_1))
                    path_1.pop()
                    path_2.pop()
                    least_common_ancestor = v_1
               elif v_1 != v_2:
                    break
  
          blossom_cycle.extend([(y,x) for (x,y) in reversed(path_1)])
          blossom_cycle.append((node_1, node_2))
          blossom_cycle.extend(path_2)
          for x,y in blossom_cycle:
               blossom_vertices.add(x)
          if stem:
               has_stem = True
          return (stem, blossom_vertices, blossom_cycle, least_common_ancestor, has_stem)
     

class Matching:
    #match_dict = {v: match[v] for all v in vertex_list}
    #Note: If no match, match[v] is set to  None
    def __init__(self, match_dict):
         self.matchededges = set()
         self.matchedvertices = set()
         cardinality = 0
         for v in match_dict:
             if match_dict[v]!= None:
                 self.matchedvertices.add(v)
                 cardinality += 1
                 self.matchededges.add((v,match_dict[v]))

    
         self.cardinality = (cardinality//2)
         self.matchdict = match_dict
         
         
         
    def xor_even_path(self, even_path):
         
         #even_path = [(v_0,v_1), (v_1,v_2),...,(v_{2n-1}, v_2n)]
         if len(even_path) == 0:
             return
         
         not_in_match = True
         for edge in even_path:
             if not_in_match:
                 self.matchdict[edge[0]] = edge[1]
                 self.matchdict[edge[1]] = edge[0]
                 self.matchededges.add((edge[0],edge[1]))
                 self.matchededges.add((edge[1], edge[0]))
                 not_in_match = False
             else:
                 self.matchededges.discard((edge[0],edge[1]))
                 self.matchededges.discard((edge[1],edge[0]))
                 not_in_match = True

        
         self.matchedvertices.add(even_path[0][0])
         self.matchedvertices.discard(even_path[-1][1])
         self.matchdict[even_path[-1][1]] = None

    def xor_aug_path(self, aug_path):
         #aug_path = [(v_0,v_1), (v_1,v_2),...,(v_{n-1}, v_n)]
         if len(aug_path) == 0:
             return
         
         not_in_match = True
         for edge in aug_path:
             if not_in_match:
                 self.matchdict[edge[0]] = edge[1]
                 self.matchdict[edge[1]] = edge[0]
                 self.matchededges.add((edge[0],edge[1]))
                 self.matchededges.add((edge[1], edge[0]))
                 not_in_match = False
             else:
                 self.matchededges.discard((edge[0],edge[1]))
                 self.matchededges.discard((edge[1],edge[0]))
                 not_in_match = True

        
         self.matchedvertices.add(aug_path[0][0])
         self.matchedvertices.add(aug_path[-1][1])
         self.cardinality += 1

def create_quotient(vertices, graph_adj_dict, current_matching, blossom_vertices, least_common_ancestor):
     quotient_vertices = vertices - blossom_vertices
     quotient_vertices.add(least_common_ancestor)
     quotient_graph_adj_dict = defaultdict(list)
     section = {}
     for v in graph_adj_dict:
          if v not in blossom_vertices:
               blossom_vertex_detected = False
               for w in graph_adj_dict[v]:
                    if w not in blossom_vertices:
                         quotient_graph_adj_dict[v].append(w)
                    else:
                         if blossom_vertex_detected == False:
                              quotient_graph_adj_dict[v].append(least_common_ancestor)
                              quotient_graph_adj_dict[least_common_ancestor].append(v)
                              section[(v,least_common_ancestor)] = (v,w)
                              blossom_vertex_detected = True

     quotient_match_dict = {}
     for v in quotient_vertices:
          quotient_match_dict[v] = current_matching.matchdict[v]
     quotient_matching = Matching(quotient_match_dict)

     return quotient_vertices, quotient_graph_adj_dict, quotient_matching, section

def find_even_path(node, blossom_cycle):
     #blossom_cycle = [(lca, v_1), (v_1, v_2), ..... (v_2n, lca)]
     #              = [unmatched, matched, unmatched,.......matched, unmatched]
     count = 0
     path = []
     while(blossom_cycle[count][0]!= node):
          path.append((blossom_cycle[count][1],blossom_cycle[count][0]))
          count +=1
     if (count % 2) == 0:
          return list(reversed(path))
     else:
          return blossom_cycle[count:]
          
  
def find_aug_path(graph_adjacency_dict, current_matching, vertices):
        #label vertices with 0 (even), 1 (odd) or None
        vertex_label = defaultdict(lambda: None)
        
        #label matched edges as explored
        is_explored_edge = defaultdict(lambda: False)
        for v in vertices:
            for w in vertices:
                if (v,w) in current_matching.matchededges:
                    is_explored_edge[(v,w)] = True

        #create a forest with trees (just roots) of unmatched vertices
        #create a queue of to_be_explored vertices
        #If v in the  queue, v will be even labelled
        to_be_explored_nodes = deque()
        F = Forest()
        for u in vertices  - current_matching.matchedvertices:
            vertex_label[u] = 0
            F.add_root(u)
            to_be_explored_nodes.append(u)
       

        while to_be_explored_nodes:
             v = to_be_explored_nodes.popleft()
             for w in graph_adjacency_dict[v]:
                  if is_explored_edge[(v,w)] is False:
                       if w not in F.allnodes:
                            vertex_label[w] = 1
                            F.add_edge(v, w)
                            x = current_matching.matchdict[w]
                            vertex_label[x] = 0
                            F.add_edge(w, x)
                            to_be_explored_nodes.append(x)
                            is_explored_edge[(w,x)] = True
                            is_explored_edge[(x,w)] = True

                       else:
                            if (vertex_label[w] % 2) == 0:
                                 if F.rootdict[w] != F.rootdict[v]:
                                      my_aug_path = []
                                      for edge in reversed(F.path_to_root(v)):
                                           my_aug_path.append((edge[1], edge[0]))
                                      my_aug_path.append((v,w))
                                      my_aug_path.extend(F.path_to_root(w))
                                      return my_aug_path
                                 else:
                                      #BLOSSOMS!!!!!!!
                                      (stem, blossom_vertices, blossom_cycle, least_common_ancestor, has_stem) = F.bloom(v,w)
                                      if has_stem:
                                           #toggle_stem
                                           current_matching.xor_even_path(stem)                                      
                                      quotient_vertices, quotient_graph_adjacency_dict, quotient_matching, section = (
                                           create_quotient(
                                                vertices, graph_adjacency_dict, current_matching,
                                                blossom_vertices, least_common_ancestor))
                                      
                                      quotient_aug_path = find_aug_path(quotient_graph_adjacency_dict,
                                                                        quotient_matching, quotient_vertices)
                                      
                                      if not quotient_aug_path:
                                           return quotient_aug_path
                                      elif (quotient_aug_path[0][0] != least_common_ancestor and
                                           quotient_aug_path[-1][1] != least_common_ancestor):
                                           return quotient_aug_path
                                      else:
                                           if quotient_aug_path[0][0] == least_common_ancestor:
                                                quotient_aug_path = list(reversed(quotient_aug_path))
                                                for pos, (x,y) in  enumerate(quotient_aug_path):
                                                     quotient_aug_path[pos] = (y,x)
                                                     
                                           #So quotient_aug_path[-1][1] = least_common_ancestor:
                                           v = quotient_aug_path[-1][0]
                                           quotient_aug_path.pop()
                                           attaching_point_to_bloom = section[(v,least_common_ancestor)][1]
                                           quotient_aug_path.append((v,attaching_point_to_bloom))
                                           quotient_aug_path.extend(find_even_path(attaching_point_to_bloom, blossom_cycle))
                                           return quotient_aug_path


                  is_explored_edge[(v,w)] = True
                  is_explored_edge[(w,v)] = True



     
def find_max_matching(graph_adjacency_dict, current_matching, vertices):
        my_path = find_aug_path(graph_adjacency_dict, current_matching, vertices)
        if not my_path:
            return current_matching.matchdict, current_matching.cardinality
        else:
            current_matching.xor_aug_path(my_path)
            return find_max_matching(graph_adjacency_dict, current_matching, vertices)
     
def find_a_maximal_matching(graph_adjacency_dict,vertices):
     """returns a maximal matching given vertices(set) and graph_adjacency_dict"""
     
     my_match_dict = {}
     outdegree = {}
     for v in vertices:
          my_match_dict[v] = None
          outdegree[v] = len(graph_adjacency_dict[v])
          
     for v in sorted(outdegree, key=outdegree.get):
       if my_match_dict[v] is None:
               candidates = [w for w in graph_adjacency_dict[v] if my_match_dict[w] == None]
               if candidates:
                    w = min(candidates, key = lambda x: outdegree[x])
                    my_match_dict[v] = w
                    my_match_dict[w] = v
 
     return  Matching(my_match_dict)


def create_graph_adjacency_dict(adjacency_matrix, list_of_vertices):
     """returns the graph adjacency dictionary given the adjacency matrix, list_of_vertices"""
     assert(len(adjacency_matrix) == len(list_of_vertices)), "no_of_vertices not compatible with adjacency matrix row dimension"
     n = len(list_of_vertices)
     graph_adjacency_dict = defaultdict(list)
     for i in range(n):
          for j in range(n):
              assert(adjacency_matrix[i][j] == adjacency_matrix[j][i]), "adjacency matrix is not symmetric"
              if adjacency_matrix[i][j] == 1:
                   graph_adjacency_dict[list_of_vertices[i]].append(list_of_vertices[j])
              else:
                   graph_adjacency_dict[list_of_vertices[i]].extend([])
         
     return graph_adjacency_dict



               
     
     
def run_blossoms_algorithm(adjacency_matrix, list_of_vertices = None):
     start_time = time()
     
     no_of_vertices = len(adjacency_matrix)
     if list_of_vertices is None:
          list_of_vertices = list(range(no_of_vertices))
          
     #ensuring matrix dimensions are compatible with list of_vertices
     assert(no_of_vertices == len(list_of_vertices)), "no_of_vertices not compatible with adjacency matrix row dimension"
     assert(all([no_of_vertices == len(adjacency_matrix[row]) for row in adjacency_matrix])), "no_of_vertices not compatible with adjacency matrix col dimension"
     
          
     #Create graph_adjacency_dict
     graph_adjacency_dict =  create_graph_adjacency_dict(adjacency_matrix, list_of_vertices)
     vertices = set(list_of_vertices)

     #Find a maximal matching
     current_matching = find_a_maximal_matching(graph_adjacency_dict,vertices)

     #Find maximum matching
     final_match_dict, no_of_matched_edges = find_max_matching(graph_adjacency_dict, current_matching, vertices)

     #Print results and statistics
     print("Maximum Matching", end ='')
     pprint.pprint(final_match_dict)

     print(f"Number of matched edges : {no_of_matched_edges}")

     print(f"Time taken : {time()-start_time}")
             
            

        

                    
        
        
        
        
        



        
    
    
            
            
            
        
        
  
        
        
        


                        




     


