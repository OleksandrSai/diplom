import { Component } from '@angular/core';
import { MenuComponent } from '../menu/menu.component';
import { MainPageComponent } from '../main-page/main-page.component';

@Component({
  selector: 'app-page',
  standalone: true,
  imports: [MenuComponent, MenuComponent, MainPageComponent],
  templateUrl: './page.component.html',
  styleUrl: './page.component.scss'
})
export class PageComponent {

}
