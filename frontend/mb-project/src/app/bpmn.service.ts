import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BpmnService {
  private readonly bpmnUrl = 'http://127.0.0.1:5000/bpmn';

  constructor(private http: HttpClient) { }

  public getBPMN(traces: File, eventThreshold: string): Observable<any> {
    const formData = new FormData();
    formData.append("traces", traces);

    let headers = new HttpHeaders();
    headers = headers.append('Threshold', eventThreshold);

    return this.http.post(this.bpmnUrl, formData, {headers: headers, responseType: 'blob', observe: 'response'});
  }
}
