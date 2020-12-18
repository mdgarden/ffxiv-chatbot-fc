from scrape_homepage import extract_maintenance_post_jp, extract_character_profile

command_list = {
    "@점검": {"category": "maintenance"},
    "@이엣타이가": {"category": "character", "name": "House Tiger", "profile": "23985452"},
    "@엣탱": {"category": "character", "name": "Alpha Sertan", "profile": "23508489"},
    "@튜플": {
        "category": "character",
        "name": "Tuple Cardinality",
        "profile": "23240790",
    },
    "@교수님": {"category": "character", "name": "Meetra Surik", "profile": "14369815"},
    "@로딩": {"category": "character", "name": "Cilia Aden", "profile": "25206858"},
    "@공홈": {"category": "link"},
}


def find_command(command):
    try:
        first_command = command_list[command]
    except:
        pass

    if first_command is not None:
        category = command_list[command]["category"]
        if category == "maintenance":
            return extract_maintenance_post_jp()
        elif category == "link":
            pass
        elif category == "character":
            return extract_character_profile(first_command)
        else:
            pass
