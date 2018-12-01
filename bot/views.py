import json
import logging
# import os
import random
import telepot
# from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
 

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')

GREETINGS_KEYWORDS = ('hi', 'hello', 'привет', 'прив')
GREETINGS_RESPONSES = ['ни хао', 'бонжур', 'привет']

class Commands():
    # def __init__(self):
    #     os.environ["DEBUG"] = "0"

    def help(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Under development.')

    def start(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Поехали!')

    def stop(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Приехали.')

    def main(self, chat_id, text):
        for word in text.words:
            if word.lower() in GREETINGS_KEYWORDS:
                TelegramBot.sendMessage(chat_id, random.choice(GREETINGS_RESPONSES))
                break
        else:
            TelegramBot.sendMessage(chat_id, text)

    # def debug(self, chat_id):
    #     if os.environ["DEBUG"] == "0":
    #         TelegramBot.sendMessage(chat_id, 'Включаем отладку.')
    #         os.environ["DEBUG"] = "1"
    #     else:
    #         TelegramBot.sendMessage(chat_id, 'Всё отладили.')
    #         os.environ["DEBUG"] = "0"

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        c = Commands()
        commands = {
            '/start': c.start,
            '/stop': c.stop,
            '/help': c.help,
            # '/debug': c.debug,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            message = payload['message']
            chat_id = message['chat']['id']
            text = message.get('text')
            if text:
                func = commands.get(text.split()[0].lower())
                if func:
                    func(chat_id)
                else:
                    # if os.environ["DEBUG"] == "0":
                    #     TelegramBot.sendMessage(chat_id, raw)
                    # else:
                    c.main(chat_id, text)

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs) 