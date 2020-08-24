import speech
import sound
from time import sleep

sound.play_effect('drums:Drums_04')



from objc_util import *

AVSpeechUtterance=ObjCClass('AVSpeechUtterance')
AVSpeechSynthesisVoice = ObjCClass('AVSpeechSynthesisVoice')
AVSpeechSynthesizer=ObjCClass('AVSpeechSynthesizer')
voices = AVSpeechSynthesisVoice.speechVoices()
voice=voices[8]

synthesizer=AVSpeechSynthesizer.new()

import cb
import sound
import time
import struct

class HeartRateManager (object):
    def __init__(self):
        self.peripheral = None
        self.counter = 0

    def did_discover_peripheral(self, p):
        if p.name and 'Polar' in p.name and not self.peripheral:
            self.peripheral = p
            print('Connecting to heart rate monitor...')
            cb.connect_peripheral(p)

    def did_connect_peripheral(self, p):
        print('Connected:', p.name)
        print('Discovering services...')
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print('Failed to connect: %s' % (error,))

    def did_disconnect_peripheral(self, p, error):
        print('Disconnected, error: %s' % (error,))
        self.peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            if s.uuid == '180D':
                print('Discovered heart rate service, discovering characteristitcs...')
                p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print('Did discover characteristics...')
        for c in s.characteristics:
            if c.uuid == '2A37':
                self.peripheral.set_notify_value(c, True)

    def did_update_value(self, c, error):
        #print(c.value[1])
        print(self.counter)
        utterance = AVSpeechUtterance.speechUtteranceWithString_(str(c.value[1]))
        utterance.rate=0.5
        utterance.voice=voice
        utterance.useCompactVoice=False
        self.counter += 1
        
        if self.counter % 5 == 0:
        	synthesizer.speakUtterance_(utterance)
        heart_rate = struct.unpack('<B', c.value[1].encode())[0]
        print('hi')
        self.values.append(heart_rate)
        print('Heart rate: %i' % heart_rate)

mngr = HeartRateManager()
cb.set_central_delegate(mngr)
print('Scanning for peripherals...')
cb.scan_for_peripherals()

try:
    while True: pass
except KeyboardInterrupt:
    cb.reset()