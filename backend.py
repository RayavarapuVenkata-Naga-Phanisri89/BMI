from flask import request, jsonify, send_file
from reportlab.pdfgen import canvas


# Food Recommendations
food_recommendations = {

    "Underweight": {
        "foods": [
            "Eggs - 2 (140 kcal)",
            "Banana - 1 (105 kcal)",
            "Milk - 1 Glass (120 kcal)",
            "Rice - 1 Cup (200 kcal)",
            "Chicken - 100g (165 kcal)",
            "Nuts - 30g (170 kcal)"
        ],
        "total": "Approx 900 kcal"
    },

    "Normal Weight": {
        "foods": [
            "Green Vegetables - 1 Bowl (80 kcal)",
            "Apple - 1 (95 kcal)",
            "Brown Rice - 1 Cup (215 kcal)",
            "Fish - 100g (150 kcal)",
            "Milk - 1 Glass (120 kcal)",
            "Nuts - 30g (170 kcal)"
        ],
        "total": "Approx 830 kcal"
    },

    "Overweight": {
        "foods": [
            "Salad - 1 Bowl (40 kcal)",
            "Apple - 1 (95 kcal)",
            "Broccoli - 1 Bowl (55 kcal)",
            "Oats - 40g (150 kcal)",
            "Green Tea (2 kcal)"
        ],
        "total": "Approx 342 kcal"
    },

    "Obese": {
        "foods": [
            "Broccoli (55 kcal)",
            "Spinach (40 kcal)",
            "Tomato (22 kcal)",
            "Apple (95 kcal)",
            "Oats (150 kcal)",
            "Grilled Fish (150 kcal)"
        ],
        "total": "Approx 512 kcal"
    }

}


def get_bmi_details(bmi):

    if bmi < 18.5:
        status = "Underweight"
        recommendation = "Eat healthy foods like milk, eggs, fruits and nuts to gain weight."

    elif bmi < 25:
        status = "Normal Weight"
        recommendation = "Maintain your healthy diet and continue regular exercise."

    elif bmi < 30:
        status = "Overweight"
        recommendation = "Reduce junk food, do cardio and drink plenty of water."

    else:
        status = "Obese"
        recommendation = "Follow a healthy diet and regular exercise. Consult a healthcare professional if needed."

    foods = food_recommendations[status]["foods"]
    total = food_recommendations[status]["total"]

    return status, recommendation, foods, total


# ---------------- BMI API ---------------- #

def calculate_bmi():

    data = request.get_json()

    height = float(data["height"]) / 100
    weight = float(data["weight"])

    bmi = round(weight / (height * height), 2)

    status, recommendation, foods, total = get_bmi_details(bmi)

    return jsonify({

        "bmi": bmi,
        "status": status,
        "recommendation": recommendation,
        "foods": foods,
        "total_calories": total

    })


# ---------------- PDF Report ---------------- #

def download_report():

    data = request.get_json()

    name = data.get("name", "User")
    height = float(data["height"])
    weight = float(data["weight"])

    bmi = round(weight / ((height / 100) ** 2), 2)

    status, recommendation, foods, total = get_bmi_details(bmi)

    filename = "BMI_Report.pdf"

    pdf = canvas.Canvas(filename)

    pdf.setTitle("BMI Health Report")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "BMI HEALTH REPORT")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(80, 760, f"Name : {name}")
    pdf.drawString(50, 735, f"Height : {height} cm")
    pdf.drawString(50, 710, f"Weight : {weight} kg")
    pdf.drawString(50, 685, f"BMI : {bmi}")
    pdf.drawString(50, 660, f"Status : {status}")

    pdf.drawString(50, 630, "Recommendation:")
    pdf.drawString(70, 610, recommendation)

    pdf.drawString(50, 575, "Recommended Foods:")

    y = 555

    for food in foods:
        pdf.drawString(70, y, food)
        y -= 18

    pdf.drawString(50, y - 10, f"Total Calories : {total}")

    pdf.save()

    return send_file(filename, as_attachment=True)