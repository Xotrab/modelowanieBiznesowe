import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';
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

  private downloadUrl: string;

  constructor(
    private fileHandler: FileHandlerService,
    private bpmnService: BpmnService,
    private sanitizer: DomSanitizer,
    private snackbar: MatSnackBar,
    private router: Router
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
      this.downloadUrl = URL.createObjectURL(blobObj);
      this.imageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.downloadUrl);
    });
  }

  public navigateHome(): void {
    this.router.navigate(['/']);
  }

  public downloadModel(): void {
    var a = document.createElement("a");
    a.href = this.downloadUrl;
    a.download = "model";
    a.click();
  }

  private validateThresholdInput(threshold: string): boolean {
    const number = Number(threshold);

    return  threshold && Number.isInteger(number) && number >= 0
  }

}
