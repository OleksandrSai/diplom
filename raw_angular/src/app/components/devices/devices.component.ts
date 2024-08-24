import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzPaginationModule } from 'ng-zorro-antd/pagination';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzTableModule } from 'ng-zorro-antd/table';
import { Subscription } from 'rxjs';
import { WebsocketService } from '../../shared/websocket.service';
import { DevicesService } from '../../shared/service/devices.service';

@Component({
  selector: 'app-devices',
  standalone: true,
  imports: [
    NzButtonModule,
    NzTableModule,
    NzIconModule,
    NzPaginationModule,
    NzSelectModule,
    NzInputModule,
    FormsModule],
  templateUrl: './devices.component.html',
  styleUrl: './devices.component.scss'
})
export class DevicesComponent {

  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  totalItems: number | undefined
  selectedFilter:number = 0
  searchText:string=""



  constructor(private websocketService: DevicesService) {}
  messages: string[] = [];

  ngOnInit(): void {
    this.loadData()
    this.websocketService.onMessage().subscribe(message => {
      console.log(message)
      this.messages.push(message);
    });

  }


  get pageSize(): number {
    return Number(this._pageSize);
  }


  onPageIndexChange(newPageIndex: number): void {
    this.pageIndex = newPageIndex
    this.loadData()
  }


  onPageSizeChange(event:Event): void {
    this.loadData()
  }


  loadData(): void {
    // if (this.aSub) this.aSub.unsubscribe();
    // this.aSub = this.serviceGroup.getGroups(this.pageIndex, this.pageSize, this.selectedFilter, this.searchText).subscribe((res: ItemsResponse) =>
    //   {
    //     this.arrData = res.items as GroupInfo[]
    //     this.totalItems = res.totalItems
    //   })
  }


  openDialog(): void {
    // const dialogRef = this.dialog.open(GroupAddComponent);
    // this.cSub = dialogRef.afterClosed().subscribe(result => this.loadData());
  }


  openEditWindow(element:any): void {
  //   const dialogRef = this.dialog.open(GroupEditComponent, {
  //     data: element
  // })
  //   this.cSub = dialogRef.afterClosed().subscribe(result => this.loadData());
  }


  deleteGroup(id:number): void {
    // this.cSub = this.serviceGroup.deleteGroup(id).subscribe((el)=> this.loadData())
  }


  search(value:string): void {
    this.searchText = value
    this.loadData()
  }


  ngOnDestroy(): void {
    this.aSub?.unsubscribe();
    this.cSub?.unsubscribe();
  }

}
