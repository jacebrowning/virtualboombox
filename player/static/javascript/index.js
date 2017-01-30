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
            success: showNextSong,
        });
    });
}

function showNextSong(event) {
    // TODO: Update DOM to show next song
    console.log(event);
}

window.load = updateLocation();
