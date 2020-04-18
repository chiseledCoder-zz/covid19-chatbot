from django.shortcuts import render
from googletrans import Translator
# Create your views here.

translator = Translator()


def detect_lang(message):
    return translator.detect(message).lang


def translate(phrase, lang):
    return translator.translate(phrase, dest=lang).text
