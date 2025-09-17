import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, timer } from 'rxjs';

import { ApiService } from '../../core/services/api.service';
import { WebsocketService } from '../../core/services/websocket.service';

interface EventRow {
  id: number;
  timestamp: string;
  status: string;
  confidence: number;
  user: string | null;
  device: string | null;
  snapshot_path: string | null;
}

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrls: ['./dashboard-page.component.scss']
})
export class DashboardPageComponent implements OnInit, OnDestroy {
  events: EventRow[] = [];
  statusMessage = '';
  private wsSubscription?: Subscription;
  private pollSubscription?: Subscription;

  constructor(private api: ApiService, private websocket: WebsocketService) {}

  ngOnInit(): void {
    this.loadEvents();
    this.wsSubscription = this.websocket.connect('ws://localhost:8000/ws/events').subscribe(message => {
      this.statusMessage = `Evento ${message.event} - ${message.status}`;
      this.loadEvents();
    });
    this.pollSubscription = timer(0, 30000).subscribe(() => this.loadEvents());
  }

  ngOnDestroy(): void {
    this.wsSubscription?.unsubscribe();
    this.pollSubscription?.unsubscribe();
  }

  private loadEvents(): void {
    this.api.get<EventRow[]>('/events/recent').subscribe(events => {
      this.events = events;
    });
  }
}
