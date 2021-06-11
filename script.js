
function validateEmail(email) {

    var pattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/;
    var patternCo = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[co]{2,4}$/;
    var email = document.getElementById("email");
    var error = document.getElementById("error");
    var terms = document.getElementById("terms");
    var submitEmail = document.getElementById("submit-email");


    if (email.value === "") {
        error.innerHTML = "Email address is required";
        submitEmail.style.visibility = "hidden";
        return false;
    } else if (!(pattern.test(email.value))) {
        error.innerHTML = "Please provide a valid e-mail address";
        submitEmail.style.visibility = "hidden";
        return false;
    } else if (patternCo.test(email.value)) {
        error.innerHTML = "We are not accepting subscriptions from Colombia emails";
        submitEmail.style.visibility = "hidden";
        return false;
    } else if (!(terms.checked)) {
        error.innerHTML = "You must accept the terms and conditions";
        submitEmail.style.visibility = "hidden";
        return false;
    } else {
        error.innerHTML = "";
        submitEmail.style.visibility = "visible";
    }
}

function submitEmail() {
    document.getElementById("newsletter").style.display = "none";
    document.getElementById("subscribed").style.display = "block";
}

