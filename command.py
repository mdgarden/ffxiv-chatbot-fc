from scrape_homepage import (
    extract_maintenance_post_jp,
    extract_character_profile
)

command_list = {
    "@점검" : "maintenance",
    "@이엣타이가":{'name':'House Tiger', 'profile':'23985452'},
    "@엣탱":{'name':'Alpha Sertan', 'profile':'23508489'},
    "@튜플":{'name':'Tuple Cardinality', 'profile':'23240790'},
    "@교수님":{'name':'Meetra Surik', 'profile':'14369815'},
    "@로딩":{'name':'Cilia Aden', 'profile':'25206858'},
    "@공홈":"link",
}


def find_command(command):
    if command_list[command] is not None:
        category = command_list[command]
        if category == "maintenance":
            return extract_maintenance_post_jp()
        elif category == "link":
            pass
        else:
            return extract_character_profile(category)

find_command("@튜플")