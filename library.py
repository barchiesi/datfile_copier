import xml.etree.ElementTree as ET
import copy


class HeaderRule:
    def __init__(self, header_end, data = None, data_offset = None):
        self.header_end = header_end
        self.data = data
        self.data_offset = data_offset


    def strip_header_from_rom(self, rom_content):
        if self.data:
            check_bytes = rom_content[self.data_offset: len(self.data)]
            idx = 0
            for val in self.data:
                if check_bytes[idx] != val:
                    return None
                idx += 1
            return rom_content[self.header_end:]
        else:
            return rom_content[self.header_end:]




class GameLibrary:
    known_header_rules = []
    known_game_groups = {}
    known_roms = {}

    def __init__(self, dat_filename):
        self.known_game_groups = {}
        self.known_roms = {}
        tree = ET.parse(dat_filename)
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


    def set_header_xml(self, xml_filename):
        self.known_header_rules = []
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        for rule in root.findall('.//rule'):
            rule_offset = int(rule.attrib['start_offset'], 16)
            datas = rule.findall('.//data')
            if len(datas) == 0:
                header_rule = HeaderRule(rule_offset)
                self.known_header_rules.append(header_rule)
            else:
                for data in datas:
                    raw_data = data.attrib['value']
                    clean_data = [int(x, 16) for x in [raw_data[i:i+2] for i in range(0, len(raw_data), 2)]]
                    header_rule = HeaderRule(rule_offset,
                        data=clean_data,
                        data_offset=int(data.attrib['offset'], 16),
                    )
                    self.known_header_rules.append(header_rule)


    def get_header_rules(self):
        return copy.deepcopy(self.known_header_rules)


    def _set_selection_all(self, selection):
        for rom in self.known_roms.values():
            rom['selected'] = selection


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
                        continue
                    if game['region'] == region:
                        game['selected'] = True
                        found = True
                        break

                if found:
                    # We found a match for this region
                    break


    def get_by_md5sum(self, md5sum):
        return self.known_roms.get(md5sum, None)


    def get_seen_selected(self):
        result = [x for x in self.known_roms.values() if x['seen'] == True and x['selected'] == True]
        return copy.deepcopy(result)


    def get_missing_selected(self):
        result = [x for x in self.known_roms.values() if x['seen'] == False and x['selected'] == True]
        return copy.deepcopy(result)
