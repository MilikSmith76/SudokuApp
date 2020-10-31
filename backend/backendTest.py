import unittest
from flask import json
from sudoku import Sudoku
from app import app


class BackendTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testValidGrid(self):
        self.assertTrue(Sudoku.validate([7, 9, 6, 2, 1, 3, 5, 8, 4, 3, 1, 2, 4, 5, 8, 6, 9, 7, 4, 8, 5, 7, 6, 9, 2, 3, 1, 2, 3, 9, 1, 7, 6, 8, 4, 5, 8, 5, 1, 3, 2, 4, 7, 6, 9, 6, 7, 4, 8, 9, 5, 3, 1, 2, 5, 4, 8, 9, 3, 2, 1, 7, 6, 1, 2, 3, 6, 4, 7, 9, 5, 8, 9, 6, 7, 5, 8, 1, 4, 2, 3]))
        self.assertTrue(Sudoku.validate([3, 2, 5, 4, 1, 6, 7, 9, 8, 7, 8, 4, 2, 9, 3, 1, 6, 5, 9, 6, 1, 7, 8, 5, 4, 2, 3, 1, 7, 9, 5, 3, 8, 6, 4, 2, 2, 3, 8, 6, 4, 9, 5, 1, 7, 4, 5, 6, 1, 7, 2, 8, 3, 9, 6, 9, 2, 8, 5, 1, 3, 7, 4, 8, 4, 3, 9, 6, 7, 2, 5, 1, 5, 1, 7, 3, 2, 4, 9, 8, 6]))

    def testInvalidGrid(self):
        # Invalid value (10)
        self.assertFalse(Sudoku.validate(
            [7, 9, 6, 2, 1, 3, 5, 8, 4, 3, 1, 2, 4, 5, 8, 6, 9, 7, 4, 8, 5, 7, 6, 9, 2, 3, 1, 2, 3, 9, 1, 7, 6, 8, 4, 5,
             8, 5, 1, 3, 2, 4, 7, 6, 9, 6, 10, 4, 8, 9, 5, 3, 1, 2, 5, 4, 8, 9, 3, 2, 1, 7, 6, 1, 2, 3, 6, 4, 7, 9, 5, 8,
             9, 6, 7, 5, 8, 1, 4, 2, 3]))

        # Repeated 9 in row 0, block 1, and column 3
        self.assertFalse(Sudoku.validate(
            [7, 9, 6, 9, 1, 3, 5, 8, 4, 3, 1, 2, 4, 5, 8, 6, 9, 7, 4, 8, 5, 7, 6, 9, 2, 3, 1, 2, 3, 9, 1, 7, 6, 8, 4, 5,
             8, 5, 1, 3, 2, 4, 7, 6, 9, 6, 7, 4, 8, 9, 5, 3, 1, 2, 5, 4, 8, 9, 3, 2, 1, 7, 6, 1, 2, 3, 6, 4, 7, 9, 5, 8,
             9, 6, 7, 5, 8, 1, 4, 2, 3]))

    def testSudokuGenerate(self):
        sudoku = Sudoku()
        grid = sudoku.generate()
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB0(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(10, 1)
        self.assertEqual(grid[10], 1)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB1(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(4, 2)
        self.assertEqual(grid[4], 2)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB2(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(26, 3)
        self.assertEqual(grid[26], 3)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB3(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(28, 4)
        self.assertEqual(grid[28], 4)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB4(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(40, 5)
        self.assertEqual(grid[40], 5)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB5(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(35, 6)
        self.assertEqual(grid[35], 6)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB6(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(54, 7)
        self.assertEqual(grid[54], 7)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB7(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(66, 8)
        self.assertEqual(grid[66], 8)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuGenerateFixedB8(self):
        sudoku = Sudoku()
        grid = sudoku.generateFixed(80, 9)
        self.assertEqual(grid[80], 9)
        self.assertTrue(Sudoku.validate(grid))

    def testSudokuBoardAPI(self):
        response = self.app.get('/sudoku/board')
        data = json.loads(response.data)
        self.assertEqual(data["success"], "true")
        self.assertNotEqual(data["data"][0], 0)

    def testSudokuFixedBoardAPI(self):
        response = self.app.get('/sudoku/fixedBoard', query_string=dict(position=80, value=9))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "true")
        self.assertNotEqual(data["data"][0], 0)
        self.assertEqual(data["data"][80], 9)

    def testSudokuFixedBoardAPI(self):
        response = self.app.get('/sudoku/fixedBoard', query_string=dict(position=80, value=9))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "true")
        self.assertNotEqual(data["data"][0], 0)
        self.assertEqual(data["data"][80], 9)

    def testSudokuFixedBoardInvalid(self):
        # Invalid positions
        response = self.app.get('/sudoku/fixedBoard', query_string=dict(position=-1, value=9))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "false")

        response = self.app.get('/sudoku/fixedBoard', query_string=dict(position=82, value=3))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "false")

        # Invalid values
        response = self.app.get('/sudoku/fixedBoard', query_string=dict(position=20, value=0))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "false")

        esponse = self.app.get('/sudoku/fixedBoard', query_string=dict(position=30, value=10))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "false")

        # Non numeric parameters
        esponse = self.app.get('/sudoku/fixedBoard', query_string=dict(position="hello", value="world"))
        data = json.loads(response.data)
        self.assertEqual(data["success"], "false")

if __name__ == '__main__':
    unittest.main()