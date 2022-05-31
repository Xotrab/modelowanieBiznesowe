import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BpmnViewerComponent } from './bpmn-viewer/bpmn-viewer.component';
import { CsvPreviewComponent } from './csv-preview/csv-preview.component';
import { StartingPageComponent } from './starting-page/starting-page.component';
import { UploadFilePageComponent } from './upload-file-page/upload-file-page.component';

const routes: Routes = [
  {
    path: '',
    component: StartingPageComponent
  },
  {
    path: 'uploadFile',
    component: UploadFilePageComponent
  },
  {
    path: 'csvPreview',
    component: CsvPreviewComponent
  },
  {
    path: 'bpmnViewer',
    component: BpmnViewerComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
