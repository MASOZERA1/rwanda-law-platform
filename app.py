import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# GUHUZA DATABASE KURI PYTHON 3.14 NEZA NTA IKOSA
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://gadadmin:fvK3Te51qekk4DiFTIMBIUBEFbCx1QKx@://render.com"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# IMBONERAHAMWE Y'AMATEGEKO (LAW TABLE)
class Law(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    title_rw = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=False)
    content_rw = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False)

# IMBONERAHAMWE Y'ABAKENEYE UBUFASHA
class LegalAidRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    issue = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Pending Allocation")

# GUSUKA AMATEGEKO YOSE Y'U RWANDA MU BUBIKO (AUTO-SEEDING)
@app.before_request
def setup_database():
    try:
        db.create_all()
        if Law.query.count() < 7:
            db.session.query(Law).delete()
            laws = [
                Law(category="1", title_rw="Itegeko Nshinga rya Repubulika y'u Rwanda", title_en="Constitution of Rwanda", content_rw="Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 13: Agaciro k'umuntu ntibwogerwa. IBIHANO: Ikintu cyose kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).", content_en="Article 1: The Rwandan State is a Republic. Article 13: Inviolability of human dignity. SANCTION: Any law or act contrary to the Constitution is null and void.", tags="itegeko nshinga, constitution, uburenganzira"),
                Law(category="2", title_rw="Itegeko ry'Ibyaha n'Ibano (Penal Code)", title_en="Penal Code of Rwanda", content_rw="Ingingo ya 120 (Ubujura): IBIHANO: Igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande ari hagati ya 100,000 Frw na 500,000 Frw. Ingingo ya 166 (Gukubita/Gukomeretsa): IBIHANO: Igifungo cy'imyaka 5 kugeza kuri 7 n'amande.", content_en="Article 120 (Theft): PENALTY: Imprisonment of 6 months to 2 years and a fine of 100k to 500k RWF. Article 166 (Assault): PENALTY: Imprisonment of 5 to 7 years.", tags="ibyaha, penal, ubujura, theft, gukubita"),
                Law(category="3", title_rw="Itegeko ry'Umuryango n'Abantu (Family Law)", title_en="Law Governing Persons and Family", content_rw="Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. IBIHANO: Gusezerana mu buryo bwa magendu (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1.", content_en="Article 35 (Marriage): Only civil marriage is recognized. PENALTY: Illegal marriage or bigamy is punishable by 6 months to 1 year imprisonment.", tags="umuryango, family, gushyingirwa, marriage, izungura"),
                Law(category="4", title_rw="Itegeko ry'Umurimo mu Rwanda (Labor Law)", title_en="Law Governing Labor in Rwanda", content_rw="Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. IBIHANO: Umukoresha wishe iri tegeko ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (1 month notice salary damage).", content_en="Article 28: 1-month termination notice. PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.", tags="akazi, umurimo, contract, fire, kwirukanwa"),
                Law(category="5", title_rw="Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)", title_en="Traffic Regulations", content_rw="Ingingo ya 14 (Gutwara nta permis): IBIHANO: Amande ya 50,000 Frw no gufatira ikinyabiziga. Ingingo ya 22 (Kurenza umuvuduko/Speeding): IBIHANO: Amande y'amafaranga 25,000 Frw ako kanya.", content_en="Article 14 (No license): PENALTY: Fine of 50,000 RWF and vehicle impoundment. Article 22 (Speeding): PENALTY: Fixed traffic fine of 25,000 RWF.", tags="umuhanda, imodoka, permis, license, amande"),
                Law(category="6", title_rw="Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)", title_en="Cybercrimes Law", content_rw="Ingingo ya 32 (Kwinjira mu miterere ya mudasobwa y'undi): IBIHANO: Igifungo kuva ku mwaka 1 kugeza ku myaka 3 n'amande kuva kuri miliyoni 1 kugeza kuri miliyoni 3 Frw.", content_en="Article 32 (Unauthorized hacking/access): PENALTY: Imprisonment of 1 to 3 years and a fine of 1M to 3M RWF.", tags="internet, cybersecurity, cybercrime, mudasobwa"),
                Law(category="7", title_rw="Itegeko ry'Uburenganzira bw'Umwana (Child Protection)", title_en="Law on Child Protection", content_rw="Ingingo ya 18 (Gukubita umwana): Karabujijwe burundu. IBIHANO: Umuntu wese gukubita umwana bihannywe n'amategeko y'ibyaha, bishobora kuvamo igifungo kuva ku mezi 2 kugeza ku myaka 2.", content_en="Article 18 (Corporal punishment): Prohibited. PENALTY: Anyone who subjects a child to corporal punishment faces imprisonment of 2 months to 2 years.", tags="umwana, child, uburenganzira, protection")
            ]
            db.session.bulk_save_objects(laws)
            db.session.commit()
    except Exception:
        pass

# --- URUBUGA RW'AMAKURU MURI JSON REZA KUKURINDA IKOSA ---
@app.route("/", methods=["GET"])
def dashboard():
    try:
        all_laws = Law.query.all()
        laws_data = [{"title": l.title_rw, "content_rw": l.content_rw, "content_en": l.content_en} for l in all_laws]
        return jsonify({"status": "Live", "developer": "GAD MASOZERA", "message": "Rwanda Law App Server Running", "laws": laws_data})
    except Exception as e:
        return jsonify({"status": "Database Error", "error": str(e)})

# --- USSD CORE SERVICE ---
@app.route("/ussd", methods=["POST"])
def ussd_handler():
    text_input = request.form.get("text", "")
    phone_number = request.form.get("phoneNumber", "")
    steps = text_input.split('*') if text_input else []
    
    if text_input == "":
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English\n3. Quick Search"

    elif len(steps) == 1:
        lang = steps
        if lang in ["1", "2"]:
            try:
                all_laws = Law.query.all()
                menu = "CON Hitamo Icyiciro:\n" if lang == "1" else "CON Choose Category:\n"
                for law in all_laws:
                    title = law.title_rw if lang == "1" else law.title_en
                    menu += f"{law.category}. {title}\n"
                return menu
            except Exception:
                return "END Database Error."
        elif lang == "3":
            return "CON Andika ijambo ushaka (e.g., akazi, ibyaha, amande):"
        return "END Invalid input."

    elif len(steps) == 2 and steps == "3":
        keyword = steps.lower().strip()
        try:
            found_law = Law.query.filter(Law.tags.like(f"%{keyword}%")).first()
            if found_law:
                return f"CON {found_law.content_rw}\n\n9. Siga Ubufasha (Legal Aid)"
            return "END Ntacyo twabonye. / No results found."
        except Exception:
            return "END Error."

    elif len(steps) == 2:
        lang, category = steps, steps
        try:
            law = Law.query.filter_by(category=category).first()
            if law:
                content = law.content_rw if lang == "1" else law.content_en
                aid_opt = "\n\n9. Gusa Ubufasha" if lang == "1" else "\n\n9. Request Legal Aid"
                return f"CON {content}{aid_opt}"
            return "END Invalid."
        except Exception:
            return "END Error."

    elif len(steps) == 3 and steps == "9":
        try:
            new_req = LegalAidRequest(phone=phone_number, issue="Urgent Legal Support Needed")
            db.session.add(new_req)
            db.session.commit()
            return "END Murakoze. Umunyamategeko agiye kuguhamagara mukanya. / A lawyer will call you."
        except Exception:
            return "END Error."

    return "END System error."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
