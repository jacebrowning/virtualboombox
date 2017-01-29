function updateLocation() {

    navigator.geolocation.getCurrentPosition(function(location) {
        var data = {
            "latitude": location.coords.latitude,
            "longitude": location.coords.longitude,
        };

        $.ajax({
            url: "/api/next/",
            type: "post",
            data: data,
        });
    });
}

window.load = updateLocation();
