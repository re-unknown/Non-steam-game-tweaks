from steamgrid import SteamGridDB, StyleType, MimeType, ImageType

# APIキーを設定
API_KEY = 'api key'
sgdb = SteamGridDB(API_KEY)

def search_game(app_name):
    return sgdb.search_game(app_name)

def get_grids_by_gameid(game_id):
    return sgdb.get_grids_by_gameid([game_id])
