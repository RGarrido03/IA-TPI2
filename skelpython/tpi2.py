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
        self.query_result: list[Declaration] = []
        self.assoc_stats: dict[
            tuple[str, str], tuple[dict[str, float], dict[str, float]]
        ] = {}

    def query_local(
        self, user: str = None, e1: str = None, rel: str = None, e2: str = None
    ) -> list[Declaration]:
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

    def query(self, entity: str, rel: str = None) -> list[Declaration]:
        decl_local = self.query_local(e1=entity, rel=rel) + self.query_local(
            e2=entity, rel=rel
        )

        pred_direct = self.query_local(e1=entity, rel="member") + self.query_local(
            e1=entity, rel="subtype"
        )

        decl = decl_local
        for dp in pred_direct:
            decl += self.query(dp.relation.entity2, rel)

        self.query_result = decl
        return self.query_result

    def update_assoc_stats(self, assoc: str, user: str = None) -> None:
        # TODO: Check if user is None
        # TODO: Get probability

        assoc_decl = self.query_local(user=user, rel=assoc)

        def predecessor_path(c: str) -> list:
            decl = self.query_local(user=user, e1=c, rel="subtype")
            if len(decl) == 0:
                return [c]
            for d in decl:
                if res := predecessor_path(d.relation.entity2):
                    return res + [c]

        # In the next variables, each one is a list of two elements.
        # The first element is related to e1, the second one is related to e2.
        entities: list[set[str]] = [
            {d.relation.entity1 for d in assoc_decl},
            {d.relation.entity2 for d in assoc_decl},
        ]
        entities_member_decl: list[list[list[Declaration]]] = [
            [self.query_local(user=user, e1=e, rel="member") for e in entities[0]],
            [self.query_local(user=user, e1=e, rel="member") for e in entities[1]],
        ]
        entities_member_of: list[set[str]] = [
            {d.relation.entity2 for ld in entities_member_decl[0] for d in ld},
            {d.relation.entity2 for ld in entities_member_decl[1] for d in ld},
        ]
        entities_member_of_with_hierarchy: list[set[str]] = [
            {e for c in entities_member_of[0] for e in predecessor_path(c)},
            {e for c in entities_member_of[1] for e in predecessor_path(c)},
        ]

        d1 = {e: 1.0 for e in entities_member_of_with_hierarchy[0]}
        d2 = {e: 1.0 for e in entities_member_of_with_hierarchy[1]}

        self.assoc_stats[(assoc, user)] = (d1, d2)


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
