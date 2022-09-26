# Segmentez des clients d'un site e-commerce
> The notebooks are in english, the Readme in french. Yup. Not that practical

## Projet :

Vous êtes consultant pour Olist, une entreprise brésilienne qui propose une solution de vente sur les marketplaces en ligne.

Olist souhaite que vous fournissiez à ses équipes d'e-commerce une segmentation des clients qu’elles pourront utiliser au quotidien pour leurs campagnes de communication.

Votre objectif est de comprendre les différents types d’utilisateurs grâce à leur comportement et à leurs données personnelles.

Vous devrez fournir à l’équipe marketing une description actionnable de votre segmentation et de sa logique sous-jacente pour une utilisation optimale, ainsi qu’une proposition de contrat de maintenance basée sur une analyse de la stabilité des segments au cours du temps.

- [Description entière ici](https://openclassrooms.com/fr/paths/164/projects/630/assignment)
- Données : [https://www.kaggle.com/olistbr/brazilian-ecommerce](https://www.kaggle.com/olistbr/brazilian-ecommerce)

## Notebooks :

> - Les notebooks ont et tout le reste du projet a majoritairement été effectué sur Visual Studio, ainsi, des librairies telles que Plotly doivent être configurées en conséquence si le notebook est à examiner via d'autres IDEs/éditeurs (cellule 1, ligne `pio.renderers.default = "notebook_connected"`)...
> - PEP8 contrôlée par Flake8, cf. requirements.txt (`pip install -r requirements.txt`, ou équivalent conda)
> - Le projet utilise python-dotenv pour permettre le réglage de variables d'environnements locales et spécifiques à la machine utilisée - ici un fichier .env non versionne précise le nombre de cœurs et le DPI du moniteur. Ne pas avoir cette dépendance ne nuit pas à l'exécution des programmes mais présuppose par exemple les DPI du moniteurs a 100 DPI.
> - Le projet utilise a plusieurs instance le module de la stdlib concurrent.futures pour effectuer des taches utilisant du multiprocessing. Une alternative au MP est proposée dans les scripts si cette approche ne convient pas pour des raisons matérielles.


Les notebooks ont un ordre d'exécution détaillé dans le fichier nb_exe_order.txt -->
- Le premier (Rekey) se focalise sur un allègement considérable du dataset et du passage de clés primaires et étrangères des dumps SQL de Hexadécimal a uint32 (on note un gain de 28% en taille, aucun test n'a été fait pour estimer le temps de traitement gagné mais les avantages de travailler avec un dtype numpy comparé à une chaine de chars est généralement très grande. Néanmoins, ce notebook s'exécute en 2693.51s). A noter que pour que le dtype d'une variable soit préservée, il faut utiliser le format Pickle et non CSV (si CSV, il suffit de re enforce les bons dtypes)
- Le deuxième notebook, rfm_approach represente une rapide analyse exploratoire et un des premières propositions de clustering se basant sur RecencyFrequencyMonetary. Une première conclusion est rendue avant un export pour une potentielle amélioration des modèles.
- Le troisième notebook se concentre sur la géolocalisation en prévision du notebook suivant et permet d’associer correctement les clients et les vendeurs a une lat/lon, évitant de recharger et re associer ces valeurs lors de l'exécution du notebook suivant
- Le quatrième notebook etend les theories emises suite à l'analyse RFM en utilisant potentiellement le DeltaT(order->delivery), DeltaDist(Buyer-->Seller) et les notes et commentaires utilisateurs. L'idée est d'arriver à un modèle final, possiblement suivant les conclusions déjà proposées dans `rfm_approach`, ainsi que les données pouvant satisfaire cette citation du cahier des charges :
>*Vous devrez fournir à l’équipe marketing une description actionnable de votre segmentation et de sa logique sous-jacente pour une utilisation optimale, ainsi qu’une proposition de contrat de maintenance basée sur une analyse de la stabilité des segments au cours du temps.*
