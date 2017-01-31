function initCompass() {
    var rotations = 10;
    $("#compass").rotate({
        angle: -90,
        animateTo: 270 + (360 * rotations),
        duration: 20000 * rotations,
    });
}

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
    console.log(event);
    // TODO: Update DOM to show next song
    $("#compass").stopRotate();
    // TODO: rotate to new angle
}

window.onload = function() {
    initCompass();
    updateLocation();
}
