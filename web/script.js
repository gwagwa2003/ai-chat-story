$(document).ready(() => {
    const fileUploader = document.querySelector('#file-uploader');
    let mediaRecorder;
    let audioChunks = [];
    

    $('.uploadButton').click(() => {
        fileUploader.click();
    });

    //上傳檔案
    fileUploader.addEventListener('change', (e) => {
        console.log(e.target.files[0]);
        const reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);

        reader.onloadend = () => {
            let json = {};
            json.type = "pic";
            json.msg = reader.result;

            let myStatement = document.createElement("div");
            let content = document.createElement("img");
            myStatement.className = "myMessage";
            content.src = reader.result;
            content.className = "res_img";
            myStatement.appendChild(content)
            $(".botResponseArea").prepend(myStatement)
            ws.send(JSON.stringify(json));
        };
    });

    //錄音檔
    $(".recordButton").click(async () => {

        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();

        } else {
            if (!mediaRecorder) {
                const stream = await navigator.mediaDevices.getUserMedia({audio: true});
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audio = document.createElement("audio");
                    const audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audio.src = audioUrl;
                    audio.controls = true;
                    audioChunks = [];

                    const reader = new FileReader();
                    reader.onloadend = () => {
                        const base64data = reader.result;
                        let json = {};
                        json.type = "audio";
                        json.msg = base64data;
                        ws.send(JSON.stringify(json));
                    };
                    reader.readAsDataURL(audioBlob);

                    let myStatement = document.createElement("div");
                    myStatement.className = "myMessage";
                    myStatement.appendChild(audio);
                    $(".botResponseArea").prepend(myStatement);

                };
            }
            mediaRecorder.start();

        }
    });

    $(".musiclist").hide();

    $(".submitButton").click(() => {
        sendMsg();
    })

    $('.userText').on('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMsg();
        }
    });

    $(".navbar-brand").click(() => {
        $(".musiclist").hide()
    })

    $(".btn-close").click(() => {
        $(".musiclist").hide()
    })

    $(".popoutlist").click(() => {
        $(".musiclist").show()
    })

    const audios = document.querySelectorAll('.music');

    audios.forEach(audio => {
        audio.addEventListener('play', () => {
            audios.forEach(a => {
                if (a !== audio) {
                    a.pause();
                }
            });
        });
    });

    addEventListener("click", (e) => {
        if (!e.target.id !== "") {
            let id = e.target.id
            console.log(e.target.id)
            new Audio('../Output/' + id + '.wav').play()
        }
    });
})

function sendMsg() {
    let statement = $(".userText").val()
    if (!CheckEmpty(statement)) {
        let myStatement = '<div class="myMessage"><p class="modifyChat">' + statement + '</p></div>'
        $(".botResponseArea").prepend(myStatement)
        $(".userText").val("")
        json = {}
        json.type = "content"
        json.msg = statement
        ws.send(JSON.stringify(json))
    }
    $(".userText").val("");

}

function changePersonality(data) {
    json = {}
    json.type = "mode"
    json.msg = data
    ws.send(JSON.stringify(json))
}

function CheckEmpty(code) {
    let ans = /^\s*$/.test(code)
    return ans
}

function showEmoji(id) {
    Class = ".EL" + id
    $(Class).toggle()
}

let audioElement = null;
let isGloballyPaused = false;

function sendEmoji(msg) {
    json = {}
    json.type = "content"
    $("body").removeClass("bk");
    
    if (audioElement) {
        audioElement.pause();
    }
    
    switch (msg) {
        case 0: //happy
            json.msg = "我對你的回覆感到開心"
            $("body").css("background-image", "url('source/img/background/BK.png')");
            audioElement = new Audio("source/music/Waterfall.mp3");
            break;
        case 1: //angry
            json.msg = "我對你的回覆感到生氣"
            $("body").css("background-image", "url('source/img/background/classroomdark.png')");
            audioElement = new Audio("source/music/Mysterious_Sorrows.mp3");
            break;
        case 2: //surprise
            json.msg = "我對你的回覆感到驚訝"
            $("body").css("background-image", "url('source/img/background/classroomlight.png')");
            audioElement = new Audio("source/music/Angels_Dream.mp3");
            break;
    }
    $("body").css("background-size", "cover");
    $("body").css("background-attachment", "fixed");
    ws.send(JSON.stringify(json))
    if (!isGloballyPaused) {
        audioElement.play();
    }
    updateGlobalPlayPauseButton();
    //ws.send(JSON.stringify(json))
}

document.addEventListener('DOMContentLoaded', function() {
    const globalPlayPauseButton = document.getElementById('globalPlayPauseButton');

    function toggleGlobalPlayPause() {
        if (audioElement) {
            if (audioElement.paused) {
                audioElement.play();
                isGloballyPaused = false;
            } else {
                audioElement.pause();
                isGloballyPaused = true;
            }
        } else {
            // 如果沒有正在播放的音樂，嘗試播放音樂列表中的第一首
            const firstAudio = document.querySelector('.music');
            if (firstAudio) {
                audioElement = firstAudio;
                audioElement.play();
                isGloballyPaused = false;
            }
        }
        updateGlobalPlayPauseButton();
    }

    function updateGlobalPlayPauseButton() {
        if (audioElement && !audioElement.paused) {
            globalPlayPauseButton.textContent = '暫停';
        } else {
            globalPlayPauseButton.textContent = '播放';
        }
    }

    globalPlayPauseButton.addEventListener('click', toggleGlobalPlayPause);

    // 當音樂列表中的任何音樂開始播放時更新按鈕狀態
    document.querySelectorAll('.music').forEach(audio => {
        audio.addEventListener('play', function() {
            audioElement = this;
            isGloballyPaused = false;
            updateGlobalPlayPauseButton();
        });

        audio.addEventListener('pause', function() {
            if (this === audioElement) {
                updateGlobalPlayPauseButton();
            }
        });
    });
});