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

    var distance = "<b>" + event.miles + "</b>" + "<br>" + "miles";
    $("#compass-text").html(distance);

    var title = "<p><b>" + event.title + "</b></p>";
    var artist = "<p>" + event.artist + "</p>";
    var song = title + artist;
    $("#current-song").html(song);

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
