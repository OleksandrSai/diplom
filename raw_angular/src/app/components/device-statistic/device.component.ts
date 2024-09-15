import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { NzTableModule } from 'ng-zorro-antd/table';
import { NzPaginationModule } from 'ng-zorro-antd/pagination';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { CommonModule } from '@angular/common';
import { NzInputModule } from 'ng-zorro-antd/input';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-device',
  standalone: true,
  imports: [
    NzTableModule,
    NzIconModule,
    NzPaginationModule,
    NzSelectModule,
    CommonModule,
    NzInputModule,
    FormsModule],
  templateUrl: './device.component.html',
  styleUrl: './device.component.scss'
})
export class DeviceComponent {

  constructor(private route: ActivatedRoute){}


  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  totalItems: number | undefined

  searchText:string=""


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
    // this.aSub = this.serviceGroup.getAllGroup(this.pageIndex, this.pageSize, this.searchText).subscribe((res: any) =>
    //   {
    //     this.arrData = res.items as any[]
    //     this.totalItems = res.totalItems
    //   })
  }


  openDialog(): void {

  }


  openEditWindow(element:any): void {

  }


  deleteGroup(id:number): void {

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
