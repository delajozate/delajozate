import json
import os
import datetime
import dateutil.parser
import time
import settings
import sunburnt
from magnetogrami.models import Seja, SejaInfo, Zasedanje, Zapis

class Importer():
    def __init__(self, file_directory):
        """
        file_directory - search path for files to import
        """
        self.file_directory = file_directory

    def parse_time(self, time_string):
        try:
            parsed_time = time.strptime(time_string, "%H.%S")
        except:
            try:
                parsed_time = time.strptime(time_string, "%H")
            except:
                parsed_time = None

        if parsed_time:
            return time.strftime("%H:%S", parsed_time)
        else:
            return None

    def do_import(self):
        files = os.listdir(self.file_directory)

        Seja.objects.all().delete()
        Zasedanje.objects.all().delete()
        Zapis.objects.all().delete()

        for file in files:
            print file, "..."
            counter = 0
            for fileData in open(os.path.join(self.file_directory, file), 'r'):
                counter = counter + 1
                print counter, ".."
                # Parse JSON data and create models
                jsonData = json.loads(fileData.replace("\\\\", "\\"))

                seja = Seja()
                seja.mandat = int(jsonData.get('mandat'))
                seja.naslov = jsonData.get('naslov')
                seja.seja = jsonData.get('seja')
                seja.url = jsonData.get('url')
                seja.save()

                # jsonSeja objects
                for jsonSeja in jsonData.get('seja_info'):
                    sejaInfo = SejaInfo()
                    sejaInfo.seja = seja
                    sejaInfo.url = jsonSeja.get('url')
                    sejaInfo.naslov = jsonSeja.get('naslov')
                    sejaInfo.datum = dateutil.parser.parse(jsonSeja.get('datum'), dayfirst=True)
                    sejaInfo.save()

                # Zasedanja
                for jsonZasedanje in jsonData.get('zasedanja'):
                    for jsonPovezava in jsonZasedanje.get('povezave'):
                        zasedanje = Zasedanje()
                        zasedanje.datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
                        zasedanje.seja = seja

                        if jsonPovezava.get('zacetek'):
                            zasedanje.zacetek = self.parse_time(jsonPovezava.get('zacetek'))
                        if jsonPovezava.get('konec'):
                            zasedanje.konec = self.parse_time(jsonPovezava.get('konec'))

                        zasedanje.tip = jsonPovezava.get('tip')
                        zasedanje.naslov = jsonPovezava.get('naslov')
                        zasedanje.save()

                        for jsonOdsek in jsonPovezava.get('odseki'):
                            for jsonZapis in jsonOdsek.get('zapisi'):
                                zapis = Zapis()
                                zapis.zasedanje = zasedanje
                                zapis.govorec = jsonZapis.get('govorec')
                                zapis.odstavki = ' '.join(jsonZapis.get('odstavki'))
                                zapis.save()


        print "Database insert OK, importing dataset into Solr...."
        # Shrani zapise v Solr
        solr = sunburnt.SolrInterface(settings.SOLR_URL)
        solr.delete_all()       # Clear Solr index

        midnight = datetime.time(0, 0)
        numZapis = Zapis.objects.count()
        counter = 0
        for zapis in Zapis.objects.select_related().all():
            dict = { "id": zapis.pk,
                     "zasedanje_id":zapis.zasedanje.pk,
                     "seja_id": zapis.zasedanje.seja.pk,
                     "datum_zapisa": datetime.datetime.combine(zapis.zasedanje.datum, midnight),    # Sunburnt expects datetime
                     "govorec":zapis.govorec,
                     "govorec_exact":zapis.govorec,
                     "besedilo" : zapis.odstavki }
            solr.add(dict)
            counter += 1
            if counter % 100 == 0:
                print counter,"/",numZapis

        solr.commit()
        print "Data commited to Solr."


