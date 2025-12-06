# Website API

Une API RESTful construite avec Django et Django REST Framework pour gérer le contenu d'un site web, incluant des fonctionnalités de blog, d'événements et de gestion d'utilisateurs.

## 📋 Prérequis

- Python 3.8+
- PostgreSQL 12+
- Redis (pour le cache et les files d'attente)
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/charles-kamga/website_api.git
   cd website_api
   ```

2. **Configurer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données PostgreSQL**
   ```sql
   -- Se connecter à PostgreSQL
   sudo -u postgres psql
   
   -- Créer la base de données
   CREATE DATABASE django_website_db;
   
   -- Créer un utilisateur (remplacez les valeurs entre crochets)
   CREATE USER [db_user] WITH PASSWORD '[votre_mot_de_passe]';
   
   -- Accorder les privilèges
   GRANT ALL PRIVILEGES ON DATABASE django_website_db TO [db_user];
   ```

5. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   ```
   
   Modifiez le fichier `.env` avec vos paramètres :
   - `DB_*` : Paramètres de connexion à la base de données
   - `SECRET_KEY` : Clé secrète Django (générez-en une nouvelle pour la production)
   - `EMAIL_*` : Configuration SMTP pour les emails
   - `TWILLIO_*` : Identifiants Twilio pour la vérification par SMS (optionnel)

6. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

7. **Créer un superutilisateur (optionnel)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```
   
   L'API sera disponible à l'adresse : http://127.0.0.1:8000/
   L'interface d'administration sera disponible à : http://127.0.0.1:8000/admin/

## 🏗 Structure du projet

```
website_api/
├── apps/                  # Applications Django
│   ├── blog/             # Gestion des articles de blog
│   ├── events/           # Gestion des événements
│   └── users/            # Gestion des utilisateurs et authentification
├── config/               # Configuration du projet
├── documentation/        # Documentation supplémentaire
├── middlewares/          # Middlewares personnalisés
├── services/             # Logique métier
└── website_api/          # Paramètres principaux du projet
```

## 🔧 Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `DEBUG` | Mode débogage | `True` en développement, `False` en production |
| `SECRET_KEY` | Clé secrète Django | À définir en production |
| `DB_*` | Paramètres de la base de données | Voir `.env.example` |
| `EMAIL_*` | Configuration SMTP | À configurer pour les emails |
| `REDIS_URL` | URL de connexion à Redis | `redis://127.0.0.1:6379` |
| `TWILLIO_*` | Identifiants Twilio (SMS) | Optionnel |

## 📚 Documentation de l'API

La documentation de l'API est disponible à l'adresse `/api/docs/` lorsque le serveur est en cours d'exécution.

## 🧪 Exécution des tests

```bash
# Exécuter tous les tests
python manage.py test

# Exécuter les tests d'une application spécifique
python manage.py test apps.users
```

## 🛠 Outils de développement

- **Linting** : `flake8`
- **Formatage** : `black`
- **Tri des imports** : `isort`

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajouter une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/ma-nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📧 Contact

Pour toute question, veuillez ouvrir une issue sur GitHub ou contacter l'équipe de développement.