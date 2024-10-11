
function checkStatus() {
    var suiteName = document.getElementById("suite-name").value;
    // Make an AJAX request to your Flask endpoint to get the status
    fetch('/check-status', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ suiteName: suiteName })
    })
    .then(response => response.json())
    .then(data => {
      var statusMessage = data.status;
      document.getElementById("status-message").innerHTML = statusMessage;
      document.getElementById("status-popup").style.display = "block";
    })
    .catch(error => console.error(error));
  }