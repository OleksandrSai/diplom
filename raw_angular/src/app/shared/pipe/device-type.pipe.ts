import { Pipe, PipeTransform } from '@angular/core';
import { DeviceType } from '../interface/device-type';

@Pipe({
  name: 'deviceType',
  standalone: true
})
export class DeviceTypePipe implements PipeTransform {
  transform(value: DeviceType): string {
    return DeviceType[value] || 'Unknown device';
  }
}
