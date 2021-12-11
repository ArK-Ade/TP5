"""
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python

https://evanhahn.com/python-skip-header-csv-reader/

https://www.kite.com/python/docs/csv.reader

https://stackoverflow.com/questions/16846460/skip-the-last-row-of-csv-file-when-iterating-in-python
"""

import sqlite3
import os

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


def afficher_pop_all_departements_regions():
    # affichage des populations totales par départements
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


def afficher_meme_commune_different_departement():
    request = "SELECT nom_commune, code_departement FROM Communes GROUP BY nom_commune,code_departement"
    pops = c.execute(request)

    for pop in pops:
        print("Commune " + str(pop[0]) + " Departement " + str(pop[1]))


create_tables()  # cree les 3 tables dans data_insee.db
parsing_communes()
parsing_departements()
parsing_regions()

#afficher_pop_all_departements_regions()
afficher_meme_commune_different_departement()
