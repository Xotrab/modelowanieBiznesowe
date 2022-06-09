import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { BpmnService } from '../bpmn.service';
import { FileHandlerService } from '../file-handler.service';

@Component({
  selector: 'app-bpmn-viewer',
  templateUrl: './bpmn-viewer.component.html',
  styleUrls: ['./bpmn-viewer.component.scss']
})
export class BpmnViewerComponent implements OnInit {
  public imageUrl: SafeResourceUrl;

  public eventThreshold: string = '0';

  private traces: File;

  constructor(
    private fileHandler: FileHandlerService,
    private bpmnService: BpmnService,
    private sanitizer: DomSanitizer,
    private snackbar: MatSnackBar
  ) { }

  public ngOnInit(): void {
    this.fileHandler.file$.subscribe(file => {
      this.traces = file;
      this.getBPMN();
    });
  }

  public getBPMN(): void {
    if (!this.validateThresholdInput(this.eventThreshold)) {
      this.snackbar.open("The event threshold is not a non-negative integer value!", 'Ok',{
        duration: 3000
      });

      return;
    }

    this.bpmnService.getBPMN(this.traces, this.eventThreshold).subscribe(result => {
      var blobObj = new Blob([result.body], { type: "image/png" });
      let objectURL = URL.createObjectURL(blobObj);
      this.imageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectURL);
    });
  }

  private validateThresholdInput(threshold: string): boolean {
    const number = Number(threshold);

    return  threshold && Number.isInteger(number) && number >= 0
  }

}
