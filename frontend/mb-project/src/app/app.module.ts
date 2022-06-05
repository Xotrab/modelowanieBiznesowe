import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {MatTableModule} from '@angular/material/table';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StartingPageComponent } from './starting-page/starting-page.component';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { UploadFilePageComponent } from './upload-file-page/upload-file-page.component';
import { NavbarComponent } from './navbar/navbar.component';
import { NgxDropzoneModule } from 'ngx-dropzone';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { CsvPreviewComponent } from './csv-preview/csv-preview.component';
import { BpmnViewerComponent } from './bpmn-viewer/bpmn-viewer.component';
import { NgxCsvParserModule } from 'ngx-csv-parser';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';

@NgModule({
    declarations: [AppComponent, StartingPageComponent, UploadFilePageComponent, NavbarComponent, CsvPreviewComponent, BpmnViewerComponent],
    imports: [
        BrowserModule,
        AppRoutingModule,
        NoopAnimationsModule,
        MatButtonModule,
        NgxDropzoneModule,
        MatSnackBarModule,
        NgxCsvParserModule,
        BrowserAnimationsModule,
        MatTableModule,
        MatCheckboxModule,
        FormsModule,
        MatInputModule
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
