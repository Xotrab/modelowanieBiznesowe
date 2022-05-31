import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StartingPageComponent } from './starting-page/starting-page.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { UploadFilePageComponent } from './upload-file-page/upload-file-page.component';
import { NavbarComponent } from './navbar/navbar.component';
import { NgxDropzoneModule } from 'ngx-dropzone';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { CsvPreviewComponent } from './csv-preview/csv-preview.component';
import { BpmnViewerComponent } from './bpmn-viewer/bpmn-viewer.component';

@NgModule({
    declarations: [AppComponent, StartingPageComponent, UploadFilePageComponent, NavbarComponent, CsvPreviewComponent, BpmnViewerComponent],
    imports: [
        BrowserModule,
        AppRoutingModule,
        NoopAnimationsModule,
        MatButtonModule,
        NgxDropzoneModule,
        MatSnackBarModule
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
