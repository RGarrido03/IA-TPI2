#encoding: utf8

# YOUR NAME:
# YOUR NUMBER:

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        # IMPLEMENT HERE
        pass
        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def query(self,entity,assoc=None):
        # IMPLEMENT HERE
        pass
        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here


    def update_assoc_stats(self,assoc,user=None):
        # IMPLEMENT HERE
        pass


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def search_all(self,domains=None,xpto=None):
        # If needed, you can use argument 'xpto'
        # to pass information to the function
        #
        # IMPLEMENTAR AQUI
        pass

