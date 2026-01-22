const video = document.getElementById("videoFeed");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

startBtn.onclick = () => {
  video.src = "/webcam";
  startBtn.disabled = true;
  stopBtn.disabled = false;
};

stopBtn.onclick = () => {
  video.src = "";
  startBtn.disabled = false;
  stopBtn.disabled = true;
};
