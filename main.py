"""
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python

https://evanhahn.com/python-skip-header-csv-reader/

https://www.kite.com/python/docs/csv.reader

https://stackoverflow.com/questions/16846460/skip-the-last-row-of-csv-file-when-iterating-in-python
"""

import sqlite3
import os
import xml.etree.ElementTree as ET

os.remove("data_insee.db")

conn = sqlite3.connect('data_insee.db')
c = conn.cursor()


def print_table(table_name):
    request = "SELECT * FROM " + table_name
    c.execute(request)
    print(c.fetchall())


def create_tables():
    c.execute('''
        CREATE TABLE Communes
        (id INTEGER PRIMARY KEY, 
        code_departement TEXT, 
        code_commune INTEGER, 
        nom_commune TEXT, 
        population_totale INTEGER)''')

    c.execute('''
        CREATE TABLE Departements
        (id INTEGER PRIMARY KEY, 
        code_departement TEXT, 
        nom_departement TEXT, 
        code_region INTEGER)''')

    c.execute('''
        CREATE TABLE Regions
        (id INTEGER PRIMARY KEY, 
        code_region INTEGER, 
        nom_region TEXT)''')


def parsing_communes():
    file = open('communes.csv', 'rt')
    lignes = file.readlines()

    print(lignes.__len__() - 1)
    for x in range(8, lignes.__len__() - 1):
        current_line = lignes[x].split(';')
        donnees = (current_line[2], current_line[5], current_line[6], current_line[9].replace(' ', ''))
        c.execute("INSERT INTO Communes(code_departement,code_commune,nom_commune,population_totale) VALUES(?,?,?,?)",
                  donnees)

    file.close()


def parsing_departements():
    file = open('departements.csv', 'rt')
    lignes = file.readlines()

    for x in range(8, lignes.__len__() - 1):
        current_line = lignes[x].split(';')
        donnees = (current_line[2], current_line[3], current_line[0])
        c.execute("INSERT INTO Departements(code_departement,nom_departement,code_region) VALUES(?,?,?)",
                  donnees)

    file.close()


def parsing_regions():
    file = open('regions.csv', 'rt')
    lignes = file.readlines()

    for x in range(8, lignes.__len__() - 1):
        current_line = lignes[x].split(';')
        donnees = (current_line[0], current_line[1])
        c.execute("INSERT INTO Regions(code_region,nom_region) VALUES(?,?)",
                  donnees)

    file.close()


# affichage des populations totales par départements
def afficher_pop_all_departements_regions():
    print("Affichage population départements")

    request = "SELECT SUM(population_totale), code_departement FROM Communes GROUP BY code_departement"
    pops = c.execute(request)

    for pop in pops:
        print("Département " + str(pop[1]) + " a une population totale de " + str(pop[0]))

    # affichage des populations totales par régions
    print("affichage population régions")
    request = "SELECT SUM(population_totale), code_region " \
              "FROM Communes INNER JOIN Departements ON Communes.code_departement = Departements.code_departement " \
              "GROUP BY code_region"

    pops = c.execute(request)

    for pop in pops:
        print("Régions " + str(pop[1]) + " a une population totale de " + str(pop[0]))


# affichage des communes possédant le meme nom dans diverses communes
def afficher_meme_commune_different_departement():
    request = "SELECT nom_commune, code_departement FROM Communes GROUP BY nom_commune,code_departement"
    pops = c.execute(request)

    affichageCommune = "Commune "
    affichageDepartement = " Departement "
    prevCommune = ""
    prevCodeDepartement = []
    count = 0

    for pop in pops:

        if prevCommune == str(pop[0]) or prevCommune == "":
            prevCodeDepartement.append(str(pop[1]))
        elif pops.__sizeof__() == count and prevCommune == str(pop[0]):
            prevCodeDepartement.append(str(pop[1]))
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
        elif pops.__sizeof__() == count and prevCommune != str(pop[0]):
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
            print(affichageCommune + str(pop[0]) + affichageDepartement + str(pop[1]))
        else:
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
            prevCodeDepartement = [str(pop[1])]

        prevCommune = str(pop[0])
        count += 1


def sauvegarde_bdd():
    tree = ET.parse('database.xml')
    root = tree.getroot()
    print(root[0][1])

    # TODO Creer le fichier XML s'il n'existe pas
    # Creer la source source data dans le fichier
    # creer un parent Commune dont les enfants sont id, code_departement etc
    # creer Departements
    # creer Regions
    # Faire boucle : une commande SQL qui parse la table Commune
    # Ajouter au fichier XML
    # Faire boucle : une commande SQL qui parse la table Departement
    # Ajouter au fichier XML
    # Faire boucle : une commande SQL qui parse la table Regions
    # Ajouter au fichier XML


def restauration_bdd():
    pass
    # TODO Reinitaliser la bdd
    create_tables()
    # TODO Parser le fichier XML et injecter les données dans la BDD


create_tables()  # cree les 3 tables dans data_insee.db
parsing_communes()
parsing_departements()
parsing_regions()

# afficher_pop_all_departements_regions()
# afficher_meme_commune_different_departement()
sauvegarde_bdd()
