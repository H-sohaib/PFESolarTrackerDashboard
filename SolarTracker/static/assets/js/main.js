reqURL = `${window.location.href}`
let modeButton = document.querySelector("#mode")
let currentMode = document.querySelector("#currentMode")

// Switch button for mode 
modeButton.onclick = () => {
  if (currentMode.innerHTML == "Automatic") {
    console.log("Manual Mode");
    currentMode.innerHTML = "Manual";
    // fetch update the mode
    fetch(reqURL, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        mode: 0
      }),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    // end fitch
  } else if (currentMode.innerHTML == "Manual") {
    console.log("Automatic Mode");
    currentMode.innerHTML = "Automatic";
    // fetch update the mode
    fetch(reqURL, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        mode: 1
      }),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
  }
}

// Servo control position part ****************************************
let range = document.querySelectorAll(".range-width");
let hSlider = range[0];
let vSlider = range[1];
let cardValue = document.querySelectorAll(".cardValue");
let body;

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
    console.log("ONchange done");
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
})

// positionne slider to current value in db on load of documents
window.onload = () => {
  hSlider.value = parseInt(cardValue[0].innerHTML)
  vSlider.value = parseInt(cardValue[1].innerHTML)
}

// update and show the LDR Recordes 
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
      values[0].innerHTML = data.ldrtr;
      values[1].innerHTML = data.ldrtl;
      values[2].innerHTML = data.ldrbr;
      values[3].innerHTML = data.ldrbl;
    })
  })
  // end fitch

}, interval);