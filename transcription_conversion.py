'''
Conversion from ARPABET to X-SAMPA and vice versa, and to IPA
'''

class phoneme:
    def __init__(self, arpa, xsampa, ipa):
        self.arpa   = arpa
        self.xsampa = xsampa
        self.ipa    = ipa
    
    def print_phoneme(self):
        print self.arpa.ljust(7), self.xsampa.ljust(7), self.ipa.encode('utf-8')

class phoneme_set:
    def __init__(self, phoneme_list):
        self.phonemes = phoneme_list
    
    def print_set(self):
        print 'ARPA  X-SAMPA   IPA'
        for phoneme in self.phonemes:
            phoneme.print_phoneme()
    
    def get_arpa(self, symbol):
        # return the phoneme with this ARPABET symbol
        for phoneme in self.phonemes:
            if phoneme.arpa == symbol:
                return phoneme
        raise ValueError('ARPABET ' + symbol + ' not in phoneme set')
    
    def get_xsampa(self, symbol):
        # return the phoneme with this X-SAMPA symbol
        for phoneme in self.phonemes:
            if phoneme.xsampa == symbol:
                return phoneme
        raise ValueError('X-SAMPA ' + symbol + ' not in phoneme set')

unchanged_phonemes = [
        'p','b','t','d','k','g',  # stops
        'm','n',                  # nasals
        'f','v','s','z','h',      # fricatives
        'w','l',                  # approximants
        '.']                      # syllable break

eng_phoneme_set = phoneme_set(
        # unchanged phonemes
       [phoneme(x, x, x) for x in unchanged_phonemes] +
       [# nasals
        phoneme('ng', 'N', u'\u014B'),
        # fricatives
        phoneme('th', 'T', u'\u03B8'),
        phoneme('dh', 'D', u'\u00F0'),
        phoneme('sh', 'S', u'\u0283'),
        phoneme('zh', 'Z', u'\u0292'),
        # affricates
        phoneme('ch', 'tS', u't\u0283'),
        phoneme('jh', 'dZ', u'd\u0292'),
        # single-character IPA affricate symbols, if preferred
        #phoneme('ch', 'tS', u'\u02A7'),
        #phoneme('jh', 'dZ', u'\u02A4'),
        # approximants
        phoneme('r', 'r\\', u'\u0279'),
        phoneme('y', 'j', 'j'),
        # vowels
        phoneme('a', '{', u'\u00E6'),
        phoneme('aa', 'A', u'\u0251:'),
        phoneme('i', 'I', u'\u026A'),
        phoneme('ii', 'i:', 'i:'),
        phoneme('uh', 'V', u'\u028C'),
        phoneme('u', 'U', u'\u028A'),
        phoneme('uu', 'u:', 'u:'),
        phoneme('e', 'E', u'\u025B'),
        phoneme('ax', '@', u'\u0259'),
        phoneme('aax', '3:', u'\u025C:'),
        phoneme('o', 'Q', u'\u0252'),
        phoneme('oo', 'O', u'\u0254:'),
        # diphthongs
        phoneme('ai', 'aI', u'a\u026A'),
        phoneme('oi', 'OI', u'\u0254\u026A'),
        phoneme('au', 'aU', u'a\u028A'),
        phoneme('ou', '@U', u'\u0259\u028A'),
        phoneme('iax', 'I@', u'\u026A\u0259'),
        phoneme('eax', 'E@', u'\u025B\u0259'),
        phoneme('uax', 'U@', u'\u028A\u0259'),       
        # stress
        phoneme('1', '"', u'\u02C8'),
        phoneme('2', '%', u'\u02CC'),
        phoneme('0', '-', '')])

def phoneme_to_phoneme(symbol, input_notation, output_notation):
    # return the output symbol corresponding to the input symbol
    from_input = {'arpa':   (lambda phoneme_set: phoneme_set.get_arpa(symbol)),
                  'xsampa': (lambda phoneme_set: phoneme_set.get_xsampa(symbol)),
                  'ipa':    (lambda phoneme_set: phoneme_set.get_ipa(symbol))}
    to_output  = {'arpa':   (lambda phoneme: phoneme.arpa),
                  'xsampa': (lambda phoneme: phoneme.xsampa),
                  'ipa':    (lambda phoneme: phoneme.ipa.encode('utf-8'))}
    return to_output[output_notation](from_input[input_notation](eng_phoneme_set))

def notation_to_notation(input_string, input_notation, output_notation):
    output = ''
    for phoneme in input_string.split(' '):
        # stress markers
        if (input_notation == 'arpa' and phoneme[-1] in ['1','2','0']) or (input_notation == 'xsampa' and phoneme[-1] in ['"','%','-']):
            # if vowel and stress marker concatenated, deal with vowel
            if len(phoneme) > 1:
                output += phoneme_to_phoneme(phoneme[:-1], input_notation, output_notation) + ' '
            # stress marker position: shift to front of syllable for IPA
            stress_marker = phoneme_to_phoneme(phoneme[-1], input_notation, output_notation)
            idx = len(output)
            if output_notation == 'ipa':
                while idx > 0 and output[idx - 1] != '.':
                    idx -= 1
            output = output[:idx] + stress_marker + output[idx:]
        # all other characters: retrieve by phoneme_to_phoneme
        else:
            try:
                output += phoneme_to_phoneme(phoneme, input_notation, output_notation)
            except:
                raise ValueError(input_notation + ' ' + phoneme + ': not recognised')
        if output_notation in ['xsampa', 'arpa']:
            output += ' '
    return output

arpa_input = 'g uu 1 . g ax 0 l . b a 2 ng . ax 0'
print 'ARPA:   ', arpa_input
print 'X-SAMPA:', notation_to_notation(arpa_input, 'arpa', 'xsampa')
print 'IPA:    ', notation_to_notation(arpa_input, 'arpa', 'ipa')
print

xsampa_input = 'g u: " . g @ - l . b { % N . @ -'
print 'X-SAMPA:', xsampa_input
print 'ARPA:   ', notation_to_notation(xsampa_input, 'xsampa', 'arpa')
print 'IPA:    ', notation_to_notation(xsampa_input, 'xsampa', 'ipa')
print

eng_phoneme_set.print_set()
