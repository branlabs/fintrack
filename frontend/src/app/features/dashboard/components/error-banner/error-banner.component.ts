import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-error-banner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './error-banner.component.html',
  styleUrls: ['./error-banner.component.scss'],
})
export class ErrorBannerComponent {
  @Input() message = '';
}
