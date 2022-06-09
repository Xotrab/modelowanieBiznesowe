import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { FileHandlerService } from '../file-handler.service';

@Component({
    selector: 'app-upload-file-page',
    templateUrl: './upload-file-page.component.html',
    styleUrls: ['./upload-file-page.component.scss'],
})
export class UploadFilePageComponent implements OnInit {
    constructor(private fileHandler: FileHandlerService, private snackbar: MatSnackBar, private router: Router) {}
    public file$: Observable<File>;
    private isCSV: boolean;

    ngOnInit(): void {
        this.fileHandler.clearFile();
        this.file$ = this.fileHandler.file$;
    }

    onSelect(event) {
        const addedFile: File = event.addedFiles[0];
        const split = addedFile.name.split('.');
        if(split.length < 2 || !(split[1].toLowerCase() == 'csv') && !(split[1].toLowerCase() == 'xes')) {
            this.snackbar.open('Invalid file type', 'Ok',{
                duration: 3000
            });
            return;
        }

        if(addedFile.name.split('.')[1] == 'csv') {
            this.isCSV = true;
        }

        this.fileHandler.setFile(event.addedFiles[0]); 
    }

    onRemove() {
        this.fileHandler.clearFile();
    }

    nextStep() {
        if(this.isCSV) {
            this.router.navigate(['csvPreview']);
            return;
        }

        this.router.navigate(['bpmnViewer']);
    }

    previousStep() {
        this.router.navigate([''])
    }
}
