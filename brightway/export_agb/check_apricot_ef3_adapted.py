import brightway2 as bw
from brightway2 import *
from bw2calc.errors import AllArraysEmpty
from impacts import impacts


def open_db(dbname):
    bw.projects.set_current("EF calculation")
    bw.bw2setup()
    return Database(dbname)


if __name__ == "__main__":
    agb = open_db("agribalyse3")
    apricot = agb.search("[Ciqual code: 13712]")[0]

    demand = {apricot: 1}

    for key, method in impacts.items():
        print(f"{key}: ", end="")
        try:
            lca = LCA(demand, method)
            lca.lci()
            lca.lcia()
            print(lca.score)
        except AllArraysEmpty as e:
            print("erreur: all arrays empty")
