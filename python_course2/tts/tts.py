#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyttsx3 as tts

end = None


def main():
    engine = tts.init()
    engine.setProperty('volume', 0.7)
    engine.setProperty('rate', 190)

    while True:
        tekst = input('>>')
        engine.say(tekst)
        engine.runAndWait()


################################################################################

main()

################################################################################
