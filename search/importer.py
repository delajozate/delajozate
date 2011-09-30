import json
import os
import dateutil.parser
import time
from search.models import Seja, SejaInfo, Zasedanje, Zapis

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

        for seja in Seja.objects.all():
            seja.delete()

        for file in files:
            try:
                fileData = open(os.path.join(self.file_directory, file), 'r').read()
            except:
                print "Error opening %s, skipping..." % file
                continue

            print file, "..."

            # Parse JSON data and create models
            jsonData = json.loads(fileData)

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
                            zapis.odstavki = jsonZapis.get('odstavki')
                            zapis.save()

        print "Import ok!"


