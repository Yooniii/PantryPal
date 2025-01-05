let btn = document.getElementsByClassName("collapsible");

for (i = 0; i < btn.length; i++) {
  btn[i].addEventListener("click", function()  {
    this.classList.toggle("active");

    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

function waiting() {
    const waitingDiv = document.createElement('div');
    waitingDiv.innerHTML = `
    <div class="waiting">
        <img class="waiting-img" src="static/loading_icon.gif"/>
    </div>
    <div class="waiting">
        <h2>AI is thinking ...</h2>
    </div>
    `;
    document.body.appendChild(waitingDiv);

    waitingDiv.style.textAlign = 'center';
    const waitingImg = waitingDiv.querySelector('.waiting-img');
    waitingImg.style.marginTop = '100px';
    waitingImg.style.width = '100px'; 
    waitingImg.style.height = '100px';
}
