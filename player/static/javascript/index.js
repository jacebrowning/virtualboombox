var locationAvailable = false;

function spinCompass() {
    if ($("#current-song").html() == "") {
        $("#current-song").html("Locating the nearest song...");
    }

    var start = $("#compass").getRotateAngle() % 360;
    var rotations = 10;
    $("#compass").rotate({
        angle: start,
        animateTo: 360 * rotations,
        duration: 20 * 1000 * rotations,
    });
}

function stopCompass() {
    $("#compass").stopRotate();

    $("#current-song").empty();

    $("#next-song").prop("disabled", false);

    locationAvailable = false;
}

function updateLocation() {
    $("#messages").empty();

    var options = {
      timeout: 10 * 1000,
      maximumAge: 5 * 60 * 1000,
    };

    console.log("Getting current position...");
    navigator.geolocation.getCurrentPosition(
        getNextSong, showLocationWarning, options);
}

function getNextSong(location) {
    var data = {
        "latitude": location.coords.latitude,
        "longitude": location.coords.longitude,
        "accuracy": location.coords.accuracy,
    };
    console.log("Current position: ", data);

    locationAvailable = true;

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
    console.log("Position unavailable: ", error);

    if (error.code == error.PERMISSION_DENIED) {
        $("#messages").append('<li class="alert alert-danger">Location sharing is disabled for your browser.</li>');
        stopCompass();
    } else {
        stopCompass();
        $("#messages").append('<li class="alert alert-warning">Your location could not be determined.</li>');
        setTimeout(updateLocation, 3 * 1000);
    }
}

$(document).ready( function () {
    $("#next-song").prop("disabled", locationAvailable);
});

$(window).ready( function(e) {
    spinCompass();
    updateLocation();
});

$("#next-song").on("click", function() {
    $("#next-song").prop("disabled", locationAvailable);
    spinCompass();
    updateLocation();
});
