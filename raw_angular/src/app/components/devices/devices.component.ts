import { Component, TemplateRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzPaginationModule } from 'ng-zorro-antd/pagination';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzTableModule } from 'ng-zorro-antd/table';
import { Subscription } from 'rxjs';
import { DevicesService } from '../../shared/service/devices.service';
import { CommonModule } from '@angular/common';
import { NzSwitchModule } from 'ng-zorro-antd/switch';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzStatisticModule } from 'ng-zorro-antd/statistic';
import { NzModalModule } from 'ng-zorro-antd/modal';
import { MatDialog } from '@angular/material/dialog';
import { ChangeDeviceComponent } from './change-device/change-device.component';

@Component({
  selector: 'app-devices',
  standalone: true,
  imports: [
    CommonModule,
    NzButtonModule,
    NzTableModule,
    NzIconModule,
    NzPaginationModule,
    NzSelectModule,
    NzInputModule,
    FormsModule,
    NzSwitchModule,
    NzCardModule,
    NzStatisticModule,
    NzModalModule],
  templateUrl: './devices.component.html',
  styleUrl: './devices.component.scss'
})
export class DevicesComponent {

  @ViewChild('prefixTplOne', { static: true }) prefixTplOne: TemplateRef<any> | undefined;
  @ViewChild('prefixTplTwo', { static: true }) prefixTplTwo: TemplateRef<any> | undefined;

  aSub: Subscription | undefined;
  bSub: Subscription | undefined;
  cSub: Subscription | undefined;
  pageSizes: number [] = [10, 25, 50];
  _pageSize: string = "10";
  pageIndex: number = 1;
  arrData:any[] = []
  totalItems: number | undefined
  selectedFilter:number = 0
  searchText:string=""
  intervalId: any
  flagButtonUpdate:boolean = false
  timeoutId: any;
  totalCurrent:number = 0.0
  totalVoltage:number = 0.0

  selectedPrefixVoltage: any;
  selectedPrefixAmpere:any;



  constructor(private deviceService: DevicesService, public dialog: MatDialog) {}
  messages: string[] = [];

  ngOnInit(): void {
    this.loadInfoDevice()
    this.loadData()
    this.selectedPrefixVoltage = this.prefixTplOne
    this.selectedPrefixAmpere = this.prefixTplOne


  }

  openEditWindow(element:any): void {
    const dialogRef = this.dialog.open(ChangeDeviceComponent, {
      data: element
    });

    dialogRef.afterClosed().subscribe((result:any) => {
      console.log('Диалоговое окно закрыто', result);
    });
  }

  changeState(state:boolean, nwk_adr:number): void{
    this.flagButtonUpdate = true
    clearTimeout(this.timeoutId)
    this.cSub = this.deviceService.changeState(nwk_adr, state).subscribe((res:boolean)=>{
      if (res == state){
        this.timeoutId =setTimeout(() => {
          this.flagButtonUpdate = false
        }, 3000);
      }else{
        this.flagButtonUpdate = false
      }
    })
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

  loadInfoDevice(): void {
    this.deviceService.onMessage().subscribe(message => {
      console.log(message)
      let currentParams:any[] = JSON.parse(message)
      const oldTotalCurrent = this.totalCurrent
      const oldTotalVoltage = this.totalVoltage

      this.totalCurrent = 0.0
      this.totalVoltage = 0.0
      currentParams.forEach((el: any) => {
        const found = this.arrData.find((item: any) => item.nwk_adr === el.nwk_adr);

        if (found) {
            found.instantVoltage = el.current_power;
            found.instantCurrent = el.current_current;
            found.total_energy = el.total_energy;
            if (!this.flagButtonUpdate){
            found.state = el.current_state

            this.totalCurrent += el.current_current;
            this.totalVoltage += el.current_power;
          }
          }
        })

        this.selectedPrefixVoltage = this.totalVoltage > oldTotalVoltage ? this.prefixTplOne : this.prefixTplTwo;
        this.selectedPrefixAmpere = this.totalCurrent > oldTotalCurrent ? this.prefixTplOne : this.prefixTplTwo;
      })
    }

    changeColor(prefix: any): boolean {
      if (prefix == this.prefixTplTwo){
        return true
      }else{
        return false
      }

    }


  loadData(): void {
    if (this.aSub) this.aSub.unsubscribe();
    this.aSub = this.deviceService.getAllDevices(this.pageIndex, this.pageSize, this.searchText).subscribe((res: any) =>

      {
        res.items.forEach((element:any) => {
          element.instantCurrent = null;
          element.instantVoltage = null;
          element.total_energy = null;
          element.state = null;
        });

        this.arrData = res.items
        this.totalItems = res.totalItems
        this.startAutoUpdate()
      })
  }


  startAutoUpdate(): void {
    this.deviceService.sendMessage(JSON.stringify(this.arrData))
    if (this.intervalId) clearInterval(this.intervalId);

    this.intervalId = setInterval(() => {
      this.deviceService.sendMessage(JSON.stringify(this.arrData))
      },  3000);
  }

  deleteDevice(device_id: number){

  }



  search(value:string): void {
    this.searchText = value
    this.loadData()
  }


  ngOnDestroy(): void {
    this.aSub?.unsubscribe();
    this.bSub?.unsubscribe();
    this.cSub?.unsubscribe();
  }

}
