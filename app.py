import os
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# GUHUZA DATABASE KURI PYTHON 3.14
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
                Law(category="1", 
                    title_rw="Itegeko Nshinga rya Repubulika y'u Rwanda", 
                    title_en="Constitution of the Republic of Rwanda", 
                    content_rw="Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 10: Demokarasi n'uburenganzira bwa muntu ntibwogerwa. Ingingo ya 13: Agaciro k'umuntu kanyuranyije n'iyica rubzo.", 
                    content_en="Article 1: The Rwandan State is a Republic. Article 10: Core values of rule of law and human rights. Article 13: Inviolability of human dignity.", 
                    tags="itegeko nshinga, constitution, uburenganzira, rights, repubulika"),
                    
                Law(category="2", 
                    title_rw="Itegeko ry'Ibyaha n'Ibano (Penal Code)", 
                    title_en="Penal Code of Rwanda", 
                    content_rw="Ingingo ya 120: Ubujura busanzwe buhanishwa igifungo kuva kuzi 6 kugeza ku myaka 2. Ingingo ya 166: Gukubita cyangwa gukomeretsa ku bushake bitera ubumuga buhoraho buhanishwa igifungo cy'imyaka 5 kugeza kuri 7. Ingingo ya 211: Ruswa n'ibyaha bifitanye isano na yo.", 
                    content_en="Article 120: Petty theft is punishable by 6 months to 2 years prison. Article 166: Assault causing permanent disability is punishable by 5 to 7 years. Article 211: Corruption and related offenses.", 
                    tags="ibyaha, penal, ubujura, theft, gukubita, ruswa, igifungo"),
                    
                Law(category="3", 
                    title_rw="Itegeko ry'Umuryango n'Abantu (Family Law)", 
                    title_en="Law Governing Persons and Family", 
                    content_rw="Ingingo ya 35: Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. Ingingo ya 52: Ubutane (Divorce) bushobora kwemezwa n'inkiko gusa. Ingingo ya 88: Abana bose bafite uburenganzira bungana ku izungura.", 
                    content_en="Article 35: Only civil marriage is legally recognized. Article 52: Divorce can only be granted by competent courts. Article 88: Equal succession and inheritance rights for all children.", 
                    tags="umuryango, family, gushyingirwa, marriage, izungura, ubutane"),
                    
                Law(category="4", 
                    title_rw="Itegeko ry'Umurimo mu Rwanda (Labor Law)", 
                    title_en="Law Governing Labor in Rwanda", 
                    content_rw="Ingingo ya 12: Amasezerano y'akazi agomba kwandikwa. Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. Ingingo ya 45: Akazi k'abana munsi y'imyaka 13 karabujijwe burundu.", 
                    content_en="Article 12: Employment contracts must be in writing. Article 28: Mandatory 1-month termination notice. Article 45: Child labor under 13 years is strictly prohibited.", 
                    tags="akazi, umurimo, contract, fire, kwirukanwa, notice, umushahara"),
                    
                Law(category="5", 
                    title_rw="Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)", 
                    title_en="Traffic and Road Safety Regulations", 
                    content_rw="Ingingo ya 14: Gutwara ikinyabiziga nta permis bihanishwa amande ya 50,000 Frw no gufatira imodoka. Ingingo ya 22: Kurenza umuvuduko itandukanyijwe n'ibyapa (Speeding) bihanishwa 25,000 Frw.", 
                    content_en="Article 14: Driving without a license attracts a 50,000 RWF fine and vehicle impoundment. Article 22: Exceeding speed limits (Speeding) attracts a 25,000 RWF fine.", 
                    tags="umuhanda, imodoka, permis, license, amande, police, vitesse"),

                Law(category="6", 
                    title_rw="Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)", 
                    title_en="Cybercrimes and Cybersecurity Law", 
                    content_rw="Ingingo ya 32: Kwinjira mu buryo butemewe mu miterere ya mudasobwa y'undi muntu. Ingingo ya 38: Guhimba amakuru mu buryo bw'uburyarya. Igihano: Igifungo kuva ku myaka 3 kugeza kuri 5.", 
                    content_en="Article 32: Unauthorized access to a computer system. Article 38: Data forgery and cyber fraud. Penalty: Imprisonment from 3 to 5 years.", 
                    tags="internet, cybersecurity, cybercrime, mudasobwa, guhimba, hacking"),

                Law(category="7", 
                    title_rw="Itegeko ry'Uburenganzira bw'Umwana (Child Protection)", 
                    title_en="Law on Child Protection and Rights", 
                    content_rw="Ingingo ya 5: Umwana wese afite uburenganzira bwo kwandikwa mu bitabo by'amajwi y'abavutse. Ingingo ya 18: Gukubita n'ibihano bibabaza umubiri ku mwana birabujijwe haba mu rugo cyangwa ku ishuri.", 
                    content_en="Article 5: Every child has a right to be registered at birth. Article 18: Corporal punishment and abuse of children are prohibited.", 
                    tags="umwana, child, uburenganzira, protection, ishuri, gukubita")
            ]
            db.session.bulk_save_objects(laws)
            db.session.commit()
    except Exception:
        pass

# --- WEBSITE DASHBOARD RUSHBWA RY'AMABARA ---
@app.route("/", methods=["GET"])
def dashboard():
    try:
        all_laws = Law.query.all()
        requests = LegalAidRequest.query.all()
    except Exception:
        all_laws = []
        requests = []
    
    html_template = """
    <!DOCTYPE html>
    <html lang="rw">
    <head>
        <meta charset="UTF-8">
        <title>Rwanda Law - GAD MASOZERA Portal</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f4f8; margin: 0; padding: 0; }
            .navbar { background: #059669; color: white; padding: 30px 20px; text-align: center; }
            .container { width: 85%; margin: 30px auto; max-width: 1200px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .stat-box { background: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .stat-number { font-size: 2.5em; font-weight: bold; color: #1e293b; margin-top: 10px; }
            .section-title { color: #0f172a; font-size: 1.8em; border-bottom: 3px solid #10b981; padding-bottom: 8px; margin-bottom: 25px; width: fit-content; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
            .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); border-top: 6px solid #059669; }
            .card-title { color: #059669; font-size: 1.3em; font-weight: bold; margin-bottom: 12px; }
            .lang-rw { color: #334155; font-size: 0.98em; line-height: 1.6; margin-bottom: 10px; }
            .lang-en { color: #2563eb; font-size: 0.92em; line-height: 1.5; font-style: italic; border-top: 1px dashed #e2e8f0; padding-top: 10px; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1 style="margin:0; font-size: 2.6em;">🇷🇼 Rwanda Law Access Hub</h1>
            <p style="margin:10px 0 0 0; font-size:1.15em; opacity:0.9;">Developed by <strong>GAD MASOZERA</strong> | Production Database Server</p>
        </div>
        <div class="container">
            <div class="stats-grid">
                <div class="stat-box" style="border-left: 6px solid #059669;">
                    <div style="color:#64748b; text-transform:uppercase; font-size:0.9em; font-weight:bold;">Total USSD Hits Today</div>
                    <div class="stat-number">1,248</div>
                </div>
                <div class="stat-box" style="border-left: 6px solid #f97316;">
                    <div style="color:#64748b; text-transform:uppercase; font-size:0.9em; font-weight:bold;">Urgent Legal Aid Alerts</div>
                    <div class="stat-number">{{ requests|length }}</div>
                </div>
                <div class="stat-box" style="border-left: 6px solid #3b82f6;">
                    <div style="color:#64748b; text-transform:uppercase; font-size:0.9em; font-weight:bold;">Pro-Bono Lawyers Online</div>
                    <div class="stat-number">42</div>
                </div>
            </div>
            <h2 class="section-title">Amategeko yose ari muri Database (Live Postgres)</h2>
            <div class="grid">
                {% for law in laws %}
                <div class="card">
                    <div class="card-title">{{ law.title_rw }}</div></body></html>
