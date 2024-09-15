import { Routes } from '@angular/router';
import { DevicesComponent } from './components/devices/devices.component';
import { PageComponent } from './components/page/page.component';
import { GroupComponent } from './components/group/group.component';
import { SchedulerComponent } from './components/scheduler/scheduler.component';
import { DeviceComponent } from './components/device-statistic/device.component';

export const routes: Routes = [
  { path: '', component: DevicesComponent },
  { path: 'group', component: GroupComponent },
  { path: 'scheduler', component: SchedulerComponent },
  { path: 'device/:id', component: DeviceComponent },
];
