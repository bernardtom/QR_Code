import numpy as np
import json

class FunctionPattern:
    def __init__(self,config:dict,version:int,correction_level:str):
        self.version = version
        self.config = config
        self.matrix_size = self.get_matrix_size(version)
        
    def get_pattern(self)->np.ndarray:
        self.function_pattern = np.full((self.matrix_size,self.matrix_size),2,dtype=int)
        self.add_alignment_pattern()
        self.add_timing_pattern()
        self.add_finder_pattern()
        self.add_separator_pattern()
        return self.function_pattern

    def get_matrix_size(self,version:int)->int:
        symbol_sizes_parameter = self.config['symbol_sizes']
        symbol_size = symbol_sizes_parameter['start_size'] + (version - 1) * symbol_sizes_parameter['step']
        return symbol_size

    def add_alignment_pattern(self)->None:
        """
        Add alignement pattern in function pattern matrix
        """
        if self.version > 1:
            symbol_data = self.config['alignment_pattern']['data']
            symbol_size = len(symbol_data)

            positions_range = self.config['alignment_pattern']['positions'][str(self.version)]
            min_pos, max_pos = min(positions_range), max(positions_range)
            for y in positions_range:
                for x in positions_range:
                    if (y,x) not in [(max_pos,min_pos),(min_pos,min_pos),(min_pos,max_pos)]:
                        for i in range(symbol_size):
                            self.function_pattern[y+i][x:x+symbol_size] = symbol_data[i]
    
    def add_timing_pattern(self)->None:
        start_pos = self.config['timing_pattern_position']
        value_list_size = self.matrix_size - start_pos
        value_list = [(i+1)%2 for i in range(value_list_size)]

        # Add horizontal values
        self.function_pattern[start_pos][start_pos:] = value_list
        # Add vertical values
        for i in range(start_pos,self.matrix_size):
            self.function_pattern[i][start_pos] = value_list[i-start_pos]

    def add_finder_pattern(self)->None:
        symbol_data = self.config['finder_pattern']['data']
        symbol_size = len(symbol_data)
        positions = self.config['finder_pattern']['positions']

        for pos in positions:
            if 'up' in pos:
                y = 0
            if 'down' in pos:
                y = self.matrix_size - symbol_size
            if 'left' in pos:
                x = 0
            if 'right' in pos:
                x = self.matrix_size - symbol_size
            # Add lines
            for i in range(symbol_size):
                self.function_pattern[y+i][x:x+symbol_size] = symbol_data[i]

    def add_separator_pattern(self)->None:
        symbol_size = self.config['separator_pattern']['size']
        symbol_datas = [0 for i in range(symbol_size)]
        positions = self.config['separator_pattern']['positions']

        for pos in positions:
            if 'up' in pos:
                y_row = 0
                y_line = symbol_size - 1
            if 'down' in pos:
                y_row = self.matrix_size - symbol_size
                y_line = y_row
            if 'left' in pos:
                x_row = symbol_size - 1
                x_line = 0
            if 'right' in pos:
                x_row = self.matrix_size - symbol_size
                x_line = self.matrix_size - symbol_size

            # Add row
            for i in range(symbol_size):
                self.function_pattern[y_row + i][x_row] = symbol_datas[i]
            # Add line
            self.function_pattern[y_line][x_line:x_line + symbol_size] = symbol_datas
