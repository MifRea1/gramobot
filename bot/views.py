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
    debug = False
    def start(chat_id):
        TelegramBot.sendMessage(chat_id, 'Поехали!')
    def stop(chat_id):
        TelegramBot.sendMessage(chat_id, 'Приехали.')
    def help(chat_id):
        pass
    def debug(self):
        self.debug = not self.__debug

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        c = Commands()
        commands = {
            '/start': Commands.start,
            '/stop': Commands.stop,
            '/help': Commands.help,
            '/debug': Commands.debug,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')
            func = commands.get(cmd.split()[0].lower())
            if func:
                func(chat_id)
            else:
                if c.debug:
                    TelegramBot.sendMessage(chat_id, 'DEBUG MODE')
                    TelegramBot.sendMessage(chat_id, raw)
                else:
                    TelegramBot.sendMessage(chat_id, cmd)

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs) 