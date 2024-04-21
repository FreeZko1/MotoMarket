document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const username = document.getElementById("registerUsername").value;
        const firstName = document.getElementById("registerFirstName").value;
        const lastName = document.getElementById("registerLastName").value;
        const email = document.getElementById("registerEmail").value;
        const phone = document.getElementById("registerPhone").value;
        const password = document.getElementById("registerPassword").value;

        let errorMessage = "";

        // Validace e-mailu
        if (!/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
            errorMessage += "Zadejte platnou e-mailovou adresu.\n";
        }

        // Kontrola délky a znaků jména a příjmení
        if (!/^[a-zA-ZěščřžýáíéďťňůúĚŠČŘŽÝÁÍÉĎŤŇŮÚ\s]{1,30}$/.test(firstName + lastName)) {
            errorMessage += "Jméno a příjmení musí obsahovat pouze písmena a diakritiku a být kratší než 30 znaků.\n";
        }

        // Validace telefonního čísla
        if (!/^\d{9}$/.test(phone)) {
            errorMessage += "Telefonní číslo musí obsahovat přesně 9 čísel.\n";
        }

        // Validace hesla
        if (!/^(?=.*[A-Z])(?=.*\d).{7,}$/.test(password)) {
            errorMessage += "Heslo musí obsahovat minimálně jedno velké písmeno, jedno číslo a musí být delší než 6 znaků.\n";
        }

        // Zobrazit chybové zprávy, pokud jsou k dispozici
        if (errorMessage.length > 0) {
            event.preventDefault(); // Zabránění odeslání formuláře
            alert(errorMessage);
        }
    });
});