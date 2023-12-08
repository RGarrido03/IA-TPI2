# encoding: utf8
from typing import Type

# YOUR NAME: Rúben Tavares Garrido
# YOUR NUMBER: 107927

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *


class MySN(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        self.query_result = []

    def query_local(self, user=None, e1=None, rel=None, e2=None):
        def get_decl(
            user_iter: str, e1_iter: str, rel_iter: str, e2_iter: Union[str, set]
        ) -> list[Declaration]:
            if rel_iter == "member":
                return [Declaration(user_iter, Member(e1_iter, e2_iter))]

            if rel_iter == "subtype":
                return [Declaration(user_iter, Subtype(e1_iter, e2_iter))]

            if isinstance(e2_iter, str):
                return [Declaration(user_iter, AssocOne(e1_iter, rel_iter, e2_iter))]

            return [
                Declaration(user_iter, Association(e1_iter, rel_iter, e2_iter_each))
                for e2_iter_each in e2_iter
            ]

        self.query_result = [
            d
            for user_iter, v in self.declarations.items()
            for (e1_iter, rel_iter), e2_iter in v.items()
            for d in get_decl(user_iter, e1_iter, rel_iter, e2_iter)
            if (user is None or user_iter == user)
            and (e1 is None or e1 == e1_iter)
            and (rel is None or rel == rel_iter)
            and (
                e2 is None
                or (e2 in e2_iter if isinstance(e2_iter, set) else e2 == e2_iter)
            )
        ]
        return self.query_result

    def query(self, entity, assoc=None):
        # IMPLEMENT HERE
        pass
        return self.query_result  # Your code must leave the output in
        # self.query_result, which is returned here

    def update_assoc_stats(self, assoc, user=None):
        # IMPLEMENT HERE
        pass


class MyCS(ConstraintSearch):
    def __init__(self, domains, constraints):
        ConstraintSearch.__init__(self, domains, constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def search_all(self, domains=None, xpto=None):
        # If needed, you can use argument 'xpto'
        # to pass information to the function
        #
        # IMPLEMENTAR AQUI
        pass
