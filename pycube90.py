# pycube90 v0.5

class Cube:
    def __init__(self, key, nonce=""):
        self.key = ""
        self.master_list = []
        self.alphabet_dict = {}
        self.alphabet_dict_rev = {}
        self.start_char = 32
        self.alphabet_size = 91
        self.size_factor = 3
        for x in range(0,self.alphabet_size):
            self.alphabet_dict[chr(x + self.start_char)] = x
            self.alphabet_dict_rev[x] = chr(x + self.start_char)

        def gen_cube(depth, width, length):
            for z in range(0,depth):
                section_list = []
                for y in range(0,width):
                    alphabet = []
                    for x in range(0,length):
                        alphabet.append(chr(x + self.start_char))
                    for mod in range(0,y):
                        shift = alphabet.pop(0)
                        alphabet.append(shift)
                        shift = alphabet.pop(2)
                        alphabet.insert(44,shift)
                    section_list.append(alphabet)
                self.master_list.append(section_list)

        gen_cube(self.size_factor, self.size_factor, self.alphabet_size)
        self.init(key)
        if nonce != "":
            self.key_cube(nonce)

    def key_cube(self, key):
        for section in self.master_list:
            for char in key:
                char_value = self.alphabet_dict[char]
                sized_pos = char_value % self.size_factor
                for alphabet in section:
                    key_sub = alphabet.pop(char_value)
                    alphabet.append(key_sub)
                    for y in range(0,char_value):
                        if y % 2 == 0:
                            shuffle = alphabet.pop(0)
                            alphabet.append(shuffle)
                            shuffle = alphabet.pop(2)
                            alphabet.insert(44,shuffle)
        for char in key:
            char_value = self.alphabet_dict[char]
            sized_pos = char_value % self.size_factor
            for x in range(char_value):
                section = self.master_list.pop(sized_pos)
                self.master_list.append(section)

    def load_key(self, skey):
	self.key_list = []
        self.key = skey
        for element in self.key:
            self.key_list.append(element)

    def key_scheduler(self, key):
        sub_key = ""
        for element in key:
            pos = self.alphabet_dict[element]
            sized_pos = pos % self.size_factor
            section = self.master_list[sized_pos]
            sub_alpha = section[sized_pos]
            sub = sub_alpha.pop(pos)
            sub_alpha.append(sub)
            sub_key += sub
        self.load_key(sub_key)
        return sub_key
    
    def init(self, key):
        self.load_key(key)
        self.key_cube(key)

    def morph_cube(self, counter, sub_key):
        mod_value = counter % self.alphabet_size
        for section in self.master_list:
            for key_element in sub_key:
                key_value = self.alphabet_dict[key_element]
                shift_value = key_value % self.size_factor
                for alphabet in section:
                    alphabet[shift_value], alphabet[mod_value] = alphabet[mod_value], alphabet[shift_value]
            section_shift = self.master_list.pop(key_value % self.size_factor)
            self.master_list.append(section_shift)

    def encrypt(self, words):
        cipher_text = ""
        sub_key = self.key
        for counter, letter in enumerate(words):
            sub = letter
            for section in self.master_list:
                for alphabet in section:
                    sub_pos = self.alphabet_dict[sub]
                    sub = alphabet[sub_pos]
                    shift = alphabet.pop(0)
                    alphabet.append(shift)
            sub_key = self.key_scheduler(sub_key)
            self.morph_cube(counter, sub_key)
            cipher_text += sub
        return cipher_text

    def decrypt(self, words):
        plain_text = ""
        sub_key = self.key
        for counter, letter in enumerate(words):
            sub = letter
            for section in reversed(self.master_list):
                for alphabet in reversed(section):
                    sub_pos = alphabet.index(sub)
                    sub = self.alphabet_dict_rev[sub_pos]
                    shift = alphabet.pop(0)
                    alphabet.append(shift)
            sub_key = self.key_scheduler(sub_key)
            self.morph_cube(counter, sub_key)
            plain_text += sub
        return plain_text

class CubePassword:
    def __init__(self, min=32, max=123):
        self.char = " "
        self.min = min
        self.max = max

    def password(self, length=12, num=1):
        import os
        from pycube256 import CubeRandom
        passw = []
        self.char = self.char * length
        for x in range(num):
            self.entropy = CubeRandom().randrange(self.min, self.max, length)
            self.cube = Cube(self.entropy)
            passw.append(self.cube.encrypt(self.char))
        return passw
