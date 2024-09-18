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
import { StatisticService } from '../../shared/service/statistic.service';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { MatDialog } from '@angular/material/dialog';
import { TrendComponent } from './trend/trend.component';

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
    FormsModule,
    NzButtonModule],
  templateUrl: './device.component.html',
  styleUrl: './device.component.scss'
})
export class DeviceComponent {

  constructor(private route: ActivatedRoute, private statisticService:StatisticService, public dialog: MatDialog){}


  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  dSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  pageId: number | undefined;
  totalItems: number | undefined

  searchText:string= ""


  ngOnInit(): void {
    this.getPageId()
    this.loadData()
  }


  openTrend(){
    if (this.dSub) this.dSub.unsubscribe;
    const dialogRef = this.dialog.open(TrendComponent, {
      data: this.pageId
    });
    this.dSub = dialogRef.afterClosed().subscribe((result:any) => this.loadData());
  }


  getPageId(){
    this.route.paramMap.subscribe(params => this.pageId = Number(params.get('id')))
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
    console.log(this.pageId)
    this.aSub = this.statisticService.getDeviceStatistic(this.pageId as number, this.pageIndex, this.pageSize, this.searchText).subscribe((res: any) =>
      {
        this.arrData = res.items as any[]
        this.totalItems = res.totalItems
      })
  }



  ngOnDestroy(): void {
    this.aSub?.unsubscribe();
    this.cSub?.unsubscribe();
  }














}
