$(document).ready(function() {
    $('#vehicleSelectModal').on('show.bs.modal', function() {
        // AJAX request to fetch vehicles
        $.ajax({
            url: '/api/compare',  // Make sure the endpoint is correct
            method: 'POST',
            success: function(vehicles) {
                var container = $('#vehicleSelectionContainer');
                container.empty();  // Clear previous entries
                vehicles.forEach(function(vehicle) {
                    var content = `
                        <div class="col-md-4">
                            <div class="card mb-3">
                                <img class="card-img-top" src="/static/path_to_images/${vehicle.VehicleID}.jpg" alt="${vehicle.Brand} ${vehicle.Model}">
                                <div class="card-body">
                                    <h5 class="card-title">${vehicle.Brand} ${vehicle.Model}</h5>
                                    <p class="card-text">${vehicle.YearOfManufacture} - ${vehicle.Mileage} km</p>
                                    <button class="btn btn-primary" onclick="selectVehicle(${vehicle.VehicleID})">Vybrat</button>
                                </div>
                            </div>
                        </div>
                    `;
                    container.append(content);
                });
            },
            error: function(error) {
                console.error("Error loading vehicles: ", error);
            }
        });
    });
});

function selectVehicle(vehicleId) {
    // Check if the vehicle is already selected
    if (!document.querySelector(`input[value="${vehicleId}"]`)) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'vehicle_ids[]';
        input.value = vehicleId;
        document.getElementById('compareForm').appendChild(input);
        alert('Vozidlo s ID ' + vehicleId + ' bylo přidáno k porovnání.');
    } else {
        alert('Toto vozidlo je již vybráno.');
    }
}


document.addEventListener("DOMContentLoaded", function() {
    fetch('ads')  // Změňte podle potřeby na správný URL endpoint
        .then(response => response.json())
        .then(data => {
            const adsContainer = document.getElementById('ads-container');
            if (data && data.length > 0) {
                data.forEach(ad => {
                    const adElement = document.createElement('div');
                    adElement.className = 'col-md-4';
                    adElement.innerHTML = `
                        <div class="card mb-3">
                            <img src="${ad.image_url}" class="card-img-top" alt="${ad.title}">
                            <div class="card-body">
                                <h5 class="card-title">${ad.title}</h5>
                                <p class="card-text"><a href="${ad.target_url}" target="_blank">Více informací</a></p>
                            </div>
                        </div>
                    `;
                    adsContainer.appendChild(adElement);
                });
            } else {
                adsContainer.innerHTML = '<div class="col-12"><p>Žádné reklamy k zobrazení.</p></div>';
            }
        })
        .catch(error => {
            console.error('Chyba při načítání reklam:', error);
            const adsContainer = document.getElementById('ads-container');
            adsContainer.innerHTML = '<div class="col-12"><p>Nelze načíst reklamy.</p></div>';
        });
});
