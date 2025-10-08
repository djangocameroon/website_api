# Documentation de l'API

Ceci est la documentation pour l'API principale du site web Django Cameroon.

## Authentification

Les endpoints d'authentification permettent de gérer les utilisateurs et leur accès.

| Endpoint | Méthode | Description |
|---|---|---|
| `/api/v1/users/auth/register/` | `POST` | Enregistre un nouvel utilisateur. |
| `/api/v1/users/auth/login/` | `POST` | Connecte un utilisateur et retourne un token. |
| `/api/v1/users/auth/logout/` | `POST` | Déconnecte un utilisateur. |
| `/api/v1/users/auth/password/reset/` | `POST` | Démarre le processus de réinitialisation de mot de passe. |
| `/api/v1/users/auth/password/reset/confirm/` | `POST` | Confirme la réinitialisation de mot de passe. |
| `/api/v1/users/user/` | `GET` | Récupère les détails de l'utilisateur connecté. |
| `/api/v1/users/user/profile/` | `PUT`, `PATCH` | Met à jour le profil de l'utilisateur connecté. |

## Blog

L'API du blog permet de gérer les articles, auteurs, catégories, etc.

| Endpoint | Méthode | Description |
|---|---|---|
| `/api/v1/blog/posts/` | `GET`, `POST` | Liste les articles ou en crée un nouveau. |
| `/api/v1/blog/posts/<id>/` | `GET`, `PUT`, `DELETE` | Récupère, met à jour ou supprime un article. |
| `/api/v1/blog/authors/` | `GET` | Liste les auteurs. |
| `/api/v1/blog/categories/` | `GET` | Liste les catégories. |
| `/api/v1/blog/images/` | `GET`, `POST` | Liste les images ou en téléverse une nouvelle. |
| `/api/v1/blog/tags/` | `GET` | Liste les tags. |

## Événements

L'API des événements gère les événements, les intervenants et les réservations.

| Endpoint | Méthode | Description |
|---|---|---|
| `/api/v1/events/events/` | `GET`, `POST` | Liste les événements ou en crée un nouveau. |
| `/api/v1/events/events/<id>/` | `GET`, `PUT`, `DELETE` | Récupère, met à jour ou supprime un événement. |
| `/api/v1/events/speakers/` | `GET`, `POST` | Liste les intervenants ou en ajoute un nouveau. |
| `/api/v1/events/speakers/<id>/` | `GET`, `PUT`, `DELETE` | Récupère, met à jour ou supprime un intervenant. |
| `/api/v1/events/reservations/` | `GET`, `POST` | Liste les réservations ou en crée une nouvelle. |
| `/api/v1/events/reservations/<id>/` | `GET`, `PUT`, `DELETE` | Récupère, met à jour ou supprime une réservation. |