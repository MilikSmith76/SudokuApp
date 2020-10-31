Suduko Application Guide

REQUIREMENTS:
  - Docker
  - Docker Compose

HOW THE APPLICATION WORKS:
  - The front end will display buttons with values that create a sudoku board.
  - Click one of the buttons on the sudoku board to have the value frozen.
    A frozen value will not update on board refresh unless an error occurs
    while getting a new board. If a value is frozen during an error (grid of
    all 0) the value will be ignored.
  - Click the refresh button to generate a new sudoku board.
  - Click the title ("Sudoku App") to change the color scheme between 1 of the 5
    color schemes.

CREATING THE DOCKER CONTAINERS AND RUN THEM:
  - Unzip the given file
  - In the command prompt / terminal change the working directory to where the
    file was unzipped
  - In this directory run "docker-compose up" ("docker-compose up -d" can also
    be used).
  - Both the "frontend" and "backend" containers should be created and running
  - The containers applications can be reached at the docker machines IP address
    on ports 5000 (backend) and 4200 (frontend)

  RUN BACKEND UNIT TEST:
  - In the backend container run "python -m unittest backendTest.py" in the
    "/src/backend" directory to run the unit tests
  - Additional "docker exec backend python -m unittest backendTest.py" can used
    to run the unit test
