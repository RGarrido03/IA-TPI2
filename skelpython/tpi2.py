# encoding: utf8
import typing
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
        assoc_decl = self.query_local(user=user, rel=assoc)
        n = len(assoc_decl)

        def predecessor_path(c: str) -> list:
            decl = self.query_local(user=user, e1=c, rel="subtype")
            if len(decl) == 0:
                return [c]
            for d in decl:
                if res := predecessor_path(d.relation.entity2):
                    return res + [c]

        def get_members_with_hierarchy(num_entity: typing.Literal[1, 2]) -> set:
            entities = (
                {d.relation.entity1 for d in assoc_decl}
                if num_entity == 1
                else {d.relation.entity2 for d in assoc_decl}
            )
            e_member_decl = [
                self.query_local(user=user, e1=e, rel="member") for e in entities
            ]
            e_is_member_of: set[str] = {
                d.relation.entity2 for ld in e_member_decl for d in ld
            }
            return {e for c in e_is_member_of for e in predecessor_path(c)}

        def get_prob(entity: str, num_entity: typing.Literal[1, 2]) -> float:
            matching = 0
            for decl in assoc_decl:
                for decl1 in self.query_local(
                    user=user,
                    e1=(
                        decl.relation.entity1
                        if num_entity == 1
                        else decl.relation.entity2
                    ),
                ):
                    if entity == decl1.relation.entity2:
                        matching += 1
            return matching / n

        d1 = {e: get_prob(e, 1) for e in get_members_with_hierarchy(1)}
        d2 = {e: get_prob(e, 2) for e in get_members_with_hierarchy(2)}

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
