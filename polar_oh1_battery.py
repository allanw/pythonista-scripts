import cb
import sound
import time
import struct

class HeartRateManager (object):
    def __init__(self):
        self.peripheral = None

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
            print(s.uuid)
            if s.uuid == '180F':
                print('Discovered heart rate service, discovering characteristitcs...')
                p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print('Did discover characteristics...')
        for c in s.characteristics:
            print(c.uuid)
            if c.uuid == '2A19':
                print('dude')
                self.peripheral.read_characteristic_value(c)
                
                self.peripheral.set_notify_value(c, True)
            

    def did_update_value(self, c, error):
        print('wham')
        print(c.value[0])
        print(struct.unpack('<B', c.value[0:]))
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