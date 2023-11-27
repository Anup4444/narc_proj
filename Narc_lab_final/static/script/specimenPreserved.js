$(document).ready(function() {

    // Initialize the select2 for DiagnosticTest
    $("#specimenPreserved").select2({
        placeholder: "Search for a Diagnostic Test",
    });

    // Update the text input when the DiagnosticTest select is changed
    $('#specimenPreserved').change(function() {
        if ($('#specimenPreserved option:selected').val() == "default") {
            $('#specimenPreservedtext').val('');
        } else {
            $('#specimenPreservedtext').val($('#specimenPreserved option:selected').text());
        }
    });

    // Edit functionality for DiagnosticTest
    $('#specimenPreservededit').on('click', function() {
        if ($('#specimenPreserved option:selected').val() == "default" || $('#specimenPreservedtext').val() == "") {
            alert("you cannot leave it empty");
            $('#specimenPreservedtext').val($('#specimenPreserved option:selected').text());
        } else {
            const select = $('#specimenPreservedtext').val();
            const id = $('#specimenPreserved option:selected').val();
            const dataToSend = { 'value': select, 'id': id, "type": "edit" };
            var tk = $('#tk').val();

            $.ajax({
                url: '/setup_form/specimenpreserved',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    var existingOption = $('#specimenPreserved option:selected');
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });
                    existingOption.replaceWith(newOption);
                    $("#specimenPreserved").val(dataToSend["id"]);
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
    $('#specimenPreserveddel').on('click', function() {
        const id = $('#specimenPreserved option:selected').val();
        var result = confirm("Do you want to proceed?");
        if (result) {
            const dataToSend = { 'id': id, "type": "del" };
            var tk = $('#tk').val();

            $.ajax({
                url: '/setup_form/specimenPreserved',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    $('#specimenPreserved option:selected').remove();
                    $('#specimenPreservedtext').val("");
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
    $('#specimenPreservedadd').on('click', function() {
        const newData = $('#specimenPreservedtextadd').val();
        if (newData == "") {
            alert("Cannot be empty");
        } else {
            var result = confirm("Do you want to proceed?");
            if (result) {
                const dataToSend = { 'value': newData, "type": "add" };
                var tk = $('#tk').val();

                $.ajax({
                    url: '/setup_form/specimenpreserved',
                    method: 'POST',
                    data: JSON.stringify(dataToSend),
                    headers: {
                        'X-CSRFToken': tk,
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        console.log('Success:', JSON.stringify(response));
                        $('#specimenPreservedtextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);
                        $("#specimenPreserved").append(option);
                        $('#specimenPreserved').val(response["data"]["id"]);
                        $('#specimenPreserved').change();
                        alert("Success");
                        $('#specimenPreservedtextadd').val("");
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