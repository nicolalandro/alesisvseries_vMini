import mido
import os

PORT = 'VMini:VMini MIDI 1 20:0'

if __name__ == '__main__':
    print(mido.get_ioport_names())
    port = mido.open_ioport(PORT)

    while True:
        r = port.receive()
        if r.type == 'control_change' and r.channel == 0 and r.control == 14:
            print(r.value)
            os.system(('pactl set-sink-volume 0 %d' % r.value) + '%')

    port.close()
