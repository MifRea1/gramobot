import json
import logging

import telepot
# from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
 

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


class Commands():
    debugOn = False
    def __init__(self):
        self.debugOn = False

    def help(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Under development.')

    def start(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Поехали!')

    def stop(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Приехали.')

    def debug(self, chat_id):
        self.debugOn = not self.debugOn

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        c = Commands()
        commands = {
            '/start': c.start,
            '/stop': c.stop,
            '/help': c.help,
            '/debug': c.debug,
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
                    if c.debugOn:
                        TelegramBot.sendMessage(chat_id, 'DEBUG MODE')
                        TelegramBot.sendMessage(chat_id, raw)
                    else:
                        TelegramBot.sendMessage(chat_id, text)

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs) 