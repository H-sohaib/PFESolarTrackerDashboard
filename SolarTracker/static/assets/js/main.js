let reqURL = `${window.location.href}`;
let modeButton = document.querySelector("#mode");
let currentMode = document.querySelector("#currentMode");
let refreshedData;
// Servo Declaration
let range = document.querySelectorAll(".range-width");
let hSlider = range[0];
let vSlider = range[1];
let cardValue = document.querySelectorAll(".cardValue");
let body;

// Servo control position part ****************************************

// Horizontale Servo -----------------------
hSlider.oninput = () => {
  cardValue[0].innerHTML = hSlider.value;
}
// Vertical Servo ------------------------------------
vSlider.oninput = () => {
  cardValue[1].innerHTML = vSlider.value;
}

// Send slider stat
range.forEach((r) => {
  r.onchange = () => {
    if (mode == 0) {
      console.log("Send slider value !!");
      if (r.classList.contains("hori")) {
        console.log("Hori servo");
        body = {
          Hposi: r.value
        };
      } else {
        console.log("Verti servo");
        body = {
          Vposi: r.value
        };
      }

      // r.children
      // start fitch 
      fetch(reqURL, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(body),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
      })
      // end fitch
    }
  }
})

// positionne slider to current value in db on load of documents
window.onload = () => {
  hSlider.value = parseInt(cardValue[0].innerHTML)
  vSlider.value = parseInt(cardValue[1].innerHTML)
}

// elements need refresh without reload -----------*
// LDR Value & Position Error & Servo position in auto mode
let left, right, topr, bottom;
let moyennIndicators = document.querySelectorAll(".moyenne")
let values = document.querySelectorAll(".ldr-value");
let interval = 1000;
setInterval(() => {
  // start fitch 
  fetch(reqURL, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({}),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    }),
  }).then((response) => {
    response.json().then((data) => {
      // LDR Part
      values[0].innerHTML = data.ldrtr;
      values[1].innerHTML = data.ldrtl;
      values[2].innerHTML = data.ldrbr;
      values[3].innerHTML = data.ldrbl;
      left = (data.ldrtl + data.ldrbl) / 2;
      right = (data.ldrtr + data.ldrbr) / 2;
      topr = (data.ldrtr + data.ldrtl) / 2;
      bottom = (data.ldrbr + data.ldrbl) / 2;
      moyennIndicators[0].innerHTML = topr - bottom;
      moyennIndicators[1].innerHTML = right - left;
      // end LDR part
      // Position Part
      refreshedData = data
      // console.log(`mode is : ${data.mode}`);
      if (currentMode.innerHTML == "Automatic") {
        hSlider.value = 0;
        vSlider.value = 0;
        cardValue[0].innerHTML = data.Hposi;
        cardValue[1].innerHTML = data.Vposi;
      }
      // end Position Part
    })

  }) // End Reponse 
  // end fitch

}, interval);



// ONCLICK Switch button for mode  
modeButton.onclick = () => {
  let modeNum;
  if (currentMode.innerHTML == "Automatic") {
    // console.log("Manual Mode");
    currentMode.innerHTML = "Manual";
    modeNum = 0;
    // return slider to indicate the value when swotch to manuel again
    hSlider.value = refreshedData.Hposi;
    vSlider.value = refreshedData.Vposi;

  } else if (currentMode.innerHTML == "Manual") {
    // console.log("Automatic Mode");
    currentMode.innerHTML = "Automatic";
    modeNum = 1;
  }
  // start fetch update the mode
  fetch(reqURL, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({
      mode: modeNum
    }),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  // end fitch
}