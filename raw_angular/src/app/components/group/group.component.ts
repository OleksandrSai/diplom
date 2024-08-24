import { Component } from '@angular/core';
import { GroupService } from '../../shared/service/group.service';
import { Subscription } from 'rxjs';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzTableModule } from 'ng-zorro-antd/table';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzPaginationModule } from 'ng-zorro-antd/pagination';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzInputModule } from 'ng-zorro-antd/input';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-group',
  standalone: true,
  imports: [ NzButtonModule,
    NzTableModule,
    NzIconModule,
    NzPaginationModule,
    NzSelectModule,
    NzInputModule,
    FormsModule],
  templateUrl: './group.component.html',
  styleUrl: './group.component.scss'
})
export class GroupComponent {

  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  totalItems: number | undefined

  searchText:string=""

  constructor(private serviceGroup:GroupService){}

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
    this.aSub = this.serviceGroup.getAllGroup(this.pageIndex, this.pageSize, this.searchText).subscribe((res: any) =>
      {
        this.arrData = res.items as any[]
        this.totalItems = res.totalItems
      })
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
