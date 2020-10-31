import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

/*
  Description:
    Class to handle grid component.
  Variables:
    counter (number): An array used to help create sudoku grid.
  Variables (Inputs):
    colorId (number): The current color-choice-n class being used.
    focus (number): The current value being frozen/fixed. -1 indicates no values being fixed;
    sudokuGrid (number[]): Values for the sudoku grid.
  Variables (Output):
    focusEmitter (EventEmitter<number>): Emits to parent component that the fixed value has changed, and what value it is.
  Methods:
    onClick(number)
*/
@Component({
  selector: 'app-grid',
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.css']
})
export class GridComponent implements OnInit {
  counter: number[] = [0, 1, 2, 3, 4, 5, 6, 7, 8];

  @Input() colorId: number;
  @Input() sudokuGrid: number[];
  @Input() focus: number;

  @Output() focusEmitter: EventEmitter<number> = new EventEmitter<number>();

  constructor() { }

  ngOnInit() { }

  /*
    Description:
      When a value in the grid is clicked, send the parent componet the new position being fixed.
  */
  onClick(position: number): void {
    // If the position that is already fixed is clicked, unfocus it. Otherwise set the new fixed position.
    if (position == this.focus) {
      this.focusEmitter.emit(-1);
    } else {
      this.focusEmitter.emit(position);
    }
  }

}
