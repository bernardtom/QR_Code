import numpy as np
from PIL import Image, ImageDraw

class QRImage:
    def __init__(self,matrix:np.ndarray,img_size=210):
        """
        Create and save the image of the matrix
        :param matrix: Matrix of QR Code
        :type matrix: np.ndarray
        :param img_size: Size of the image : pixels
        :type img_size: int
        """
        # Check Inputs
        if not isinstance(matrix,np.ndarray):
            raise TypeError('Invalite Type of matrix : have to be an ndarray')
        if not matrix.dtype == np.int_:
            raise TypeError('Invalite Type of data in matrix : have to be a bool')
        if matrix.shape == (0,0):
            raise ValueError("Invalide Value of matrix shape : have to be different of (0,0)")
        if not matrix.shape[0] == matrix.shape[1]:
            raise ValueError('Invalide Value of matrix shape : width and height have to be same')
        self.matrix = matrix
        self.matrix_size = len(matrix)
        
        if not isinstance(img_size,int):
            raise TypeError('Invalite Type of image size')
            raise ValueError('Invalide Value of image shape : width and height have to be same')
        
        self.module_size = self.get_module_size(self.matrix_size,img_size)
        self.img_size = self.matrix_size * self.module_size
        self.img_shape = (self.img_size,self.img_size)

    def get_module_size(self,matrix_size:int,img_size:int)->int:
        min_module_size = 50
        module_size = int(img_size / matrix_size)
        if not module_size >= min_module_size:
            module_size = min_module_size
        return module_size
    
    def generate(self,img_file_name='img'):
        """
        Create and save the image of the matrix
        :param self: Description
        :param img_file_name: Description
        """
        if not isinstance(img_file_name,str):
            raise TypeError('Invalid type of img_file_name : have to be str')
        
        image = Image.new(mode='RGB', size=self.img_shape, color='white')
        draw = ImageDraw.Draw(image)
        
        colors={0: 'white',
                1: 'black',
                2: 'grey'}    
        for (y,x) , value in np.ndenumerate(self.matrix):
                y_start = y*self.module_size
                x_start = x *self.module_size
                y_end = y_start + self.module_size
                x_end = x_start + self.module_size
                draw.rectangle([x_start,y_start,x_end,y_end],fill=colors[value])
        
        image.save(img_file_name+".png")
        print(f'Image generated : image size : {self.img_size}, filename : {img_file_name}')
    
