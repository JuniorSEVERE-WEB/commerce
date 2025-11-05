# 🛠️ Guide d'Administration CommerceHub

## 📋 Accès à l'Interface d'Administration

### Informations de Connexion
- **URL d'accès** : `http://127.0.0.1:8000/admin/`
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin123`

### Accès Rapide depuis le Site
Si vous êtes connecté en tant qu'administrateur (utilisateur `staff`), un bouton **"Administration"** apparaît dans l'en-tête du site.

---

## 🎯 Fonctionnalités Disponibles

### 1. 📊 Tableau de Bord Personnalisé
- **Statistiques en temps réel** : Nombre d'annonces, utilisateurs, enchères, commentaires
- **Actions rapides** : Liens directs pour créer de nouvelles entrées
- **Activité récente** : Dernières annonces et commentaires

### 2. 👥 Gestion des Utilisateurs
- **Voir tous les utilisateurs** : Liste complète avec filtres
- **Informations détaillées** : Email, dates, statuts
- **Watchlist** : Nombre d'articles suivis par chaque utilisateur
- **Recherche** : Par nom d'utilisateur, nom, prénom, email

### 3. 📝 Gestion des Annonces (Listings)
**Fonctionnalités disponibles :**
- ✅ **Voir** toutes les annonces (actives et fermées)
- ✅ **Ajouter** de nouvelles annonces
- ✅ **Modifier** les annonces existantes
- ✅ **Supprimer** des annonces
- ✅ **Filtrer** par statut, catégorie, propriétaire
- ✅ **Rechercher** par titre, description, propriétaire

**Informations affichées :**
- Titre et propriétaire
- Catégorie et prix actuel
- Statut (actif/fermé)
- Nombre de personnes qui suivent
- Nombre de commentaires

### 4. 🏷️ Gestion des Catégories
- **Créer** de nouvelles catégories
- **Modifier** les catégories existantes
- **Voir** le nombre d'annonces par catégorie
- **Supprimer** des catégories (attention aux dépendances)

### 5. 💰 Gestion des Enchères (Bids)
**Fonctionnalités :**
- ✅ **Voir** toutes les enchères
- ✅ **Ajouter** des enchères
- ✅ **Modifier** des enchères existantes
- ✅ **Supprimer** des enchères

**Informations affichées :**
- Utilisateur et montant
- Annonce liée
- Date de création

### 6. 💬 Gestion des Commentaires
**Fonctionnalités :**
- ✅ **Voir** tous les commentaires
- ✅ **Ajouter** de nouveaux commentaires
- ✅ **Modifier** des commentaires existants
- ✅ **Supprimer** des commentaires

**Informations affichées :**
- Auteur et annonce
- Aperçu du message
- Date de création

---

## 🔍 Fonctionnalités Avancées

### Recherche et Filtres
- **Recherche textuelle** : Dans tous les champs pertinents
- **Filtres par date** : Pour les utilisateurs et activités
- **Filtres par statut** : Actif/inactif, staff/non-staff
- **Filtres par relation** : Par catégorie, propriétaire, etc.

### Interface Utilisateur
- **Design moderne** : Interface personnalisée aux couleurs du site
- **Responsive** : Fonctionne sur tous les appareils
- **Navigation intuitive** : Liens rapides et breadcrumbs
- **Actions en lot** : Sélection multiple pour les suppressions

### Sécurité
- **Authentification requise** : Seuls les administrateurs peuvent accéder
- **Permissions** : Contrôle d'accès basé sur les rôles
- **Confirmations** : Demandes de confirmation pour les actions critiques

---

## 📈 Utilisation Courante

### Pour voir l'activité du site :
1. Aller sur le **Tableau de bord**
2. Consulter les **statistiques**
3. Vérifier l'**activité récente**

### Pour gérer une annonce problématique :
1. Aller dans **Auctions > Listings**
2. **Rechercher** l'annonce par titre
3. **Cliquer** pour modifier
4. Ajuster les paramètres ou **désactiver**

### Pour ajouter une nouvelle catégorie :
1. Aller dans **Auctions > Categories**
2. Cliquer **"Ajouter Category"**
3. Saisir le nom de la catégorie
4. **Enregistrer**

### Pour modérer les commentaires :
1. Aller dans **Auctions > Comments**
2. **Filtrer** ou **rechercher**
3. **Modifier** ou **supprimer** si nécessaire

---

## ⚡ Actions Rapides

| Action | Raccourci |
|--------|-----------|
| Retourner au site | Bouton "Retour au site" en haut |
| Nouvelle annonce | Tableau de bord > "Nouvelle Annonce" |
| Voir les stats | Page d'accueil admin |
| Rechercher | Utiliser la barre de recherche de chaque section |

---

## 🎨 Personnalisation

L'interface d'administration a été personnalisée avec :
- **Couleurs du site** : Bleu primaire et accents
- **Icônes Font Awesome** : Pour une meilleure visualisation
- **Statistiques temps réel** : Mise à jour automatique
- **Navigation améliorée** : Liens contextuels

---

## 🔧 Support Technique

Si vous rencontrez des problèmes :
1. Vérifiez que vous êtes connecté avec un compte `staff`
2. Assurez-vous que le serveur Django fonctionne
3. Consultez les logs du serveur en cas d'erreur
4. Contactez le développeur pour un support technique

---

**Interface d'Administration CommerceHub - Version 1.0**  
*Dernière mise à jour : Novembre 2025*