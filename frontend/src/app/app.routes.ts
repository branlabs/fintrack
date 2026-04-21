import { Routes } from '@angular/router';

import { AppShellComponent } from './layout/app-shell/app-shell.component';
import { DashboardPageComponent } from './features/dashboard/dashboard.page';

export const routes: Routes = [
  {
    path: '',
    component: AppShellComponent,
    children: [
      {
        path: '',
        component: DashboardPageComponent,
      },
    ],
  },
];
