from time import sleep
from pprint import pprint
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from strings import ru

class Private(object):
    def __init__(self, bot , db, view):
        self.bot = bot
        self.db = db
        self.view = view

    def main(self, message, is_doc = False):
        print(f'\nMessage from user: {message.from_user.first_name}, text: {message.text}, user  {message.from_user.username}chat: {message.chat.username} | {message.chat.type}')
        user_id = message.from_user.id
        user = self.db.is_user(user_id)
        if not user:
            self.db.new_user(user_id)    
            print('Add user on db')
            self.view.welcom(user_id, is_new = True)
        elif message.text in ['/start','/help','/menu', 'm']:
            self.view.main(user_id, is_new = True)

        elif user[1] == 'ch_add':
            print(f'Add new ch {message.text}  user: {message.from_user.first_name}')
            self.add_new_ch(message.text, user_id)

        elif user[1] == 'set_mark':
            
                
            if is_doc:
                photo_id =  message.document.file_id
                self.db.channel_set(user_id, 'text_mark', 'off')
                self.db.channel_set(user_id, 'id_photo_mark', photo_id)
                self.bot.send_message(user_id, ru['mark_set'])

            else:
                self.db.channel_set(user_id, 'id_photo_mark', 'off')
                self.db.channel_set(user_id, 'text_mark', message.text)
                self.bot.send_message(user_id, ru['textmark_set'].format(text = message.text), parse_mode = 'Markdown')
            self.view.ch_setting(user_id, is_new = True)
            self.db.user_set(user_id, 'menu_select', 'ch_sett')
           
        elif user[1] == 'color_mark':
            bts = InlineKeyboardMarkup()
            bts.add(InlineKeyboardButton(text = ru['back'], callback_data='open ch_sett'))
            rgba = message.text.split()
            
            if len(rgba) == 3:
                for c in rgba:
                    if not c.isdigit() or int(c) < 0 or int(c) > 256: 
                      
                        self.view.send(user_id, text = ru['wrong_format_color'], markup = bts, is_new = True)
                        return
                self.db.channel_set(user_id, 'color_mark', message.text)
                self.bot.send_message(user_id, ru['color_set'])
                self.view.ch_setting(user_id, is_new = True)
            else:
                self.view.send(user_id, text = ru['wrong_format_color'], markup = bts, is_new = True)
                
                        
                    
                        
                
        else:
            self.view.main(user_id, is_new = True)


    def add_new_ch(self, username_ch, user_id):
        print('User {} add new channel {}'.format(user_id, username_ch))
        bts = InlineKeyboardMarkup()
        bts.add(InlineKeyboardButton(text = ru['back'], callback_data='open ch_list del_up'))
        txt_error = None

        if len(username_ch.split('t.me/')) > 1:
            username_ch = username_ch.split('t.me/')[1]

        if not username_ch[0] =='@':
            username_ch = '@' + username_ch
        
        try:
            msg = self.bot.send_message(username_ch, 'Hello:)')
        except Exception as e:    
            txt_error = ru['channel_no_exist']
            print(f'Error add chanel: {e} txterror {txt_error}')
        else:
            self.bot.delete_message(username_ch, msg.message_id)
            ch_ids = self.db.get_channel_id(user_id)
            print(ch_ids)
            if len(ch_ids) > 0 and msg.chat.id in ch_ids[0]:
                txt_error = ru['channel_exist']
        
        if txt_error:
            self.view.send(user_id = user_id, text = txt_error, is_new = True,  markup = bts)
        
        
        else:       
            self.db.new_channel(user_id, msg.chat.id, msg.chat.title) 
            self.view.send(user_id = user_id, text = ru['channel_added'].format(channel_name = msg.chat.title), is_new = True, markup = None)
            self.db.user_set(user_id, 'group_select', msg.chat.id)
            sleep(3)
            self.view.ch_setting(user_id, is_new = True)
            print('Sucessful added chanel!')
            










































            
