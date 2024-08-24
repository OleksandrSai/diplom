import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GroupService {


  constructor(private http: HttpClient) { }

  getAllGroup(pageIndex: number, pageSize: number, searchText:string): Observable<any[]>{
    return this.http.get<any[]>(`/api/meter/?startIndex=${pageIndex}&pageSize=${pageSize}&searchText=${searchText}`)
  }

  addGroup(cron_str:string): Observable<any[]>{
    return this.http.post<any[]>('/api/group/', {cron_str})
  }

  delGroup(id:number): Observable<string>{
    return this.http.delete<string>(`/api/group/${id}`, )
  }

}
