    from flask import Flask, request, render_template
import os
import pandas as pd

app = Flask(__name__)

# Existing translations for tips
translations = {
    "Not possible, please check with your ownership.": {
        "kn": "ಸಾಧ್ಯವಿಲ್ಲ, ದಯವಿಟ್ಟು ನಿಮ್ಮ ಮಾಲೀಕತ್ವವನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "ta": "சாத்தியமில்லை, உங்கள் உரிமையுடன் சரிபார்க்கவும்.",
        "te": "సాధ్యం కాదు, దయచేసి మీ యాజమాన్యంతో తనిఖీ చేయండి.",
        "ml": "സാധ്യമല്ല, ദയവായി നിങ്ങളുടെ ഉടമസ്ഥാവകാശം പരിശോധിക്കുക.",
        "hi": "संभव नहीं है, कृपया अपने स्वामित्व से जाँच करें।",
        "fr": "Pas possible, veuillez vérifier avec votre propriétaire.",
        "es": "No es posible, verifique con su propiedad."
    },
    "Low mileage: Check tire pressure and avoid idling.": {
        "kn": "ಕಡಿಮೆ ಮೈಲೇಜ್: ಟೈರ್ ಒತ್ತಡವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿರುದ್ಯೋಗವನ್ನು ತಪ್ಪಿಸಿ.",
        "ta": "குறைந்த மைலேஜ்: டயர் அழுத்தத்தை சரிபார்த்து, இட்லிங் தவிர்க்கவும்.",
        "te": "తక్కువ మైలేజ్: టైర్ ఒత్తిడిని తనిఖీ చేసి, ఇడ్లింగ్ నివారించండి.",
        "ml": "കുറഞ്ഞ മൈലേജ്: ടയർ മർദ്ദം പരിശോധിച്ച്, ഇട്ലിംഗ് ഒഴിവാക്കുക.",
        "hi": "कम माइलेज: टायर का दबाव जांचें और इंजन को बेकार न चलाएं।",
        "fr": "Faible kilométrage : vérifiez la pression des pneus et évitez le ralenti.",
        "es": "Bajo kilometraje: revise la presión de las llantas y evite el ralentí."
    },
    "Moderate mileage: Maintain steady speeds and reduce AC usage.": {
        "kn": "ಮಧ್ಯಮ ಮೈಲೇಜ್: ಸ್ಥಿರ ವೇಗವನ್ನು ಕಾಯ್ದುಕೊಳ್ಳಿ ಮತ್ತು ಎಸಿ ಬಳಕೆಯನ್ನು ಕಡಿಮೆ ಮಾಡಿ.",
        "ta": "மிதமான மைலேஜ்: நிலையான வேகத்தை பராமரித்து, ஏசி பயன்பாட்டை குறைக்கவும்.",
        "te": "మధ్యస్థ మైలేజ్: స్థిరమైన వేగాలను నిర్వహించి, ఏసీ వినియోగాన్ని తగ్గించండి.",
        "ml": "മിതമായ മൈലേജ്: സ്ഥിരമായ വേഗത പാലിച്ച്, എസി ഉപയോഗം കുറയ്ക്കുക.",
        "hi": "मध्यम माइलेज: स्थिर गति बनाए रखें और एसी का उपयोग कम करें।",
        "fr": "Kilométrage modéré : maintenez des vitesses stables et réduisez l'utilisation de la climatisation.",
        "es": "Kilometraje moderado: mantenga velocidades constantes y reduzca el uso del aire acondicionado."
    },
    "High mileage: Great job! Keep servicing regularly.": {
        "kn": "ಹೆಚ್ಚು ಮೈಲೇಜ್: ಉತ್ತಮ ಕೆಲಸ! ನಿಯಮಿತವಾಗಿ ಸೇವೆ ಮಾಡುತ್ತಿರಿ.",
        "ta": "அதிக மைலேஜ்: சிறந்த வேலை! முறையாக சேவை செய்யவும்.",
        "te": "అధిక మైలేజ్: గొప్ప పని! క్రమం తప్పకుండా సేవ చేయండి.",
        "ml": "ഉയർന്ന മൈലേജ്: നല്ല ജോലി! സ്ഥിരമായി സർവീസ് ചെയ്യുക.",
        "hi": "उच्च माइलेज: बहुत अच्छा! नियमित रूप से सर्विस करते रहें।",
        "fr": "Haut kilométrage : excellent travail ! Continuez l'entretien régulier.",
        "es": "Alto kilometraje: ¡Buen trabajo! Siga realizando mantenimientos regularmente."
    }
}

# NEW: translations for form labels
form_labels = {
    "mileage": {"en":"Enter Mileage","kn":"ಮೈಲೇಜ್ ನಮೂದಿಸಿ","ta":"மைலேஜை உள்ளிடவும்","hi":"माइलेज दर्ज करें"},
    "language": {"en":"Choose Language","kn":"ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ","ta":"மொழியைத் தேர்ந்தெடுக்கவும்","hi":"भाषा चुनें"},
    "driver_id": {"en":"Driver ID","kn":"ಚಾಲಕ ಐಡಿ","ta":"ஓட்டுநர் ஐடி","hi":"ड्राइवर आईडी"},
    "route_id": {"en":"Route / Place in Bengaluru","kn":"ಮಾರ್ಗ / ಬೆಂಗಳೂರು ಸ್ಥಳ","ta":"பாதை / பெங்களூரு இடம்","hi":"मार्ग / बेंगलुरु स्थान"},
    "fuel_type": {"en":"Fuel Type","kn":"ಇಂಧನ ಪ್ರಕಾರ","ta":"எரிபொருள் வகை","hi":"ईंधन प्रकार"},
    "idling_time": {"en":"Idling Time (mins)","kn":"ನಿಷ್ಕ್ರಿಯ ಸಮಯ (ನಿಮಿಷಗಳು)","ta":"இட்லிங் நேரம் (நிமிடங்கள்)","hi":"इंजन बंद समय (मिनट)"},
    "avg_speed": {"en":"Avg Speed (km/h)","kn":"ಸರಾಸರಿ ವೇಗ (ಕಿ.ಮೀ/ಗಂ)","ta":"சராசரி வேகம் (கிமீ/மணி)","hi":"औसत गति (किमी/घं)"}
}

# --- Eco-Driver Index Helper Functions (NEW) ---
def calculate_mileage(distance_km, fuel_l):
    return distance_km / fuel_l if fuel_l > 0 else 0

def calculate_carbon_intensity_from_mileage(mileage_km_per_l, emission_factor_g_per_l):
    """
    Carbon intensity in grams CO2-equivalent per km.
    emission_factor_g_per_l is grams per liter for the fuel.
    mileage_km_per_l is km per liter.
    So: g_per_km = emission_factor_g_per_l / mileage_km_per_l
    """
    if mileage_km_per_l and mileage_km_per_l > 0:
        return emission_factor_g_per_l / mileage_km_per_l
    return 0

def calculate_composite_score(mileage, idling, speed_var):
    # Define expected ranges
    mileage_range = (10, 25)       # km/L, higher is better
    idling_range = (0, 60)         # minutes, lower is better
    optimal_speed_low, optimal_speed_high = 30, 50

    # Normalize mileage (higher is better)
    mileage_score = (mileage - mileage_range[0]) / (mileage_range[1] - mileage_range[0])
    mileage_score = max(0, min(1, mileage_score))

    # Normalize idling (lower is better → invert)
    idling_score = 1 - (idling - idling_range[0]) / (idling_range[1] - idling_range[0])
    idling_score = max(0, min(1, idling_score))

    # Speed scoring: best between 30–50 km/h
    if optimal_speed_low <= speed_var <= optimal_speed_high:
        speed_score = 1.0
    else:
        if speed_var < optimal_speed_low:
            deviation = optimal_speed_low - speed_var
        else:
            deviation = speed_var - optimal_speed_high
        max_dev = 70  # assume beyond 70 km/h deviation is worst
        speed_score = max(0, 1 - deviation / max_dev)

    # Weighted average → scale to 0–50
    composite = (mileage_score + idling_score + speed_score) / 3 * 50
    return int(round(composite))

def fuel_recommendation(mileage):
    if mileage <= 0 or mileage > 1000000:
        return "Not possible, please check with your ownership."
    elif mileage < 15:
        return "Low mileage: Check tire pressure and avoid idling."
    elif 15 <= mileage <= 20:
        return "Moderate mileage: Maintain steady speeds and reduce AC usage."
    else:
        return "High mileage: Great job! Keep servicing regularly."

# File paths (relative to this script)
BASE_DIR = os.path.dirname(__file__)
TRANSIT_CSV = os.path.join(BASE_DIR, "transit_data.csv")
DRIVER_PERF_CSV = os.path.join(BASE_DIR, "driver_performance.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    tip = ""
    translated_tip = ""
    lang = "en"
    labels = {k:v["en"] for k,v in form_labels.items()}  # default English
    record = None

    if request.method == "POST":
        lang = request.form.get("language","en")
        labels = {k:v.get(lang,v["en"]) for k,v in form_labels.items()}

        try:
            # The form field "mileage" is interpreted as km per liter (km/L)
            mileage_km_per_l = float(request.form["mileage"])
            tip = fuel_recommendation(mileage_km_per_l)
            translated_tip = translations.get(tip, {}).get(lang, tip)

            driver_id = request.form.get("driver_id","Unknown")
            route_id = request.form.get("route_id","Unknown")
            fuel_type = request.form.get("fuel_type","Diesel")
            idling_time = float(request.form.get("idling_time",0))
            avg_speed = float(request.form.get("avg_speed",0))

            emission_factors = {"Diesel":2640, "CNG":2030, "Petrol":2392}  # g per liter
            emission_factor = emission_factors.get(fuel_type,2640)

            # Carbon intensity: g CO2e per km
            carbon_intensity = calculate_carbon_intensity_from_mileage(mileage_km_per_l, emission_factor)
            composite_score = calculate_composite_score(mileage_km_per_l, idling_time, avg_speed)

            record = {
                "Driver_ID": driver_id,
                "Route_ID": route_id,
                "Fuel_Type": fuel_type,
                "Distance_Covered_km_equiv": None,  # kept for compatibility if needed
                "Idling_Time_Mins": idling_time,
                "Avg_Speed_kmh": avg_speed,
                "Mileage_km_per_l": mileage_km_per_l,
                "Carbon_Intensity_g_per_km": carbon_intensity,
                "Composite_Eco_Score": composite_score,
                "Tip": tip,
                "Translated_Tip": translated_tip
            }

            # --- Write to transit_data.csv using pandas ---
            df_record = pd.DataFrame([record])
            if os.path.exists(TRANSIT_CSV) and os.path.getsize(TRANSIT_CSV) > 0:
                df_record.to_csv(TRANSIT_CSV, mode="a", header=False, index=False)
            else:
                df_record.to_csv(TRANSIT_CSV, index=False)

            # --- Export to driver_performance.csv for dashboard using pandas ---
            # Keep the same schema so dashboard can read it directly
            if os.path.exists(DRIVER_PERF_CSV) and os.path.getsize(DRIVER_PERF_CSV) > 0:
                df_record.to_csv(DRIVER_PERF_CSV, mode="a", header=False, index=False)
            else:
                df_record.to_csv(DRIVER_PERF_CSV, index=False)

        except ValueError:
            tip = "Not possible, please check with your ownership."
            translated_tip = translations.get(tip, {}).get(lang, tip)

    return render_template(
        "index.html",
        tip=tip,
        translated_tip=translated_tip,
        labels=labels,
        lang=lang,
        record=record
    )

if __name__ == "__main__":
    # Run on all interfaces so others can access it
    app.run(host="0.0.0.0", port=5000, debug=True)
