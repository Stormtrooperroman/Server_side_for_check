$("#test_button").click(function (e) { 
    e.preventDefault();

    var formData = new FormData();
    for(var i = 0; i<$('#filein')[0].files.length; i++){
        formData.append('file', $('#filein')[0].files[i])
    }
    
    $.ajax({
        type: "POST",
        url: "api/load/",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $("#content").html("")
            myModal.show()
            
        }
    });
});

$("#fileB").click(function (e) { 
    $("#filein").trigger('click');
    
});

var myModal = new bootstrap.Modal(document.getElementById('result'), )

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/port/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    $("#content").append("<p class='"+data.status+"'>"+data.message+"</p>");

};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};