import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeDeviceComponent } from './change-device.component';

describe('ChangeDeviceComponent', () => {
  let component: ChangeDeviceComponent;
  let fixture: ComponentFixture<ChangeDeviceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChangeDeviceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChangeDeviceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
