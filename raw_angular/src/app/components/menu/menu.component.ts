import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss'
})
export class MenuComponent {
  flag:boolean = true;


  changeSise(){
    let ogj = {
      size: this.flag
    }
    return ogj
  }

  shiftButton(){
    let ogj = {
      shift: this.flag
    }
    return ogj
  }

  changeState(){
    this.flag = !this.flag
  }

}
