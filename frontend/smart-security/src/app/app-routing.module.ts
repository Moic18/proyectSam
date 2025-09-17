import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardPageComponent } from './features/dashboard/dashboard-page.component';
import { FacesPageComponent } from './features/faces/faces-page.component';
import { AlertsPageComponent } from './features/alerts/alerts-page.component';

const routes: Routes = [
  { path: '', component: DashboardPageComponent },
  { path: 'faces', component: FacesPageComponent },
  { path: 'alerts', component: AlertsPageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}