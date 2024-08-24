import { TestBed } from '@angular/core/testing';

import { DivicesService } from './divices.service';

describe('DivicesService', () => {
  let service: DivicesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DivicesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
