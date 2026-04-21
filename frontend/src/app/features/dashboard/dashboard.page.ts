import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { forkJoin } from 'rxjs';

import { Category } from '../../core/models/category.model';
import { User } from '../../core/models/user.model';
import { CreateTransactionPayload } from '../../core/models/transaction.model';
import { FinanceApiService } from '../../core/services/finance-api.service';
import { TransactionFormComponent } from './components/transaction-form/transaction-form.component';
import { ErrorBannerComponent } from './components/error-banner/error-banner.component';
import { LoadingSkeletonComponent } from './components/loading-skeleton/loading-skeleton.component';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, TransactionFormComponent, ErrorBannerComponent, LoadingSkeletonComponent],
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPageComponent implements OnInit {
  categories: Category[] = [];
  users: User[] = [];

  initialLoading = true;
  initialLoadError: string | null = null;

  submitLoading = false;
  submitError: string | null = null;
  submitSuccessMessage: string | null = null;

  constructor(private readonly financeApi: FinanceApiService) {}

  ngOnInit(): void {
    this.loadInitialData();
  }

  loadInitialData(): void {
    this.initialLoading = true;
    this.initialLoadError = null;

    forkJoin({
      categories: this.financeApi.getCategories(),
      users: this.financeApi.getUsers(),
    }).subscribe({
      next: ({ categories, users }) => {
        this.categories = categories;
        this.users = users;
        this.initialLoading = false;
      },
      error: (error: HttpErrorResponse) => {
        this.initialLoadError = this.extractErrorMessage(
          error,
          'Could not load users and categories. Please try again.',
        );
        this.initialLoading = false;
      },
    });
  }

  onSubmitTransaction(payload: CreateTransactionPayload): void {
    this.submitLoading = true;
    this.submitError = null;
    this.submitSuccessMessage = null;

    this.financeApi.createTransaction(payload).subscribe({
      next: () => {
        this.submitSuccessMessage = 'Transaction saved successfully.';
        this.submitLoading = false;
      },
      error: (error: HttpErrorResponse) => {
        this.submitError = this.extractErrorMessage(
          error,
          'Could not save transaction. Please check your input and retry.',
        );
        this.submitLoading = false;
      },
    });
  }

  get disableForm(): boolean {
    return (
      this.initialLoading ||
      !!this.initialLoadError ||
      this.categories.length === 0 ||
      this.users.length === 0
    );
  }

  private extractErrorMessage(error: HttpErrorResponse, fallback: string): string {
    const data = error?.error;
    if (typeof data === 'string' && data.trim()) {
      return data;
    }
    if (data && typeof data === 'object') {
      const detail = (data as { detail?: string }).detail;
      if (typeof detail === 'string' && detail.trim()) {
        return detail;
      }
      const nameErrors = (data as { name?: string[] }).name;
      if (Array.isArray(nameErrors) && nameErrors.length > 0) {
        return nameErrors[0];
      }
    }
    return fallback;
  }
}
