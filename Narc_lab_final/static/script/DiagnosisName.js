$(document).ready(function() {

    $("#DiagnosisName").select2({
        placeholder: "Search for a Diagnosis Name",
        // Add your options here...
    });

    // Show the input field when the select is changed
    $('#DiagnosisName').change(function() {
        if ($('#DiagnosisName option:selected').val() == "default") {
            $('#DiagnosisNametext').val('');
        } else {
            $('#DiagnosisNametext').val($('#DiagnosisName option:selected').text());
        }
    });

    // Edit event
    $('#DiagnosisNameedit').on('click', function() {
        if ($('#DiagnosisName option:selected').val() == "default" || $('#DiagnosisNametext').val() == "") {
            alert("you cannot leave it empty");
            $('#DiagnosisNametext').val($('#DiagnosisName option:selected').text());
        } else {
            const select = $('#DiagnosisNametext').val();
            const id = $('#DiagnosisName option:selected').val();

            const dataToSend = {
                'value': select,
                'id': id,
                "type": "edit"
            };

            var tk = $('#tk').val();
            $.ajax({
                url: '/setup_form/diagnosisname',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    var existingOption = $('#DiagnosisName option:selected');
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    existingOption.replaceWith(newOption);
                    $("#DiagnosisName").val(dataToSend["id"]);
                    alert("Success");
                },
                error: function(error) {
                    alert("Something went wrong");
                    console.error('Error:', error);
                }
            });
        }
    });

    // Delete event
    $('#DiagnosisNamedel').on('click', function() {
        const id = $('#DiagnosisName option:selected').val();
        var result = confirm("Do you want to proceed?");
        if (result) {
            const dataToSend = {
                'id': id,
                "type": "del"
            };

            var tk = $('#tk').val();
            $.ajax({
                url: '/setup_form/diagnosisname',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    $('#DiagnosisName option:selected').remove();
                    $('#DiagnosisNametext').val("");
                    alert("Success");
                },
                error: function(error) {
                    alert("Something went wrong");
                    console.error('Error:', error);
                }
            });
        }
    });

    // Add event
    $('#DiagnosisNameadd').on('click', function() {
        const newData = $('#DiagnosisNametextadd').val();
        if (newData == "") {
            alert("Cannot be empty");
        } else {
            var result = confirm("Do you want to proceed?");
            if (result) {
                const dataToSend = {
                    'value': newData,
                    "type": "add"
                };

                var tk = $('#tk').val();
                $.ajax({
                    url: '/setup_form/diagnosisname',
                    method: 'POST',
                    data: JSON.stringify(dataToSend),
                    headers: {
                        'X-CSRFToken': tk,
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        console.log('Success:', JSON.stringify(response));
                        $('#DiagnosisNametextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);
                        $("#DiagnosisName").append(option);
                        $('#DiagnosisName').val(response["data"]["id"]);
                        $('#DiagnosisName').change();
                        alert("Success");
                        $('#DiagnosisNametextadd').val("");
                    },
                    error: function(error) {
                        alert("Something went wrong");
                        console.error('Error:', error);
                    }
                });
            }
        }
    });

});