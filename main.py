"""
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python

https://evanhahn.com/python-skip-header-csv-reader/

https://www.kite.com/python/docs/csv.reader

https://stackoverflow.com/questions/16846460/skip-the-last-row-of-csv-file-when-iterating-in-python
"""

import sqlite3
import os
import xml.etree.ElementTree as ET
from xml import etree

import lxml
import lxml.etree as etree


def print_table(table_name):
    request = "SELECT * FROM " + table_name
    pops = c.execute(request)

    for pop in pops:
        print(pop)

# cree les 3 tables dans data_insee.db
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


# Sauvegarde la base de données dans le fichier database.xml
def sauvegarde_bdd():
    # Initialisation des tableaux

    tableauCommunes = []
    tableauDepartements = []
    tableauRegions = []

    # Initialisation XML

    root = ET.Element("root")
    Communes = ET.SubElement(root, "Communes")
    Departements = ET.SubElement(root, "Departements")
    Regions = ET.SubElement(root, "Regions")

    # Insertion des Communes

    request = "SELECT * FROM Communes"
    pops = c.execute(request)

    for pop in pops:
        tableauCommunes.append(pop)

    for ligne in tableauCommunes:
        Commune = ET.SubElement(Communes, "Commune")

        id_commune = ET.SubElement(Commune, "nom_region")
        id_commune.text = str(ligne[0])

        code_departement = ET.SubElement(Commune, "code_departement")
        code_departement.text = ligne[1]

        code_commune = ET.SubElement(Commune, "code_commune")
        code_commune.text = str(ligne[2])

        nom_commune = ET.SubElement(Commune, "nom_commune")
        nom_commune.text = ligne[3]

        population_totale = ET.SubElement(Commune, "population_totale")
        population_totale.text = str(ligne[4])

    # Insertion des Departements

    request = "SELECT * FROM Departements"
    pops = c.execute(request)

    for pop in pops:
        tableauDepartements.append(pop)

    for ligne in tableauDepartements:
        Departement = ET.SubElement(Departements, "Departement")

        id_departement = ET.SubElement(Departement, "nom_region")
        id_departement.text = str(ligne[0])

        code_departement = ET.SubElement(Departement, "code_departement")
        code_departement.text = ligne[1]

        nom_departement = ET.SubElement(Departement, "nom_departement")
        nom_departement.text = ligne[2]

        code_region = ET.SubElement(Departement, "code_region")
        code_region.text = str(ligne[3])

    # Insertion des Regions

    request = "SELECT * FROM Regions"
    pops = c.execute(request)

    for pop in pops:
        tableauRegions.append(pop)

    for ligne in tableauRegions:
        Region = ET.SubElement(Regions, "Region")

        id_region = ET.SubElement(Region, "nom_region")
        id_region.text = str(ligne[0])

        nom_region = ET.SubElement(Region, "nom_region")
        nom_region.text = str(ligne[1])

        code_region = ET.SubElement(Region, "code_region")
        code_region.text = ligne[2]

    # Creation du fichier XML
    tree = ET.ElementTree(root)
    tree.write("database.xml")

    # Parsing et affichage du fichier XML
    tree = lxml.etree.parse("database.xml")
    pretty = lxml.etree.tostring(tree, encoding="unicode", pretty_print=True)
    print(pretty)


def restauration_bdd():
    # Initialisation
    tree = ET.parse('database.xml')
    root = tree.getroot()
    tableau = []

    # Parsing du fichier XML
    for parent in root:
        for child in parent:
            ligne = [child.tag]
            for grand_child in child:
                ligne.append(grand_child.text)
            tableau.append(ligne)

    # Insertion des données dans la bdd
    for ligne in tableau:
        categorie = ligne[0]
        ligne.pop(0)
        ligne.pop(0)
        if categorie == "Commune":
            # Insertion des Communes dans la bdd
            c.execute(
                "INSERT INTO Communes(code_departement, code_commune, nom_commune, population_totale) VALUES(?,?,?,?)",
                ligne)
        elif categorie == "Departement":
            # Insertion des Departements dans la bdd
            c.execute("INSERT INTO Departements(code_departement, nom_departement, code_region) VALUES(?,?,?)", ligne)
        elif categorie == "Region":
            # Insertion des Regions dans la bdd
            c.execute("INSERT INTO Regions(code_region, nom_region) VALUES(?,?)", ligne)


os.remove("data_insee.db")
conn = sqlite3.connect('data_insee.db')
c = conn.cursor()

create_tables()
# parsing_communes()
# parsing_departements()
# parsing_regions()

# afficher_pop_all_departements_regions()
# afficher_meme_commune_different_departement()
# sauvegarde_bdd()
# restauration_bdd()

#print_table("Regions")
