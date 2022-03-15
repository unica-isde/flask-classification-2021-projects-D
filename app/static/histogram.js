/**
 * Simple long polling client based on JQuery
 * https://github.com/sigilioso/long_polling_example/blob/master/static/poll.js
 */

/**
 * Request an update to the server and once it has answered, then update
 * the content and request again.
 * The server is supposed to response when a change has been made on data.
 */

$(window).on("load", printHistogram);

function printHistogram(){
    var script = document.getElementById('readImg');
    var image_id = script.getAttribute('image_id');
    setTimeout(function (){
        processImage(getImageData(image_id))
      }, 50);
}

function getImageData(el) {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  const img = document.getElementById(el);
  canvas.width = img.width;
  canvas.height = img.height;
  context.drawImage(img, 0, 0);

  return context.getImageData(0, 0, img.width, img.height);
}

function processImage(inImg) {
  const src = new Uint32Array(inImg.data.buffer);

  let histBrightness = (new Array(256)).fill(0);
  let histR = (new Array(256)).fill(0);
  let histG = (new Array(256)).fill(0);
  let histB = (new Array(256)).fill(0);
  for (let i = 0; i < src.length; i++) {
    let r = src[i] & 0xFF;
    let g = (src[i] >> 8) & 0xFF;
    let b = (src[i] >> 16) & 0xFF;
    histBrightness[r]++;
    histBrightness[g]++;
    histBrightness[b]++;
    histR[r]++;
    histG[g]++;
    histB[b]++;
  }

  let maxBrightness = 0;
  for (let i = 0; i < 256; i++) {
    if (maxBrightness < histR[i]) {
      maxBrightness = histR[i]
    } else if (maxBrightness < histG[i]) {
      maxBrightness = histG[i]
    } else if (maxBrightness < histB[i]) {
      maxBrightness = histB[i]
    }
  }

  const canvas = document.getElementById('histogramOutput');
  const ctx = canvas.getContext('2d');
  let guideHeight = 8;
  let startY = (canvas.height - guideHeight);
  let dx = canvas.width / 256;
  let dy = startY / maxBrightness;
  ctx.lineWidth = dx;
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < 256; i++) {
    let x = i * dx;

    // Red
    ctx.strokeStyle = "rgba(220,0,0,0.5)";
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, startY - histR[i] * dy);
    ctx.closePath();
    ctx.stroke();
    // Green
    ctx.strokeStyle = "rgba(0,210,0,0.5)";
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, startY - histG[i] * dy);
    ctx.closePath();
    ctx.stroke();
    // Blue
    ctx.strokeStyle = "rgba(0,0,255,0.5)";
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, startY - histB[i] * dy);
    ctx.closePath();
    ctx.stroke();

    // Guide
    ctx.strokeStyle = 'rgb(' + i + ', ' + i + ', ' + i + ')';
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, canvas.height);
    ctx.closePath();
    ctx.stroke();
  }
}

