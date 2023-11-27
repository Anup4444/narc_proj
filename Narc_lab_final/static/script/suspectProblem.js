$(document).ready(function() {

    $("#suspectProblem").select2({
        placeholder: "Search for a Suspected Problem",
        // Add your options here...
    });

    // Show the input field when the select is changed
    $('#suspectProblem').change(function() {
        if ($('#suspectProblem option:selected').val() == "default") {
            $('#suspectProblemtext').val('');
        } else {
            $('#suspectProblemtext').val($('#suspectProblem option:selected').text());
        }
    });

    // Edit event
    $('#suspectProblemedit').on('click', function() {
        if ($('#suspectProblem option:selected').val() == "default" || $('#suspectProblemtext').val() == "") {
            alert("you cannot leave it empty");
            $('#suspectProblemtext').val($('#suspectProblem option:selected').text());
        } else {
            const select = $('#suspectProblemtext').val();
            const id = $('#suspectProblem option:selected').val();

            const dataToSend = {
                'value': select,
                'id': id,
                "type": "edit"
            };

            var tk = $('#tk').val();
            $.ajax({
                url: '/setup_form/suspectedproblem',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    var existingOption = $('#suspectProblem option:selected');
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    existingOption.replaceWith(newOption);
                    $("#suspectProblem").val(dataToSend["id"]);
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
    $('#suspectProblemdel').on('click', function() {
        const id = $('#suspectProblem option:selected').val();
        var result = confirm("Do you want to proceed?");
        if (result) {
            const dataToSend = {
                'id': id,
                "type": "del"
            };

            var tk = $('#tk').val();
            $.ajax({
                url: '/setup_form/suspectedproblem',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    $('#suspectProblem option:selected').remove();
                    $('#suspectProblemtext').val("");
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
    $('#suspectProblemadd').on('click', function() {
        const newData = $('#suspectProblemtextadd').val();
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
                    url: '/setup_form/suspectedproblem',
                    method: 'POST',
                    data: JSON.stringify(dataToSend),
                    headers: {
                        'X-CSRFToken': tk,
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        console.log('Success:', JSON.stringify(response));
                        $('#suspectedProblemtextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);
                        $("#suspectProblem").append(option);
                        $('#suspectProblem').val(response["data"]["id"]);
                        $('#suspectProblem').change();
                        alert("Success");
                        $('#suspectProblemtextadd').val("");
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