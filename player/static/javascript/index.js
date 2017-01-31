function initCompass() {
    var rotations = 10;
    $("#compass").rotate({
        angle: 0,
        animateTo: 360 * rotations,
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
            url: "/api/queue/",
            type: "post",
            data: data,
            success: showNextSong,
        });
    });
}

function showNextSong(event) {
    console.log(event);
    $("#compass").stopRotate();
    $("#compass").rotate(event.degrees);

    var compassText = event.miles + "<br>" + "miles";
    $("#compass-text").html(compassText);

    var currentSongText = event.title + "<br>" + event.artist;
    $("#current-song").html(currentSongText);
}

window.onload = function() {
    initCompass();
    updateLocation();
}
