from music21 import stream, note, tempo, chord

class BylaPart(object):
    MODE_MODULO = 1
    MODE_MIRROR = 2

    mode = None
    midi_sequence = None
    pitch_sequence = None
    base_note = None
    modulo_pitch = None
    number_of_voices = None

    def __init__(self, **kwargs):
        self.midi_sequence = kwargs.pop('midi_sequence', [])
        self.base_note = kwargs.pop('base_note', 60)
        self.modulo_pitch = kwargs.pop('modulo_pitch', 12)
        self.number_of_voices = kwargs.pop('number_of_voices', 12)
        if not self.midi_sequence:
            self.pitch_sequence = kwargs.pop('pitch_sequence', [])
            self.midi_sequence = map(lambda x: x+self.base_note, self.pitch_sequence)
        self.mode = kwargs.pop('mode', self.MODE_MODULO)

class BylaCestaCore(object):
    def get_tempo_mark(self, tempo_description=None, tempo_bpm=None, tempo_note=None):
        return tempo.MetronomeMark(self.tempo_description, self.tempo_bpm, self.tempo_beat_note)

    def get_souzvuk(self, midi_note, num_voices, mode, base_note=None, modulo_pitch=None):
        # todo
        pass

    def get_souzvuk_mirror(self, midi_note, num_voices, base_note=None):
        # todo
        pass


    def get_souzvuk_modulo(self, midi_note, num_voices, base_note=None, modulo_pitch=None):
        if not base_note:
            base_note = self.base_note

        if not modulo_pitch:
            modulo_pitch = self.modulo_pitch

        notes = set()
        for i in range(num_voices):
            pitch_num = ((midi_note-base_note)*(i+1)) % modulo_pitch
            midi_num = pitch_num + base_note
            notes.add(midi_num)

        for midi_num in notes:
            yield note.Note(midi=midi_num, quarterLength = self.whole)

    def get_measure(self, midi_note, num_voices, modulo_pitch, base_note, first_measure):
        m = stream.Measure()
        if first_measure:
            m.append(self.get_tempo_mark())

        son = chord.Chord(self.get_souzvuk_modulo(
                midi_note=midi_note,
                base_note=base_note,
                num_voices=num_voices,
                modulo_pitch=modulo_pitch,
                ))
        m.append(son)
        return m

    def render(self, structure):
        first_measure = True
        piano = stream.Part()
        for part in structure:
            for midi_note in part.midi_sequence:
                piano.append(byla.get_measure(
                        midi_note=midi_note,
                        num_voices=part.number_of_voices,
                        modulo_pitch=part.modulo_pitch,
                        base_note=part.base_note,
                        first_measure=first_measure))
                if first_measure:
                    first_measure = False
        return piano

class BylaCesta(BylaCestaCore):
    whole = 4
    midi_seq = None
    tempo_bpm = 95
    tempo_description = "medium"
    tempo_beat_note = note.Note(type='half')
    base_note = 60
    modulo_dist = 12


byla_midi_seq = [60, 64, 67, 70, 68, 67, 65, 67, 64, 60]

byla = BylaCesta()

structure = []
for i in range(12):
    structure.append(
    BylaPart(
        midi_sequence=byla_midi_seq,
        base_note=byla.base_note,
        modulo_pitch=12+i,
        number_of_voices=1+i,
        mode=BylaPart.MODE_MODULO
    ))

byla.render(structure=structure).show()
