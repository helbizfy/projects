// Places API

let autocompleteFrom, autocompleteTo, fromLocation, toLocation, pickUpLocation

function initAutocomplete() {
    autocompleteFrom = new google.maps.places.Autocomplete(
        document.getElementById('autocompleteFrom'), {
        types: ['geocode'],
        componentRestrictions: { 'country': ['LV'] },
        fields: ['place_id', 'geometry', 'name'],
    }


    )

    autocompleteTo = new google.maps.places.Autocomplete(
        document.getElementById('autocompleteTo'), {
        types: ['geocode'],
        componentRestrictions: { 'country': ['LV'] },
        fields: ['place_id', 'geometry', 'name']
    }
    )

    fromLocation = new google.maps.places.Autocomplete(
        document.getElementById('fromLocation'), {
        types: ['geocode'],
        componentRestrictions: { 'country': ['LV'] },
        fields: ['place_id', 'geometry', 'name']
    }
    )

    toLocation = new google.maps.places.Autocomplete(
        document.getElementById('toLocation'), {
        types: ['geocode'],
        componentRestrictions: { 'country': ['LV'] },
        fields: ['place_id', 'geometry', 'name']
    }
    )

    pickUpLocation = new google.maps.places.Autocomplete(
        document.getElementById('pickUpLocation'), {
        types: ['address'],
        componentRestrictions: { 'country': ['LV'] },
        fields: ['place_id', 'geometry', 'name']
    }
    )


}

//Check date and time input


document.addEventListener('DOMContentLoaded', function () {

    var now = new Date();
    var day = now.getDate()
    var month = now.getMonth() + 1
    var year = now.getFullYear()

    if (month < 10) {
        month = '0' + month.toString()
    }
    if (day < 10) {
        day = '0' + day.toString()
    }

    var minDate = year + '-' + month + '-' + day

    document.getElementById("dateWhen").setAttribute("min", minDate)





})

// Success message after rating the ride

function showSuccessMessage() {

    swal("Thank you!", "Your review is sumbitted!", "success")
    return false

}

// Function so rate ride modal rates the correct ride

function showRideId(btn) {
    document.getElementById('thisID').value = btn.value
    console.log(btn.value)

}






