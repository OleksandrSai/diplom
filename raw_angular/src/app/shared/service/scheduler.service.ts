import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SchedulerService {

  constructor(private http: HttpClient) { }

  getAllScheduler(pageIndex: number, pageSize: number, selectedFilter:string, searchText:string): Observable<any[]>{
    return this.http.get<any[]>(`/api/meter/?startIndex=${pageIndex}&pageSize=${pageSize}&selectedFilter=${selectedFilter}&searchText=${searchText}`)
  }

  addScheduler(cron_str:string): Observable<any[]>{
    return this.http.post<any[]>('/api/meter/', {cron_str})
  }

  delScheduler(id:number): Observable<string>{
    return this.http.delete<string>(`/api/scheduler/${id}`, )
  }
}
