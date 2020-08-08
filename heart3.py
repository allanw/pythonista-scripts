import speech
import sound

sound.play_effect('drums:Drums_04')



from objc_util import *

AVSpeechUtterance=ObjCClass('AVSpeechUtterance')
AVSpeechSynthesisVoice = ObjCClass('AVSpeechSynthesisVoice')
AVSpeechSynthesizer=ObjCClass('AVSpeechSynthesizer')
voices = AVSpeechSynthesisVoice.speechVoices()
voice=voices[8]

synthesizer=AVSpeechSynthesizer.new()

while True:
  utterance = AVSpeechUtterance.speechUtteranceWithString_('keep it moving mate')
  utterance.rate=0.5
  utterance.voice=voice
  utterance.useCompactVoice=False
  synthesizer.speakUtterance_(utterance)
