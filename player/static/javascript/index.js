window.locationAvailable = false;
window.playerAvailable = false;
window.autoplay = true;

// Compass /////////////////////////////////////////////////////////////////////

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
    var options = {
      timeout: 30 * 1000,
      maximumAge: 15 * 60 * 1000,
    };

    console.log("Getting current position...");
    navigator.geolocation.getCurrentPosition(
        getSongs, showLocationWarning, options);
}

function getSongs(location) {
    $("#messages").empty();

    var data = {
        "latitude": location.coords.latitude,
        "longitude": location.coords.longitude,
        "accuracy": location.coords.accuracy,
    };
    console.log("Current position: ", data);
    window.locationAvailable = true;

    data["limit"] = 100;
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

    var count = Math.min(songs.length, 4);
    for (i = 0; i < count; i++) {
        var song = songs[i];
        var item = ""
            + song.artist
            + " - "
            + "<b>" + song.title + "</b>"
        $("#song-queue").append("<li>" + item + "</li>");
    }
}

function showLocationWarning(error) {
    console.log("Position unavailable: ", error);

    $("#messages").empty();

    if (error.code == error.PERMISSION_DENIED) {
        $("#messages").append('<li class="alert alert-danger">Location sharing is disabled for your browser.</li>');
        stopCompass();
    } else {
        $("#messages").append('<li class="alert alert-warning">Your location could not be determined.</li>');
        stopCompass();
        setTimeout(getLocation, 2 * 1000);
    }
}

// Player //////////////////////////////////////////////////////////////////////

function onPlayerReady(event) {
    console.log("Player is ready")
    window.playerAvailable = true;
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        console.log("Player has finished")
        $("#player-next").trigger("click");
    } else if (event.data == YT.PlayerState.PAUSED) {
        pauseVideo();
    } else if (event.data == YT.PlayerState.PLAYING) {
        resumeVideo();
    }
}

function playVideo(url) {
    var checkExist = setInterval(function() {
       if (window.playerAvailable) {
            if (window.autoplay == true) {
                console.log("Playing video: ", url)
                window.player.loadVideoByUrl({mediaContentUrl: url});
            } else {
                console.log("Setting video: ", url)
                window.player.cueVideoByUrl({mediaContentUrl: url});
            }
            clearInterval(checkExist);
       }
    }, 1 * 1000);
}

function pauseVideo() {
    window.autoplay = false;
    window.player.pauseVideo();
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-play"></span>' +
        '&nbsp;' +
        'Resume Playback'
    );
    console.log("Video paused");
}

function resumeVideo() {
    window.autoplay = true;
    window.player.playVideo();
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-pause"></span>' +
        '&nbsp;' +
        'Pause Playback'
    );
    console.log("Video playing");
}

$("#player-toggle").on("click", function() {
    if (window.player.getPlayerState() == YT.PlayerState.PLAYING) {
        pauseVideo();
    } else {
        resumeVideo();
    }
});

$("#player-next").on("click", function() {
    $("#player-next").prop("disabled", window.locationAvailable);
    spinCompass();
    setTimeout(getLocation, 1 * 1000);
});

// Loading /////////////////////////////////////////////////////////////////////

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
