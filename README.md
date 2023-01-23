# PI2_101_Microsoft_DicMath : DicMath - Dictée vocale d'équations Mathématiques 
If you need additional information, do not hesitate to contact me by email annbl.mrcn@gmail.com (Annabel)!

_________ English version bellow _________

Note : to create a new python environment allowing the execution of the code, execute the following command in the command prompt : 
"conda create -n <Dicmath_Microsoft> --file environment.txt". The environment.txt file is given in the github repository.


[![Watch the video](https://github.com/Annabel64/PI2_101_Microsoft_DicMath/blob/main/Documents/video%20image.png)](https://github.com/Annabel64/PI2_101_Microsoft_DicMath/blob/main/Documents/DicMath%20-%20Pitch%20Video.mp4)



## 1- Objectif du projet (attendu final)

L'objectif de notre projet est de concevoir un logiciel permettant à des jeunes aveugles de dicter des équations mathématiques et de recevoir des retours vocaux pour pouvoir résoudre l’équation. Ce logiciel fonctionnera sur ordinateur. Toutes les commandes peuvent être exécutées par saisie au clavierou vocalement, ce qui évite l'utilisation de lasouris.Les principaux utilisateurs du logiciel seront des jeunes aveugles (niveau bacmax). Le logiciel ne fournira donc que les opérations mathématiques de base, notamment l'addition, la soustraction, la multiplication et la division, la puissance et les fonctions.Notre logiciel met en œuvre à la fois l'entrée et la sortie des équations : l'utilisateur dicte l'équation et le logiciel retourne vocalement l'équation comprise.Compte tenu de l'incertitude de l'équation d'entrée, le logiciel émet un signal sonore lorsque l'équation est terminée, répétant éventuellement l'équation et émettant respectivement donne un signal sonore différent lorsqu'une erreur est reportée.La fonction de navigation permet à l'utilisateur de localiser et de modifier l'équation existante. Compte tenu des ressources disponibles en bibliothèque, nous mettons en œuvre la dictée dans un maximum de langues possibles, l'anglais et le français compris.



## 2- Décomposition en tâches et sous tâches

On peut séparer ce projet en deux parties importantes qui servirons dans la répartition des taches:

### 2.1- UNE PARTIE FRONTEND,ELLE-MEME SEPAREE EN PLUSIEURS SOUS-TACHE :

•La création d’une maquette visuelle qui vise à être le plus ergonomique possible pour des étudiants aveugles.

•La mise en place de l’interface via cette maquette qui puisse intégrer et utiliser le code du backend.

### 2.2- UNE PARTIE EN BACKEND,QUI REGROUPE ELLE-MEME PLUSIEURS SOUS-PARTIES :

•La mise en place de la structure de donnée pour le stockage des équations•La création/amélioration d’un module d’Intelligence Artificielle de speech-to-text qui est suffisamment certain pour permettre à un malvoyant d’utiliser le logiciel en toute confiance

•La mise en place du mode de navigation à travers les équations avec diverses assistances (Raccourcis, retours vocaux...).

•Traduction multilingue de l’application

### 2.3- LE RASSEMBLEMENT DE CES DEUX PARTIES POUR AVOIR UNE APPLICATION FONCTIONNELLE ET COMPLETE

### 2.4- LA REDACTION D’UN MODE D’EMPLOI POUR LES POTENTIELS UTILISATEURS,OU PERSONNES QUI SOUHAITENT REPRENDRE LE SUJET.



## 3- Risk Management
Ce projet est un projet assez complet qui retrace de A à Z les étapes requises pour faire une application. Il est donc possible de retrouver des points de difficultés qui peuvent ralentir l’avancée du projet. Afin de les détecter, prenons les différentes features dans l’ordre antéchronologiques de leur implémentation et voyons comment palier à leur manque en cas de problème rencontré.

### 3.1 La navigation 

Si certaines bibliothèques permettent une meilleure compréhension de certains domaines, il n’y aucune garantie de pouvoir détecter avec exactitude les différents mots requis pour une navigation confortable. Il faudra alors revoir le fonctionnement de l’interface pour établir plus de raccourcis clavier, afin de garder l’application utilisable par la majorité des malvoyants.

### 3.2 La traduction et représentation fidèle en LateX

Nous utilisons aujourd’hui des bibliothèques qui utilisent du Speech-to-Text afin de nous faciliter la tâche lorsque nous voulons générer des Mathématiques en LateX. Malheureusement, ces librairies sont presque exclusivement en Anglais, ce qui rajoute une difficulté quant à la traduction directe de la voix d’un étudiant en texte anglais pour l’utiliser comme entrée, tout en gardant la signification mathématique exacte de ce qu’il a voulu exprimer. Dans le cas où nous ne trouvons pas de solution, il faudra revoir le reste de l’application pour que celle-ci fonctionne en Anglais, et rajouter les supports dans d’autres langues comme des features annexes lorsque le projet sera déjà dans sa phase finale.

### 3.3 Le stockage des données pour la navigation

S’il est possible d’enregistrer et d’afficher des équations assez fidèlement à l’entrée vocale, il est plus compliqué de savoir comment facilement y accéder une fois l’enregistrement fait. L’idée est donc de simplifier le problème au maximum en utilisant une séparation « en bloc » de chaque équation, elle-même placée dans une structure de donnée qui est compatible avec les notions d’équations ‘précédentes et suivantes’. Si au final, il s’avère que ces solutions sont trop compliquées à implémenter, il faudra se reposer sur de la manipulation de liste et d’index.

### 3.4  Facilitation du vocabulaire à employer

Enfin, en tant qu’étudiants sans handicap, nous n’avons que l’expérience de logiciels comme Siri et Cortana pour donner des commandes vocales efficaces, mais nous n’avons en aucun cas une vision sur le fonctionnement de la résolution d’équations mathématiques pour les étudiants malvoyants, il est alors compliqué de se mettre dans leur peau et de comprendre leur besoin sans référence. Pour pallier à ce problème, nous avons planifié un rendez-vous avec l’INJA (institut national des jeunes aveugles) pour mieux comprendre leur besoin, et savoir précisément quelles commandes vocales figureront en priorité dans notre application.



# English version

## 1- Project objective (final expectation)

The objective of our project is to design a software that will allow blind youth to dictate mathematical equations and receive voice feedback to solve the equation. All commands can be executed by keyboarding or by voice, thus avoiding the use of the mouse. The main users of the software will be young blind people (bacmax level). Our software implements both input and output of equations: the user dictates the equation and the software returns the understood equation by voice. Given the uncertainty of the input equation, the software beeps when the equation is completed, possibly repeating the equation and respectively beeps differently when an error is reported.The navigation function allows the user to locate and modify the existing equation. The navigation function allows the user to locate and modify the existing equation. Given the resources available in the library, we implement dictation in as many languages as possible, including English and French.


## 2- Breakdown into tasks and subtasks

We can separate this project into two important parts which will be used in the distribution of tasks:

### 2.1 A FRONTEND PART, WHICH IS ITSELF SEPARATED INTO SEVERAL SUBTASKS:

-The creation of a visual model that aims to be as ergonomic as possible for blind students.

-The implementation of the interface via this model which can integrate and use the code of the backend.

### 2.2 A BACKEND PART, WHICH ITSELF INCLUDES SEVERAL SUB-PARTS:

-The implementation of the data structure for the storage of equations - The creation/improvement of an Artificial Intelligence speech-to-text module that is sufficiently certain to allow a visually impaired person to use the software with confidence

-The implementation of a navigation mode through the equations with various assistances (shortcuts, voice feedback...).

-Multilingual translation of the application

### 2.3 THE GATHERING OF THESE TWO PARTS TO HAVE A FUNCTIONAL AND COMPLETE APPLICATION

### 2.4 WRITING AN INSTRUCTION MANUAL FOR POTENTIAL USERS, OR PEOPLE WHO WANT TO TAKE UP THE SUBJECT.



## 3- Risk Management

This project is a fairly complete project that retraces from A to Z the steps required to make an application. It is therefore possible to find points of difficulty that can slow down the progress of the project. In order to detect them, let's take the different features in the antechronological order of their implementation and see how to make up for their lack in case of a problem.

### 3.1 Navigation 

If some libraries allow a better understanding of certain domains, there is no guarantee to be able to detect exactly the different words required for a comfortable navigation. It will then be necessary to review the interface to establish more keyboard shortcuts, in order to keep the application usable by the majority of visually impaired people.

### 3.2 Translation and faithful representation in LateX

Today we use Speech-to-Text libraries to make it easier for us to generate mathematics in LateX. Unfortunately, these libraries are almost exclusively in English, which adds a difficulty in translating a student's voice directly into English text to use as input, while keeping the exact mathematical meaning of what he wanted to express. In case we do not find a solution, we will have to redesign the rest of the application so that it works in English, and add support for other languages as additional features when the project is already in its final phase.

### 3.3 Data storage for navigation

While it is possible to record and display equations fairly accurately to voice input, it is more complicated to know how to easily access them once the recording is done. The idea is therefore to simplify the problem as much as possible by using a "block" separation of each equation, itself placed in a data structure that is compatible with the notions of 'previous and next' equations. If, in the end, it turns out that these solutions are too complicated to implement, it will be necessary to rely on list and index manipulation

### 3.4 Facilitating the vocabulary to be used

Finally, as able-bodied students, we only have experience with software such as Siri and Cortana to give effective voice commands, but we have no insight into how solving mathematical equations works for visually impaired students, so it is complicated to put ourselves in their shoes and understand their needs without reference. To overcome this problem, we have scheduled a meeting with the INJA (National Institute for the Blind) to better understand their needs, and to know precisely which voice commands will be the priority in our application.
