from flask import Flask, jsonify, request
from flask_cors import cross_origin
from sudoku import Sudoku

# Domains that the application will accept requests from.
localFrontendURL = "http://localhost:4200"
containerFrontendURL = "http://frontend:4200"

app = Flask(__name__)

# A simple index.
@app.route('/')
@cross_origin([localFrontendURL, containerFrontendURL])
def index():
    return "This is the backend for a Sudoku application"

# RESTful API endpoint for getting a sudoku grid.
@app.route('/sudoku/board', methods=['GET'])
@cross_origin([localFrontendURL, containerFrontendURL])
def getBoard():
    sudoku = Sudoku()
    return jsonify(data=sudoku.generate(), success="true")

# Restful API endpoint for getting a sudoku grid with a fixed position.
@app.route('/sudoku/fixedBoard', methods=['GET'])
@cross_origin([localFrontendURL, containerFrontendURL])
def getFixedBoard():
    sudoku = Sudoku()

    # Get parameter values.
    position = request.args.get('position',default=-1, type=int)
    value = request.args.get('value', default=-1, type=int)

    gridData = sudoku.generateFixed(position, value)
    successString = "true" if gridData[0] != 0 else "false"
    return jsonify(data=gridData, success=successString)

# Handler in the case of error 404.
@app.errorhandler(404)
@cross_origin([localFrontendURL, containerFrontendURL])
def pageNotFound(e):
    # note that we set the 404 status explicitly
    return jsonify(data=[0 for i in range(0, 81)], success="false"), 404

# If the application is being run as the source file, accept connection from outside the network.
if (__name__ == '__main__'):
    app.run(debug=False, host="0.0.0.0", port=5000)