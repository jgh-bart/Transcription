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
        self.phonemes = set(phoneme_list)
    
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
        # single-character affricate symbols, if preferred
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

def notation_to_notation(input_string, input_notation, output_notation):
    output = ''
    for phoneme in input_string.split(' '):
        # stress markers in IPA to front of syllable
        if output_notation == 'ipa' and ((input_notation == 'arpa' and phoneme in ['1','2','0']) or (input_notation == 'xsampa' and phoneme in ['"','%','-'])):
            idx = len(output) - 1
            while idx > 0 and output[idx - 1] != '.':
                idx -= 1
            stress_marker = eng_phoneme_set.get_arpa(phoneme).ipa if input_notation == 'arpa' else eng_phoneme_set.get_xsampa(phoneme).ipa
            output = output[:idx] + stress_marker + output[idx:]
        else:
            try:
                if input_notation == 'arpa' and output_notation == 'xsampa':
                    output += eng_phoneme_set.get_arpa(phoneme).xsampa
                elif input_notation == 'xsampa' and output_notation == 'arpa':
                    output += eng_phoneme_set.get_xsampa(phoneme).arpa
                elif input_notation == 'arpa' and output_notation == 'ipa':
                    output += eng_phoneme_set.get_arpa(phoneme).ipa
                elif input_notation == 'xsampa' and output_notation == 'ipa':
                    output += eng_phoneme_set.get_xsampa(phoneme).ipa
            except:
                raise ValueError(phoneme + ': invalid input character')
        if output_notation in ['xsampa', 'arpa']:
            output += ' '
    return output.encode('utf-8')

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

def print_all(phoneme_set):
    print 'ARPA  X-SAMPA   IPA'
    for symbol in ['p','b','t','d','k','g',                 # stops
                   'm','n','ng',                            # nasals
                   'f','v','th','dh','s','z','sh','zh','h', # fricatives
                   'ch','jh',                               # affricates
                   'w','l','r','y',                         # approximants
                   'a','aa','i','ii','uh','u','uu',
                   'e','ax','aax','o','oo',                 # vowels
                   'ai','oi','au','ou','iax','eax','uax',   # diphthongs
                   '1','2','0']:                            # stress
        phoneme_set.get_arpa(symbol).print_phoneme()
