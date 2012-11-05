# encoding: utf-8
import datetime
import json
from south.db import db
from south.v2 import SchemaMigration
from django.db import models



class Migration(SchemaMigration):

    def forwards(self, orm):
        # this variable is below
        global dz_id_list
        
        import json
        from dz.models import DelovnoTelo

        m = {}
        for i in dz_id_list:
            m[(i['ime'], i['mandat_id'])] = i['dz_id']

        for dt in DelovnoTelo.objects.all():
            if (dt.ime, dt.mandat_id) in m:
                dt.dz_id = m[(dt.ime, dt.mandat_id)]
                dt.save()



    def backwards(self, orm):
        raise ValueError("Thou shall not pass back in time.")


    models = {
        'dz.clanodbora': {
            'Meta': {'object_name': 'ClanOdbora'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'funkcija': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'odbor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.DelovnoTelo']"}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poslanec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Funkcija']"})
        },
        'dz.clanstranke': {
            'Meta': {'ordering': "('-do',)", 'object_name': 'ClanStranke'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
        },
        'dz.delovnotelo': {
            'Meta': {'object_name': 'DelovnoTelo'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'dz_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'dz.drzavnizbor': {
            'Meta': {'object_name': 'DrzavniZbor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'})
        },
        'dz.funkcija': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Funkcija'},
            'do': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'funkcija': ('django.db.models.fields.CharField', [], {'default': "'poslanec'", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dz.imestranke': {
            'Meta': {'ordering': "['-od']", 'object_name': 'ImeStranke'},
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'od': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']"})
        },
        'dz.mandat': {
            'Meta': {'object_name': 'Mandat'},
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'st': ('django.db.models.fields.IntegerField', [], {})
        },
        'dz.organizacija': {
            'Meta': {'object_name': 'Organizacija'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dz.oseba': {
            'Meta': {'ordering': "('ime', 'priimek')", 'object_name': 'Oseba'},
            'dan_smrti': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priimek': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rojstni_dan': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slika': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '96', 'db_index': 'True'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'vir_slike': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'dz.pozicija': {
            'Meta': {'object_name': 'Pozicija'},
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'od': ('django.db.models.fields.DateField', [], {}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizacija': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Organizacija']", 'null': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tip': ('django.db.models.fields.CharField', [], {'default': "'poslanec'", 'max_length': '64'})
        },
        'dz.skupina': {
            'Meta': {'object_name': 'Skupina'},
            'do': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'mandat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Mandat']"}),
            'od': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
            'stranka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Stranka']", 'null': 'True', 'blank': 'True'})
        },
        'dz.stranka': {
            'Meta': {'ordering': "('-do', 'ime')", 'object_name': 'Stranka'},
            'barva': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'davcna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'do': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'maticna': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'nastala_iz': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'spremenila_v'", 'blank': 'True', 'to': "orm['dz.Stranka']"}),
            'od': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'okrajsava': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'opombe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizacija': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dz.Organizacija']", 'unique': 'True', 'null': 'True'}),
            'podatki_preverjeni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spletna_stran': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'dz.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oseba': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dz.Oseba']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['dz']

dz_id_list = json.loads(r"""[{"mandat_id": 5,"dz_id": "51","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti nosilcev javnih funkcij v zadevi Patria","id": 1},
{"mandat_id": 5,"dz_id": "11","ime": "Odbor za gospodarstvo","id": 2},
{"mandat_id": 5,"dz_id": "13","ime": "Odbor za kmetijstvo, gozdarstvo in prehrano","id": 3},
{"mandat_id": 5,"dz_id": "21","ime": "Odbor za kulturo, \u0161olstvo, \u0161port in mladino","id": 4},
{"mandat_id": 5,"dz_id": "06","ime": "Komisija za peticije ter za \u010dlovekove pravice in enake mo\u017enosti","id": 5},
{"mandat_id": 5,"dz_id": "47","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti pri pripravi in izvedbi gradbenih investicij na podro\u010dju izgradnje avtocest in objektov gospodarske javne infrastrukture, financiranih s sredstvi dr\u017eavnega prora\u010duna","id": 6},
{"mandat_id": 5,"dz_id": "50","ime": "Preiskovalna komisija za ugotovitev in oceno dejanskega stanja izdajanja in financiranja brezpla\u010dnih tednikov \"Slovenski tednik\" in \"Ekspres\"","id": 7},
{"mandat_id": 5,"dz_id": "18","ime": "Odbor za obrambo","id": 8},
{"mandat_id": 5,"dz_id": "16","ime": "Odbor za zunanjo politiko","id": 9},
{"mandat_id": 5,"dz_id": "32","ime": "Odbor za zadeve Evropske unije","id": 10},
{"mandat_id": 5,"dz_id": "01","ime": "Komisija za poslovnik","id": 11},
{"mandat_id": 5,"dz_id": "19","ime": "Odbor za promet","id": 12},
{"mandat_id": 5,"dz_id": "14","ime": "Odbor za finance in monetarno politiko","id": 13},
{"mandat_id": 5,"dz_id": "17","ime": "Odbor za notranjo politiko, javno upravo in pravosodje","id": 14},
{"mandat_id": 5,"dz_id": "KPDZ","ime": "Kolegij predsednika Dr\u017eavnega zbora","id": 15},
{"mandat_id": 5,"dz_id": "30","ime": "Ustavna komisija Dr\u017eavnega zbora","id": 16},
{"mandat_id": 5,"dz_id": "24","ime": "Odbor za delo, dru\u017eino, socialne zadeve in invalide","id": 17},
{"mandat_id": 5,"dz_id": "25","ime": "Odbor za visoko \u0161olstvo, znanost in tehnolo\u0161ki razvoj","id": 18},
{"mandat_id": 5,"dz_id": "49","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti pri pripravi in izvedbi nekaterih projektov Mestne ob\u010dine Ljubljana, Stanovanjskega sklada Republike Slovenije, Univerze na Primorskem in javnih zdravstvenih objektov, financiranih iz dr\u017eavnega oziroma prora\u010duna Mestne ob\u010dine Ljubljana","id": 19},
{"mandat_id": 5,"dz_id": "48","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti ministra za visoko \u0161olstvo, znanost in tehnologijo Gregorja Golobi\u010da zaradi suma klientelizma in koruptivnega ravnanja","id": 20},
{"mandat_id": 5,"dz_id": "05","ime": "Komisija za narodni skupnosti","id": 21},
{"mandat_id": 5,"dz_id": "20","ime": "Odbor za zdravstvo","id": 22},
{"mandat_id": 5,"dz_id": "09","ime": "Komisija za nadzor obve\u0161\u010devalnih in varnostnih slu\u017eb","id": 23},
{"mandat_id": 5,"dz_id": "15","ime": "Komisija za nadzor javnih financ","id": 24},
{"mandat_id": 5,"dz_id": "10","ime": "Odbor za lokalno samoupravo in regionalni razvoj","id": 25},
{"mandat_id": 5,"dz_id": "12","ime": "Odbor za okolje in prostor","id": 26},
{"mandat_id": 5,"dz_id": "46","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti zaradi suma vpletenosti pri financiranju spornih mened\u017eerskih prevzemov in pomanjkljive prevzemne zakonodaje","id": 27},
{"mandat_id": 5,"dz_id": "40","ime": "Mandatno-volilna komisija","id": 28},
{"mandat_id": 5,"dz_id": "26","ime": "Komisija za odnose s Slovenci v zamejstvu in po svetu","id": 29},
{"mandat_id": 5,"dz_id": "02","ime": "Komisija po Zakonu o prepre\u010devanju korupcije","id": 34},
{"mandat_id": 5,"dz_id": "90","ime": "Parlamentarna skupina GLOBE Slovenija","id": 35},
{"mandat_id": 4,"dz_id": "01","ime": "Komisija za poslovnik","id": 37},
{"mandat_id": 4,"dz_id": "02","ime": "Komisija po Zakonu o prepre\u010devanju korupcije","id": 38},
{"mandat_id": 4,"dz_id": "05","ime": "Komisija za narodni skupnosti","id": 39},
{"mandat_id": 4,"dz_id": "06","ime": "Komisija za peticije ter za \u010dlovekove pravice in enake mo\u017enosti","id": 40},
{"mandat_id": 4,"dz_id": "09","ime": "Komisija za nadzor obve\u0161\u010devalnih in varnostnih slu\u017eb","id": 41},
{"mandat_id": 4,"dz_id": "10","ime": "Odbor za lokalno samoupravo in regionalni razvoj","id": 42},
{"mandat_id": 4,"dz_id": "11","ime": "Odbor za gospodarstvo","id": 43},
{"mandat_id": 4,"dz_id": "12","ime": "Odbor za okolje in prostor","id": 44},
{"mandat_id": 4,"dz_id": "13","ime": "Odbor za kmetijstvo gozdarstvo in prehrano","id": 45},
{"mandat_id": 4,"dz_id": "14","ime": "Odbor za finance in monetarno politiko","id": 46},
{"mandat_id": 4,"dz_id": "15","ime": "Komisija za nadzor javnih financ","id": 47},
{"mandat_id": 4,"dz_id": "16","ime": "Odbor za zunanjo politiko","id": 48},
{"mandat_id": 4,"dz_id": "17","ime": "Odbor za notranjo politiko javno upravo in pravosodje","id": 49},
{"mandat_id": 4,"dz_id": "18","ime": "Odbor za obrambo","id": 50},
{"mandat_id": 4,"dz_id": "19","ime": "Odbor za promet","id": 51},
{"mandat_id": 4,"dz_id": "20","ime": "Odbor za zdravstvo","id": 52},
{"mandat_id": 4,"dz_id": "21","ime": "Odbor za kulturo \u0161olstvo in \u0161port","id": 53},
{"mandat_id": 4,"dz_id": "24","ime": "Odbor za delo dru\u017eino socialne zadeve in invalide","id": 54},
{"mandat_id": 4,"dz_id": "25","ime": "Odbor za visoko \u0161olstvo znanost in tehnolo\u0161ki razvoj","id": 55},
{"mandat_id": 4,"dz_id": "26","ime": "Komisija za odnose s Slovenci v zamejstvu in po svetu","id": 56},
{"mandat_id": 4,"dz_id": "30","ime": "Ustavna komisija","id": 57},
{"mandat_id": 4,"dz_id": "32","ime": "Odbor za zadeve Evropske unije","id": 58},
{"mandat_id": 2,"dz_id": "27","ime": "Komisija za vpra\u0161anja invalidov","id": 116},
{"mandat_id": 4,"dz_id": "37","ime": "Preiskovalna komisija za ugotovitev in oceno dejanskega stanja, ki je lahko podlaga za odlo\u010danje o politi\u010dni odgovornosti nosilcev javnih funkcij v Vladi Republike Slovenije, na Ministrstvu za pravosodje in Vrhovnem Dr\u017eavnem to\u017eilstvu Republike Slovenije v zvezi z izvr\u0161evanjem nadzora po Zakonu o dr\u017eavnem to\u017eilstvu (Uradni list RS, \u0161t. 110/02-uradno pre\u010di\u0161\u010deno besedilo), za spremembo zakonodaje in za druge odlo\u010ditve v skladu z ustavnimi pristojnostmi dr\u017eavnega zbora","id": 59},
{"mandat_id": 4,"dz_id": "38","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti nosilcev javnih funkcij v zvezi z domnevnim o\u0161kodovanjem dr\u017eavnega premo\u017eenja pri prodaji dele\u017eev Kapitalske dru\u017ebe d.d. in Slovenske od\u0161kodninske dru\u017ebe d. d. v gospodarskih dru\u017ebah in sicer tako, da zajema preiskava vse prodaje, ki so sporne z vidika skladnosti z zakoni in drugimi predpisi ter z vidikov preglednosti in gospodarnosti","id": 60},
{"mandat_id": 4,"dz_id": "39","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti nosilcev javnih funkcij, ki so sodelovali pri pripravi in izvedbi pogodbe o nakupu pehotnih bojnih oklepnih vozil - srednjih oklepnih kolesnih vozil 8x8 zaradi suma, da je posel politi\u010dno dogovorjen, voden netransparentno in da je negospodaren, ter zaradi suma o prisotnosti klientelizma in korupcije, in za ugotovitev suma o neposredni ali posredni povezavi med sedanjimi in nekdanjimi akterji ter nosilci javnih funkcij z oro\u017ejem v obdobju 1991 do 1993","id": 61},
{"mandat_id": 4,"dz_id": "40","ime": "Mandatno-volilna komisija","id": 62},
{"mandat_id": 4,"dz_id": "41","ime": "Preiskovalna komisija za ugotovitev politi\u010dne odgovornosti nosilcev javnih funkcij, ki so sodelovali pri pripravi in izvedbi nakupa lahkih oklepnih kolesnih vozil 6x6, vladnega letala, havbic 155 mm, sistema za upravljanje ognja (ACCS), letal Pilatus in obnovi tankov T55-S financiranih v okviru temeljnih razvojnih programov obrambnih sil Republike Slovenije v letih 1994 do 2007 zaradi suma, da so bili posli politi\u010dno dogovorjeni, vodeni netransparentno in da so negospodarni, ter zaradi suma o prisotnosti klientelizma in korupcije, in za ugotovitev suma o odgovornosti nosilcev javnih funkcij pri razoro\u017eitvi nekdanje teritorialne obrambe","id": 63},
{"mandat_id": 4,"dz_id": "90","ime": "Parlamentarna skupina GLOBE Slovenija","id": 64},
{"mandat_id": 4,"dz_id": "KPDZ","ime": "Kolegij predsednika DZ","id": 65},
{"mandat_id": 3,"dz_id": "01","ime": "Komisija za poslovnik","id": 66},
{"mandat_id": 3,"dz_id": "02","ime": "Mandatno-imunitetna komisija","id": 67},
{"mandat_id": 3,"dz_id": "03","ime": "Komisija za volitve imenovanja in administrativne zadeve","id": 68},
{"mandat_id": 3,"dz_id": "04","ime": "Komisija po zakonu o nezdru\u017eljivosti opravljanja javne funkcije s pridobitno dejavnostjo","id": 69},
{"mandat_id": 3,"dz_id": "05","ime": "Komisija za narodni skupnosti","id": 70},
{"mandat_id": 3,"dz_id": "06","ime": "Komisija za peticije","id": 71},
{"mandat_id": 3,"dz_id": "09","ime": "Komisija za nadzor nad delom varnostnih in obve\u0161\u010devalnih slu\u017eb","id": 72},
{"mandat_id": 3,"dz_id": "11","ime": "Odbor za gospodarstvo","id": 73},
{"mandat_id": 3,"dz_id": "12","ime": "Odbor za infrastrukturo in okolje","id": 74},
{"mandat_id": 3,"dz_id": "13","ime": "Odbor za kmetijstvo gozdarstvo in prehrano","id": 75},
{"mandat_id": 3,"dz_id": "14","ime": "Odbor za finance in monetarno politiko","id": 76},
{"mandat_id": 3,"dz_id": "15","ime": "Komisija za nadzor prora\u010duna in drugih javnih financ","id": 77},
{"mandat_id": 3,"dz_id": "16","ime": "Odbor za zunanjo politiko","id": 78},
{"mandat_id": 3,"dz_id": "17","ime": "Odbor za notranjo politiko","id": 79},
{"mandat_id": 3,"dz_id": "18","ime": "Odbor za obrambo","id": 80},
{"mandat_id": 3,"dz_id": "20","ime": "Odbor za zdravstvo delo dru\u017eino socialno politiko in invalide","id": 81},
{"mandat_id": 3,"dz_id": "21","ime": "Odbor za kulturo \u0161olstvo mladino znanost in \u0161port","id": 82},
{"mandat_id": 3,"dz_id": "211","ime": "Delovna skupina za podro\u010dje jezikovnega na\u010drtovanja in jezikovne politike","id": 83},
{"mandat_id": 3,"dz_id": "26","ime": "Komisija za odnose s Slovenci v zamejstvu in po svetu","id": 84},
{"mandat_id": 3,"dz_id": "29","ime": "Komisija za evropske zadeve","id": 85},
{"mandat_id": 3,"dz_id": "30","ime": "Ustavna komisija","id": 86},
{"mandat_id": 3,"dz_id": "31","ime": "Slovenski del Pridru\u017eitvenega parlamentarnega odbora","id": 87},
{"mandat_id": 3,"dz_id": "32","ime": "Odbor za zadeve Evropske unije","id": 88},
{"mandat_id": 3,"dz_id": "35","ime": "Preiskovalna komisija za ugotovitev odgovornosti oseb in nosilcev javnih pooblastil glede nakupa in prodaje elektri\u010dne energije zaradi \u010desar je bila domnevno povzro\u010dena gospodarska \u0161koda v sistemu slovenskega elektrogospodarstva","id": 89},
{"mandat_id": 3,"dz_id": "36","ime": "Preiskovalna komisija za ugotovitev ozadja in vzrokov napada na novinarja Mira Petka ter morebitno vpletenost in politi\u010dno odgovornost nosilcev javnih funkcij","id": 90},
{"mandat_id": 3,"dz_id": "40","ime": "Mandatno-volilna komisija","id": 91},
{"mandat_id": 3,"dz_id": "90","ime": "Parlamentarna skupina GLOBE Slovenija","id": 92},
{"mandat_id": 3,"dz_id": "KPDZ","ime": "Kolegij predsednika DZ","id": 93},
{"mandat_id": 2,"dz_id": "01","ime": "Komisija za poslovnik","id": 94},
{"mandat_id": 2,"dz_id": "02","ime": "Mandatno-imunitetna komisija","id": 95},
{"mandat_id": 2,"dz_id": "03","ime": "Komisija za volitve imenovanja in administrativne zadeve","id": 96},
{"mandat_id": 2,"dz_id": "04","ime": "Komisija po zakonu o nezdru\u017eljivosti opravljanja javne funkcije s pridobitno dejavnostjo","id": 97},
{"mandat_id": 2,"dz_id": "05","ime": "Komisija za narodni skupnosti","id": 98},
{"mandat_id": 2,"dz_id": "06","ime": "Komisija za peticije","id": 99},
{"mandat_id": 2,"dz_id": "07","ime": "Komisija za lokalno samoupravo","id": 100},
{"mandat_id": 2,"dz_id": "08","ime": "Komisija za politiko enakih mo\u017enosti","id": 101},
{"mandat_id": 2,"dz_id": "10","ime": "Komisija za nadzor lastninskega preoblikovanja in privatizacije","id": 102},
{"mandat_id": 2,"dz_id": "11","ime": "Odbor za gospodarstvo","id": 103},
{"mandat_id": 2,"dz_id": "12","ime": "Odbor za infrastrukturo in okolje","id": 104},
{"mandat_id": 2,"dz_id": "13","ime": "Odbor za kmetijstvo gozdarstvo in prehrano","id": 105},
{"mandat_id": 2,"dz_id": "14","ime": "Odbor za finance in monetarno politiko","id": 106},
{"mandat_id": 2,"dz_id": "15","ime": "Odbor za nadzor prora\u010duna in drugih javnih financ","id": 107},
{"mandat_id": 2,"dz_id": "16","ime": "Odbor za mednarodne odnose","id": 108},
{"mandat_id": 2,"dz_id": "17","ime": "Odbor za notranjo politiko in pravosodje","id": 109},
{"mandat_id": 2,"dz_id": "18","ime": "Odbor za obrambo","id": 110},
{"mandat_id": 2,"dz_id": "19","ime": "Odbor za znanost in tehnologijo","id": 111},
{"mandat_id": 2,"dz_id": "20","ime": "Odbor za zdravstvo delo dru\u017eino in socialno politiko","id": 112},
{"mandat_id": 2,"dz_id": "21","ime": "Odbor za kulturo \u0161olstvo in \u0161port","id": 113},
{"mandat_id": 2,"dz_id": "23","ime": "Preiskovalna komisija Dr\u017eavnega zbora Republike Slovenije o sumu zlorabe javnih pooblastil za vzroke okoli\u0161\u010dine in posledice dogodkov na kapitalskem trgu v marcu 1996 in uresni\u010devanju zakonskih nalog Agencije za trg vrednostnih papirjev v obdobju","id": 114},
{"mandat_id": 2,"dz_id": "26","ime": "Komisija za odnose s Slovenci v zamejstvu in po svetu","id": 115},
{"mandat_id": 2,"dz_id": "28","ime": "Odbor za spremljanje uresni\u010devanja Resolucije o izhodi\u0161\u010dih zasnove nacionalne varnosti Republike Slovenije","id": 117},
{"mandat_id": 2,"dz_id": "29","ime": "Komisija za evropske zadeve","id": 118},
{"mandat_id": 2,"dz_id": "30","ime": "Ustavna komisija","id": 119},
{"mandat_id": 2,"dz_id": "31","ime": "Slovenski del Pridru\u017eitvenega parlamentarnega odbora","id": 120},
{"mandat_id": 2,"dz_id": "32","ime": "Preiskovalna komisija Dr\u017eavnega zbora Republike Slovenije o vpletenosti in odgovornosti nosilcev javnih funkcij v zvezi z najdbo oro\u017eja na mariborskem letali\u0161\u010du ter z opremo in oro\u017ejem v skladi\u0161\u010du Lo\u017enica","id": 121},
{"mandat_id": 2,"dz_id": "33","ime": "Preiskovalna komisija Dr\u017eavnega zbora Republike Slovenije o vpletenosti nosilcev javnih funkcij v poskuse diskreditiranja slovenskih policistov in vojakov ki so leta 1991 sodelovali v osamosvojitveni vojni na Koro\u0161kem","id": 122},
{"mandat_id": 2,"dz_id": "34","ime": "Komisija za volilni sistem in ustavne spremembe","id": 123}]""")