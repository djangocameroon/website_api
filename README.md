# Website API

Une API RESTful construite avec Django et Django REST Framework pour gérer le contenu d'un site web, incluant des fonctionnalités de blog, d'événements et de gestion d'utilisateurs.

## 📋 Prérequis

- Python 3.8+
- PostgreSQL 12+
- Redis (pour le cache et les files d'attente)
- pip (gestionnaire de paquets Python)

## Installation

Download [uv](https://github.com/astral-sh/uv) if not already installed.

1. Create virtual environment:
   ```bash
   uv venv
   ```

2. Copy the environment file and fill in the values (including database credentials):
   ```bash
   cp .env.example .env
   ```

3. Run migrations:
   ```bash
   make migrate
   ```

4. Create the static directory:
   ```bash
   mkdir static
   ```

5. Start the server:
   ```bash
   make start
   ```


## 📚 Documentation de l'API

La documentation de l'API est disponible à l'adresse `/redoc/` lorsque le serveur est en cours d'exécution.

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