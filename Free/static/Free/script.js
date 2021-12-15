$("#test_button").click(function (e) { 
    e.preventDefault();

    var formData = new FormData();
    for(var i = 0; i<$('#filein')[0].files.length; i++){
        formData.append('file', $('#filein')[0].files[i])
    }
    
    console.log()
    $.ajax({
        type: "POST",
        url: "api/load/",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            alert("Ok")
            
        }
    });
});

$("#fileB").click(function (e) { 
    $("#filein").trigger('click');
    
});

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/port/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};