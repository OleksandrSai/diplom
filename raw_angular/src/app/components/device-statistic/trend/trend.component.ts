import { Component, Inject, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { NzRadioModule } from 'ng-zorro-antd/radio';
import { FormsModule } from '@angular/forms';
import { StatisticService } from '../../../shared/service/statistic.service';
import { Subscription } from 'rxjs';

const MAPPED_DAY: { [key: string]: string } = {
  "Day": `${new Date().toISOString()},${new Date().toISOString()}`,
  "Week": `${new Date(new Date().setDate(new Date().getDate() - 7)).toISOString()},${new Date().toISOString()}`,
  "Month": `${new Date(new Date().setDate(new Date().getDate() - 30)).toISOString()},${new Date().toISOString()}`
};

@Component({
  selector: 'app-trend',
  standalone: true,
  imports: [
    BaseChartDirective,
    NzRadioModule,
    FormsModule
  ],
  templateUrl: './trend.component.html',
  styleUrl: './trend.component.scss'
})
export class TrendComponent implements OnInit, OnDestroy{

  @ViewChild(BaseChartDirective) chart: BaseChartDirective | undefined;

  constructor( private statisticService:StatisticService, public dialogRef: MatDialogRef<TrendComponent>, @Inject(MAT_DIALOG_DATA) public data: any ) {}
  aSub: Subscription | undefined;
  radioValue: string = "Day";
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


  ngOnInit(): void{
    this.loadData()
  }

  rerenderChart():void {
    if (this.chart && this.chart.chart) {
      this.chart.chart.update();
    }
  }

  loadData(): void {
    if(this.aSub) this.aSub.unsubscribe()
    const day = MAPPED_DAY[this.radioValue]
    console.log(day)
    this.statisticService.getDataTrend(this.data, MAPPED_DAY[this.radioValue]).subscribe((res:any)=>{
      this.lineChartData.labels = Object.keys(res);
      this.lineChartData.datasets[0].data = Object.values(res);

      this.rerenderChart()
    })
  }

  onRadioChange(value: string): void {
    setTimeout(() => {
      this.loadData()
    }, 10);

  }

  closeDialog(): void {
    this.dialogRef.close()
  }


  ngOnDestroy(): void{
    this.aSub?.unsubscribe()
  }


}
