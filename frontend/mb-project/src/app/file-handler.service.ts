import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileHandlerService {

  private fileSubject = new BehaviorSubject<File>(undefined);
  public get file$(): Observable<File> {
    return this.fileSubject.asObservable();
  }
  constructor() { }
  
  public setFile(file: File) {
    this.fileSubject.next(file);
  }
  
  public clearFile() {
    this.fileSubject.next(undefined);
  }
}
