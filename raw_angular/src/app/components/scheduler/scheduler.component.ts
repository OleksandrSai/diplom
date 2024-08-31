import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzPaginationModule } from 'ng-zorro-antd/pagination';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzTableModule } from 'ng-zorro-antd/table';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-scheduler',
  standalone: true,
  imports: [
    CommonModule,
    NzButtonModule,
    NzTableModule,
    NzIconModule,
    NzPaginationModule,
    NzSelectModule,
    NzInputModule,
    FormsModule
  ],
  templateUrl: './scheduler.component.html',
  styleUrl: './scheduler.component.scss'
})
export class SchedulerComponent {
  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  totalItems: number | undefined
  selectedFilter:number = 0
  searchText:string=""

  constructor() {}
  messages: string[] = [];

  ngOnInit(): void {
    this.loadData()


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
    if (this.aSub) this.aSub.unsubscribe();
    // this.aSub = this.diveceService.getAllDevices(this.pageIndex, this.pageSize, this.searchText).subscribe((res: any) =>

    //   {
    //     res.items.forEach((element:any) => {
    //       element.instantCurrent = 0;
    //       element.instantVoltage = 0;
    //       element.totalConsumption = 0;
    //     });
    //     this.arrData = res.items
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
