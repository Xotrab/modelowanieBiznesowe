import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { NgxCsvParser } from 'ngx-csv-parser';
import { Subscription } from 'rxjs';
import { FileHandlerService } from '../file-handler.service';

@Component({
  selector: 'app-csv-preview',
  templateUrl: './csv-preview.component.html',
  styleUrls: ['./csv-preview.component.scss']
})
export class CsvPreviewComponent implements OnInit, OnDestroy {
  public parsedCSV: Array<any>;
  public isFirstRowHeader: boolean = true;
  public displayedColumns: Array<string>;
  public joinedColnames: string;

  public isEditingColnames: boolean = false;

  private fileHandlerSubscription: Subscription;

  constructor(
    private fileHandler: FileHandlerService,
    private ngxCsvParser: NgxCsvParser,
    private snackbar: MatSnackBar,
    private router: Router
  ) { }

  public ngOnInit(): void {
    this.parseCSV();
  }

  public parseCSV(): void {
    this.fileHandlerSubscription = this.fileHandler.file$.subscribe(file => {
      this.ngxCsvParser.parse(file, { header: this.isFirstRowHeader, delimiter: ',' })
        .pipe().subscribe((result: Array<any>) => {
          this.parsedCSV = result;
          this.displayedColumns = this.isFirstRowHeader ?
            Object.keys(this.parsedCSV[0]) :
            Array.from({length: this.parsedCSV[0].length}, (_, key) => `${key}`);
            this.joinedColnames = this.displayedColumns.join(',');
        }, _ => {
          this.snackbar.open("Error occured while parsing the csv file", 'Ok',{
            duration: 3000
          });
        });
    });
  }
  
  public ngOnDestroy(): void {
    this.fileHandlerSubscription.unsubscribe();
  }

  public updateColnames(): void {
    const newColnames = this.joinedColnames.split(',');
    const requiredColnames = ['Case ID', 'Activity', 'Start Timestamp'];

    if (newColnames.length !== this.displayedColumns.length) {
      this.snackbar.open(`Please specify ${this.displayedColumns.length} comma separated columns`, 'Ok',{
        duration: 3000
      });

      return;
    }

    if (!requiredColnames.every(required => newColnames.includes(required))) {
      this.snackbar.open('Case ID, Activity and Start Timestamp columns are required to proceed', 'Ok',{
        duration: 3000
      });

      return;
    }

    if (newColnames.includes('')) {
      this.snackbar.open('Column name can not be an empty value', 'Ok',{
        duration: 3000
      });

      return;
    }

    //If the first row was a header, then the parsedCSV includes js objects with colnames as keys, so simply update the keynames
    if (this.isFirstRowHeader) {
      for (var index in this.parsedCSV) {
        var trace = this.parsedCSV[index];
        var updatedTrace = {};

        this.displayedColumns.forEach((OldColname, index) => {
          updatedTrace[newColnames[index]] = trace[OldColname];
        });

        this.parsedCSV[index] = updatedTrace;
      }
    }
    else {
      //If the first row was not a header, then the parsedCSV includes arrays of values, so we need to create object with colnames as keys
      for (var index in this.parsedCSV) {
        var trace = this.parsedCSV[index];
        var traceObj = {};

        trace.forEach((value: string, index: number) => {
          traceObj[newColnames[index]] = value;
        });

        this.parsedCSV[index] = traceObj;
      }
    }

    this.displayedColumns = newColnames;

    this.isFirstRowHeader = true;

    //Create the updated file object and set it in the file handler service
    const csvContent = this.arrayToCSVcontent();
    const blob = new Blob([csvContent], {type: 'text/plain'});

    const updatedFile = new File([blob],"traces.csv", { type: "text/csv",});

    this.fileHandler.setFile(updatedFile);
  }

  public nextStep() {
    const requiredColnames = ['Case ID', 'Activity', 'Start Timestamp'];

    if (!requiredColnames.every(required => this.displayedColumns.includes(required))) {
      this.snackbar.open('Please define Case ID, Activity and Start Timestamp columns to proceed', 'Ok',{
        duration: 3000
      });

      return;
    }

    this.router.navigate(['/bpmnViewer']);
  }

  public previousStep() {
      this.router.navigate(['/uploadFile'])
  }

  private arrayToCSVcontent(): string {
    let csvContent = "";

    csvContent += this.joinedColnames + "\n";

    this.parsedCSV.forEach(trace => {
      const values = Object.values(trace);
      let joinedTrace = values.join(',');
      csvContent += joinedTrace + "\n"; 
    });

    return csvContent;
  }
}
