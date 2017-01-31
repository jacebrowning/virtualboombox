var locationAvailable = false;

function spinCompass() {
    var start = $("#compass").getRotateAngle() % 360;
    var rotations = 10;
    $("#compass").rotate({
        angle: start,
        animateTo: 360 * rotations,
        duration: 20 * 1000 * rotations,
    });
}

function updateLocation() {
    $("#messages").empty();

    var options = {
      enableHighAccuracy: true,
      timeout: 10 * 1000,
      maximumAge: 5 * 60 * 1000,
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
    var start = $("#compass").getRotateAngle() % 360;
    $("#compass").rotate({
        angle: start,
        animateTo: event.degrees,
        duration: 1.5 * 1000,
        easing: $.easing.easeOutElastic,
    });

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
