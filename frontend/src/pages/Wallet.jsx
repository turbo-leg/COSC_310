import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Wallet, PlusCircle, RefreshCw, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import api from '@/lib/api';

function formatCurrency(value) {
  const amount = Number(value || 0);
  return new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: 'CAD',
  }).format(amount);
}

function getRoleFromToken(token) {
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return String(payload.role || '').toLowerCase().replace(/\s+/g, '_');
  } catch {
    return null;
  }
}

export default function WalletPage() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const userRole = useMemo(() => getRoleFromToken(token), [token]);

  const [balance, setBalance] = useState(null);
  const [amount, setAmount] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [loadingBalance, setLoadingBalance] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const customerRoles = new Set(['customer', 'regular_user']);

  const loadBalance = async () => {
    setLoadingBalance(true);
    setError('');

    try {
      const { data } = await api.get('/wallet/me');
      setBalance(data.walletBalance);
    } catch (err) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      if (status === 401) {
        localStorage.removeItem('token');
        navigate('/login', { replace: true });
        return;
      }

      setError(typeof detail === 'string' ? detail : 'Unable to load wallet balance.');
    } finally {
      setLoadingBalance(false);
    }
  };

  useEffect(() => {
    if (!token) {
      navigate('/login', { replace: true });
      return;
    }

    loadBalance();
  }, [token]);

  const handleTopUp = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    const numericAmount = Number(amount);
    if (!Number.isFinite(numericAmount) || numericAmount <= 0) {
      setError('Please enter a valid top-up amount greater than 0.');
      return;
    }

    if (cardNumber.length !== 16) {
      setError('Please enter a valid 16-digit card number to add funds.');
      return;
    }

    setSubmitting(true);
    try {
      const { data } = await api.post('/wallet/top-up', {
        amount: numericAmount,
        credit_card: cardNumber,
      });
      setBalance(data.walletBalance);
      setAmount('');
      setCardNumber('');
      setSuccess(`Wallet updated successfully. New balance: ${formatCurrency(data.walletBalance)}`);
    } catch (err) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      if (status === 401) {
        localStorage.removeItem('token');
        navigate('/login', { replace: true });
        return;
      }

      setError(typeof detail === 'string' ? detail : 'Top-up failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (token && userRole && !customerRoles.has(userRole)) {
    return (
      <div className="max-w-3xl mx-auto p-6 md:p-10">
        <Card className="border-amber-300/60 bg-amber-50/40">
          <CardHeader>
            <CardTitle className="text-amber-800 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Wallet Not Available For This Role
            </CardTitle>
            <CardDescription className="text-amber-700">
              Wallet endpoints currently work for customer accounts only.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate('/')} variant="outline">Return Home</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-72px)] p-6 md:p-10 bg-gradient-to-br from-sky-50 via-cyan-50 to-emerald-50">
      <div className="max-w-3xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-3 duration-500">
        <Card className="border-cyan-200/80 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-slate-800">
              <Wallet className="w-5 h-5 text-cyan-700" />
              My Wallet
            </CardTitle>
            <CardDescription>
              View your balance and add funds for faster checkout.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-xl border border-cyan-200 bg-white/80 p-4">
              <p className="text-sm text-slate-600">Current Balance</p>
              <p className="text-3xl font-extrabold tracking-tight text-slate-900">
                {loadingBalance ? 'Loading...' : formatCurrency(balance)}
              </p>
            </div>

            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                className="gap-2"
                onClick={loadBalance}
                disabled={loadingBalance || submitting}
              >
                <RefreshCw className="w-4 h-4" />
                Refresh Balance
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-emerald-200/80 shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-slate-800">
              <PlusCircle className="w-5 h-5 text-emerald-700" />
              Top Up Wallet
            </CardTitle>
            <CardDescription>
                Enter an amount and card number to add funds to your wallet.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleTopUp} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="amount">Amount</Label>
                <Input
                  id="amount"
                  type="number"
                  min="0.01"
                  step="0.01"
                  placeholder="e.g. 25.00"
                  value={amount}
                  onChange={(event) => setAmount(event.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="card-number">Card Number</Label>
                <Input
                  id="card-number"
                  type="text"
                  inputMode="numeric"
                  maxLength="16"
                  placeholder="0000 0000 0000 0000"
                  value={cardNumber}
                  onChange={(event) => setCardNumber(event.target.value.replace(/\D/g, ''))}
                />
                <p className="text-xs text-muted-foreground">
                  Simulated payment: this card is only validated as a 16-digit number.
                </p>
              </div>

              {error && (
                <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                  <AlertCircle className="w-4 h-4" />
                  {error}
                </div>
              )}

              {success && (
                <div className="flex items-center gap-2 rounded-md border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                  <CheckCircle2 className="w-4 h-4" />
                  {success}
                </div>
              )}

              <Button type="submit" disabled={submitting || loadingBalance} className="w-full md:w-auto">
                {submitting ? 'Adding Funds...' : 'Add Funds'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
