import xml.etree.ElementTree as ET


def build_all_roms(known_games):
    wanted_roms = {}
    for game_clones in known_games.values():
        for game in game_clones:
            wanted_roms[game['rom_md5']] = game
    return wanted_roms


def build_wanted_roms(known_games, region_limit):
    wanted_roms = {}
    for game_clones in known_games.values():
        found = False
        for region in region_limit:
            for game in game_clones:
                if 'region' not in game:
                    break
                if game['region'] == region:
                    wanted_roms[game['rom_md5']] = game
                    found = True
                    break

            if found:
                break

    return wanted_roms


def build_known_games(filename):
    known_games = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for game_elem in root.findall('.//game'):
        game = {
            'name': game_elem.attrib['name'],
            'seen': False
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

        game_clones = known_games.get(game_key, [])
        game_clones.append(game)
        known_games[game_key] = game_clones

    return known_games
