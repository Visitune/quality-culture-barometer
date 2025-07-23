"""
Application principale pour Streamlit Cloud
Ce fichier est le point d'entrée pour Streamlit Cloud
"""

import streamlit as st
import sys
import os

# Ajouter le chemin src au système
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importer le dashboard principal
from dashboard.quality_dashboard_fr import TableauBordCultureQualite

if __name__ == "__main__":
    tableau_bord = TableauBordCultureQualite()
    tableau_bord.executer_tableau_bord()