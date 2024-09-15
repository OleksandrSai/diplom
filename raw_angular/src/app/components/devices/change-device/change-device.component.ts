import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { DevicesService } from '../../../shared/service/devices.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-change-device',
  standalone: true,
  imports:[FormsModule, NzInputModule, NzButtonModule],
  templateUrl: './change-device.component.html',
  styleUrl: './change-device.component.scss'
})
export class ChangeDeviceComponent implements OnInit, OnDestroy{

  constructor(private deviceService: DevicesService, public dialogRef: MatDialogRef<ChangeDeviceComponent>, @Inject(MAT_DIALOG_DATA) public data: any ) {}
  aSub:Subscription | undefined
  deviceName: string = ""

  editName(){
    this.aSub = this.deviceService.changeDeviceName(this.data.id, this.deviceName).subscribe((res:any)=>{
      this.closeDialog()
    })
  }

  ngOnInit(): void {
    this.deviceName = this.data.name
  }

  closeDialog(): void {
    this.dialogRef.close()
  }

  ngOnDestroy(): void{
    this.aSub?.unsubscribe()
  }

}
