$(document).ready(function() {

    $("#fruitSelect").select2({
        placeholder: "Search for a Host",
        // Add your options here...
    });
    // Show the input field when the select is changed to the "Please Select" option
    $('#fruitSelect').change(function() {
        if ($('#fruitSelect option:selected').val() == "default") {
            $('#customFruit').val('');
        } else {
            $('#customFruit').val($('#fruitSelect option:selected').text());
        }

    });
    // Event listener for the button click


    $('#edit').on('click', function() {
        if ($('#fruitSelect option:selected').val() == "default" || $('#customFruit').val() == "") {
            alert("you cannot left empty");
            $('#customFruit').val($('#fruitSelect option:selected').text());
        } else {
            // Data to send in the POST request
            const select = $('#customFruit').val();
            const id = $('#fruitSelect option:selected').val();

            const dataToSend = { 'value': select, 'id': id, "type": "edit" };
            //alert(dataToSend);
            var tk = $('#tk').val();
            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/host', // Replace with your API endpoint
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
                    var existingOption = $('#fruitSelect option:selected');

                    // Create a new option with the updated value
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    // Replace the existing option with the new option
                    existingOption.replaceWith(newOption);
                    $("#fruitSelect").val(dataToSend["id"]);
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
    $('#del').on('click', function() {
        const id = $('#fruitSelect option:selected').val();
        var result = confirm("Do you want to proceed?");

        // Check the result (true for Yes, false for No)
        if (result) {
            // User clicked Yes, perform your action here
            const dataToSend = { 'id': id, "type": "del" };
            //alert(dataToSend);
            var tk = $('#tk').val();

            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/host', // Replace with your API endpoint
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
                    $('#fruitSelect option:selected').remove();
                    $('#customFruit').val("");
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

        //const id=$('#fruitSelect option:selected').val();



    });


    //=======================add ====================================
    $('#add').on('click', function() {
        const newData = $('#addhost').val();
        if (newData == "") {
            alert("Cannot be empty");
        } else {
            var result = confirm("Do you want to proceed?");

            // Check the result (true for Yes, false for No)
            if (result) {
                // User clicked Yes, perform your action here
                const dataToSend = { 'value': newData, "type": "add" };
                //alert(dataToSend);

                var tk = $('#tk').val();
                // Perform the AJAX POST request using $.ajax()
                $.ajax({
                    url: '/setup_form/host', // Replace with your API endpoint
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
                        $('#addhost').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);

                        $("#fruitSelect").append(option);
                        $('#fruitSelect').val(response["data"]["id"]);
                        $('#fruitSelect').change();
                        alert("Sucess");
                        $('#addhost').val("");

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

            //const id=$('#fruitSelect option:selected').val();

        }

    });

});