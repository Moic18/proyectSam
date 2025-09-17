import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './shared/components/header/header.component';
import { DashboardPageComponent } from './features/dashboard/dashboard-page.component';
import { FacesPageComponent } from './features/faces/faces-page.component';
import { AlertsPageComponent } from './features/alerts/alerts-page.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    DashboardPageComponent,
    FacesPageComponent,
    AlertsPageComponent
  ],
  imports: [BrowserModule, HttpClientModule, ReactiveFormsModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}