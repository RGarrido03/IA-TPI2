# encoding: utf8
from typing import Callable, Literal

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
            tuple[str, str | None], tuple[dict[str, float], dict[str, float]]
        ] = {}

    def query_local(
        self, user: str = None, e1: str = None, rel: str = None, e2: str = None
    ) -> list[Declaration]:
        def get_decl(
            user_iter: str, e1_iter: str, rel_iter: str, e2_iter: str | set
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

    def query(self, entity: str, rel: str = None) -> list:
        decl = self.query_local(e1=entity, rel=rel) + self.query_local(
            e2=entity, rel=rel
        )
        decl_name = [d.relation.name for d in decl]

        for pd in self.query_local(e1=entity, rel="member") + self.query_local(
            e1=entity, rel="subtype"
        ):
            decl += [
                p
                for p in self.query(pd.relation.entity2, rel)
                if p.relation.name not in decl_name
            ]

        return decl

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

        def get_members_with_hierarchy(num_entity: Literal[1, 2]) -> dict[str, float]:
            entities = (
                {d.relation.entity1 for d in assoc_decl}
                if num_entity == 1
                else {d.relation.entity2 for d in assoc_decl}
            )
            e_member_decl = [
                self.query_local(user=user, e1=e, rel="member") for e in entities
            ]
            k = n - sum(
                [
                    len(
                        self.query_local(
                            user=d.user, e1=d.relation.entity1, rel="member"
                        )
                    )
                    for d in assoc_decl
                ]
            )
            divisor = n - k + (k ** (1 / 2))
            e_is_member_of: set[str] = {
                d.relation.entity2 for ld in e_member_decl for d in ld
            }

            ret: dict = {}
            for c in e_is_member_of:
                for p in predecessor_path(c):
                    if p not in ret:
                        ret[p] = 0
                    ret[p] = ret[p] + get_matches(c, num_entity)

            return {key: value / divisor for key, value in ret.items()}

        def get_matches(entity: str, num_entity: Literal[1, 2]) -> float:
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
            return matching

        self.assoc_stats[(assoc, user)] = (
            get_members_with_hierarchy(1),
            get_members_with_hierarchy(2),
        )


class MyCS(ConstraintSearch):
    def __init__(
        self,
        domains: dict[str, list[int]],
        constraints: dict[tuple[str, str], Callable[[int, int, int, int], bool]],
    ):
        ConstraintSearch.__init__(self, domains, constraints)

    def search_all(self, domains: dict[str, list[int]] = None) -> list[dict] | None:
        if domains is None:
            domains: dict[str, list[int]] = self.domains

        if any([lv == [] for lv in domains.values()]):
            return None

        if all([len(lv) == 1 for lv in list(domains.values())]):
            return [{v: lv[0] for (v, lv) in domains.items()}]

        for var in domains.keys():
            if len(domains[var]) > 1:
                solutions: list[dict] = []
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]

                    newdomains = self.propagate_constraints(newdomains, var)
                    solution = self.search_all(newdomains)
                    if solution is not None and solution not in solutions:
                        solutions += solution
                return solutions
        return None

    def propagate_constraints(
        self, domains: dict[str, list[int]], var: str
    ) -> dict[str, list[int]]:
        def get_constraints(var_const: str) -> list:
            return [(w1, w2) for (w1, w2) in self.constraints if w2 == var_const]

        edges = get_constraints(var)
        while edges:
            (v1, v2) = edges.pop()
            values = [
                x1
                for x1 in domains[v1]
                if any(self.constraints[v1, v2](v1, x1, v2, x2) for x2 in domains[v2])
            ]
            if len(values) < len(domains[v1]):
                domains[v1] = values
                edges += get_constraints(v1)
        return domains
