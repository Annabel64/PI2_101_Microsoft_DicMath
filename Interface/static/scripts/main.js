// On attend que le DOM soit chargé avant de lancer les fonctions
$(document).ready(function () {
    // Lancer les fonctions qui gèrent les modaux
    settings_modal();
    help_modal();
    recFunction();

    // Lorsque l'utilisateur appuie sur Echap, fermer le modal
    $(document).keydown(function (event) {
        if (event.keyCode == 76) {
            document.getElementById("read_button").click()
        }
    });
});

function start_recording() {
    navigator.mediaDevices.getUserMedia({ video: false, audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            // Arrêter l'enregistrement audio au bout de 5 secondes
            setTimeout(() => {
                mediaRecorder.stop();
            }, 6000);
            mediaRecorder.addEventListener("stop", () => {
                // Créer un fichier audio à partir des données enregistrées
                const blob = new Blob(audioChunks, {
                    type: 'audio/wav'
                });
                // Envoyer ce fichier au serveur
                const formData = new FormData();
                formData.append('audio-file', blob);
                return fetch('', {
                    method: 'POST',
                    body: formData
                });
            });
        });
}

// Fonction qui gère l'affichage et la fermeture du modal des paramètres
function settings_modal() {
    // Récupérer le modal et le bouton qui l'ouvre
    const modal = document.getElementById("settings-modal");
    const btn = document.getElementById("settings-button");

    // Lorsque l'utilisateur clique sur le bouton, afficher le modal
    btn.onclick = function () {
        modal.style.display = "block";
        document.getElementById("language-picker-select").focus()
    }

    // Lorsque l'utilisateur clique en dehors du modal, le fermer
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }

    // When the user clicks ESC, close it
    $(document).keydown(function (event) {
        if (event.keyCode == 27) {
            modal.style.display = "none";
        }
    });

    // Lorsque l'utilisateur appuie sur P, ouvrir le modal des paramètres
    $(document).keydown(function (event) {
        if (event.keyCode === 80) {
            btn.click()
        }
    });
}

// Fonction qui gère l'affichage et la fermeture du modal d'aide
function help_modal() {
    // Récupérer le modal et le bouton qui l'ouvre
    const modal = document.getElementById("help-modal");
    const btn = document.getElementById("help-button");

    // Lorsque l'utilisateur clique sur le bouton, afficher le modal
    btn.onclick = function () {
        modal.style.display = "block";
        document.getElementById("language-picker-select").focus()
    }

    // Lorsque l'utilisateur clique en dehors du modal, le fermer
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }

    // Lorsque l'utilisateur appuie sur H, ouvrir le modal d'aide
    $(document).keydown(function (event) {
        if (event.keyCode === 72) {
            btn.click()
        }
    });

    // When the user clicks ESC, close it
    $(document).keydown(function (event) {
        if (event.keyCode == 27) {
            modal.style.display = "none";
        }
    });
}


function recFunction() {
  // Créer un objet qui gère l'enregistrement audio
  var audioRecorder = {
    /** Démarrer l'enregistrement audio
      * @returns {Promise} - retourne une promesse qui se résout si l'enregistrement audio a démarré avec succès
      */
    start: function () {
      return navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioRecorder.streamBeingCaptured = stream;
            audioRecorder.recorder = new MediaRecorder(stream);
            audioRecorder.audioBlobs = [];

            audioRecorder.mediaRecorder.addEventListener("dataavailable", event => {
            audioRecorder.audioBlobs.push(event.data);
            });
        audioRecorder.recorder.start();
        });
    },
    /** Arrêter l'enregistrement audio
      * @returns {Promise} - retourne une promesse qui se résout avec les données audio enregistrées
      */
    stop: function () {
        audioRecorder.mediaRecorder.addEventListener("stop", () => {
            const blob = new Blob(audioChunks, {
                type: 'audio/wav'
            });
            const formData = new FormData();
            formData.append('audio-file', blob);
            return fetch('', {
                method: 'POST',
                body: formData
            });
        });
    }
  };

  // Lorsque l'utilisateur appuie sur L, démarrer ou arrêter l'enregistrement audio
    $(document).keydown(function (event) {
        if (event.keyCode === 32) {
            rec_button = $('#start-btn')

            if (rec_button.hasClass('Rec')) {
                rec_button.removeClass("Rec");
                rec_button.html("Lancer la dictée")
            }
            else {
                rec_button.addClass("Rec");
                rec_button.html("À l'écoute")
                start_recording()
            }
        }
    });
}