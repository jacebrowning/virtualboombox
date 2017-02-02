window.locationAvailable = false;
window.autoplay = true;

// Compass

function spinCompass() {
    if (!$.trim($("#current-song").html())) {
        $("#current-song").html("<i>Locating the nearest playing song...</i>");
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

    $("#player-next").prop("disabled", false);

    window.locationAvailable = false;
}

function getLocation() {
    $("#messages").empty();

    var options = {
      timeout: 10 * 1000,
      maximumAge: 5 * 60 * 1000,
    };

    console.log("Getting current position...");
    navigator.geolocation.getCurrentPosition(
        getSongs, showLocationWarning, options);
}

function getSongs(location) {
    var data = {
        "latitude": location.coords.latitude,
        "longitude": location.coords.longitude,
        "accuracy": location.coords.accuracy,
    };
    console.log("Current position: ", data);

    window.locationAvailable = true;

    data["limit"] = 10;
    $.ajax({
        url: "/api/queue/",
        type: "POST",
        data: data,
        success: showSongs,
    });
}

function showSongs(songs) {
    showNextSong(songs[0]);
    showSongQueue(songs.slice(1));
    playVideo(songs[0].youtube_url);
}

function showNextSong(song) {
    var start = $("#compass").getRotateAngle() % 360;
    $("#compass").rotate({
        angle: start,
        animateTo: song.degrees,
        duration: 1.5 * 1000,
        easing: $.easing.easeOutElastic,
    });

    var distance = "<b>" + song.miles + "</b>" + "<br>" + "miles";
    $("#compass-text").html(distance);

    var title = "<p><b>" + song.title + "</b></p>";
    var artist = "<p>" + song.artist + "</p>";
    $("#current-song").html(title + artist);

    $("#player-next").prop("disabled", false);
}

function showSongQueue(songs) {
    $("#song-queue").empty();
    for (i = 0; i < songs.length; i++) {
        var song = songs[i];
        var item = ""
            + song.artist
            + "&emsp;-&emsp;<b>" + song.title + "</b>"
            + "&emsp;@&emsp;<i>" + song.miles + " miles</i>";
        $("#song-queue").append("<li>" + item + "</li>");
    }
}

function showLocationWarning(error) {
    console.log("Position unavailable: ", error);

    if (error.code == error.PERMISSION_DENIED) {
        $("#messages").append('<li class="alert alert-danger">Location sharing is disabled for your browser.</li>');
        stopCompass();
    } else {
        stopCompass();
        $("#messages").append('<li class="alert alert-warning">Your location could not be determined.</li>');
        setTimeout(getLocation, 3 * 1000);
    }
}

// Player

function onPlayerReady(event) {
    console.log("Player is ready")
}

function playVideo(url) {
    var checkExist = setInterval(function() {
       if (window.player) {
            console.log("Playing video: ", url)
            if (window.autoplay == true) {
                window.player.loadVideoByUrl({mediaContentUrl: url});
            } else {
                window.player.cueVideoByUrl({mediaContentUrl: url});
            }
            clearInterval(checkExist);
       }
    }, 1 * 1000);
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        console.log("Player has finished")
        $("#player-next").trigger("click");
    }
}

// Events

$(document).ready( function () {
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-pause"></span>' +
        '&nbsp;' +
        'Pause Playback'
    );
    $("#player-next").prop("disabled", window.locationAvailable);
});

$(window).ready( function(e) {
    spinCompass();
    getLocation();
});

$("#player-toggle").on("click", function() {
    if (window.player.getPlayerState() == YT.PlayerState.PLAYING) {
        window.autoplay = false;
        window.player.pauseVideo();
        $("#player-toggle").html(
            '<span class="glyphicon glyphicon-play"></span>' +
            '&nbsp;' +
            'Resume Playback'
        );
    } else {
        window.autoplay = true;
        window.player.playVideo();
        $("#player-toggle").html(
            '<span class="glyphicon glyphicon-pause"></span>' +
            '&nbsp;' +
            'Pause Playback'
        );
    }
});

$("#player-next").on("click", function() {
    $("#player-next").prop("disabled", window.locationAvailable);
    spinCompass();
    setTimeout(getLocation, 1 * 1000);
});
