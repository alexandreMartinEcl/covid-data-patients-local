## Version 1 todo List

### Requêtes globales

- [x] Prévoir des items standards (ex.: Poids en db) (lié à la classification SNOMED). Idem pour certaines catégories (ex: antécédents avec classification LOINC)
- [x] Les cas de gravités sont _à risque_, _instable_, ou _rien_
- [x] Formulaire de base (ajout patient à un lit) doit comprendre: _nom_, _prenom_, _date de naissance_, _sexe_, _poids_, _taille_ (prévoir affichage du IMC), et surtout l'_identifiant NIP_
- [x] Dans l'affichage _Patient_, doivent figurer dans l'ordre: catégories _antécédents_, catégories _allergies_, un historique _histoire de la maladie récente_ (extensible), un historique _evolution_ (extensible), la section _Infos du jour_ avec notamment un tableau _Etat/Jour_, une Todo list (extensible/pop-up)
- [x] Les catégories _antécédents/allergies_ doivent d'abord vérifier le critère de connaissance avant affichage (autres valeurs possibles: _inconnu_, _aucun_)
- [ ] A la première connexion d'un médecin: demander et mettre à jour son rôle (aka _Médical_, _Infirmier_, _Aide soignant_, _Kiné_)
- [x] Un membre du personnel soignant peut ajouter une unité de réanimation par un code

Mise à jour 15 Avril:

- [x] Infos de base patient (démographiques): Sortir la variable sévérité et ajouter date d'hospitalisation, motif d'hospitalisation (ex: "Détresse respiratoire aigu sur Covid")
- [x] Mise en forme page Patient: Remonter dépistage et infos démographique au meme niveau et totalité écran pour antécédents/allergies, TODOList en haut a droite
- [x] Ajout de deux lignes de mesures:
  - EER: ["Hémofiltration", "Dialyse", "Hémodiafiltration"]
  - Lactatémie: chiffre (mmol/L) (après Creat/EER, avant Antibio)
  - DV: boolean ave date de début, date de fin (affich nb d'heures)
  - NAD: (mg/h)
  - Créat: (umol/l)
- [x] Page _Patient_ : ajout de la section "Photo du jour" comprenant le _Tableau de mesures_, un texte type _EditableText_ "Notes du jour" et une _CheckList_ "Défaillances", comprenant: [Foie, Rein, Cerveau, Poumon, Coeur, Biochimie] (avec Icones)
- [x] Proposer directement la modification de _Défaillances_ suivant des critères sur les ajouts de _Mesures_ du jour-même
  - EER -> Rein
  - Lactatémie > 2.0 -> défaillance biochimie = métabolique
  - P/F < 200 OU nad > 0.5 -> poumon
- [x] Affichage simplifié pour le mode garde
- [x] Page _Lits_ : afficher récap nbPatientsInstables et nbLitsDispo
- [x] Page _Lits_: enlever "depuis le", ajouter icones des défaillances, ajouter motif d'hospitalisation
- [x] _Tableau des mesures_: simplifier la modif
- [ ] Bonus: Voir la doc FHIR (pour "certifier" l'app, et donc rassurer): www.hl7.org/fhir/resourcelist.html ou patient.html

### Frontend

- [x] Set-up de base
- [x] Ajout de la page d'affichage _Beds_
- [x] Ajout de la page d'affichage _Patient_ avec infoPerso, dépistages, comorbidités, étatsPrécédents, todoList sommaire
- [x] Ajout de la modification de tout champ de la page _Patient_ (dont ajout de comorbidité)
- [x] Ajout de la modification des infos persos de la page _Patient_
- [x] Ajout de la création d'un patient sur un lit dans la page unités, avec formulaire pour les _Infos persos_ puis ouverture de page _Patient_
- [x] Ajout du retrait d'un patient d'un lit
- [ ] ~Obtenir l'username pour la requete de modification (pour modifier métier et ajouter une unité de réanimation)~ (La requête se fait différemment, getRea)

### Backend

- [x] Ajout de l'AppBar global (affichage personne connectée, options Connexion)
- [x] Ajout la page d'authentification (avec option Déconnexion dans l'AppBar)
- [x] Définition des modèles de données
- [x] Gestion de l'authentification
- [x] Permettre: création d'un UserProfile après connexion+authentification via le serveur ap-hp, obtenir les infos sur les lits dont le User est à charge, ajout d'un patient à un lit, retrait du patient, obtenir les infos sur un patient, modifier les infos du patient, obtention/ajout des mesures de l'état du patient

## Version 2 todo List (dont suggestions)

### Requêtes globales

- [ ] Possibilité d'assigner un médecin à des patients et des unités (dans l'app)

Mise à jour 15 Avril:

- [ ] v2: Structurer _Histoire maladie récente_ et _Evolution_ : date (avec affichage de _Jxx_ ou _J-xx_) et texte
- [ ] v2: Rendre le tableau modulaire
- [x] V2: _Tableau des mesures_: pouvoir modifier sans Pop-up

### Frontend

- [ ] Ajout du mode Drag'n'drop sur la page _Patient_
- [ ] Todo List de la page _Patient_ plus rigoureuse
- [ ] Ajout d'un patient existant
- [ ] Empêcher les reset_form quand le submit d'un form ne fonctionne pas (pb: envoi de requete-> change state -> fait rerender -> réinitialise le form si on a pas formData mis à jour)
- [ ] Ajout de la page paramètres accessible via l'AppBar
- [ ] Permettre l'ajout sur un lit d'un patient précédemment sorti
- [ ] Page _Patient_ obtensible d'une autre façon que par la page _Unité_ (retrouver les informations après une sortie)

### Backend

- [ ] Ajout d'un patient existant
- [ ] Ajout de la table _Historique des actions_
- [ ] Permettre la sauvegarde d'un état de la base
- [ ] Permettre l'envoi de l'état actuel (possiblement util pour une app de gestion inter-hopital) / Ou permettre d'indiquer un lit comme disponible pour les acteurs extérieurs

## Version 3 todo List

### Requêtes globales

- [ ] Concernant les tâches (Todo list liée à un patient): Ajout de la page Tâches à réaliser, avec vue par type de profil (aka _Aide soignant_, _Kiné_, etc.), par soignant (uniquement tâches attribuées au soignant), par unité

Détails:
"Je veux les taches de mes patients sachant que je suis infirmier"
"Je veux les taches de toutes les unitées sachant que je suis Kiné"

## Version 4 todo List

### Requêtes globales

- [ ] Ajout d'un forum de discussion générale, et discussion patient-centré

Détails:
"Je veux les taches de mes patients sachant que je suis infirmier"
"Je veux les taches de toutes les unitées sachant que je suis Kiné"
