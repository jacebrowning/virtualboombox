window.locationAvailable = false;
window.playerAvailable = false;
window.currentSongRef = null;

// Messages ////////////////////////////////////////////////////////////////////

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

function clearMessages() {
    $("#messages").empty();
}

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

// Songs ///////////////////////////////////////////////////////////////////////

function getSongs(location) {
    var data = {
        "latitude": location.coords.latitude,
        "longitude": location.coords.longitude,
        "accuracy": location.coords.accuracy,
    };
    console.log("Current position data: ", data);

    if (data.accuracy != -1) {
        $("#messages").empty();
        window.locationAvailable = true;
    }

    var weightDistance = $("#distance-weight").slider('getValue') / 100.0
    data["weightDistance"] = weightDistance;
    data["weightTime"] = 1.0 - weightDistance;
    data["limit"] = 100;

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
    window.currentSongRef = song.ref;

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

    if (songs.length == 0) {
        var message = "No songs are playing nearby"
        console.log(message);
        var html = '<li class="list-group-item"><i>' + message + '.</i></li>';
        $("#song-queue").append(html);
        return;
    }

    var count = Math.min(songs.length, 5);
    for (i = 0; i < count; i++) {
        var song = songs[i];
        var html ='<a href="' + song.lastfm_url + '" target="_blank" class="list-group-item">'
            + '<b>' + song.title + '</b>'
            + "&nbsp;<i>by</i>&nbsp;"
            + song.artist
            + "</a>"
        $("#song-queue").append(html);
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
    $("#player-toggle").html('<span class="glyphicon glyphicon-play"></span>');
}

function showResumeButton() {
    document.location.hash = "paused";
    $("#player-toggle").html('<span class="glyphicon glyphicon-play"></span>');
}

function showPauseButton() {
    document.location.hash = "playing";
    $("#player-toggle").html('<span class="glyphicon glyphicon-pause"></span>');
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
    updateReactions();
});

// Reactions ///////////////////////////////////////////////////////////////////

function updateReactions() {
    $.ajax({
        url: "/api/reactions/",
        type: "GET",
        success: showReactions,
    });
}

function showReactions(reactions) {
    $("#comments").empty();

    if (reactions.length == 0) {
        var message = "No one has reacted to your songs";
        console.log(message);
        var html = '<li class="list-group-item"><i>' + message + '.</i></li>';
        $("#comments").append(html);
        return;
    }

    var count = Math.min(reactions.length, 5);
    for (i = 0; i < count; i++) {
        var reaction = reactions[i];
        var html = reaction.comment;
        var html ='<li class="list-group-item">' + reaction.comment +  '</li>';
        $("#comments").append(html);
    }
}

$("#reaction-form").on("submit", function (event) {
    var data = {
        "song": window.currentSongRef,
        "comment": $("#reaction-text").val(),
    };
    console.log("Reaction data: ", data);

    $.ajax({
        url: "/api/reactions/",
        type: "POST",
        data: data,
        success: function() {
            $("#messages").append('<li class="alert alert-info">Your message has been delivered!</li>');
            setTimeout(clearMessages, 3 * 1000);
        },
    });

    this.reset();
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

$(window).ready( function(event) {
    spinCompass();
    getLocation();
    updateReactions();
});

$("#distance-weight").slider({
    id: 'distance-weight-slider',
    ticks: [0, 50, 100],
    ticks_snap_bounds: 2,
    value: 50,
    tooltip: 'hide',
});
