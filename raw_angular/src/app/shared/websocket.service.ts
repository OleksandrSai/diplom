import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  socket!: WebSocket;
  messageSubject = new Subject<any>();

  constructor() {
    this.connect();
  }

  connect() {
    this.socket = new WebSocket('ws://your-websocket-url');

    this.socket.onmessage = (event) => {
      this.messageSubject.next(JSON.parse(event.data));
    };

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  sendMessage(message: any) {
    this.socket.send(JSON.stringify(message));
  }

  get messages$() {
    return this.messageSubject.asObservable();
  }



}
