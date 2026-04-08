import React, { useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import api from '../lib/api';
import { CreditCard, CheckCircle2, AlertCircle, Lock } from 'lucide-react';

const CheckoutPayment = () => {
  const navigate = useNavigate();
  const { orderId } = useParams();
  const location = useLocation();
  const amount = location.state?.amount || 0;
  const [creditCard, setCreditCard] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [transactionId, setTransactionId] = useState('');

  const handlePayment = async (e) => {
    e.preventDefault();
    if (creditCard.length < 16) {
      setError('Please enter a valid 16-digit credit card number.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      // 1. Process Payment
      const paymentRes = await api.post('/payments/process', {
        order_id: orderId,
        credit_card: creditCard
      });

      setTransactionId(paymentRes.data.transaction_id);

      // 2. Update Order Status
      await api.patch(`/orders/${orderId}/payment`, {
        status: 'accepted'
      });

      setSuccess(true);
      setTimeout(() => {
        navigate('/orders'); // Redirect to user's orders later
      }, 3000);
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Payment processing failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-8 text-center animate-in zoom-in duration-500">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
          <CheckCircle2 className="w-10 h-10 text-green-600" />
        </div>
        <h2 className="text-3xl font-extrabold text-gray-900 mb-2">Payment Successful!</h2>
        <p className="text-gray-500 mb-6 text-lg">Transaction ID: {transactionId}</p>
        <p className="text-gray-400">Redirecting to your orders...</p>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto p-6 md:p-10 my-10 bg-white rounded-3xl shadow-xl border border-gray-100 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="mb-10 text-center">
        <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-blue-100 shadow-sm">
          <CreditCard className="w-8 h-8" />
        </div>
        <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">Secure Checkout</h2>
        <p className="text-gray-500 mt-2">Complete your order payment</p>
      </div>

      {amount > 0 && (
        <div className="bg-gray-50 rounded-2xl p-6 mb-8 flex justify-between items-center border border-gray-200/60">
          <span className="text-gray-600 font-medium">Total Amount Due</span>
          <span className="text-3xl font-bold text-gray-900">${amount.toFixed(2)}</span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-3 p-4 mb-8 bg-red-50 text-red-700 rounded-xl border border-red-100 animate-in shake">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <p className="font-medium text-sm">{error}</p>
        </div>
      )}

      <form onSubmit={handlePayment} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Card Number</label>
          <div className="relative group">
            <input
              type="text"
              maxLength="16"
              placeholder="0000 0000 0000 0000"
              value={creditCard}
              onChange={(e) => setCreditCard(e.target.value.replace(/\D/g, ''))}
              className="w-full pl-12 pr-4 py-4 bg-gray-50 border border-gray-200 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-gray-900 font-mono tracking-wider shadow-sm group-hover:border-gray-300"
              required
            />
            <CreditCard className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || creditCard.length < 16}
          className={`w-full py-4 px-6 rounded-2xl text-white font-bold text-lg transition-all shadow-md hover:shadow-xl flex justify-center items-center gap-2
            ${loading || creditCard.length < 16 
              ? 'bg-gray-300 cursor-not-allowed text-gray-500' 
              : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 transform hover:-translate-y-0.5'
            }`}
        >
          {loading ? (
            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Lock className="w-5 h-5" />
              Pay Securely
            </>
          )}
        </button>
        <p className="text-center text-xs text-gray-400 flex items-center justify-center gap-1 mt-4">
          <Lock className="w-3 h-3" /> Payments are encrypted and secure
        </p>
      </form>
    </div>
  );
};

export default CheckoutPayment;
