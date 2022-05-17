from mido import Message, MidiFile, MidiTrack
from scipy.interpolate import interp1d
from os import getcwd

m = interp1d([-180, 180], [0, 127])


def quake_to_msg(quake):
    lat, long, z = quake.lat, quake.long, quake.z

    n = min(int(2*m(long)), 100)
    # min velocity 10, max 127
    v = max(min(int(quake.mag / 4.0 * 127.0), 127), 10)
    on = Message('note_on', note=n, velocity=v, time=32)
    off = Message('note_off', note=n, time=32)
    return on, off, n


# takes earthquake list, makes MIDI, writes it to quakes.mid
def quakes_to_midi(quakes):
    mid = MidiFile()
    mid.type = 0
    track = MidiTrack()
    mid.tracks.append(track)

    if len(quakes) == 0:
        pass

    prev_time = quakes[0].time
    track.append(Message('program_change', program=12, time=0))

    for q in quakes:
        on, off, note = quake_to_msg(q)
        time_diff = q.time - prev_time
        time_diff = int(time_diff / 1000)

        track.append(Message('note_off', note=64, time=time_diff))
        track.append(on)
        track.append(off)
        prev_time = q.time

    mid.save(getcwd()+"/quakes.mid")

    return 0
