/*
  Description:
    Interface used to work with responses from the backend.
  Variables:
    data (number): The array of values for the sudoku grid.
    success (string): A string value representing a boolean value.
*/
export interface BackendResponse {
  data: number[];
  success: string;
}
