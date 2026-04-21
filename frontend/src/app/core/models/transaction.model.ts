export interface CreateTransactionPayload {
  category: number;
  user: number;
  amount: string;
  occurred_on: string;
  note: string;
}

export interface Transaction {
  id: number;
  category: number;
  user: number;
  amount: string;
  occurred_on: string;
  note: string;
  created_at: string;
  updated_at: string;
}
