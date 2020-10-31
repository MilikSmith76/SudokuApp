import { Component } from '@angular/core';

import { BackendApiService } from './backend-api.service';
import { BackendResponse } from './backend-response'

/*
  Description:
    Class for the handling the main App Component
  Variables:
    colors (number): The number of colors options available. Note: New color css classes need to be added to work with higher values.
    colorId (number): The current color-choice-n class being used.
    focus (number): The current value being frozen/fixed. -1 indicates no values being fixed;
    loading (boolean): Flag that determines if the app is loading a new grid.
    sudokuGrid (number[]): Values for the sudoku grid.
    success (boolean): Flag that indicates whether getting a sudoku grid was successful or not.
  Methods:
    colorChange()
    gridClick()
    refresh()
*/
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  colors: number = 5;
  colorId: number;
  focus: number = -1;
  loading: boolean = true;
  sudokuGrid: number[];
  success: boolean = true;

  constructor(private backendApiService: BackendApiService) { }

  ngOnInit() {
    // Get the current color choosen during this session.
    let possibleColorId: number = Number(sessionStorage.getItem("frontend_color_choice"));

    // In the case of an invalid color choice, set the color to the default. If valid, use the color.
    if (isNaN(possibleColorId) || possibleColorId < 0 || possibleColorId >= this.colors) {
      this.colorId = 0;
      sessionStorage.setItem("frontend_color_choice", "0");
    } else {
      this.colorId = possibleColorId;
    }

    // Get the sudoku grid and success flag. Additionally stops the app from showing the laoding spinner.
    this.backendApiService.getGrid().subscribe(res => {
      this.sudokuGrid = res.data;
      this.success = (res.success == 'true');
      this.loading = false;
    });
  }

  /*
    Description:
      Changes the color choice when the title is clicked.
  */
  colorChange(): void {
    this.colorId += 1;

    // If the color choice is higher then the available colors, the first color is used.
    if (this.colorId >= this.colors) {
      this.colorId = 0;
    }

    // Stores the color choice in a session cookie.
    sessionStorage.setItem("frontend_color_choice", String(this.colorId));
  }

  /*
    Description:
      Fixes the position of the clicked value in the grid.
  */
  gridClick(position: number): void {
    this.focus = position;
  }

  /*
    Description:
      Refreshes the sudoku grid.
  */
  refresh(): void {
    this.loading = true;

    // Makes a call to the backend for a sudoku grid.
    // If no position is fixed, or if the grid is from an error get a regular grid. Otherwise get a grid with the fixed position value.
    if (this.focus == -1 || this.sudokuGrid[0] == 0) {
      this.backendApiService.getGrid().subscribe(res => {
        this.sudokuGrid = res.data;
        this.success = (res.success == 'true');
        this.loading = false;
      });
    } else {
      this.backendApiService.getGridFixed(this.focus, this.sudokuGrid[this.focus]).subscribe(res => {
        this.sudokuGrid = res.data;
        this.success = (res.success == 'true');
        this.loading = false;
      });
    }
  }
}
