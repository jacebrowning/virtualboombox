window.locationAvailable = false;
window.playerAvailable = false;

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
    var data = {
        "latitude": location.coords.latitude,
        "longitude": location.coords.longitude,
        "accuracy": location.coords.accuracy,
    };
    console.log("Current position: ", data);

    if (data.accuracy != -1) {
        $("#messages").empty();
        window.locationAvailable = true;
    }

    data["limit"] = 100;
    data["distance-weight"] = $("#distance-weight").slider('getValue') / 100.0;
    $.ajax({
        url: "/api/queue/",
        type: "POST",
        data: data,
        success: showSongs,
    });
}

function showSongs(songs) {
    showNowPlaying(songs[0]);
    showNearbySongs(songs.slice(1));
    showVideo(songs[0].youtube_url);
}

function showNowPlaying(song) {
    if (!song) {
        console.log("No song currently playing")
        return;
    }

    var start = $("#compass").getRotateAngle() % 360;
    $("#compass").rotate({
        angle: start,
        animateTo: song.degrees,
        duration: 1.5 * 1000,
        easing: $.easing.easeOutElastic,
    });

    var html = "<b>" + song.miles + "</b>" + "<br>" + "miles";
    $("#compass-text").html(html);

    var html = ""
        + '<p><a href="' + song.lastfm_url + '" target="_blank"><b>' + song.title + '</b></a></p>'
        + "<p><i>by&nbsp;&nbsp;</i></p>"
        + "<p>" + song.artist + "</p>";
    $("#current-song").html(html);

    $("#player-next").prop("disabled", false);
}

function showNearbySongs(songs) {
    $("#song-queue").empty();

    $("#nearby-songs").css("visibility", "visible");

    var count = Math.min(songs.length, 4);
    for (i = 0; i < count; i++) {
        var song = songs[i];
        var html = "<li>"
            + '<a href="' + song.lastfm_url + '" target="_blank"><b>' + song.title + '</b></a>'
            + "&nbsp;&nbsp;<i>by</i>&nbsp;&nbsp;"
            + song.artist
            + "</li>"
        $("#song-queue").append(html);
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
        getSongs({
            "coords": {
                // Oceanic Pole of Inaccessibility
                "latitude": -48.876667,
                "longitude": -123.393333,
                "accuracy": -1,
            },
        });
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
        playVideo();
    }
}

function showVideo(url) {
    var checkExist = setInterval(function() {
       if (window.playerAvailable) {
            $("#player").css("visibility", "visible");

            if (document.location.hash == "#paused") {
                console.log("Setting video: ", url)
                window.player.cueVideoByUrl({mediaContentUrl: url});

            } else {
                console.log("Playing video: ", url)
                window.player.loadVideoByUrl({mediaContentUrl: url});
            }

            clearInterval(checkExist);
       }
    }, 1 * 1000);
}

function playVideo(init) {
    window.player.playVideo();
    showPauseButton();
    console.log("Video playing");
}

function pauseVideo(init) {
    window.player.pauseVideo();
    showResumeButton();
    console.log("Video paused");
}

function showPlayButton() {
    document.location.hash = "paused";
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-play"></span>' +
        '&nbsp;' +
        'Start Playback'
    );
}

function showResumeButton() {
    document.location.hash = "paused";
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-play"></span>' +
        '&nbsp;' +
        'Resume Playback'
    );
}

function showPauseButton() {
    document.location.hash = "playing";
    $("#player-toggle").html(
        '<span class="glyphicon glyphicon-pause"></span>' +
        '&nbsp;' +
        'Pause Playback'
    );
}

$("#player-toggle").on("click", function() {
    if (window.player.getPlayerState() == YT.PlayerState.PLAYING) {
        pauseVideo();
    } else {
        playVideo();
    }
});

$("#player-next").on("click", function() {
    $("#player-next").prop("disabled", window.locationAvailable);
    spinCompass();
    setTimeout(getLocation, 1 * 1000);
});

// Loading /////////////////////////////////////////////////////////////////////

$(document).ready( function () {
    isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
    if ( isMobile ) {
        showPlayButton();
    } else if (document.location.hash == "#paused") {
        showResumeButton();
    } else {
        showPauseButton();
    }
    $("#player-next").prop("disabled", window.locationAvailable);
});

$(window).ready( function(e) {
    spinCompass();
    getLocation();
});


$("#distance-weight").slider({
    id: 'slider',
    ticks: [0, 50, 100],
    ticks_snap_bounds: 2,
    value: 50,
    tooltip: 'hide',
});
