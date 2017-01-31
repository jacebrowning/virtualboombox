var locationAvailable = false;

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
    $("#messages").empty();

    var options = {
      enableHighAccuracy: true,
      timeout: 5 * 1000,
      maximumAge: 10 * 1000,
    };

    navigator.geolocation.getCurrentPosition(
        getNextSong, showLocationWarning, options);
}

function getNextSong(location) {
    locationAvailable = true;

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

function showLocationWarning(error) {
    if (error.code == error.PERMISSION_DENIED) {
        locationAvailable = false;
        $("#messages").append('<li class="alert alert-danger">Location sharing is disabled for your browser.</li>');
    } else if (error.code == error.POSITION_UNAVAILABLE) {
        locationAvailable = false;
        $("#messages").append('<li class="alert alert-warning">Your location could not be determined.</li>');
    }

    $("#next-song").prop("disabled", false);
}

$(document).ready( function () {
    $("#next-song").prop("disabled", locationAvailable);
});

$(window).ready( function(e) {
    spinCompass();
    updateLocation();
});

$("#next-song").on( "click", function() {
    $("#next-song").prop("disabled", locationAvailable);
    spinCompass();
    updateLocation();
});
