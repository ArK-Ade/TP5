# Librairies
import sqlite3
import os
import xml.etree.ElementTree as ET
from xml import etree
import lxml
import lxml.etree as etree

"""
Affiche la table (base de données) choisi en paramètre
"""


def print_table(nom_table_bdd: str):
    if nom_table_bdd is not "Regions" or "Departements" or "Communes":
        print("Paramètre incorrecte")

    requete = "SELECT * FROM " + nom_table_bdd
    resultat_bdd = c.execute(requete)

    for ligne_bdd in resultat_bdd:
        print(ligne_bdd)


"""
cree les 3 tables dans data_insee.db
"""


def creation_tables():
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


"""
Parcours les fichiers CSV et importe les données dans la base de données
"""


def parsing_bdd():
    # Parsing Communes
    with open('communes.csv') as fichier:

        lignes = fichier.readlines()

        for x in range(8, lignes.__len__() - 1):
            ligne_actuelle = lignes[x].split(';')
            tableau_donnee = (ligne_actuelle[2], ligne_actuelle[5], ligne_actuelle[6],
                              ligne_actuelle[9].replace(' ', ''))
            c.execute(
                "INSERT INTO Communes(code_departement,code_commune,nom_commune,population_totale) VALUES(?,?,?,?)",
                tableau_donnee)

    # Parsing Départements
    with open('departements.csv') as fichier:

        lignes = fichier.readlines()

        for x in range(8, lignes.__len__() - 1):
            ligne_actuelle = lignes[x].split(';')
            tableau_donnee = (ligne_actuelle[2], ligne_actuelle[3], ligne_actuelle[0])
            c.execute("INSERT INTO Departements(code_departement,nom_departement,code_region) VALUES(?,?,?)",
                      tableau_donnee)

    # Parsing Regions
    with open('regions.csv') as fichier:

        lignes = fichier.readlines()

        for x in range(8, lignes.__len__() - 1):
            ligne_actuelle = lignes[x].split(';')
            tableau_donnee = (ligne_actuelle[0], ligne_actuelle[1])
            c.execute("INSERT INTO Regions(code_region,nom_region) VALUES(?,?)",
                      tableau_donnee)


"""
affichage des populations totales par départements
"""


def afficher_pop_all_departements_regions():
    print("Affichage population départements")

    requete = "SELECT SUM(population_totale), code_departement FROM Communes GROUP BY code_departement"
    resultat = c.execute(requete)

    for ligne_actuelle in resultat:
        print("Département " + str(ligne_actuelle[1]) + " a une population totale de " + str(ligne_actuelle[0]))

    # affichage des populations totales par régions
    print("affichage population régions")
    requete = "SELECT SUM(population_totale), code_region " \
              "FROM Communes INNER JOIN Departements ON Communes.code_departement = Departements.code_departement " \
              "GROUP BY code_region"

    resultat = c.execute(requete)

    for ligne_actuelle in resultat:
        print("Régions " + str(ligne_actuelle[1]) + " a une population totale de " + str(ligne_actuelle[0]))


"""
affichage des communes possédant le meme nom dans diverses communes
"""


def afficher_meme_commune_different_departement():
    requete = "SELECT nom_commune, code_departement FROM Communes GROUP BY nom_commune,code_departement"
    resultat = c.execute(requete)

    affichageCommune = "Commune "
    affichageDepartement = " Departement "
    prevCommune = ""
    prevCodeDepartement = []
    count = 0

    for ligne_actuelle in resultat:

        if prevCommune == str(ligne_actuelle[0]) or prevCommune == "":
            prevCodeDepartement.append(str(ligne_actuelle[1]))
        elif resultat.__sizeof__() == count and prevCommune == str(ligne_actuelle[0]):
            prevCodeDepartement.append(str(ligne_actuelle[1]))
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
        elif resultat.__sizeof__() == count and prevCommune != str(ligne_actuelle[0]):
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
            print(affichageCommune + str(ligne_actuelle[0]) + affichageDepartement + str(ligne_actuelle[1]))
        else:
            code_as_string = repr(prevCodeDepartement)
            print(affichageCommune + prevCommune + affichageDepartement + code_as_string)
            prevCodeDepartement = [str(ligne_actuelle[1])]

        prevCommune = str(ligne_actuelle[0])
        count += 1


"""
Sauvegarde la base de données dans le fichier database.xml et affiche le contenu du fichier xml 
"""


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
    requete = "SELECT * FROM Communes"
    resultat = c.execute(requete)

    for ligne_actuelle in resultat:
        tableauCommunes.append(ligne_actuelle)

    for ligne_actuelle in tableauCommunes:
        Commune = ET.SubElement(Communes, "Commune")

        id_commune = ET.SubElement(Commune, "nom_region")
        id_commune.text = str(ligne_actuelle[0])

        code_departement = ET.SubElement(Commune, "code_departement")
        code_departement.text = ligne_actuelle[1]

        code_commune = ET.SubElement(Commune, "code_commune")
        code_commune.text = str(ligne_actuelle[2])

        nom_commune = ET.SubElement(Commune, "nom_commune")
        nom_commune.text = ligne_actuelle[3]

        population_totale = ET.SubElement(Commune, "population_totale")
        population_totale.text = str(ligne_actuelle[4])

    # Insertion des Departements
    requete = "SELECT * FROM Departements"
    resultat = c.execute(requete)

    for ligne_actuelle in resultat:
        tableauDepartements.append(ligne_actuelle)

    for ligne_actuelle in tableauDepartements:
        Departement = ET.SubElement(Departements, "Departement")

        id_departement = ET.SubElement(Departement, "nom_region")
        id_departement.text = str(ligne_actuelle[0])

        code_departement = ET.SubElement(Departement, "code_departement")
        code_departement.text = ligne_actuelle[1]

        nom_departement = ET.SubElement(Departement, "nom_departement")
        nom_departement.text = ligne_actuelle[2]

        code_region = ET.SubElement(Departement, "code_region")
        code_region.text = str(ligne_actuelle[3])

    # Insertion des Regions
    requete = "SELECT * FROM Regions"
    resultat = c.execute(requete)

    for ligne_actuelle in resultat:
        tableauRegions.append(ligne_actuelle)

    for ligne_actuelle in tableauRegions:
        Region = ET.SubElement(Regions, "Region")

        id_region = ET.SubElement(Region, "nom_region")
        id_region.text = str(ligne_actuelle[0])

        nom_region = ET.SubElement(Region, "nom_region")
        nom_region.text = str(ligne_actuelle[1])

        code_region = ET.SubElement(Region, "code_region")
        code_region.text = ligne_actuelle[2]

    # Creation du fichier XML
    tree = ET.ElementTree(root)
    tree.write("database.xml")

    # Parsing et affichage du fichier XML
    tree = lxml.etree.parse("database.xml")
    pretty = lxml.etree.tostring(tree, encoding="unicode", pretty_print=True)
    print(pretty)


"""
Convertit le fichier XML en base de données SQLite
"""


def restauration_bdd():
    # Initialisation
    tree = ET.parse('database.xml')
    root = tree.getroot()
    tableau = []

    # Parsing du fichier XML
    for parent in root:
        for enfant in parent:
            ligne = [enfant.tag]
            for petit_fils in enfant:
                ligne.append(petit_fils.text)
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


# Main
try:
    # Supprime le fichier s'il existe
    os.remove("data_insee.db")
    conn = sqlite3.connect('data_insee.db')
    c = conn.cursor()

    # Fonctions
    creation_tables()
    parsing_bdd()
    afficher_pop_all_departements_regions()
    afficher_meme_commune_different_departement()
    sauvegarde_bdd()
    restauration_bdd()
    print_table("Regions")

except sqlite3.Error as error:
    print("Erreur pendant la connexion SQLite")

finally:
    if conn:
        conn.commit()
        conn.close()
        print("Fin de la connexion de la base de données")
