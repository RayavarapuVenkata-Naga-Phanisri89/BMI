function calculateBMI() {

    let name = document.getElementById("name").value;
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;

    if (name === "" || height === "" || weight === "") {
        alert("Please enter Name, Height and Weight.");
        return;
    }

    fetch("/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            height: height,
            weight: weight
        })
    })

    .then(response => response.json())

    .then(data => {


        // BMI Results
        document.getElementById("bmi").innerHTML = data.bmi;
        document.getElementById("status").innerHTML = data.status;
        document.getElementById("recommendation").innerHTML = data.recommendation;



        // Recommended Foods
        let foodHTML = "<h3>🍽️ Recommended Foods</h3><ul>";

        data.foods.forEach(function(food) {
            foodHTML += "<li>" + food + "</li>";
        });

        foodHTML += "</ul>";

        // Add calories without disturbing design
        foodHTML += "<h3>🔥 Estimated Calories</h3>";
        foodHTML += "<p>" + data.total_calories + "</p>";

        document.getElementById("foods").innerHTML = foodHTML;



        // BMI Indicator Movement
        let indicator = document.getElementById("indicator");

        if (data.bmi < 18.5) {
            indicator.style.left = "12%";
        }
        else if (data.bmi < 25) {
            indicator.style.left = "37%";
        }
        else if (data.bmi < 30) {
            indicator.style.left = "62%";
        }
        else {
            indicator.style.left = "87%";
        }




        // Health Image + Score

        let healthImage = document.getElementById("healthImage");


        if (data.status === "Underweight") {

            healthImage.src = "/static/images/underweight.jpg";

            document.getElementById("healthScore").innerHTML = "60/100";

            document.getElementById("scoreMessage").innerHTML =
            "⚠️ Your health score is below average. Gain healthy weight.";

        }


        else if (data.status === "Normal Weight") {

            healthImage.src = "/static/images/normal.jpg";

            document.getElementById("healthScore").innerHTML = "100/100";

            document.getElementById("scoreMessage").innerHTML =
            "🎉 Excellent! Keep maintaining your healthy lifestyle.";

        }


        else if (data.status === "Overweight") {

            healthImage.src = "/static/images/overweight.jpg";

            document.getElementById("healthScore").innerHTML = "75/100";

            document.getElementById("scoreMessage").innerHTML =
            "🙂 Good, but losing some weight can improve your health.";

        }


        else {

            healthImage.src = "/static/images/obese.jpg";

            document.getElementById("healthScore").innerHTML = "50/100";

            document.getElementById("scoreMessage").innerHTML =
            "⚠️ Your health score is low. Focus on improving your lifestyle.";

        }



    })


    .catch(error => {

        console.error(error);

        alert("Something went wrong!");

    });

}





function downloadReport() {

    let name = document.getElementById("name").value;
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;


    fetch("/download_report", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,
            height: height,
            weight: weight

        })

    })


    .then(response => response.blob())


    .then(blob => {

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "BMI_Report.pdf";

        a.click();


        window.URL.revokeObjectURL(url);

    })


    .catch(error => {

        console.error(error);

        alert("Unable to download report.");

    });

}