from random import shuffle

adjectives = [
    'cute',
    'frisky',
    'hungy',
    'eepy',
    'playful',
    'kittenish',
    'catty',
    'sulky',
    'destructive',
    'meowy',
    'sleek',
    'agile',
    'toothy',
    'purring',
    'mewing',
    'hunting',
    'feral',
    'sharp',
    'yowling',
    'prowling',
    'fluffy'
]

nouns = [
    'kitty',
    'kitten',
    'huntress',
    'mittens',
    'climber',
    'stinker',
    'mischief_maker',
    'gremlin',
    'fluff_ball',
    'shrimpy',
    'fuzz_muffin',
    'cutie_pie',
    'prowess',
    'claws',
    'purr',
    'meow',
    'biscuits',
    'panther',
    'litter_box',
    'hair_ball'
]

class LabelMaker:
    def __init__(self):
        self.free_labels = []
        self.round = 0

    def build(self):
        for adj in adjectives:
            for noun in nouns:
                label = adj + '_' + noun
                if self.round > 0:
                    label += '_' + str(self.round)
                self.free_labels.append(label)

        shuffle(self.free_labels)
        self.round += 1

    def make(self):
        if len(self.free_labels) == 0:
            self.build()
        return self.free_labels.pop()

