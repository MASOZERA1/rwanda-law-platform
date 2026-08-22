import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# UBUBIKO BW'AMATEGEKO Y'U RWANDA N'IBIHANO (PYTHON DICTIONARY)
LAW_DATABASE = {
    "1": {
        "title_rw": "Itegeko Nshinga rya Repubulika y'u Rwanda",
        "title_en": "Constitution of Rwanda",
        "content_rw": "Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 13: Agaciro k'umuntu ntibwogerwa. IBIHANO: Ikintu cyose kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).",
        "content_en": "Article 1: The Rwandan State is a Republic. Article 13: Inviolability of human dignity. SANCTION: Any law or act contrary to the Constitution is null and void.",
        "tags": "itegeko nshinga, constitution, uburenganzira"
    },
    "2": {
        "title_rw": "Itegeko ry'Ibyaha n'Ibano (Penal Code)",
        "title_en": "Penal Code of Rwanda",
        "content_rw": "Ingingo ya 120 (Ubujura): IBIHANO: Igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande ari hagati ya 100,000 Frw na 500,000 Frw. Ingingo ya 166 (Gukubita/Gukomeretsa): IBIHANO: Igifungo cy'imyaka 5 kugeza kuri 7 n'amande.",
        "content_en": "Article 120 (Theft): PENALTY: Imprisonment of 6 months to 2 years and a fine of 100k to 500k RWF. Article 166 (Assault): PENALTY: Imprisonment of 5 to 7 years.",
        "tags": "ibyaha, penal, ubujura, theft, gukubita"
    },
    "3": {
        "title_rw": "Itegeko ry'Umuryango n'Abantu (Family Law)",
        "title_en": "Law Governing Persons and Family",
        "content_rw": "Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. IBIHANO: Gusezerana mu buryo bwa magendu (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1.",
        "content_en": "Article 35 (Marriage): Only civil marriage is recognized. PENALTY: Illegal marriage or bigamy is punishable by 6 months to 1 year imprisonment.",
        "tags": "umuryango, family, gushyingirwa, marriage, izungura"
    },
    "4": {
        "title_rw": "Itegeko ry'Umurimo mu Rwanda (Labor Law)",
        "title_en": "Law Governing Labor in Rwanda",
        "content_rw": "Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. IBIHANO: Umukoresha wishe iri tegeko ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (1 month notice salary damage).",
        "content_en": "Article 28: 1-month termination notice. PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.",
        "tags": "akazi, umurimo, contract, fire, kwirukanwa"
    },
    "5": {
        "title_rw": "Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)",
        "title_en": "Traffic Regulations",
        "content_rw": "Ingingo ya 14 (Gutwara nta permis): IBIHANO: Amande ya 50,000 Frw no gufatira ikinyabiziga. Ingingo ya 22 (Kurenza umuvuduko/Speeding): IBIHANO: Amande y'amafaranga 25,000 Frw ako kanya.",
        "content_en": "Article 14 (No license): PENALTY: Fine of 50,000 RWF and vehicle impoundment. Article 22 (Speeding): PENALTY: Fixed traffic fine of 25,000 RWF.",
        "tags": "umuhanda, imodoka, permis, license, amande"
    },
    "6": {
        "title_rw": "Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)",
        "title_en": "Cybercrimes Law",
        "content_rw": "Ingingo ya 32 (Kwinjira mu miterere ya mudasobwa y'undi): IBIHANO: Igifungo kuva ku mwaka 1 kugeza ku myaka 3 n'amande kuva kuri miliyoni 1 kugeza kuri miliyoni 3 Frw.",
        "content_en": "Article 32 (Unauthorized hacking/access): PENALTY: Imprisonment of 1 to 3 years and a fine of 1M to 3M RWF.",
        "tags": "internet, cybersecurity, cybercrime, mudasobwa"
    },
    "7": {
        "title_rw": "Itegeko ry'Uburenganzira bw'Umwana (Child Protection)",
        "title_en": "Law on Child Protection",
        "content_rw": "Ingingo ya 18 (Gukubita umwana): Karabujijwe burundu. IBIHANO: Umuntu wese gukubita umwana bihannywe n'amategeko y'ibyaha, bishobora kuvamo igifungo kuva ku mezi 2 kugeza ku myaka 2.",
        "content_en": "Article 18 (Corporal punishment): Prohibited. PENALTY: Anyone who subjects a child to corporal punishment faces imprisonment of 2 months to 2 years.",
        "tags": "umwana, child, uburenganzira, protection"
    }
}

# --- WEBSITE DASHBOARD NYAYO IFITE AMABARA —--
@app.route("/", methods=["GET"])
def dashboard():
    laws_html = ""
    for k, v in LAW_DATABASE.items():
        laws_html += f"""
        <div style="background: white; padding: 25px; margin-bottom: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); border-left: 6px solid #059669;">
            <h3 style="color: #059669; margin-top: 0; font-size: 1.3em; font-family: sans-serif;">{k}. {v['title_rw']} / {v['title_en']}</h3>
            <p style="color: #334155; font-size: 1em; line-height: 1.6; margin: 10px 0; font-family: sans-serif;"><strong>Kinyarwanda:</strong> {v['content_rw']}</p>
            <p style="color: #2563eb; font-size: 0.95em; line-height: 1.5; font-style: italic; border-top: 1px dashed #e2e8f0; padding-top: 10px; margin-bottom: 0; font-family: sans-serif;"><strong>English:</strong> {v['content_en']}</p>
        </div>
        """
        
    html_template = f"""
    <!DOCTYPE html>
    <html lang="rw">
    <head>
        <meta charset="UTF-8">
        <title>Rwanda Law - GAD MASOZERA Portal</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f0f4f8; margin: 0; padding: 0;">
        <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 35px 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h1 style="margin: 0; font-size: 2.6em; letter-spacing: 1px;">🇷🇼 Rwanda Law Access Hub</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.95;">Developed by <strong style="text-decoration: underline;">GAD MASOZERA</strong> | Official Production Server</p>
        </div>
        
        <div style="width: 85%; margin: 40px auto; max-width: 1000px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px;">
                <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #059669;">
                    <div style="color: #64748b; text-transform: uppercase; font-size: 0.85em; font-weight: bold;">USSD Platform</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: #1e293b; margin-top: 5px;">*384*61254#</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #f97316;">
                    <div style="color: #64748b; text-transform: uppercase; font-size: 0.85em; font-weight: bold;">System Status</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: #059669; margin-top: 5px;">Active / Live</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #3b82f6;">
                    <div style="color: #64748b; text-transform: uppercase; font-size: 0.85em; font-weight: bold;">Law Categories</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: #1e293b; margin-top: 5px;">7 Full Codes</div>
                </div>
            </div>

            <h2 style="color: #0f172a; font-size: 1.8em; border-bottom: 3px solid #10b981; padding-bottom: 8px; width: fit-content; margin-bottom: 30px;">Amategeko yose n'Ibihano birimo (Live Database)</h2>
            
            <div>
                {laws_html}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

# --- USSD CORE SERVICE ---
@app.route("/ussd", methods=["POST"])
def ussd_handler():
    text_input = request.form.get("text", "")
    steps = text_input.split('*') if text_input else []
    
    if text_input == "":
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English\n3. Quick Search"

    elif len(steps) == 1:
        lang = steps
        if lang in ["1", "2"]:
            menu = "CON Hitamo Icyiciro:\n" if lang == "1" else "CON Choose Category:\n"
            for k, v in LAW_DATABASE.items():
                title = v["title_rw"] if lang == "1" else v["title_en"]
                menu += f"{k}. {title}\n"
            return menu
        elif lang == "3":
            return "CON Andika ijambo ushaka (e.g., akazi, ibyaha, amande):"
        return "END Invalid input."

    elif len(steps) == 2 and steps == "3":
        keyword = steps.lower().strip()
        for k, v in LAW_DATABASE.items():
            if keyword in v["tags"]:
                return f"CON {v['content_rw']}\n\n9. Siga Ubufasha (Legal Aid)"
        return "END Ntacyo twabonye. / No results found."

    elif len(steps) == 2:
        lang, category = steps, steps
        if category in LAW_DATABASE:
            v = LAW_DATABASE[category]
            content = v["content_rw"] if lang == "1" else v["content_en"]
            aid_opt = "\n\n9. Gusa Ubufasha" if lang == "1" else "\n\n9. Request Legal Aid"
            return f"CON {content}{aid_opt}"
        return "END Invalid Category."

    elif len(steps) == 3 and steps == "9":
        return "END Murakoze. Umunyamategeko agiye kuguhamagara mukanya. / A lawyer will call you."

    return "END System error."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
