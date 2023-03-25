#!/usr/bin/python3
# -*- coding: utf-8 -*-

end = None

import speech_recognition as sr

r = sr.Recognizer()

while True:
  tekst = input(">>")
  if len(tekst)>0:
    print("sig/stt/pc",tekst)
  else:
    with sr.Microphone() as source:
      print("slucham ...")
      audio = r.listen(source)
      try:
        tekst = r.recognize_google(audio, language='pl_PL')
        # send(f"sig/stt/{SRC}",tekst)
        print(tekst)

        if tekst=='koniec':
          break
      except sr.UnknownValueError:
        print('nie rozumiem')
      except sr.RequestError as e:
        print('error:',e)
      end
    end
  end
end

################################################################################
