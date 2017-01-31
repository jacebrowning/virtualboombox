function spinCompass() {
    var start = $("#compass").getRotateAngle();
    var rotations = 10;
    $("#compass").rotate({
        angle: start,
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
    $("#compass").stopRotate();
    $("#compass").rotate(event.degrees);

    var compassText = event.miles + "<br>" + "miles";
    $("#compass-text").html(compassText);

    var currentSongText = event.title + "<br>" + event.artist;
    $("#current-song").html(currentSongText);

    $("#next-song").prop("disabled", false);
}

$(document).ready( function () {
    $("#next-song").prop("disabled", true);
});

$(window).ready( function(e) {
    spinCompass();
    updateLocation();
});

$("#next-song").on( "click", function() {
    $("#next-song").prop("disabled", true);
    spinCompass();
    updateLocation();
});
