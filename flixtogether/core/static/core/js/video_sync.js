// Basic structure to handle sync events over WebSocket for video play, pause, seek

const videoPlayer = document.getElementById('video-player');

const syncSocket = new WebSocket('ws://' + window.location.host + '/ws/room/' + roomSlug + '/sync/');

syncSocket.onopen = () => {
    console.log('Sync socket connected');
};

syncSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    switch(data.type) {
        case 'play':
            if (videoPlayer.paused) videoPlayer.play();
            break;
        case 'pause':
            if (!videoPlayer.paused) videoPlayer.pause();
            break;
        case 'seek':
            if (Math.abs(videoPlayer.currentTime - data.time) > 0.5) {
                videoPlayer.currentTime = data.time;
            }
            break;
    }
};

videoPlayer.onplay = () => {
    syncSocket.send(JSON.stringify({type: 'play'}));
};

videoPlayer.onpause = () => {
    syncSocket.send(JSON.stringify({type: 'pause'}));
};

videoPlayer.onseeked = () => {
    syncSocket.send(JSON.stringify({type: 'seek', time: videoPlayer.currentTime}));
};
