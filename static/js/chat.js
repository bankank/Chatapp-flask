$(document).ready(function () {
        
var socket = io.connect('http://127.0.0.1:5000');

function removeTags(str) {   
    if ((str===null) || (str===''))
    return false;
    else
    str = str.toString();
return str.replace( /(<([^>]+)>)/ig, ''); 
}


socket.on('user-connected-message', function(data) {  //@socketio.on('connect')

    $("#display-message").append(' <div class="join-display"> <div class="joined-chat-message">' + data.message + '</div> <div class="joinedat">' + data.joinedat + '</div> </div>')
    // document.getElementById('display-message').innerHTML = JSON.stringify(data); //  JSON FORMAT
    });

socket.on('message-user-sent', function(message) { //@socketio.on('message')

    $("#display-message" ).append(`<div class="message-display">  <div class="nickname-display">` 
                                + removeTags( message.messageuser) + `<span class="datetime">`
                                + message.date_time_message        + `</span> </div> <div class="msg-display">` 
                                + removeTags(message.messagevalue) + `</div> </div>`)
    // document.getElementById('display-message').innerHTML = JSON.stringify(message);  //  JSON FORMAT
    });

    $('#send-btn').on('click', function() {
             

        var msg_input = document.getElementById("input-message");
      
        if (msg_input &&msg_input.value) {
        
    socket.send($('#input-message').val());
    $('#input-message').val('');
        } else {
            return ;
        }
    });

});


document.addEventListener("DOMContentLoaded", function () {
// window.setInterval(function() {
//     var scroll = document.getElementById('display-message')
//     scroll.scrollTop = scroll.scrollHeight ;
    
//     }, 10000);


var inputmessage = document.getElementById("input-message");
    inputmessage.addEventListener("keypress", function (event) {
          if (event.key === "Enter") {
            var msg_input = document.getElementById("input-message");
            if (msg_input &&msg_input.value) {
              document.getElementById("send-btn").click();
              var scroll = document.getElementById('display-message')
              scroll.scrollTop = scroll.scrollHeight ;

            } else {
             return ;
            }
          }
    });


});
