import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

import { ApiService } from './api.service';

interface TokenResponse {
  access_token: string;
  token_type: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'smart-security-token';
  private loggedIn$ = new BehaviorSubject<boolean>(false);

  constructor(private api: ApiService) {
    const token = this.token;
    this.loggedIn$.next(!!token);
  }

  get token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  login(email: string, password: string): Observable<TokenResponse> {
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);

    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
    return this.api.post<TokenResponse>('/auth/token', body.toString(), { headers }).pipe(
      tap(response => {
        localStorage.setItem(this.tokenKey, response.access_token);
        this.loggedIn$.next(true);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.loggedIn$.next(false);
  }

  isLoggedIn(): Observable<boolean> {
    return this.loggedIn$.asObservable();
  }
}
