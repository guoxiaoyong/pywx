import requests

class MENU_TYPE:
  CLICK = "click"
  VIEW = "view"
  SCANCODE_PUSH = "scancode_push"
  SCANCODE_WAITMSG = "scancode_waitmsg"
  PIC_SYSPHOTO = "pic_sysphoto"
  PIC_PHOTO_OR_ALBUM = "pic_photo_or_album"
  PIC_WEIXIN = "pic_weixin"
  LOCATION_SELECT = "location_select"
  MEDIA_ID = "media_id"
  VIEW_LIMITED = "view_limited"

ACCESS_TOKEN = {'access_token':
        'eUadik8d0w7oD8Q7YLtigb8uMV1dTw4nbb7CYo90fMI2Q6xuFd74fEzF0wKVsmnELcqvLS5_A0AgoKmUucV0XXmomNxAF1gqCHnD1JWC1mr5c2c6PLHtQTbMAG1IfbgNLWSgAFAZKG'}
def create_menu():
  url = "https://api.weixin.qq.com/cgi-bin/menu/create"
  json = open('menu.json').read()
  req = requests.post(url, params=ACCESS_TOKEN, data=json)
  return req.json()

print create_menu()
quit()

class Menu(object):
  def __init__(self):
    pass

  def AddMenu(self):
    pass
