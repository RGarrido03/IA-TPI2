from typing import Union


# class Relation and derived classes
# -------------------------------------
class Relation:
    def __init__(self, e1, rel, e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2

    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + str(self.entity2) + ")"

    def __repr__(self):
        return str(self)


class Association(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


class AssocOne(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


class Subtype(Relation):
    def __init__(self, sub, super):
        Relation.__init__(self, sub, "subtype", super)


class Member(Relation):
    def __init__(self, obj, type):
        Relation.__init__(self, obj, "member", type)


# classe Declaration
# ------------------------
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self, user, rel):
        self.user = user
        self.relation = rel

    def __str__(self):
        return "decl(" + str(self.user) + "," + str(self.relation) + ")"

    def __repr__(self):
        return str(self)


# classe SemanticNetwork
# -- data stored in the form of dictionaries
#    Main dictionary: { user1: data1, user2:data2, .... }
#    User data dictionary: { (e11,rel1):e12, (e21,rel2):e22, .... }
class SemanticNetwork:
    def __init__(self):
        self.declarations: dict[str, dict[tuple[str, str], str | set]] = {}

    def __str__(self):
        return str(self.declarations)

    def insert(self, decl):
        if decl.user not in self.declarations:
            # create dict entry for the new user
            self.declarations[decl.user] = {}

        # ensure upper/lower case conventions are followed
        assert not isinstance(decl.relation, Member) or is_object_name(
            decl.relation.entity1
        )
        assert not isinstance(decl.relation, Subtype) or is_type_name(
            decl.relation.entity1
        )
        assert not isinstance(decl.relation, (Member, Subtype)) or is_type_name(
            decl.relation.entity2
        )

        key = decl.relation.entity1, decl.relation.name
        if key not in self.declarations[decl.user]:
            if isinstance(decl.relation, Association):
                self.declarations[decl.user][key] = set()
        if isinstance(decl.relation, Association):
            self.declarations[decl.user][key].add(decl.relation.entity2)
        else:  # AssocOne: new entity2 overwrites what existed before
            self.declarations[decl.user][key] = decl.relation.entity2
        print("Added:", decl)

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))


# for convenience
def is_object_name(name):
    return name[0].isupper()


def is_type_name(name):
    return name[0].islower()
