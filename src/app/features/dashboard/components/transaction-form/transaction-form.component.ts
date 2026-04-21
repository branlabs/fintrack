import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Category } from '../../../../core/models/category.model';
import { User } from '../../../../core/models/user.model';
import { CreateTransactionPayload } from '../../../../core/models/transaction.model';

@Component({
  selector: 'app-transaction-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './transaction-form.component.html',
  styleUrls: ['./transaction-form.component.scss'],
})
export class TransactionFormComponent implements OnInit {
  @Input() categories: Category[] = [];
  @Input() users: User[] = [];
  @Input() submitLoading = false;
  @Input() disabled = false;

  @Output() submitTransaction = new EventEmitter<CreateTransactionPayload>();

  readonly form = this.fb.group({
    category: ['', Validators.required],
    user: ['', Validators.required],
    amount: ['', [Validators.required, Validators.min(0.01)]],
    occurred_on: ['', Validators.required],
    note: [''],
  });

  constructor(private readonly fb: FormBuilder) {}

  ngOnInit(): void {
    this.form.patchValue({ occurred_on: this.today() });
  }

  onSubmit(): void {
    if (this.disabled || this.submitLoading) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const amountNumber = Number(this.form.value.amount);
    if (!Number.isFinite(amountNumber) || amountNumber <= 0) {
      this.form.get('amount')?.setErrors({ invalid: true });
      return;
    }

    const payload: CreateTransactionPayload = {
      category: Number(this.form.value.category),
      user: Number(this.form.value.user),
      amount: amountNumber.toFixed(2),
      occurred_on: this.form.value.occurred_on || '',
      note: this.form.value.note?.trim() || '',
    };

    this.submitTransaction.emit(payload);
  }

  private today(): string {
    const d = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${mm}-${dd}`;
  }
}
