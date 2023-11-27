$(document).ready(function() {

    $("#GenusLabMethods").select2({
        placeholder: "Search for a Genus Lab Methods",
        // Add your options here...
    });
    // Show the input field when the select is changed to the "Please Select" option
    $('#GenusLabMethods').change(function() {
        if ($('#GenusLabMethods option:selected').val() == "default") {
            $('#GenusLabMethodstext').val('');
        } else {
            $('#GenusLabMethodstext').val($('#GenusLabMethods option:selected').text());
        }

    });
    // Event listener for the button click


    $('#GenusLabMethodsedit').on('click', function() {
        if ($('#GenusLabMethods option:selected').val() == "default" || $('#GenusLabMethodstext').val() == "") {
            alert("you cannot left empty");
            $('#GenusLabMethodstext').val($('#GenusLabMethods option:selected').text());
        } else {
            // Data to send in the POST request
            const select = $('#GenusLabMethodstext').val();
            const id = $('#GenusLabMethods option:selected').val();

            const dataToSend = { 'value': select, 'id': id, "type": "edit" };
            //alert(dataToSend);
            var tk = $('#tk').val();
            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/genuslabmethods', // Replace with your API endpoint
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
                    var existingOption = $('#GenusLabMethods option:selected');

                    // Create a new option with the updated value
                    var newOption = $('<option>', {
                        value: dataToSend['id'],
                        text: dataToSend['value']
                    });

                    // Replace the existing option with the new option
                    existingOption.replaceWith(newOption);
                    $("#GenusLabMethods").val(dataToSend["id"]);
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
    $('#GenusLabMethodsdel').on('click', function() {
        const id = $('#GenusLabMethods option:selected').val();
        var result = confirm("Do you want to proceed?");

        // Check the result (true for Yes, false for No)
        if (result) {
            // User clicked Yes, perform your action here
            const dataToSend = { 'id': id, "type": "del" };
            //alert(dataToSend);
            var tk = $('#tk').val();
            // Perform the AJAX POST request using $.ajax()
            $.ajax({
                url: '/setup_form/genuslabmethods', // Replace with your API endpoint
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
                    $('#GenusLabMethods option:selected').remove();
                    $('#GenusLabMethodstext').val("");
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
    $('#GenusLabMethodsadd').on('click', function() {
        const newData = $('#GenusLabMethodstextadd').val();
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
                    url: '/setup_form/genuslabmethods', // Replace with your API endpoint
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
                        $('#GenusLabMethodstextadd').val("");
                        var option = $('<option></option>').attr("value", response["data"]["id"]).text(response["data"]["value"]);

                        $("#GenusLabMethods").append(option);
                        $('#GenusLabMethods').val(response["data"]["id"]);
                        $('#GenusLabMethods').change();
                        alert("Sucess");
                        $('#GenusLabMethodstextadd').val("");

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