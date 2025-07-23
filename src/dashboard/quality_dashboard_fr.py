"""
Tableau de bord Culture Qualité - Version Française
Dashboard interactif avec explications claires en français
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

class TableauBordCultureQualite:
    """Dashboard interactif en français avec guide étape par étape"""
    
    def __init__(self):
        self.cadres = {
            "ISO10010": {
                "nom": "ISO 10010:2022 Culture Qualité",
                "description": "Norme internationale d'évaluation de la culture qualité avec 4 dimensions : Leadership, Processus, Personnes, Résultats"
            },
            "AFNOR": {
                "nom": "Baromètre AFNOR Culture Qualité", 
                "description": "Baromètre français de culture qualité avec 20 items et score NPQS"
            },
            "PDA": {
                "nom": "Évaluation PDA Culture Qualité",
                "description": "Standard industriel pharmaceutique avec 21 éléments de maturité répartis en 5 domaines"
            }
        }
        
    def executer_tableau_bord(self):
        """Exécution principale du tableau de bord en français"""
        st.set_page_config(
            page_title="Baromètre Culture Qualité",
            page_icon="📊",
            layout="wide"
        )
        
        # Barre latérale pour la configuration
        st.sidebar.title("⚙️ Guide de Configuration")
        
        # Étape 1 : Sélection du cadre
        st.sidebar.markdown("### 📋 Étape 1 : Choisir le Cadre")
        cadre_selectionne = st.sidebar.selectbox(
            "Sélectionner le Cadre d'Évaluation",
            list(self.cadres.keys()),
            format_func=lambda x: self.cadres[x]["nom"],
            help="Chaque cadre a des domaines de focus et méthodes de notation différentes"
        )
        
        # Afficher l'explication du cadre
        st.sidebar.info(self.cadres[cadre_selectionne]["description"])
        
        # Étape 2 : Mode d'évaluation
        st.sidebar.markdown("### 🚀 Étape 2 : Sélectionner le Mode")
        mode = st.sidebar.radio(
            "Choisir le Mode d'Opération",
            ["📊 Mode Démo", "🎯 Nouvelle Évaluation", "📈 Charger des Données"],
            help="Démo montre des exemples, Nouvelle crée une évaluation fraîche, Charge utilise vos données"
        )
        
        # Zone principale
        st.title("📊 Baromètre Culture Qualité")
        st.subheader("Évaluation scientifique et rigoureuse de votre culture qualité organisationnelle")
        
        # Guide d'utilisation
        with st.expander("🎯 Guide d'utilisation", expanded=True):
            st.markdown("""
            ### 🚀 Guide de Démarrage Rapide
            
            **Ce tableau de bord vous aide à mesurer et améliorer la culture qualité de votre organisation.**
            
            #### 📋 **Processus Étape par Étape :**
            
            1. **Choisir le Cadre** (barre latérale gauche)
               - **ISO 10010** : Norme internationale avec 4 dimensions
               - **AFNOR** : Baromètre français avec score NPQS
               - **PDA** : Standard industriel pharmaceutique
            
            2. **Sélectionner le Mode** (barre latérale gauche)
               - **Mode Démo** : Voir des exemples de résultats et fonctionnalités
               - **Nouvelle Évaluation** : Créer une nouvelle enquête
               - **Charger Données** : Importer vos réponses existantes
            
            3. **Configurer l'Évaluation** (zone principale)
               - Définir les détails de l'organisation
               - Choisir les démographies
               - Personnaliser les questions
            
            4. **Déployer l'Enquête**
               - Générer des liens d'enquête
               - Envoyer aux participants
               - Suivre les réponses
            
            5. **Analyser les Résultats**
               - Voir le tableau de bord en temps réel
               - Exporter les rapports
               - Créer des plans d'action
            
            #### 🎯 **Ce que vous obtiendrez :**
            - **Score Global Culture Qualité** (0-100)
            - **Score NPQS** (-100 à +100)
            - **Niveau de Maturité** (Initial → Optimisation)
            - **Analyse Détaillée** par département/rôle
            - **Comparatifs de Référence**
            - **Recommandations d'Amélioration**
            """)
        
        # Contenu spécifique au mode
        if mode == "📊 Mode Démo":
            self.afficher_mode_demo(cadre_selectionne)
        elif mode == "🎯 Nouvelle Évaluation":
            self.afficher_nouvelle_evaluation(cadre_selectionne)
        else:
            self.afficher_charger_donnees(cadre_selectionne)
    
    def afficher_mode_demo(self, cadre: str):
        """Afficher le mode démo avec explications en français"""
        st.header("📊 Mode Démo - Exemples de Résultats")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("💡 **Données de démonstration** - Montre à quoi vos résultats ressembleront")
        
        # Générer des données de démo
        donnees = self.generer_donnees_demo(cadre)
        
        # Indicateurs clés avec explications
        st.markdown("### 📊 Indicateurs Clés de Performance")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Réponses Totales", len(donnees), 
                     help="Nombre de personnes ayant complété l'évaluation")
        with col2:
            st.metric("Score NPQS", "72,5", 
                     help="Score Net Promoter Qualité : Promoteurs - Détracteurs")
        with col3:
            st.metric("Score Global", "78,2/100", 
                     help="Score moyen de culture qualité sur toutes les dimensions")
        with col4:
            st.metric("Taux de Complétion", "94,3%", 
                     help="Pourcentage de personnes ayant terminé l'évaluation complète")
        
        # Onglets détaillés
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'Ensemble", "🔍 Analyse Détaillée", "🎯 Référentiel", "📋 Actions"])
        
        with tab1:
            self.afficher_vue_ensemble_avec_explications(donnees, cadre)
        
        with tab2:
            self.afficher_analyse_detaillee(donnees, cadre)
        
        with tab3:
            self.afficher_comparaison_referentiel(donnees, cadre)
        
        with tab4:
            self.afficher_actions_recommandees(donnees, cadre)
    
    def afficher_nouvelle_evaluation(self, cadre: str):
        """Créer une nouvelle configuration d'évaluation en français"""
        st.header("🎯 Créer une Nouvelle Évaluation")
        
        with st.form("nouvelle_evaluation"):
            st.markdown("### 🏢 Détails de l'Organisation")
            
            col1, col2 = st.columns(2)
            with col1:
                nom_org = st.text_input("Nom de l'Organisation", placeholder="ex: Entreprise ABC")
                industrie = st.selectbox("Industrie", 
                    ["Industrie manufacturière", "Santé", "Pharmaceutique", "Éducation", "Technologie", "Autre"])
            
            with col2:
                nb_employes = st.number_input("Nombre d'Employés", min_value=10, max_value=100000, value=100)
                sites = st.multiselect("Sites/Emplacements", ["Site A", "Site B", "Site C", "Télétravail"], default=["Site A"])
            
            st.markdown("### 👥 Démographie à Collecter")
            demographies = st.multiselect(
                "Sélectionner les questions démographiques",
                ["Département", "Niveau de Rôle", "Années d'Expérience", "Emplacement", "Groupe d'Âge", "Niveau d'Éducation"],
                default=["Département", "Niveau de Rôle", "Années d'Expérience"]
            )
            
            st.markdown("### 📋 Configuration de l'Évaluation")
            col1, col2 = st.columns(2)
            with col1:
                cible_reponses = st.number_input("Nombre Cible de Réponses", min_value=10, max_value=10000, value=100)
                anonymat = st.checkbox("Garantir l'anonymat complet", value=True)
            
            with col2:
                langue_enquete = st.selectbox("Langue de l'Enquête", ["Français", "Anglais", "Espagnol", "Allemand"])
                frequence_rappel = st.selectbox("Fréquence des Rappels", ["Aucun", "Hebdomadaire", "Tous les 3 jours", "Quotidien"])
            
            soumis = st.form_submit_button("🚀 Générer l'Évaluation", use_container_width=True)
            
            if soumis and nom_org:
                config_evaluation = {
                    "cadre": cadre,
                    "organisation": nom_org,
                    "industrie": industrie,
                    "employes": nb_employes,
                    "sites": sites,
                    "demographies": demographies,
                    "cible_reponses": cible_reponses,
                    "anonymat": anonymat,
                    "langue": langue_enquete,
                    "rappels": frequence_rappel
                }
                
                st.success("✅ Évaluation Créée avec Succès!")
                st.json(config_evaluation)
                
                # Générer des liens d'enquête
                st.markdown("### 🔗 Distribution de l'Enquête")
                lien_enquete = f"http://localhost:8501/enquete/{nom_org.lower().replace(' ', '_')}_{cadre.lower()}"
                st.code(lien_enquete, language="text")
                
                st.markdown("**Partager ce lien avec vos employés :**")
                st.info(f"📧 **Modèle d'Email :**\n\nBonjour l'Équipe,\n\nNous menons une évaluation de la culture qualité. Veuillez prendre 10-15 minutes pour compléter :\n\n🔗 {lien_enquete}\n\nVos réponses sont {'anonymes' if anonymat else 'confidentielles'} et nous aideront à améliorer notre culture qualité.\n\nMerci!")
    
    def afficher_charger_donnees(self, cadre: str):
        """Charger des données d'évaluation existantes"""
        st.header("📈 Charger des Données d'Évaluation Existantes")
        
        fichier_telecharge = st.file_uploader(
            "Télécharger vos données d'évaluation",
            type=['csv', 'xlsx', 'json'],
            help="Télécharger les réponses en format CSV, Excel ou JSON"
        )
        
        if fichier_telecharge is not None:
            try:
                if fichier_telecharge.name.endswith('.csv'):
                    donnees = pd.read_csv(fichier_telecharge)
                elif fichier_telecharge.name.endswith('.xlsx'):
                    donnees = pd.read_excel(fichier_telecharge)
                else:
                    donnees = pd.read_json(fichier_telecharge)
                
                st.success("✅ Données chargées avec succès!")
                st.dataframe(donnees.head())
                
                # Traiter et afficher les résultats
                self.afficher_resultats_donnees(donnees, cadre)
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement : {str(e)}")
                st.info("💡 Format attendu : Les colonnes doivent inclure les dimensions du cadre et les démographies")
    
    def afficher_vue_ensemble_avec_explications(self, donnees: pd.DataFrame, cadre: str):
        """Afficher la vue d'ensemble avec explications détaillées"""
        st.markdown("### 📊 Vue d'Ensemble de la Culture Qualité")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🎯 Explication du Graphique Radar")
            st.info("Ce graphique montre les forces et domaines d'amélioration de votre organisation")
            
            if cadre == "ISO10010":
                dimensions = ['Leadership', 'Processus', 'Personnes', 'Résultats']
            elif cadre == "AFNOR":
                dimensions = ['Responsabilité', 'Qualité dès la 1ère fois', 'Remontée problèmes', 'Amélioration continue']
            else:  # PDA
                dimensions = ['Engagement Leadership', 'Systèmes Qualité', 'Gestion Risques', 'Formation Compétences']
            
            scores = [donnees[dim].mean() * 20 for dim in dimensions]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=dimensions,
                fill='toself',
                name='Votre Score',
                line_color='rgb(55, 128, 191)'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(range=[0, 100], tickfont_size=12),
                    angularaxis=dict(tickfont_size=12)
                ),
                title="Dimensions de la Culture Qualité",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Interprétation des Scores")
            
            gammes_scores = {
                "90-100": "🏆 Excellent - Culture qualité de classe mondiale",
                "80-89": "⭐ Très Bon - Fondation solide avec des améliorations mineures",
                "70-79": "👍 Bon - Performance solide, place pour l'amélioration",
                "60-69": "⚠️ Moyen - Lacunes significatives à adresser",
                "50-59": "❌ Faible - Transformation majeure requise",
                "<50": "🚨 Critique - Action immédiate nécessaire"
            }
            
            for gamme, interpretation in gammes_scores.items():
                st.write(f"**{gamme}**: {interpretation}")
    
    def afficher_analyse_detaillee(self, donnees: pd.DataFrame, cadre: str):
        """Afficher l'analyse détaillée avec explications"""
        st.markdown("### 🔍 Analyse Détaillée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Comparaison par Département")
            st.info("Comparer les scores de culture qualité entre différents départements")
            
            if cadre == "ISO10010":
                dimensions = ['Leadership', 'Processus', 'Personnes', 'Résultats']
            elif cadre == "AFNOR":
                dimensions = ['Responsabilité', 'Qualité dès la 1ère fois', 'Remontée problèmes', 'Amélioration continue']
            else:  # PDA
                dimensions = ['Engagement Leadership', 'Systèmes Qualité', 'Gestion Risques', 'Formation Compétences']
            
            dept_scores = donnees.groupby('department')[dimensions].mean() * 20
            
            fig = px.bar(
                dept_scores.reset_index().melt(id_vars='department'),
                x='department',
                y='value',
                color='variable',
                title="Scores par Département",
                labels={'value': 'Score (0-100)', 'variable': 'Dimension'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Distribution des Scores")
            st.info("Voir comment les scores sont répartis dans votre organisation")
            
            if cadre == "ISO10010":
                dimensions = ['Leadership', 'Processus', 'Personnes', 'Résultats']
            elif cadre == "AFNOR":
                dimensions = ['Responsabilité', 'Qualité dès la 1ère fois', 'Remontée problèmes', 'Amélioration continue']
            else:  # PDA
                dimensions = ['Engagement Leadership', 'Systèmes Qualité', 'Gestion Risques', 'Formation Compétences']
            
            dim_selectionnee = st.selectbox("Sélectionner la Dimension", dimensions)
            
            fig = px.histogram(
                donnees, 
                x=dim_selectionnee,
                nbins=20,
                title=f"Distribution des Scores - {dim_selectionnee}",
                labels={'x': 'Score (0-100)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def afficher_comparaison_referentiel(self, donnees: pd.DataFrame, cadre: str):
        """Afficher la comparaison avec le référentiel"""
        st.markdown("### 🎯 Comparaison avec le Référentiel")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📊 Comparaison Industrielle")
            st.info("Comparer la performance de votre organisation avec les standards de l'industrie")
            
            if cadre == "ISO10010":
                categories = ['Leadership', 'Processus', 'Personnes', 'Résultats']
            elif cadre == "AFNOR":
                categories = ['Responsabilité', 'Qualité dès la 1ère fois', 'Remontée problèmes', 'Amélioration continue']
            else:  # PDA
                categories = ['Engagement Leadership', 'Systèmes Qualité', 'Gestion Risques', 'Formation Compétences']
            
            actuel = [84, 76, 82, 78]
            industrie = [75, 70, 73, 71]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Votre Organisation', 
                x=categories, 
                y=actuel,
                marker_color='rgb(55, 128, 191)'
            ))
            fig.add_trace(go.Bar(
                name='Moyenne Industrie', 
                x=categories, 
                y=industrie,
                marker_color='rgb(219, 64, 82)'
            ))
            fig.update_layout(
                title="Comparaison avec le Référentiel",
                yaxis_title="Score (0-100)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Insights du Référentiel")
            
            insights = [
                "✅ **Leadership** : 9 points au-dessus de la moyenne",
                "✅ **Personnes** : 9 points au-dessus de la moyenne", 
                "⚠️ **Processus** : 6 points au-dessus, mais dimension la plus faible",
                "✅ **Résultats** : 7 points au-dessus de la moyenne"
            ]
            
            for insight in insights:
                st.write(insight)
    
    def afficher_actions_recommandees(self, donnees: pd.DataFrame, cadre: str):
        """Afficher les actions recommandées"""
        st.markdown("### 📋 Actions Recommandées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Actions Prioritaires")
            
            actions = [
                {
                    "priorite": "🔴 Haute",
                    "action": "Améliorer la Standardisation des Processus",
                    "dimension": "Processus",
                    "score_actuel": "76/100",
                    "objectif": "85/100",
                    "delai": "3 mois"
                },
                {
                    "priorite": "🟡 Moyenne", 
                    "action": "Renforcer la Communication du Leadership",
                    "dimension": "Leadership",
                    "score_actuel": "84/100",
                    "objectif": "90/100",
                    "delai": "2 mois"
                },
                {
                    "priorite": "🟢 Faible",
                    "action": "Célébrer le Succès de l'Engagement des Personnes",
                    "dimension": "Personnes", 
                    "score_actuel": "82/100",
                    "objectif": "85/100",
                    "delai": "1 mois"
                }
            ]
            
            for action in actions:
                with st.expander(f"{action['priorite']} - {action['action']}"):
                    st.write(f"**Dimension :** {action['dimension']}")
                    st.write(f"**Score Actuel :** {action['score_actuel']}")
                    st.write(f"**Objectif :** {action['objectif']}")
                    st.write(f"**Délai :** {action['delai']}")
        
        with col2:
            st.markdown("#### 📊 Prochaines Étapes")
            
            st.info("""
            **Actions Immédiates (30 prochains jours) :**
            1. Partager les résultats avec l'équipe de direction
            2. Identifier les champions de l'amélioration des processus
            3. Planifier des sessions de feedback spécifiques aux départements
            
            **Moyen terme (1-3 mois) :**
            1. Mettre en œuvre la formation à la standardisation des processus
            2. Établir des points de contrôle réguliers
            3. Créer des plans d'action d'amélioration
            
            **Long terme (3-6 mois) :**
            1. Ré-évaluer pour mesurer les progrès
            2. Étendre l'évaluation à d'autres sites
            3. Intégrer à l'amélioration continue
            """)
    
    def generer_donnees_demo(self, cadre: str) -> pd.DataFrame:
        """Générer des données de démo réalistes"""
        np.random.seed(42)
        n = 500
        
        if cadre == "ISO10010":
            donnees = {
                'Leadership': np.random.normal(4.2, 0.6, n),
                'Processus': np.random.normal(3.8, 0.7, n),
                'Personnes': np.random.normal(4.1, 0.5, n),
                'Résultats': np.random.normal(3.9, 0.8, n),
            }
        elif cadre == "AFNOR":
            donnees = {
                'Responsabilité': np.random.normal(4.0, 0.5, n),
                'Qualité dès la 1ère fois': np.random.normal(3.7, 0.6, n),
                'Remontée problèmes': np.random.normal(4.2, 0.5, n),
                'Amélioration continue': np.random.normal(3.9, 0.7, n),
            }
        else:  # PDA
            donnees = {
                'Engagement Leadership': np.random.normal(4.1, 0.5, n),
                'Systèmes Qualité': np.random.normal(3.9, 0.6, n),
                'Gestion Risques': np.random.normal(4.0, 0.5, n),
                'Formation Compétences': np.random.normal(3.8, 0.7, n),
            }
        
        donnees.update({
            'department': np.random.choice(['Production', 'R&D', 'Ventes', 'Qualité', 'Opérations'], n),
            'site': np.random.choice(['Site A', 'Site B', 'Site C', 'Télétravail'], n),
            'role_level': np.random.choice(['Individuel', 'Chef d\'Équipe', 'Manager', 'Direction'], n),
            'experience': np.random.choice(['<1an', '1-3ans', '3-5ans', '5-10ans', '>10ans'], n)
        })
        
        return pd.DataFrame(donnees)
    
    def afficher_resultats_donnees(self, donnees: pd.DataFrame, cadre: str):
        """Afficher les résultats à partir des données téléchargées"""
        st.success("✅ Données traitées avec succès!")
        
        # Calculer les scores
        dimensions = [col for col in donnees.columns if col not in ['department', 'site', 'role_level', 'experience']]
        scores = donnees[dimensions].mean() * 20
        
        st.markdown("### 📊 Résumé des Résultats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score Global", f"{scores.mean():.1f}/100")
        with col2:
            st.metric("Réponses Totales", len(donnees))
        with col3:
            st.metric("Dimensions", len(dimensions))
        
        # Visualisations
        fig = px.bar(
            x=dimensions,
            y=scores.values,
            title="Scores par Dimension",
            labels={'x': 'Dimension', 'y': 'Score (0-100)'}
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    tableau_bord = TableauBordCultureQualite()
    tableau_bord.executer_tableau_bord()