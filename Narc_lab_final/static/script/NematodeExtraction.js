$(document).ready(function() {

    $("#NematodeExtraction").select2({
        placeholder: "Search for a Nematode Extraction",
        // Add your options here...
    });
    // Show the input field when the select is changed to the "Please Select" option
    $('#NematodeExtraction').change(function() {
        if ($('#NematodeExtraction option:selected').val() == "default") {
            $('#NematodeExtractiontext').val('');
        } else {
            $('#NematodeExtractiontext').val($('#NematodeExtraction option:selected').text());
        }

    });
    // Event listener for the button click


    $('#NematodeExtractionedit').on('click', function() {
        if ($('#NematodeExtraction option:selected').val() == "default" || $('#NematodeExtractiontext').val() == "") {
            alert("you cannot left empty");
            $('#NematodeExtractiontext').val($('#NematodeExtraction option:selected').text());
        } else {
            // Data to send in the POST request
            const select = $('#NematodeExtractiontext').val();
            const id = $('#NematodeExtraction option:selected').val();

            const dataToSend = { 'value': select, 'id': id, "type": "edit" };
            //alert(dataToSend);
            var tk = $('#tk').val();
            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/nematodeextraction', // Replace with your API endpoint
                method: 'POST',
                data: JSON.stringify(dataToSend),

                headers: {
                    'X-CSRFToken': tk, // Set the X-CSRFToken header with the CSRF token value
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    //alert("sucess")
                    console.log('Success:', response);
                    // Find the option with value "2"
                    //alert(typeof(dataToSend["id"]));
                    var existingOption = $('#NematodeExtraction option:selected');

                    // Create a new option with the updated value
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    // Replace the existing option with the new option
                    existingOption.replaceWith(newOption);
                    $("#NematodeExtraction").val(dataToSend["id"]);
                    alert("Sucess");
                },
                error: function(error) {
                    alert("Something went worng ")
                    console.error('Error:', error);
                    // Handle errors here
                }
            });
        }
    });
    //=======================================START delete ===================================================
    $('#NematodeExtractiondel').on('click', function() {
        const id = $('#NematodeExtraction option:selected').val();
        var result = confirm("Do you want to proceed?");

        // Check the result (true for Yes, false for No)
        if (result) {
            // User clicked Yes, perform your action here
            const dataToSend = { 'id': id, "type": "del" };
            //alert(dataToSend);
            var tk = $('#tk').val();
            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/nematodeextraction', // Replace with your API endpoint
                method: 'POST',
                data: JSON.stringify(dataToSend),

                headers: {
                    'X-CSRFToken': tk, // Set the X-CSRFToken header with the CSRF token value
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                    //alert("sucess")
                    console.log('Success:', response)
                        // Find the option with value "2"
                    $('#NematodeExtraction option:selected').remove();
                    $('#NematodeExtractiontext').val("");
                    alert("Sucess");
                },
                error: function(error) {
                    alert("Something went worng ")
                    console.error('Error:', error);
                    // Handle errors here
                }
            });
        } else {
            // User clicked No, do something else here or simply ignore
            //alert("You clicked No!");
        }
        // Data to send in the POST request

        //const id=$('#suspectProblem option:selected').val();



    });



    //=======================add ====================================
    $('#NematodeExtractionadd').on('click', function() {
        const newData = $('#NematodeExtractiontextadd').val();
        if (newData == "") {
            alert("Cannot be empty");
        } else {
            var result = confirm("Do you want to proceed?");

            // Check the result (true for Yes, false for No)
            if (result) {
                // User clicked Yes, perform your action here
                const dataToSend = { 'value': newData, "type": "add" };

                var tk = $('#tk').val();
                // Perform the AJAX POST request using $.ajax()
                $.ajax({
                    url: '/setup_form/nematodeextraction', // Replace with your API endpoint
                    method: 'POST',
                    data: JSON.stringify(dataToSend),

                    headers: {
                        'X-CSRFToken': tk, // Set the X-CSRFToken header with the CSRF token value
                        'Content-Type': 'application/json'
                    },
                    success: function(response) {
                        //alert("sucess")
                        console.log('Success:', JSON.stringify(response));
                        // Find the option with value "2"
                        $('#NematodeExtractiontextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);

                        $("#NematodeExtraction").append(option);
                        $('#NematodeExtraction').val(response["data"]["id"]);
                        $('#NematodeExtraction').change();
                        alert("Sucess");
                        $('#NematodeExtractiontextadd').val("");

                    },
                    error: function(error) {
                        alert("Something went worng ")
                        console.error('Error:', error);
                        // Handle errors here
                    }
                });
            } else {
                // User clicked No, do something else here or simply ignore
                //alert("You clicked No!");
            }
            // Data to send in the POST request

            //const id=$('#suspectProblem option:selected').val();

        }

    });

});