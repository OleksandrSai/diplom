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
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from "chart.js";

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
    NzButtonModule,
    BaseChartDirective],
  templateUrl: './device.component.html',
  styleUrl: './device.component.scss'
})
export class DeviceComponent {

  constructor(private route: ActivatedRoute, private statisticService:StatisticService){}


  aSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  pageId: number | undefined;
  totalItems: number | undefined

  searchText:string=""


  ngOnInit(): void {
    this.getPageId()
    this.loadData()
  }

  getPageId(){
    this.route.paramMap.subscribe(params => this.pageId = Number(params.get('id')))
  }

  get pageSize(): number {
    return Number(this._pageSize);
  }


  onPageIndexChange(newPageIndex: number): void {
    console.log(newPageIndex)
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
        console.log(res)
        this.arrData = res.items as any[]
        this.totalItems = res.totalItems
      })
  }



  ngOnDestroy(): void {
    this.aSub?.unsubscribe();
    this.cSub?.unsubscribe();
  }





  title = 'ng2-charts-demo';

  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July'
    ],
    datasets: [
      {
        data: [ 65, 59, 80, 81, 56, 55, 40 ],
        label: 'average consumption KW/h',
        fill: true,
        tension: 0.5,
        borderColor: 'black',
        backgroundColor: 'rgba(255,0,0,0.3)'
      }
    ]
  };
  public lineChartOptions: ChartOptions<'line'> = {
    responsive: false
  };
  public lineChartLegend = true;













}
