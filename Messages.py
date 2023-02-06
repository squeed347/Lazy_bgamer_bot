# -*- coding: utf8 -*-
class Message_to_user():

    __rules_link = 'http://vk.com/'
    __email = 'email@gmail.com'

    def greeting_response(self, text=str):
        return ("Привет, {}!\nДобро пожаловать к Ленивому настольщику!"
                "\nЯ готов помочь тебе быстро пробежаться по правилам известных мне настольных игр."
                "\nИспользуй меню слева при возникновении вопросов. Удачной партии, дружище!".format(text))

    def help_response(self):
        return ("Чтобы выбрать игру, введи её название, либо найди её в списке всех известных мне игр."
                "\nПри выборе игры, для навигации по правилам, я покажу тебе нужные их части."
                "\nЧтобы выбрать другую игру - нажми кнопку start в меню, а затем скажи во что хочешь сыграть.")

    def addgame_response(self):
        return ("Правила мы пишем сами и на это нужно время, а порой - немало :("
                "\nНо если хочешь помочь, то правила можно подготовить по форме {link} и отправить их на {mail}, тогда я смогу рассказывать их другим игрокам и тебе!"
                "\nКакие-либо предложения по улучшения бота или по оказанию иной помощи можно отправлять туда же, будем рады обратной связи :)".format(link=self.__rules_link, mail=self.__email))