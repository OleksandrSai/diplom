import { Component } from '@angular/core';
import { MenuComponent } from '../menu/menu.component';
import { DevicesComponent } from '../devices/devices.component';

import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-page',
  standalone: true,
  imports: [DevicesComponent, MenuComponent, RouterModule],
  templateUrl: './page.component.html',
  styleUrl: './page.component.scss'
})
export class PageComponent {

}
