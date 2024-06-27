document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("predict-btn")
    .addEventListener("click", function (e) {
      e.preventDefault();

      var fd = new FormData(document.querySelector("form"));

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/predict", true);
      document.getElementById("prediction-result").innerHTML =
        "Wait! Predicting Price.....";
      xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
          if (xhr.status == 200) {
            let data = JSON.parse(xhr.responseText);
            document.getElementById(
              "prediction-result"
            ).innerHTML = `Based on the provided information, the predicted price is: 💰 $ ${data.price.toFixed(
              2
            )}`;
          } else {
            document.getElementById("prediction-result").innerHTML =
              "Prediction failed. Please try again.";
          }
        }
      };

      xhr.send(fd);
    });

  document.getElementById("reset-btn").addEventListener("click", function () {
    document.getElementById("prediction-result").innerHTML = "";
    document.getElementById("prediction-form").reset();
  });
});
