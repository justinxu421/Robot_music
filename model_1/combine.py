from music21 import * 
import os
import random

def getMidisToCombine(source_location):
    midisList = os.listdir(source_location)
    midisToCombine = random.sample(midisList, 4)
    #midisToCombine = [source_location + midi for midi in midisToCombine]
    return midisToCombine

def combineMidis(source_location, write_location, midisToCombine):
    if len(midisToCombine) == 0: return 

    # Combine all the midis into one midi
    first_file = source_location + midisToCombine[0]
    midi = converter.parse(first_file)
    for i in range(1, len(midisToCombine)): 
        musicPart = converter.parse(source_location + midisToCombine[i])
        midi.insert(0, musicPart)

    # Create a unique name for the new combined midi
    new_file_name = write_location 
    for midi_name in midisToCombine:
        new_file_name += midi_name[:-4]
    new_file_name += ".mid"

    # Write the midi to disk 
    midi.write('midi', new_file_name)
    return new_file_name

source_location = './new_beats/'
write_location = './new_songs/'
midisToCombine = getMidisToCombine(source_location)
print(midisToCombine)
new_file_name = combineMidis(source_location, write_location, midisToCombine)

def getFeatures(source_location, midi_name):
    score = converter.parse(source_location + midi_name)

    features = {}

    key = score.analyze('key')
    features['key'] = key.tonic.name
    features['mode'] = key.mode

    for part in score:
        print(part)
        for i in part:

            # If this is a music note
            if str(type(i)) == str(type(note.Note("F5"))): 
                
                if i.name in features:
                    features[i.name] += 1
                else:
                    features[i.name] = 1
                
                octave = "octave-" + str(i.octave)
                if octave in features: 
                    features[octave] += 1
                else:
                    features[octave] = 1

                length = "noteLength-" + str(i.quarterLength)
                if length in features:
                    features[length] += 1
                else:
                    features[length] = 1

    return features

source_location = './old_songs/'
midi_name = 'Piano man - Bridge.midi'
features = getFeatures(source_location, midi_name)
print(features)