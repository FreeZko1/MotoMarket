$(document).ready(function() {
    $('#vehicleSelectModal').on('show.bs.modal', function() {
        $.ajax({
            url: '/compare/api/compare',
            method: 'GET',
            success: function(vehicles) {
                var container = $('#vehicleSelectionContainer');
                container.empty();
                vehicles.forEach(function(vehicle) {
                    var content = `
                        <div class="col-md-4">
                            <div class="card mb-3">
                                <img class="card-img-top" src="vehicle-image/${vehicle.VehicleID}" alt="${vehicle.Brand} ${vehicle.Model}">
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
                console.log("Error loading vehicles: ", error);
            }
        });
    });
});


function selectVehicle(vehicleId) {
    $.ajax({
        url: '/compare/select-vehicle',
        method: 'POST',
        data: { vehicle_id: vehicleId },
        success: function(response) {
            if (response.status === 'success') {
                alert('Vozidlo s ID ' + vehicleId + ' bylo přidáno k porovnání.');
            } else {
                alert('Chyba: ' + response.message);
            }
        },
        error: function(xhr) {
            alert('Chyba při přidávání vozidla k porovnání: ' + xhr.responseText);
        }
    });
}

