import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Guhuza na ya Database ya Render twafunguye
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://gadadmin:fvK3Te51qekk4DiFTIMBIUBEFbCx1QKx@://render.com"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Law(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    title_rw = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=False)
    content_rw = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False)

def seed_all_rwanda_laws():
    with app.app_context():
        # Guhanagura amategeko make yari arimo mbere ngo twandikemo amashya yose
        db.session.query(Law).delete()
        
        AMATEGEKO_Y_URWANDA = [
            Law(category="1", 
                title_rw="Itegeko Nshinga rya Repubulika y'u Rwanda", 
                title_en="Constitution of the Republic of Rwanda", 
                content_rw="Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 10: Demokarasi n'uburenganzira bwa muntu ntibwogerwa. Ingingo ya 13: Agaciro k'umuntu kanyuranyije n'iyica rubzo.", 
                content_en="Article 1: The Rwandan State is a Republic. Article 10: Core values of rule of law and human rights. Article 13: Inviolability of human dignity.", 
                tags="itegeko nshinga, constitution, uburenganzira, rights, repubulika, lera"),
                
            Law(category="2", 
                title_rw="Itegeko ry'Ibyaha n'Ibano (Penal Code)", 
                title_en="Penal Code of Rwanda", 
                content_rw="Ingingo ya 120: Ubujura busanzwe buhanishwa igifungo kuva ku mezi 6 kugeza ku myaka 2. Ingingo ya 166: Gukubita cyangwa gukomeretsa ku bushake bitera ubumuga buhoraho buhanishwa igifungo cy'imyaka 5 kugeza kuri 7. Ingingo ya 211: Ruswa n'ibyaha bifitanye isano na yo.", 
                content_en="Article 120: Petty theft is punishable by 6 months to 2 years prison. Article 166: Assault causing permanent disability is punishable by 5 to 7 years. Article 211: Corruption and related offenses.", 
                tags="ibyaha, penal, ubujura, theft, gukubita, ruswa, igifungo, amande"),
                
            Law(category="3", 
                title_rw="Itegeko ry'Umuryango n'Abantu (Family Law)", 
                title_en="Law Governing Persons and Family", 
                content_rw="Ingingo ya 35: Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'izina ry'ubuyobozi bwa Leta. Ingingo ya 52: Ubutane (Divorce) bushobora kwemezwa n'inkiko gusa. Ingingo ya 88: Abana bose, abahungu n'abakobwa, bafite uburenganzira bungana ku izungura.", 
                content_en="Article 35: Only civil marriage is legally recognized. Article 52: Divorce can only be granted by competent courts. Article 88: Equal succession and inheritance rights for all children regardless of gender.", 
                tags="umuryango, family, gushyingirwa, marriage, izungura, ubutane, abana, abahungu, abakobwa"),
                
            Law(category="4", 
                title_rw="Itegeko ry'Umurimo mu Rwanda (Labor Law)", 
                title_en="Law Governing Labor in Rwanda", 
                content_rw="Ingingo ya 12: Amasezerano y'akazi agomba kwandikwa. Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. Ingingo ya 45: Akazi k'abana munsi y'imyaka 13 karabujijwe burundu.", 
                content_en="Article 12: Employment contracts must be in writing. Article 28: Mandatory 1-month termination notice. Article 45: Child labor under 13 years is strictly prohibited.", 
                tags="akazi, umurimo, contract, fire, kwirukanwa, notice, umushahara, abana"),
                
            Law(category="5", 
                title_rw="Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)", 
                title_en="Traffic and Road Safety Regulations", 
                content_rw="Ingingo ya 14: Gutwara ikinyabiziga nta permis bihanishwa amande ya 50,000 Frw no gufatira imodoka. Ingingo ya 22: Kurenza umuvuduko itandukanyijwe n'ibyapa (Speeding) bihanishwa 25,000 Frw.", 
                content_en="Article 14: Driving without a license attracts a 50,000 RWF fine and vehicle impoundment. Article 22: Exceeding speed limits (Speeding) attracts a 25,000 RWF fine.", 
                tags="umuhanda, imodoka, permis, license, amande, police, vitesse, ibyapa"),

            Law(category="6", 
                title_rw="Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)", 
                title_en="Cybercrimes and Cybersecurity Law", 
                content_rw="Ingingo ya 32: Kwinjira mu buryo butemewe mu miterere ya mudasobwa y'undi muntu. Ingingo ya 38: Guhimba cyangwa guhindura amakuru mu buryo bw'uburyarya. Igihano: Igifungo kuva ku myaka 3 kugeza kuri 5.", 
                content_en="Article 32: Unauthorized access to a computer system. Article 38: Data forgery and cyber fraud. Penalty: Imprisonment from 3 to 5 years.", 
                tags="internet, cybersecurity, cybercrime, mudasobwa, guhimba, hacking, uburyarya"),

            Law(category="7", 
                title_rw="Itegeko ry'Uburenganzira bw'Umwana", 
                title_en="Law on Child Protection and Rights", 
                content_rw="Ingingo ya 5: Umwana wese afite uburenganzira bwo kwandikwa mu bitabo by'amajwi y'abavutse. Ingingo ya 18: Gukubita n'ibihano bibabaza umubiri ku mwana birabujijwe haba mu rugo cyangwa ku ishuri.", 
                content_en="Article 5: Every child has a right to be registered at birth. Article 18: Corporal punishment and abuse of children are prohibited at home and school.", 
                tags="umwana, child, uburenganzira, protection, ishuri, gukubita, abavutse")
        ]
        
        db.session.bulk_save_objects(AMATEGEKO_Y_URWANDA)
        db.session.commit()
        print("🎉 Amategeko yose y'u Rwanda yasutswe muri Render Database neza 100%!")

if __name__ == "__main__":
    seed_all_rwanda_laws()
