
class Encoder:
    def __init__(self,config:dict,data_string:str,err_corr_level:str):
        self.config = config
        self.data_string = data_string
        self.err_corr_level = err_corr_level

    def select_mode(self)->str:
        """
        Select the better mode according to the data string by converting characters into bytes and checking in mode byte table
        :return: mode : numeric | alphanumeric | byte
        :rtype: str
        """
        mode = 'numeric'
        for c in self.data_string:
            if self.char_in_mode(c,'byte'):
                mode = 'byte'
            elif self.char_in_mode(c,'alphanumeric'):
                if not mode == 'byte':
                    mode = 'alphanumeric'
            else: 
                if not self.char_in_mode(c,'numeric'):
                    raise ValueError('Character not available')
        return mode

    def char_in_mode(self,char:str,mode:str)->bool:
        """
        Return True if the character is in the mode byte table
        :type char: str
        :type mode: str 
        :rtype: bool
        """
        char_unicode = ord(char)
        inside = False
        for byte_range in self.config['mode_bytes'][mode]:
            min, max = int(byte_range[0],16), int(byte_range[1],16)
            if min <= char_unicode <= max:
                inside = True
                break
        if inside == False:
            #print(f'char : {char} not in {mode} ; hex : {hex(char_unicode)}')
            return False
        return True