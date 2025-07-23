# Guide de Configuration et Déploiement GitHub

## 🚀 Pousser vers GitHub

### Étape 1 : Initialiser le dépôt Git
```bash
cd quality-culture-barometer
git init
git add .
git commit -m "Initial commit: Quality Culture Barometer Framework"
```

### Étape 2 : Créer le dépôt GitHub
1. Allez sur [github.com](https://github.com)
2. Cliquez sur "New repository"
3. Nommez le dépôt : `quality-culture-barometer`
4. Gardez-le public ou privé selon vos besoins
5. Ne cochez pas "Initialize with README" (nous avons déjà un README)

### Étape 3 : Connecter et pousser
```bash
# Ajouter le dépôt distant (remplacez USERNAME par votre nom d'utilisateur)
git remote add origin https://github.com/USERNAME/quality-culture-barometer.git

# Pousser vers GitHub
git branch -M main
git push -u origin main
```

### Étape 4 : Vérifier le déploiement
- Votre projet est maintenant sur GitHub
- Vous pouvez accéder via : `https://github.com/USERNAME/quality-culture-barometer`

## 🐛 Résolution des problèmes GitHub

### Si vous avez déjà un dépôt avec le même nom :
```bash
# Supprimer l'ancien dépôt local
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/quality-culture-barometer.git
git push -u origin main --force
```

### Configuration Git locale (si nécessaire) :
```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

## 📁 Structure du Projet sur GitHub

Votre dépôt contiendra :
```
quality-culture-barometer/
├── src/
│   ├── core/           # Moteur d'évaluation principal
│   ├── dashboard/      # Dashboards Streamlit (FR/EN)
│   ├── sectors/        # Modules sectoriels
│   ├── analytics/      # Pipeline statistique
│   └── versions/       # Gestion des versions
├── deployment/         # Plans de déploiement
├── docs/              # Documentation
├── requirements.txt   # Dépendances Python
├── README.md         # Documentation principale
└── SETUP.md         # Ce fichier
```

## 🎯 Utilisation après GitHub

### Installation locale :
```bash
git clone https://github.com/USERNAME/quality-culture-barometer.git
cd quality-culture-barometer
pip install -r requirements.txt
```

### Lancer les dashboards :
```bash
# Version anglaise
python -m streamlit run src/dashboard/quality_dashboard.py

# Version française  
python -m streamlit run src/dashboard/quality_dashboard_fr.py
```

## 🔄 Mises à jour futures

Pour mettre à jour votre dépôt :
```bash
git add .
git commit -m "Description des changements"
git push origin main