$(document).ready(function() {

    $("#storageCondition").select2({
        placeholder: "Search for a fruit",
        // Add your options here...
    });

    // Show the input field when the select is changed
    $('#storageCondition').change(function() {
        if ($('#storageCondition option:selected').val() == "default") {
            $('#storageConditiontext').val('');
        } else {
            $('#storageConditiontext').val($('#storageCondition option:selected').text());
        }
    });

    // Edit event
    $('#storageConditionedit').on('click', function() {
        if ($('#storageCondition option:selected').val() == "default" || $('#storageConditiontext').val() == "") {
            alert("you cannot leave it empty");
            $('#storageConditiontext').val($('#storageCondition option:selected').text());
        } else {
            const select = $('#storageConditiontext').val();
            const id = $('#storageCondition option:selected').val();

            const dataToSend = {
                'value': select,
                'id': id,
                "type": "edit"
            };

            var tk = $('#tk').val();
            $.ajax({
                url: '/setup_form/storagecondition',
                method: 'POST',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': tk,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    console.log('Success:', response);
                    var existingOption = $('#storageCondition option:selected');
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    existingOption.replaceWith(newOption);
                    $("#storageCondition").val(dataToSend["id"]);
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
    $('#storageConditiondel').on('click', function() {
        const id = $('#storageCondition option:selected').val();
        var result = confirm("Do you want to proceed?");
        if (result) {
            const dataToSend = {
                'id': id,
                "type": "del"
            };

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
                    $('#storageCondition option:selected').remove();
                    $('#storageConditiontext').val("");
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
    $('#storageConditionadd').on('click', function() {
        const newData = $('#storageConditiontextadd').val();
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
                    url: '/setup_form/specimenpreserved',
                    method: 'POST',
                    data: JSON.stringify(dataToSend),
                    headers: {
                        'X-CSRFToken': tk,
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        console.log('Success:', JSON.stringify(response));
                        $('#storageConditiontextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);
                        $("#storageCondition").append(option);
                        $('#storageCondition').val(response["data"]["id"]);
                        $('#storageCondition').change();
                        alert("Success");
                        $('#storageConditiontextadd').val("");
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