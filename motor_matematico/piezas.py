#motor_matematico/piezas.py
import numpy as np

#Tetrominos
tetrominos = {
    "i": np.array([[1, 1, 1, 1]]),
    "O": np.array([[1, 1],
                   [1, 1]]),
    "S" : np.array([[0, 1, 1],
                    [1, 1, 0],]),
    "l" : np.array([[1, 0]
                    [1, 0]
                    [1, 1]]),
    "T" : np.array([[1, 1, 1],
                    [0, 1, 0]])
}
#Pentominos
pentaminos = {
    "F" : np.array([[0, 1, 1],
                    [1, 1, 0],
                    [0, 1, 0]]),
    "I" : np.array([[1, 1, 1, 1, 1]]),
    "L" : np.array ([[1, 0],
                     [1, 0],
                     [1, 0],
                     [1, 1]]),
    "N" : np.array([[0, 1],
                    [1, 1],
                    [1, 0],
                    [1, 0]]),
    "P" : np.array([[0, 1],
                    [1, 1]
                    [1, 1],]),
    "t" : np.array([[1, 1, 1],
                    [0, 1, 0],
                    [0, 1, 0]]),
    "U" : np.array([[1, 0, 1],
                    [1, 1, 1]]),
    "V" : np.array([[1, 0, 0],
                    [1, 0, 0],
                    [1, 1, 1]]),
    "W" : np.array([[1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 1]]),
    "X" : np.array([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]]),
    "Y" : np.array([[0, 1],
                    [1, 1],
                    [0, 1],
                    [0, 1]]),
    "Z" : np.array([[1, 1, 0],
                     [0, 1, 0],
                     [0, 1, 1]])                                                                                            

}

