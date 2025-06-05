const signalingSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/webrtc/' + roomSlug + '/'
);

let localStream = null;
let peerConnection = null;
const configuration = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

signalingSocket.onmessage = async function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'offer') {
        await handleOffer(data.offer);
    } else if (data.type === 'answer') {
        await handleAnswer(data.answer);
    } else if (data.type === 'ice-candidate') {
        await handleIceCandidate(data.candidate);
    }
};

signalingSocket.onopen = async function() {
    localStream = await navigator.mediaDevices.getUserMedia({audio:true, video:false});
    setupPeerConnection();
};

function setupPeerConnection() {
    peerConnection = new RTCPeerConnection(configuration);

    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            signalingSocket.send(JSON.stringify({
                type: 'ice-candidate',
                candidate: event.candidate
            }));
        }
    };

    peerConnection.ontrack = (event) => {
        const remoteAudio = document.getElementById('remoteAudio');
        if (remoteAudio.srcObject !== event.streams[0]) {
            remoteAudio.srcObject = event.streams[0];
        }
    };

    createAndSendOffer();
}

async function createAndSendOffer() {
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    signalingSocket.send(JSON.stringify({
        type: 'offer',
        offer: offer
    }));
}

async function handleOffer(offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    signalingSocket.send(JSON.stringify({
        type: 'answer',
        answer: answer
    }));
}

async function handleAnswer(answer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

async function handleIceCandidate(candidate) {
    try {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    } catch (e) {
        console.error('Error adding received ice candidate', e);
    }
}


/////



