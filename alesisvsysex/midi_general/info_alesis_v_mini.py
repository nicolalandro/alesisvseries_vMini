import mido

PORT = 'VMini:VMini MIDI 1 20:0'

if __name__ == '__main__':
    print(mido.get_ioport_names())
    port = mido.open_ioport(PORT)

    while True:
        r = port.receive()
        print(r.type)

    port.close()
