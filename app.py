import os
from flask import Flask, request, render_template

app = Flask(__name__)

LAW_DATABASE = {
    "1": "Itegeko Nshinga: Umuryango nyarwanda uteye imbere. IBIHANO: Ikintu cyose kinyuranyije na ryo nta gaciro kiba gifite.",
    "2": "Itegeko ry'Ibyaha: Ubujura buhanishwa igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande.",
    "3": "Itegeko ry'Umuryango: Ishyingirwa ryemewe ni irisezeranyijwe imbere y'ubuyobozi.",
    "4": "Itegeko ry'Umurimo: Integuza y'ukwezi imbere yo kwirukana umukozi.",
    "5": "Amategeko y'Umuhanda: Gutwara nta permis bihanishwa amande ya 50,000 Frw."
}

# URUBUGA RWA INTERNET (YAGUYE MURI INDEX.HTML NYAYO)
@app.route("/", methods=["GET"])
def dashboard():
    return render_template("index.html")

# --- USSD CORE SERVICE INYURA KURI AFRICA'S TALKING ---
@app.route("/ussd", methods=["POST"])
def ussd_handler():
    text_input = request.form.get("text", "")
    steps = text_input.split('*') if text_input else []
    
    if text_input == "":
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English"

    elif len(steps) == 1:
        lang = steps
        if lang in ["1", "2"]:
            menu = "CON Hitamo Icyiciro:\n1. Itegeko Nshinga\n2. Itegeko ry'Ibyaha\n3. Itegeko ry'Umuryango\n4. Itegeko ry'Umurimo\n5. Amategeko y'Umuhanda"
            return menu
        return "END Invalid input."

    elif len(steps) == 2:
        category = steps
        if category in LAW_DATABASE:
            return f"END {LAW_DATABASE[category]}"
        return "END Category Not Found."

    return "END System error."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
