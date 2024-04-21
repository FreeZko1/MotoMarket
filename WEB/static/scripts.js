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
