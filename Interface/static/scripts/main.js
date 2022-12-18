$(document).ready(function () {
    settings_modal();
    help_modal();
    rec_function();

    // When the user clicks ESC, close it
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

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);
            mediaRecorder.addEventListener("stop", () => {
                //   const audioBlob = new Blob(audioChunks);
                //   const audioUrl = URL.createObjectURL(audioBlob);
                //   const audio = new Audio(audioUrl);
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

        });
}

function settings_modal() {
    // Get the modal
    var modal = document.getElementById("settings-modal");

    // Get the button that opens the modal
    var btn = document.getElementById("settings-button");

    // When the user clicks on the button, open the modal
    btn.onclick = function () {
        modal.style.display = "block";
        document.getElementById("language-picker-select").focus()
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // When the user clicks ESC, close it
    $(document).keydown(function (event) {
        if (event.keyCode == 27) {
            modal.style.display = "none";
        }
    });

    // When the user clicks S, open modal
    $(document).keydown(function (event) {
        if (event.keyCode === 80) {
            btn.click()
        }
    });
}

function help_modal() {
    // Get the modal
    var modal = document.getElementById("help-modal");

    // Get the button that opens the modal
    var btn = document.getElementById("help-button");

    // When the user clicks on the button, open the modal
    btn.onclick = function () {
        modal.style.display = "block";
        document.getElementById("language-picker-select").focus()
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // When the user clicks ESC, close it
    $(document).keydown(function (event) {
        if (event.keyCode == 27) {
            modal.style.display = "none";
        }
    });

    // When the user clicks S, open modal
    $(document).keydown(function (event) {
        if (event.keyCode === 72) {
            btn.click()
        }
    });
}

function rec_function() {
    var audioRecorder = {
        /** Start recording the audio
          * @returns {Promise} - returns a promise that resolves if audio recording successfully started
          */
        start: function () {
            return navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {

                    audioRecorder.streamBeingCaptured = stream;

                    audioRecorder.mediaRecorder = new MediaRecorder(stream);

                    audioRecorder.audioBlobs = [];

                    audioRecorder.mediaRecorder.addEventListener("dataavailable", event => {
                        audioRecorder.audioBlobs.push(event.data);
                    });

                    audioRecorder.mediaRecorder.start();
                });
        },
        /** Stop the started audio recording
          * @returns {Promise}
          */
        stop: function () {
            audioRecorder.mediaRecorder.addEventListener("stop", () => {
                //   const audioBlob = new Blob(audioChunks);
                //   const audioUrl = URL.createObjectURL(audioBlob);
                //   const audio = new Audio(audioUrl);
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
    }
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