import xml.etree.ElementTree as ET
import copy


class GameLibrary:
    def __init__(self, filename):
        self.known_game_groups = {}
        self.known_roms = {}
        tree = ET.parse(filename)
        root = tree.getroot()
        for game_elem in root.findall('.//game'):
            game = {
                'name': game_elem.attrib['name'],
                'seen': False,
                'selected': False,
            }
            if 'cloneof' in game_elem.attrib:
                game_key = game_elem.attrib['cloneof']
            else:
                game_key = game['name']

            game_release_elem = game_elem.find('.//release')
            if game_release_elem != None:
                game['region'] = game_release_elem.attrib['region']

            rom_elem = game_elem.find('.//rom')
            game['rom_md5'] = rom_elem.attrib['md5'].lower()
            game['rom_filename'] = rom_elem.attrib['name']

            game_clones = self.known_game_groups.get(game_key, [])
            game_clones.append(game)
            self.known_game_groups[game_key] = game_clones

            game['rom_md5'] = rom_elem.attrib['md5'].lower()
            self.known_roms[game['rom_md5']] = game


    def _set_selection_all(self, selection):
        for rom in self.known_roms.values():
            rom['selected'] = selection
        pass


    def select_all(self):
        self._set_selection_all(True)


    def deselect_all(self):
        self._set_selection_all(False)


    def select_by_region_limit(self, region_limit):
        self.deselect_all()
        for game_clones in self.known_game_groups.values():
            found = False
            for region in region_limit:
                for game in game_clones:
                    if 'region' not in game:
                        break
                    if game['region'] == region:
                        game['selected'] = True
                        found = True
                        break

                if found:
                    break


    def get_by_md5sum(self, md5sum):
        return self.known_roms.get(md5sum, None)


    def get_seen_selected(self):
        result = [x for x in self.known_roms.values() if x['seen'] == True and x['selected'] == True]
        return copy.deepcopy(result)


    def get_missing_selected(self):
        result = [x for x in self.known_roms.values() if x['seen'] == False and x['selected'] == True]
        return copy.deepcopy(result)
