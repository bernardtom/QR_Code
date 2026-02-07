import numpy as np
import json

class FunctionPattern:
    def __init__(self,config:dict,version:int):
        self.version = version
        self.config = config
        self.matrix_size = self.get_matrix_size(version)
        self.function_pattern = np.full((self.matrix_size,self.matrix_size),2,dtype=int)

    def get_matrix_size(self,version:int)->int:
        symbol_sizes_parameter = self.config['symbol_sizes']
        symbol_size = symbol_sizes_parameter['start_size'] + (version - 1) * symbol_sizes_parameter['step']
        return symbol_size
    
    def get_alignment_positions(self)->list[tuple[int]]:
        """
        Return a list with origin position of all symbols 
        :return: Alignement pattern : [(y1_origin,x1_origin),(y2_origin,x2_origin), ...]
        :rtype: list[tuple[int]]
        """
        symbol_size = self.config['alignment_pattern']['size']
        center_positions_range = self.config['alignment_pattern']['positions'][str(self.version)]
        origin_position_range = [pos - int(symbol_size/2) for pos in center_positions_range]
        min_pos_range, max_pos_range = min(origin_position_range), max(origin_position_range)

        symbol_positions = []
        for y in range(len(origin_position_range)):
            for x in range(len(origin_position_range)):
                if (origin_position_range[y],origin_position_range[x]) not in [
                                        (max_pos_range,min_pos_range),
                                        (min_pos_range,min_pos_range),
                                        (min_pos_range,max_pos_range)
                                    ]:
                    symbol_positions.append((origin_position_range[y],origin_position_range[x]))
        return symbol_positions

    def add_alignment_pattern(self)->None:
        """
        Add alignement pattern in function pattern matrix
        """
        if self.version > 1:
            symbol_data = self.config['alignment_pattern']['data']
            symbol_size = self.config['alignment_pattern']['size']

            positions = self.get_alignment_positions()

            for pos in positions:
                for i in range(symbol_size):
                        self.function_pattern[pos[0]+i][pos[1]:pos[1]+symbol_size] = symbol_data[i]