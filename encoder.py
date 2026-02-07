
class Encoder:
    def __init__(self,config:dict,data_string:str,err_corr_level:str):
        self.config = config
        self.data_string = data_string
        self.err_corr_level = err_corr_level
        self.mode = ''
        self.version = 40

    ################## DATA ANALYSIS ##################
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
                self.version = int(version)
                return int(version)
        raise ValueError('No QR version founded for the size of input')
    
    ################## ENCODE DATA ##################
    def encode(self)->list[str]:
        """
        Return the encoded data of data_string as codewords
        :param self: Description
        :return: data_codewords
        :rtype: list[str]
        """
        mode_ind = self.get_mode_indicator()
        char_count_ind = self.get_char_count_indicator()
        data_sequence = self.get_data_sequence()
        terminator = self.get_terminator()
        data_bitstream = mode_ind + char_count_ind + ''.join(map(str,data_sequence)) + terminator 
        data_codewords = self.get_data_codewords(data_bitstream)
        return data_codewords

    def get_data_sequence(self)->list[str]:
        """
        Return the data_sequence depending of the selected mode
        :return: data_sequence
        :rtype: list[str]
        """
        sequence = []
        match self.mode:
            case 'numeric':
                # Split into groupe size
                groups= self.split(self.data_string,self.config['group_sizes'][self.mode])
                # Convert each group of digits to its binary equivalent with according lenght
                for i in range(len(groups)): 
                    sequence.append(bin(int(groups[i]))[2:].rjust(self.config['numeric_group_sizes_encoding'][str(len(groups[i]))],'0'))
            case 'alphanumeric':                
                # Convert each character into integer by using Table 5
                string_datas = [self.config['alphanumeric_encoding_table'][char] for char in self.data_string]
                # Split into groupe size
                groups = self.split(string_datas,self.config['group_sizes'][self.mode])

                for group in groups:
                    if len(group) == 2:
                        res = int(group[0] * 45 + group[1])
                    else: 
                        res = group[0]
                    if groups.index(group) == len(groups)-1 and not len(self.data_string) % 2 == 0:
                        res = bin(res)[2:].rjust(self.config['alphanumeric_group_sizes_encoding'][1],'0')
                    else:
                        res = bin(res)[2:].rjust(self.config['alphanumeric_group_sizes_encoding'][0],'0')
                    sequence.append(res)
            case 'byte':
                sequence = [bin(ord(char))[2:] for char in self.data_string]
        return sequence        

    def get_data_codewords(self,data_bitstream:str)->list[str]:
        """
        Split into 8 bit codewords and add pad bytes if necessary
        :type data_bitstream: str
        :return: data_codewords
        :rtype: list[str]
        """
        # Split into 8 bit codewords 
        data_codewords = self.split(data_bitstream,8)
        for i in range(len(data_codewords)):
            if len(data_codewords[i]) < 8:
                data_codewords[i] = data_codewords[i].ljust(8,'0')
        # Add pad codewords
        nb_data_codewords = self.config['data_codewords_number'][str(self.version)][self.err_corr_level]
        nb_pad_codewords = nb_data_codewords - len(data_codewords)
        if not nb_pad_codewords == 0:
            for i in range(0,nb_pad_codewords):
                if i%2 == 0: 
                    data_codewords.append(self.config['pad_codewords'][0])
                else: 
                    data_codewords.append(self.config['pad_codewords'][1])
        return data_codewords

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
    
    #################### TOOLS ####################
    def split(self,list:list,size:int):
        return [list[i:i+size] for i in range(0,len(list),size)]

