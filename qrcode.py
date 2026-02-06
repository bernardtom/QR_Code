import numpy as np
import json

from encoder import Encoder

CONFIG_FILE = 'config.json'

class QRCode:
    def __init__(self,data_string:str,correction_level:str):
        # Load config file
        self.config = self.load_config(CONFIG_FILE)

        # Check inputs types
        if not isinstance(data_string,str):
            raise TypeError('Invalid Type for data string level parameter')
        if not isinstance(correction_level,str):    
            raise TypeError('Invalid Type for error correction level parameter')
        
        # Check inputs values
        if not len(data_string) > 0:
            raise ValueError('Empty Value for data_string parameter')
        if not correction_level in self.config['correction_levels']:           
            raise ValueError('Invalide Value for error correction level parameter')
        
        self.data_string = data_string
        self.correction_level = correction_level
        self.mode, self.version = self.data_analysis()

    def data_analysis(self)->list:
        self.encoder = Encoder(self.config,self.data_string,self.correction_level)
        mode = self.encoder.select_mode()
        version = self.encoder.select_version()
        return mode,version

    def load_config(self,filename:str)->dict:
        try:
            with open(filename,'r',encoding='utf-8') as file:
                config = json.load(file)
            return config
        except:
            raise FileNotFoundError('config file not founded')