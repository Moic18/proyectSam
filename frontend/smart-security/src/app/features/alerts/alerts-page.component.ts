import { Component, OnInit } from '@angular/core';

import { ApiService } from '../../core/services/api.service';

interface AlertRow {
  id: number;
  message: string;
  created_at: string;
  resolved: boolean;
  event: {
    id: number;
    status: string;
    device: { name: string } | null;
    user: { name: string } | null;
  };
}

@Component({
  selector: 'app-alerts-page',
  templateUrl: './alerts-page.component.html',
  styleUrls: ['./alerts-page.component.scss']
})
export class AlertsPageComponent implements OnInit {
  alerts: AlertRow[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadAlerts();
  }

  private loadAlerts(): void {
    this.api.get<AlertRow[]>('/notifications/').subscribe(alerts => (this.alerts = alerts));
  }
}
