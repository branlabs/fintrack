import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../config/api.config';
import { Category } from '../models/category.model';
import { User } from '../models/user.model';
import { CreateTransactionPayload, Transaction } from '../models/transaction.model';

@Injectable({ providedIn: 'root' })
export class FinanceApiService {
  constructor(private readonly http: HttpClient) {}

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${API_BASE_URL}category/list/`);
  }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${API_BASE_URL}user/list/`);
  }

  createTransaction(payload: CreateTransactionPayload): Observable<Transaction> {
    return this.http.post<Transaction>(`${API_BASE_URL}transaction/list/`, payload);
  }
}
