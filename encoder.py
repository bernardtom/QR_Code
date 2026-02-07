
class Encoder:
    def __init__(self,config:dict,data_string:str,err_corr_level:str):
        self.config = config
        self.data_string = data_string
        self.err_corr_level = err_corr_level
        self.mode = ''
        self.version = 40

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
        self.mode = mode
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
    
    def select_version(self)->int:
        for version in self.config['data_capacity'][self.mode]:
            data_capacity = self.config['data_capacity'][self.mode][version][self.err_corr_level]
            if len(self.data_string) <= data_capacity:
                self.version = version
                return int(version)
        raise ValueError('No QR version founded for the size of input')
    
    ################## INDICATORS ##################
    def get_mode_indicator(self)->str:
        return self.config['mode_indicators'][self.mode]

    def get_char_count_indicator(self)->str:
        for version in self.config['char_count_indicator_sizes'][self.mode]:
            version_min, version_max = version.split('-')
            if int(version_min) <= self.version <= int(version_max):
                count_ind_size = self.config['char_count_indicator_sizes'][self.mode][version]
                return bin(len(self.data_string))[2:].rjust(count_ind_size,'0')

    def get_terminator(self)->str:
        return self.config['terminator']
