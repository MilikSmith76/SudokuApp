from random import randint
from math import floor

class VerifierTemplate:
    @staticmethod
    def getTemplate():
        return dict({1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False})
# End of VerifierTemplate

class Sudoku:
    """
    Description:
        A class used to generate 9X9 sudoku grids.
    Variables:
        sudokuGrid (Array): An array representing a flattened sudoku grid.
        rowVerifiers (dict[]): An array of dictionaries used to determine which numbers are present in certain rows.
        colVerifiers (dict[]): An array of dictionaries used to determine which numbers are present in certain columns.
        blockVerifiers (dict[]): An array of dictionaries used to determine which numbers are present in certain block.
        blockCoordinates (int[]): A 2d array used to determine what block a position belongs in.
    Methods:
        resetVerifiers()
        validPosition(int, int, int, int)
        fillPosition(int, int, int, int, int, (boolean))
        fillBlock(int, (int))
        fillGrid(int, (int))
        generate()
        generateFixed(int, int)
        getGrid()
        validate(int[])
        printVerifierResults()
        printGrid(int[])
    """

    def __init__(self):
        """
        Description:
            Constructor for the Sudoku class.
        """
        self.sudokuGrid = []
        self.rowVerifiers = None
        self.colVerifiers = None
        self.blockVerifiers = None

        # Creates an array relating a position to the block it belongs in.
        bMap1 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        bMap2 = [3, 3, 3, 4, 4, 4, 5, 5, 5]
        bMap3 = [6, 6, 6, 7, 7, 7, 8, 8, 8]
        self.blockCoordinates = bMap1 + bMap1 + bMap1 + bMap2 + bMap2 + bMap2 + bMap3 + bMap3 + bMap3

    def resetVerifiers(self):
        """
        Description:
            Resets the verifiers used for sudoku grid creation
        """
        self.rowVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]
        self.colVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]
        self.blockVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]

    def validPosition(self, row, col, block, value):
        """
        Descripton:
            Determines if it is valid to insert a value into a certain row, column, and block combination.
        Parameters:
            row (int): The row to be checked for value insertion validity.
            col (int): The column to be checked for value insertion validity.
            block (int): The block to be checked for value insertion validity.
            value (int): The value to be checked for insertion.
        Returns:
            True if the value can be inserted in this position, otherwise returns false.
        """
        # Checks if the value exists in the row, column and block. If it does not exist in any of them then return true
        return not (self.rowVerifiers[row][value] or self.colVerifiers[col][value] or self.blockVerifiers[block][value])

    def fillPosition(self, position, row, col, block, value, fill=True):
        """
        Description:
            Inserts a value into the sudoku grid, and updates the verifiers.
        Parameters:
            position (int): The position where the value will be inserted.
            row (int): The row corresponding to the position.
            col (int): The column corresponding to the position.
            block (int): The block corresponding to the position.
            value (int): The value to be inserted.
            fill (int): Flag used to determine whether to insert the value or remove the value.
        """
        if (fill):
            self.sudokuGrid[position] = value
        else:
            self.sudokuGrid[position] = 0
        self.rowVerifiers[row][value] = fill
        self.colVerifiers[col][value] = fill
        self.blockVerifiers[block][value] = fill

    def fillBlock(self, block, value=None):
        """
        Description:
            Fills remaining values in a 3X3 blocks for the sudoku grid.
        Parameters:
            block (int): The block to filled in.
            value (int): The value that has already been inserting into the block.
        """
        # Creates an array with 1 to 9 in order
        numbers = [i for i in range(1, 10)]

        counter = 9

        # If a value has already been inserted into the block, remove the value from the array.
        if (value is not None):
            numbers.pop(value - 1)

        # Get the position of the upper lef most value in the block. Also get the row and column associated to the position.
        position = 27 * floor(block / 3) + 3 * (block % 3)
        row = floor(position / 9)
        col = position % 9

        # Creates block by randomly taking numbers from the array of numbers.
        while counter > 0:
            # If the position has no value randomly insert a value remaining in the array of numbers.
            if (self.sudokuGrid[position] == 0):
                value = numbers.pop(randint(1, len(numbers)) - 1)
                self.fillPosition(position, row, col, block, value)
            counter -= 1

            # Move to the next position in the block.
            if (counter % 3 == 0):
                position += 7
                row += 1
                col -= 2
            else:
                position += 1
                col += 1

    def fillGrid(self, position, fixedPosition=None):
        """
        Description:
            Recursively fills the rest of the sudoku grid.
        Parameters:
            position (int): The position to be assigned a value.
            fixedPosition (int): The position that is fixed, thus needing to be skipped over.
        Returns:
            Returns True if this position has a valid value that can be inserted into it.
        """
        # Stop recursing when all positions are filled.
        if (position >= len(self.sudokuGrid)):
            return True

        # determine the bock, row, and column for the position.
        block = self.blockCoordinates[position]
        row = floor(position / 9)
        col = position % 9

        # Determine what position after this one needs to be filled.
        nextPosition = position + 1
        while (nextPosition < len(self.sudokuGrid) and (self.blockCoordinates[nextPosition] in [0, 4, 8] or nextPosition == fixedPosition)):
            nextPosition += 1

        number = 1
        valid = False
        # Loop through all possible values until a valid value is found or all values are proven to not be valid in this position
        while (not valid and number < 10):
            if (self.validPosition(row, col, block, number)):
                self.fillPosition(position, row, col, block, number)

                # Check if the next position has a valid value, otherwise check if the next value is valid in this position
                # Recurse until a valid sudoku grid is created
                if (self.fillGrid(nextPosition, fixedPosition)):
                    valid = True
                else:
                    self.fillPosition(position, row, col, block, number, fill=False)

            number += 1
        return valid

    def generate(self):
        """
        Description:
            Generates a sudoku grid.
        Returns:
            Returns a int array representing a sudoku grid.
        """
        # Create a temporary sudoku grid filled with 0s.
        self.sudokuGrid = [0 for i in range(0, 81)]

        # Resets the verifiers to be used for sudoku grid generation.
        self.resetVerifiers()

        # Create the diagonal blocks as a block's values are independent from values in the other blocks.
        self.fillBlock(0)
        self.fillBlock(4)
        self.fillBlock(8)

        # Recursively fill values in other positions.
        self.fillGrid(3)

        # Return a copy of the sudoku grid
        return list(self.sudokuGrid)

    def generateFixed(self, position, value):
        """
        Description:
            Generates a sudoku grid with a fixed value at a position.
        Parameters:
            position (int): The position of the fixed value.
            value (int): The value that is fixed.
        Returns:
            Returns a int array representing a sudoku grid.
        """
        # Create a temporary sudoku grid filled with 0s.
        self.sudokuGrid = [0 for i in range(0, 81)]

        # Checks that the given position and value params are valid.
        if (position < 0 or position >= 81 or value <= 0 or value > 9):
            return list(self.sudokuGrid)

        # Resets the verifiers to be used for sudoku grid generation.
        self.resetVerifiers()

        # Getting the block, row, and column for the position of the fixed value.
        fixedBlock = self.blockCoordinates[position]
        fixedRow = floor(position / 9)
        fixedCol = position % 9

        # Insert the fixed value.
        self.fillPosition(position, fixedRow, fixedCol, fixedBlock, value)

        # Create the diagonal blocks
        # If the fixed value can conflict with a value in block 0, manually insert value into block 0 in a position that does not conflict
        if (fixedBlock != 0 and (fixedRow < 3 or fixedCol < 3)):
            rowTemp = randint(0, 2)
            while (rowTemp == fixedRow):
                rowTemp = randint(0, 2)
            colTemp = randint(0, 2)
            while (colTemp == fixedCol):
                colTemp = randint(0, 2)
            self.fillPosition(rowTemp * 9 + colTemp, rowTemp, colTemp, self.blockCoordinates[rowTemp * 9 + colTemp], value)
        self.fillBlock(0, value=value if fixedBlock == 0 or fixedRow < 3 or fixedCol < 3 else None)

        # If the fixed value can conflict with a value in block 4, manually insert value into block 4 in a position that does not conflict
        if (fixedBlock != 4 and ((fixedRow > 2 and fixedRow < 6) or (fixedCol > 2 and fixedCol < 6))):
            rowTemp = randint(3, 5)
            while (rowTemp == fixedRow):
                rowTemp = randint(3, 5)
            colTemp = randint(3, 5)
            while (colTemp == fixedCol):
                colTemp = randint(3, 5)
            self.fillPosition(rowTemp * 9 + colTemp, rowTemp, colTemp, self.blockCoordinates[rowTemp * 9 + colTemp], value)
        self.fillBlock(4, value=value if fixedBlock == 4 or (fixedRow > 2 and fixedRow < 6) or (fixedCol > 2 and fixedCol < 6) else None)

        # If the fixed value can conflict with a value in block 8, manually insert value into block 8 in position that does not conflict
        if (fixedBlock != 8 and (fixedRow > 5 or fixedCol > 5)):
            rowTemp = randint(6, 8)
            while (rowTemp == fixedRow):
                rowTemp = randint(6, 8)
            colTemp = randint(6, 8)
            while (colTemp == fixedCol):
                colTemp = randint(6, 8)
            self.fillPosition(rowTemp * 9 + colTemp, rowTemp, colTemp, self.blockCoordinates[rowTemp * 9 + colTemp],
                              value)
        self.fillBlock(8, value=value if fixedBlock == 8 or fixedRow > 5 or fixedCol > 5 else None)

        # Recursively fill the other positions.
        if (position == 3):
            self.fillGrid(4)
        else:
            self.fillGrid(3, position)

        # Return a copy of the sudoku grid.
        return list(self.sudokuGrid)

    def getGrid(self):
        """
        Description:
            Gets the current grid of this class.
        Returns:
            An array respenting a sudoku grid.
        """
        return list(self.sudokuGrid)


    @staticmethod
    def validate(sudokuGrid):
        """
        Description:
            Determines that a given grid is a valid sudoku grid.
        Parameters:
            sudokuGrid (int[]): The sudoku grid to be tested.
        Returns:
            True if the given sudoku grid is valid, otherwise false.
        """
        if (len(sudokuGrid) != 81):
            return False

        # Create verifiers for rows, columns, and blocks.
        rowVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]
        colVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]
        blockVerifiers = [VerifierTemplate.getTemplate() for i in range(0, 9)]

        valid = True
        position = 0

        # Creates an array relating a position to the block it belongs in.
        bMap1 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        bMap2 = [3, 3, 3, 4, 4, 4, 5, 5, 5]
        bMap3 = [6, 6, 6, 7, 7, 7, 8, 8, 8]
        blockCoordinates = bMap1 + bMap1 + bMap1 + bMap2 + bMap2 + bMap2 + bMap3 + bMap3 + bMap3

        # Loop though grid until a value is not valid, or the end is reached
        while (valid and position < 81):
            block = blockCoordinates[position]
            row = floor(position / 9)
            col = position % 9
            value = sudokuGrid[position]

            if value > 0 and value < 10 and not (rowVerifiers[row][value] or colVerifiers[col][value] or blockVerifiers[block][value]):
                rowVerifiers[row][value] = True
                colVerifiers[col][value] = True
                blockVerifiers[block][value] = True
                position += 1
            else:
                valid = False
        return valid

    def printVerifiers(self):
        """
        Description:
            Prints out dictionaries telling what values are in certain rows, columns, and blocks. Used primarily for testing purposes.
        """
        print("Row")
        row = 0
        for rowVerifier in self.rowVerifiers:
            print("Row {}: {}".format(row, rowVerifier))
            row += 1
        print()

        print("Col")
        col = 0
        for colVerifier in self.colVerifiers:
            print("Column {}: {}".format(col, colVerifier))
            col += 1
        print()

        print("Block")
        block = 0
        for blockVerifier in self.blockVerifiers:
            print("{}: {}".format(block, blockVerifier))
            block += 1
        print()

    @staticmethod
    def PrintGrid(sudokuGrid):
        """
        Description:
            Prints out a sudoku grid.
        Parameters:
            sudokuGrid (int[]): The sudoku grid to be printed out.
        """
        sudokuString = ''
        position = 1
        for i in sudokuGrid:
            sudokuString += "{:2} ".format(i)
            if (position % 9 == 0):
                sudokuString += "\n"
            position += 1
        print(sudokuString)
#End of Sudoku Class#