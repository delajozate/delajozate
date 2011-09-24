import json
import os
import dateutil.parser
from search.models import Seja, SejaInfo, Zasedanje, Povezava

class Importer():

    def __init__(self, file_directory):
        """
        file_directory - search path for files to import
        """
        self.file_directory = file_directory

    def do_import(self):
        files = os.listdir(self.file_directory)

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
                zasedanje = Zasedanje()
                zasedanje.datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
                zasedanje.seja = seja
                zasedanje.save()

                for jsonPovezava in jsonZasedanje.get('povezave'):
                    povezava = Povezava()
                    povezava.zasedanje = zasedanje
                    povezava.url = jsonPovezava.get('url')
                    povezava.naslov = jsonPovezava.get('naslov')
                    povezava.text = jsonPovezava.get('text')
                    povezava.save()

        print "Import ok!"


