import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, timeout } from 'rxjs/operators';

import { BackendResponse } from './backend-response'

/*
  Desription:
    A service used to make API calls to the backend.
  Variables:
    backendURL (string): Endpoint for the backend.
  Method:
    getGrid()
    getGridFixed(number, number)
    errorHandler()
*/
@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  backendURL: string = "http://" + window.location.hostname + ":5000";

  constructor(private http: HttpClient) { }

  /*
    Description:
      Makes a call to backend and gets a sudoku grid.
    Returns:
      An array containing values for a sudoku grid.
  */
  getGrid(): Observable<BackendResponse> {
    return this.http.get<BackendResponse>(this.backendURL + "/sudoku/board")
      .pipe(
        // Stoping attempting to get response after 3 seconds.
        timeout(3000),

        // Handle error, and resume
        catchError(this.errorHandler())
      );
  }

  /*
    Description:
      Makes a call to backend and gets a sudoku grid with a fixed value at a position.
    Parameters:
      position (number): The position in the grid that is fixed.
      value (number): The value the fixed position should have.
    Returns:
      An array containing values for a sudoku grid with a fixed value in a certain position.
  */
  getGridFixed(position:number, value: number): Observable<BackendResponse> {
    const params: HttpParams = new HttpParams()
      .set("position", String(position))
      .set("value", String(value));
    return this.http.get<BackendResponse>(this.backendURL + "/sudoku/fixedBoard", { params })
    .pipe(
      timeout(3000),
      catchError(this.errorHandler())
    );
  }

  /*
    Description:
      Handles errors during API calls.
    Returns:
      A sudoku grid with all 0s.
   */
  private errorHandler() {
    return (error: any) => {
      return of({
        data: new Array<number>(81).fill(0),
        success: 'false',
      });
    }
  }
}
