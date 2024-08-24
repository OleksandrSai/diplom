import { Injectable } from '@angular/core';
import { Observable, Observer, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DevicesService {

  socket!: WebSocket;
  messageSubject = new Subject<any>();

  constructor() {
    this.connect();
  }

  private connect(): void {
    this.socket = new WebSocket('ws://localhost:8000/ws');

    this.socket.onopen = (event) => {
      console.log('Connected to WebSocket server.');
    };

    this.socket.onclose = (event) => {
      console.log('Disconnected from WebSocket server.');
    };
  }

  public onMessage(): Observable<string> {
    return new Observable((observer: Observer<string>) => {
      this.socket.onmessage = (event) => observer.next(event.data);
    });
  }

  public sendMessage(message: string): void {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    } else {
      console.error('WebSocket connection is not open.');
    }
  }

  public close(): void {
    this.socket.close();
  }

}
