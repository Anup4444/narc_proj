$(document).ready(function() {

    // Initialize the select2 for DiagnosticTest
    $("#DiagnosticTest").select2({
        placeholder: "Search for a Diagnostic Test",
    });

    // Update the text input when the DiagnosticTest select is changed
    $('#DiagnosticTest').change(function() {
        if ($('#DiagnosticTest option:selected').val() == "default") {
            $('#DiagnosticTesttext').val('');
        } else {
            $('#DiagnosticTesttext').val($('#DiagnosticTest option:selected').text());
        }
    });

    // Edit functionality for DiagnosticTest
    $('#DiagnosticTestedit').on('click', function() {
        if ($('#DiagnosticTest option:selected').val() == "default" || $('#DiagnosticTesttext').val() == "") {
            alert("you cannot leave it empty");
            $('#DiagnosticTesttext').val($('#DiagnosticTest option:selected').text());
        } else {
            const select = $('#DiagnosticTesttext').val();
            const id = $('#DiagnosticTest option:selected').val();
            const dataToSend = { 'value': select, 'id': id, "type": "edit" };
            var tk = $('#tk').val();

            $.ajax({
                url: '/setup_form/diagnostictest',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    var existingOption = $('#DiagnosticTest option:selected');
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });
                    existingOption.replaceWith(newOption);
                    $("#DiagnosticTest").val(dataToSend["id"]);
                    alert("Success");
                },
                error: function(error) {
                    alert("Something went wrong")
                    console.error('Error:', error);
                }
            });
        }
    });

    // Delete functionality for DiagnosticTest
    $('#DiagnosticTestdel').on('click', function() {
        const id = $('#DiagnosticTest option:selected').val();
        var result = confirm("Do you want to proceed?");
        if (result) {
            const dataToSend = { 'id': id, "type": "del" };
            var tk = $('#tk').val();

            $.ajax({
                url: '/setup_form/diagnostictest',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    $('#DiagnosticTest option:selected').remove();
                    $('#DiagnosticTesttext').val("");
                    alert("Success");
                },
                error: function(error) {
                    alert("Something went wrong")
                    console.error('Error:', error);
                }
            });
        }
    });

    // Add functionality for DiagnosticTest
    $('#DiagnosticTestadd').on('click', function() {
        const newData = $('#DiagnosticTesttextadd').val();
        if (newData == "") {
            alert("Cannot be empty");
        } else {
            var result = confirm("Do you want to proceed?");
            if (result) {
                const dataToSend = { 'value': newData, "type": "add" };
                var tk = $('#tk').val();

                $.ajax({
                    url: '/setup_form/diagnostictest',
                    method: 'POST',
                    data: JSON.stringify(dataToSend),
                    headers: {
                        'X-CSRFToken': tk,
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        console.log('Success:', JSON.stringify(response));
                        $('#DiagnosticTesttextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);
                        $("#DiagnosticTest").append(option);
                        $('#DiagnosticTest').val(response["data"]["id"]);
                        $('#DiagnosticTest').change();
                        alert("Success");
                        $('#DiagnosticTesttextadd').val("");
                    },
                    error: function(error) {
                        alert("Something went wrong")
                        console.error('Error:', error);
                    }
                });
            }
        }
    });

});