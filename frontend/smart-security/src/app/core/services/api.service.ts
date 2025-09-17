import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://localhost:8000';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  get<T>(path: string, options: { headers?: HttpHeaders } = {}): Observable<T> {
    return this.http.get<T>(`${API_URL}${path}`, options);
  }

  post<T>(path: string, body: any, options: { headers?: HttpHeaders } = {}): Observable<T> {
    return this.http.post<T>(`${API_URL}${path}`, body, options);
  }

  upload<T>(path: string, formData: FormData, options: { headers?: HttpHeaders } = {}): Observable<T> {
    return this.http.post<T>(`${API_URL}${path}`, formData, options);
  }
}
