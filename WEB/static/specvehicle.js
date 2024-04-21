$(document).ready(function () {
    $('#contactSellerForm').submit(function(event) {
        event.preventDefault();
        var senderID = $('#senderId').val();
        var recipientID = $('#recipientId').val();
        var message = $('#messageText').val();

        $.post('/api/send-message', {
            text: message,
            sender_id: senderID,
            recipient_id: recipientID
        }, function(response) {
            if (response.success) {
                $('#contactSellerModal').modal('hide');
                alert('Zpráva byla odeslána.');
                $('#messageText').val('');
            } else {
                alert('Nepodařilo se odeslat zprávu.');
            }
        });
    });
});