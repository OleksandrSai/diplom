import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatisticService {

  constructor(private http: HttpClient) {}

  getDeviceStatistic(deviceId: number, pageIndex: number, pageSize: number, searchText:string): Observable<any[]>{
    return this.http.get<any[]>(`/api/statistic/${deviceId}/?pageIndex=${pageIndex}&pageSize=${pageSize}&searchText=${searchText}`)
  }

}
