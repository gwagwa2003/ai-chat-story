var ws = new WebSocket("ws://localhost:8888/socket")
// var ws = new WebSocket("ws://192.168.1.114:8765/socket")
const uuid=crypto.randomUUID()

let soundCounter=0

ws.onopen  = function(e)
{
   console.log("connected")
}
ws.onmessage=(e)=>
    {
        soundCounter+=1
        let myStatement='<div class="emojiList"><button class="showEmoji" onclick="showEmoji('+soundCounter+')">🔘</button><button class="emoji '+"EL"+''+soundCounter+'" onclick="sendEmoji(0)">😆</button><button class="emoji '+"EL"+''+soundCounter+'" onclick="sendEmoji(1)">😠</button><button class="emoji '+"EL"+''+soundCounter+'" onclick="sendEmoji(2)">🤯</button></div>' +
            '<div class="botMessage"><p class="modifyChat" id="'+soundCounter+'">'+e.data+'</p></div>'
        $(".botResponseArea").html(myStatement+$(".botResponseArea").html())
    
        console.log(e.data)
    }
ws.onclose=(e)=>
{
    console.log("closed")
}

