import { Injectable, NgZone } from '@angular/core';
import { Observable, Subject } from 'rxjs';

interface EventMessage {
  event: number;
  status: string;
  confidence: number;
  action: string;
  alert: number | null;
}

@Injectable({ providedIn: 'root' })
export class WebsocketService {
  private ws?: WebSocket;
  private subject = new Subject<EventMessage>();

  constructor(private zone: NgZone) {}

  connect(url: string): Observable<EventMessage> {
    if (this.ws) {
      this.ws.close();
    }
    this.ws = new WebSocket(url);
    this.ws.onmessage = event => {
      const data = JSON.parse(event.data);
      this.zone.run(() => this.subject.next(data));
    };
    return this.subject.asObservable();
  }
}
