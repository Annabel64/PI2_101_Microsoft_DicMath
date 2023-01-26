# PI2_101_Microsoft_DicMath : DicMath - Dictée vocale d'équations Mathématiques 
If you need additional information, do not hesitate to contact me by email annbl.mrcn@gmail.com (Annabel)!

_________ English version bellow _________

Note : to create a new python environment allowing the execution of the code, execute the following command in the command prompt : 
"conda create -n <Dicmath_Microsoft> --file environment.txt". The environment.txt file is given in the github repository.


[![Watch the video](https://github.com/Annabel64/PI2_101_Microsoft_DicMath/blob/main/Documents/video%20image.png)](https://github.com/Annabel64/PI2_101_Microsoft_DicMath/blob/main/Documents/DicMath%20-%20Pitch%20Video.mp4)



## Résumé Français

### Description du projet

Notre projet vise à développer un logiciel alimenté par l'IA pour aider les lycéens malvoyants à résoudre des équations mathématiques en utilisant leur voix. L'objectif est de permettre aux étudiants de dicter des équations, de recevoir un retour vocal de l’équation comprise par le logiciel et de naviguer pour les modifier. Les principaux utilisateurs seront des étudiants aveugles jusqu'au niveau bac et mais le logiciel permet également de fournir que des opérateurs mathématiques avancés (intégrales, etc.).

Pour atteindre cet objectif, nous avons utilisé plusieurs technologies et méthodes de travail. Tout d'abord, nous avons utilisé Whisper, un outil récent de Speech-To-Text de OpenAI pour transcrire la voix de l'utilisateur en équations mathématiques texte. Nous avons ensuite développé une fonction de traduction texte-Latex, qui est le format le plus adapté pour gérer des équations mathématiques. Enfin, nous avons utilisé des services cognitifs Microsoft Azure pour implémenter un bot Text-To-Speech pour relire les équations à l'utilisateur.

En ce qui concerne l'interface utilisateur, nous avons développé une interface graphique, basée sur Python, qui permet à l'utilisateur de dicter une équation mathématique via le microphone et affiche l’équation transcrite, en utilisant des technologies HTML, CSS et JS. L’interface est travaillée pour être simple et accessible : l’élève peut interagir avec l’interface avec la voix, grâce à des commandes vocales, ou grâce au clavier, l’utilisation de la souris étant impossible pour eux.

Pour assurer la qualité du logiciel, nous avons mis en place une méthode de travail en équipe, où chaque membre a été assigné à des tâches spécifiques. Certains membres ont travaillé sur l'interface graphique et d'autres encore sur l'intégration des services d'IA. Nous avons également effectué des tests utilisateur réguliers pour vérifier la facilité d'utilisation et la pertinence des fonctionnalités. Enfin, une fois que tous les modules ont été développés, nous les avons fusionnés en un seul projet pour créer une expérience utilisateur fluide. En plus d’être un défi technique car aucune technologie actuelle permet de faire ce que nous avons réalisé, cette expérience nous a permis d’aborder la notion d’accessibilité. Nous sommes extrêmement reconnaissants envers Microsoft de nous avoir offert cette opportunité.


### Pistes d'améliorations et travail qu'il reste à faire
Tout le module d'IA, de reconnaissance et retour vocal, sont 100% opérationnels. Cependant, il reste du travail, notamment sur l'interface et tout le module de navigation. Voici les pistes de travail que nous proposons :

#### L'interface
- améliorer l'interface : la rendre plus accessible pour les malvoyants (couleurs, emplacement des boutons...)
- continuer le travail sur les commandes clavier pour pouvoir actionner TOUS les boutons de l'interface
- ajouter des commandes vocale pour activer les boutons de l'interface par la voix
- travailler l'affichage des équations (pour le moment, on affiche des images dont les dimentions sont fixes, il faudrait que la taille de l'image soit modulée par la longueur de l'équation pour ne pas la couper)
#### Les paramètres
- permettre le changement de langue
- permettre le choix de la voix (sexe, rapidité de lecture...). Ces paramètres sont possibles avec le module Microsoft Azure que nous avons utilisé, il s'agit juste de relier les paramètres de l'interface et les variables dans la fonction Microsoft Azure.
#### La navigation et les modifications
- permettre de modifier une équation ou un élément de l'équation (qui est dans l'historique ou dans l'équation en court)
Nous avons commencé un travail sur la navigation en fonctionnant sur des blocs séparés par les opérateurs +,-,*,/,(,), mais notre travail n'a pas été intégré à l'interface, n'hésitez pas à nous contacter pour plus de détail.
#### Test et tuto
- développer un tuto d'utilisation (accessible aux malvoyanrs), détaillant les commandes et fonctionnalités de l'interface.
- aller voir des élèves lycées de l'INJA (Institut National des Jeunes Aveugles à Paris) et tester le logiciel
- tester également le logiciel sur des malvoyants (personnes dont la vision est réduite)




## English Abstract

### Project description

Our project aims to develop AI-powered software to help visually impaired high school students solve math equations using their voice. The goal is to allow students to dictate equations, receive voice feedback of the equation understood by the software, and navigate to edit them. The main users will be blind students up to baccalaureate level, but the software also makes it possible to provide only advanced mathematical operators (integrals, etc.).

To achieve this goal, we used several technologies and working methods. First, we used Whisper, a recent Speech-To-Text tool from OpenAI to transcribe the user's voice into text math equations. We then developed a text-Latex translation function, which is the most suitable format for managing mathematical equations. Finally, we used Microsoft Azure Cognitive Services to implement a Text-To-Speech bot to read the equations back to the user.

Regarding the user interface, we have developed a graphical interface, based on Python, which allows the user to dictate a mathematical equation via the microphone and displays the transcribed equation, using HTML, CSS and JS technologies. . The interface is worked to be simple and accessible: the student can interact with the interface with the voice, thanks to voice commands, or thanks to the keyboard, the use of the mouse being impossible for them.

To ensure the quality of the software, we have implemented a teamwork method, where each member has been assigned to specific tasks. Some members worked on the GUI and still others on the integration of AI services. We also performed regular user testing to check the usability and relevance of features. Finally, once all the modules were developed, we merged them into a single project to create a smooth user experience. In addition to being a technical challenge because no current technology allows us to do what we have achieved, this experience allowed us to approach the notion of accessibility. We are extremely grateful to Microsoft for giving us this opportunity.

### Areas for improvement and work that remains to be done
All the AI module, recognition and voice feedback, are 100% operational. However, there is still work to be done, especially on the interface and the entire navigation module. Here are the lines of work we offer:

#### Interface
- improve the interface: make it more accessible for the visually impaired (colors, location of buttons, etc.)
- continue working on the keyboard commands to be able to operate ALL the buttons of the interface
- add voice commands to activate interface buttons by voice
- work on the display of equations (for the moment, we display images whose dimensions are fixed, the size of the image should be modulated by the length of the equation so as not to cut it)
#### The settings
- allow language change
- allow the choice of the voice (sex, speed of reading...). These parameters are possible with the Microsoft Azure module that we used, it is just a matter of linking the interface parameters and the variables in the Microsoft Azure function.
#### Navigation and modifications
- allow to modify an equation or an element of the equation (which is in the history or in the current equation)
We have started a work on the navigation by working on blocks separated by the operators +,-,*,/,(,), but our work has not been integrated into the interface, do not hesitate to contact us for more detail.
#### Test
- develop a user tutorial (accessible to the visually impaired), detailing the commands and features of the interface.
- go see high school students from INJA (National Institute for Young Blind People in Paris) and test the software
- also test the software on visually impaired people (people with reduced vision)
