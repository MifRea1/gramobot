import json
import logging
import random
import telepot
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')

GREETINGS_KEYWORDS = ('hi', 'hello', 'привет', 'прив',)
GREETINGS_RESPONSES = ['ни хао', 'бонжур', 'привет']

class Commands():
    def help(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Under development.')

    def start(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Поехали!')

    def stop(self, chat_id):
        TelegramBot.sendMessage(chat_id, 'Приехали.')

    def timer(self, chat_id, time):
        TelegramBot.sendMessage(chat_id, 'Таймер установлен на ' + str(time) + ' минут.')

    def main(self, chat_id, text):
        words = text.split(' ')
        for word in words:
            if word.lower() in GREETINGS_KEYWORDS:
                TelegramBot.sendMessage(chat_id, random.choice(GREETINGS_RESPONSES))
                break
        else:
            TelegramBot.sendMessage(chat_id, text)

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        c = Commands()
        commands = {
            '/start': c.start,
            '/stop': c.stop,
            '/help': c.help,
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
                words = text.split()
                first_word = words[0]
                func = commands.get(first_word.lower())
                if func:
                    func(chat_id)
                elif first_word == '/timer':
                    c.timer(chat_id, int(words[1]))
                else:
                    c.main(chat_id, text)
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
