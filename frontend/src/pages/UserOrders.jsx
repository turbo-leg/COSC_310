import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { Package, Clock, XCircle, ArrowRight, RotateCcw, X, Bell } from 'lucide-react';

const REFUND_REASONS = [
  { value: 'never_arrived', label: 'Order never arrived' },
  { value: 'wrong_order', label: 'Wrong order received' },
  { value: 'poor_quality', label: 'Poor food quality' },
  { value: 'missing_items', label: 'Items missing from order' },
  { value: 'other', label: 'Other' },
];

export default function UserOrders() {
  const [orders, setOrders] = useState([]);
  const [refundsByOrder, setRefundsByOrder] = useState({});
  const [loading, setLoading] = useState(true);
  const [refundModal, setRefundModal] = useState(null);
  const [refundReason, setRefundReason] = useState('never_arrived');
  const [refundDescription, setRefundDescription] = useState('');
  const [refundError, setRefundError] = useState('');
  const [refundSubmitting, setRefundSubmitting] = useState(false);
  const [dismissedNotifications, setDismissedNotifications] = useState([]);
  const [toastNotifications, setToastNotifications] = useState([]);
  const seenNotificationIdsRef = useRef(new Set());
  const initializedNotificationsRef = useRef(false);
  const audioContextRef = useRef(null);
  const soundUnlockedRef = useRef(false);
  const navigate = useNavigate();

  const token = localStorage.getItem('token');
  const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
  const userId = decodedToken?.userId;

  const getAudioContext = () => {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) {
      return null;
    }

    if (!audioContextRef.current) {
      audioContextRef.current = new AudioContextClass();
    }
    return audioContextRef.current;
  };

  const unlockNotificationSound = async () => {
    try {
      const audioContext = getAudioContext();
      if (!audioContext) {
        return;
      }
      if (audioContext.state === 'suspended') {
        await audioContext.resume();
      }
      soundUnlockedRef.current = audioContext.state === 'running';
    } catch {
      soundUnlockedRef.current = false;
    }
  };

  const playNotificationSound = async () => {
    try {
      const audioContext = getAudioContext();
      if (!audioContext) {
        return;
      }
      if (audioContext.state === 'suspended') {
        await audioContext.resume();
      }
      if (audioContext.state !== 'running') {
        return;
      }

      const playTone = (frequency, startOffset, duration) => {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        const start = audioContext.currentTime + startOffset;
        const end = start + duration;

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(frequency, start);

        gainNode.gain.setValueAtTime(0.0001, start);
        gainNode.gain.exponentialRampToValueAtTime(0.09, start + 0.02);
        gainNode.gain.exponentialRampToValueAtTime(0.0001, end);

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.start(start);
        oscillator.stop(end);
      };

      // Two-note notification chime.
      playTone(784, 0.0, 0.14); // G5
      playTone(1047, 0.16, 0.18); // C6
    } catch {
      // Ignore audio playback issues (browser autoplay policy/device restrictions).
    }
  };

  useEffect(() => {
    unlockNotificationSound();

    const handleUserInteraction = () => {
      unlockNotificationSound();
    };

    window.addEventListener('pointerdown', handleUserInteraction, { passive: true });
    window.addEventListener('keydown', handleUserInteraction);

    fetchOrders();

    const intervalId = setInterval(() => {
      fetchOrders(true);
    }, 8000);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener('pointerdown', handleUserInteraction);
      window.removeEventListener('keydown', handleUserInteraction);
      if (audioContextRef.current) {
        audioContextRef.current.close();
        audioContextRef.current = null;
      }
    };
  }, []);

  const fetchOrders = async (silent = false) => {
    try {
      if (!silent) {
        setLoading(true);
      }
      const [ordersRes, refundsRes] = await Promise.all([
        api.get(`/orders/users/${userId}/orders`),
        api.get(`/refunds/user/${userId}`),
      ]);
      const fetchedOrders = ordersRes.data.reverse();
      setOrders(fetchedOrders);

      const latestNotifications = fetchedOrders
        .filter(order => order.customerNotified && order.latestNotification)
        .map(order => {
          const notification = order.latestNotification;
          const id = `${order.orderId}-${notification.sentAt || notification.newStatus || 'status'}`;
          return {
            id,
            orderId: order.orderId,
            message: notification.message || `Order #${order.orderId} status changed to ${order.status}`,
            sentAt: notification.sentAt,
          };
        });

      if (!initializedNotificationsRef.current) {
        latestNotifications.forEach(notification => seenNotificationIdsRef.current.add(notification.id));
        initializedNotificationsRef.current = true;
      } else {
        const newNotifications = latestNotifications.filter(
          notification => !seenNotificationIdsRef.current.has(notification.id)
        );

        if (newNotifications.length > 0) {
          newNotifications.forEach(notification => seenNotificationIdsRef.current.add(notification.id));
          setToastNotifications(prev => [...newNotifications, ...prev].slice(0, 3));
          if (soundUnlockedRef.current) {
            playNotificationSound();
          }
        }
      }

      const map = {};
      for (const r of refundsRes.data) {
        map[r.orderId] = r;
      }
      setRefundsByOrder(map);
    } catch (err) {
      console.error(err);
    } finally {
      if (!silent) {
        setLoading(false);
      }
    }
  };

  const handleCancel = async (orderId) => {
    if (!window.confirm("Are you sure you want to cancel this order?")) return;
    try {
      await api.put(`/orders/${orderId}/cancel`);
      fetchOrders();
    } catch (err) {
      alert("Cannot cancel order once preparation has started.");
    }
  };

  const openRefundModal = (order) => {
    setRefundModal(order);
    setRefundReason('never_arrived');
    setRefundDescription('');
    setRefundError('');
  };

  const closeRefundModal = () => {
    setRefundModal(null);
    setRefundError('');
  };

  const handleRefundSubmit = async () => {
    if (refundDescription.trim().length < 10) {
      setRefundError('Please provide a description of at least 10 characters.');
      return;
    }
    setRefundSubmitting(true);
    setRefundError('');
    try {
      await api.post(`/orders/${refundModal.orderId}/refund`, {
        user_id: userId,
        reason: refundReason,
        description: refundDescription.trim(),
      });
      closeRefundModal();
      fetchOrders();
      alert('Refund request submitted successfully.');
    } catch (err) {
      const detail = err.response?.data?.detail;
      setRefundError(detail || 'Failed to submit refund request.');
    } finally {
      setRefundSubmitting(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'accepted': return 'bg-secondary/20 text-secondary-foreground border-secondary/20';
      case 'preparing': return 'bg-purple-100 text-purple-700 border-purple-200';
      case 'assigned': case 'out-for-delivery': return 'bg-accent/20 text-accent-foreground border-accent/20';
      case 'delivered': return 'bg-green-100 text-green-700 border-green-200';
      case 'cancelled': return 'bg-red-100 text-red-700 border-red-200';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const canRequestRefund = (order) =>
    order.status === 'delivered' &&
    order.payment_status?.toLowerCase() === 'accepted' &&
    !refundsByOrder[order.orderId];

  const statusNotifications = orders
    .filter(order => order.customerNotified && order.latestNotification)
    .map(order => {
      const notification = order.latestNotification;
      const id = `${order.orderId}-${notification.sentAt || notification.newStatus || 'status'}`;
      return {
        id,
        orderId: order.orderId,
        message: notification.message || `Order #${order.orderId} status changed to ${order.status}`,
        sentAt: notification.sentAt,
      };
    })
    .filter(notification => !dismissedNotifications.includes(notification.id));

  const getRefundBadge = (orderId) => {
    const refund = refundsByOrder[orderId];
    if (!refund) return null;
    if (refund.status === 'approved') {
      return (
        <span className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-green-50 text-green-700 rounded-xl font-medium border border-green-200 text-sm">
          Refunded
        </span>
      );
    }
    if (refund.status === 'denied') {
      return (
        <span className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-red-50 text-red-600 rounded-xl font-medium border border-red-200 text-sm">
          Refund Denied
        </span>
      );
    }
    return (
      <span className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-amber-50 text-amber-700 rounded-xl font-medium border border-amber-200 text-sm">
        <RotateCcw className="w-4 h-4" /> Refund Pending
      </span>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {toastNotifications.length > 0 && (
        <div className="fixed top-20 right-4 z-50 w-full max-w-sm space-y-2">
          {toastNotifications.map(notification => (
            <div
              key={notification.id}
              className="rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-3 shadow-lg"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-bold text-emerald-800">Order Update</p>
                  <p className="text-sm text-emerald-700">{notification.message}</p>
                </div>
                <button
                  type="button"
                  className="text-emerald-700 hover:text-emerald-900"
                  onClick={() => setToastNotifications(prev => prev.filter(item => item.id !== notification.id))}
                  aria-label="Dismiss popup"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center gap-4 mb-10">
        <div className="p-4 bg-secondary/20 text-blue-600 rounded-2xl">
          <Package className="w-8 h-8" />
        </div>
        <div>
          <h1 className="text-4xl font-extrabold text-foreground">My Orders</h1>
          <p className="text-muted-foreground">Track and manage your recent meal requests.</p>
        </div>
      </div>

      {statusNotifications.length > 0 && (
        <div className="space-y-3 mb-8">
          {statusNotifications.map(notification => (
            <div
              key={notification.id}
              className="flex items-start justify-between gap-4 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3"
            >
              <div className="flex items-start gap-3">
                <Bell className="w-5 h-5 text-emerald-700 mt-0.5" />
                <div>
                  <p className="font-semibold text-emerald-800">Status Update</p>
                  <p className="text-sm text-emerald-700">{notification.message}</p>
                  {notification.sentAt && (
                    <p className="text-xs text-emerald-600 mt-1">
                      {new Date(notification.sentAt).toLocaleString()}
                    </p>
                  )}
                </div>
              </div>
              <button
                type="button"
                className="text-emerald-700 hover:text-emerald-900"
                onClick={() => setDismissedNotifications(prev => [...prev, notification.id])}
                aria-label="Dismiss notification"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {loading ? (
        <div className="space-y-4 animate-pulse">
          {[1, 2, 3].map(i => <div key={i} className="h-32 bg-muted rounded-2xl"></div>)}
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-20 bg-card text-card-foreground rounded-3xl border border-border shadow-sm">
          <Package className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-foreground">No orders yet</h3>
          <p className="text-muted-foreground mt-2">Looks like you haven't ordered anything.</p>
          <button type="button" onClick={() => navigate('/')} className="mt-6 bg-primary text-primary-foreground px-8 py-3 rounded-xl font-bold hover:bg-primary/90 transition shadow-md">Browse Restaurants</button>
        </div>
      ) : (
        <div className="grid gap-6">
          {orders.map(order => (
            <div key={order.orderId} className="bg-card text-card-foreground rounded-3xl shadow-sm border border-border p-6 flex flex-col md:flex-row gap-6 items-center hover:shadow-md transition">
              <div className="flex-1 space-y-4 w-full">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-foreground border-b border-border pb-2 mb-2">Order #{order.orderId}</h3>
                    <p className="text-sm font-medium text-muted-foreground mt-1">
                      Placed on {new Date(order.createdAt).toLocaleString()}
                    </p>
                  </div>
                  <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>

                <div className="flex flex-wrap gap-4 text-sm bg-muted p-4 rounded-xl">
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Payment:</span>
                    <span className="font-bold underline decoration-wavy decoration-green-400 capitalize">{order.payment_status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Total:</span>
                    <span className="font-bold text-foreground">${order.order_value.toFixed(2)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Items:</span>
                    <span className="font-bold text-foreground">{order.items?.length || 0}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-row md:flex-col gap-3 w-full md:w-auto mt-4 md:mt-0 justify-center">
                <button
                  type="button"
                  onClick={() => navigate(`/order/${order.orderId}/track`)}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-xl font-medium hover:bg-primary/90 transition shadow-sm"
                >
                  <Clock className="w-4 h-4" /> Track
                </button>
                {order.status === 'pending' && (
                  <button
                    type="button"
                    onClick={() => handleCancel(order.orderId)}
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-red-50 text-red-600 rounded-xl font-medium hover:bg-red-100 transition"
                  >
                    <XCircle className="w-4 h-4" /> Cancel
                  </button>
                )}
                {['pending', 'partial'].includes(order.payment_status?.toLowerCase()) &&
                  order.status !== 'cancelled' && (
                  <button
                    type="button"
                    onClick={() =>
                      navigate(`/payment/${order.orderId}`, {
                        state: { amount: order.amount_due ?? order.order_value },
                      })
                    }
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-green-50 text-green-700 rounded-xl font-medium hover:bg-green-100 transition border border-green-200"
                  >
                    Make Payment <ArrowRight className="w-4 h-4" />
                  </button>
                )}
                {getRefundBadge(order.orderId)}
                {canRequestRefund(order) && (
                  <button
                    type="button"
                    onClick={() => openRefundModal(order)}
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-amber-50 text-amber-700 rounded-xl font-medium hover:bg-amber-100 transition border border-amber-200"
                  >
                    <RotateCcw className="w-4 h-4" /> Refund
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {refundModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-card text-card-foreground rounded-3xl shadow-2xl p-8 w-full max-w-md mx-4 relative animate-in fade-in zoom-in-95 duration-200 border border-border">
            <button
              type="button"
              onClick={closeRefundModal}
              className="absolute top-4 right-4 text-muted-foreground hover:text-foreground transition"
            >
              <X className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-amber-100 rounded-xl">
                <RotateCcw className="w-6 h-6 text-amber-600" />
              </div>
              <div>
                <h2 className="text-xl font-extrabold text-foreground">Request Refund</h2>
                <p className="text-sm text-muted-foreground">Order #{refundModal.orderId} &mdash; ${refundModal.order_value.toFixed(2)}</p>
              </div>
            </div>

            <div className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-foreground mb-2">Reason</label>
                <select
                  value={refundReason}
                  onChange={e => setRefundReason(e.target.value)}
                  className="w-full border border-border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-300 bg-muted"
                >
                  {REFUND_REASONS.map(r => (
                    <option key={r.value} value={r.value}>{r.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-foreground mb-2">Description</label>
                <textarea
                  value={refundDescription}
                  onChange={e => setRefundDescription(e.target.value)}
                  rows={4}
                  placeholder="Please describe your issue in detail (min 10 characters)..."
                  className="w-full border border-border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-300 bg-muted resize-none"
                />
                <p className="text-xs text-muted-foreground mt-1">{refundDescription.length} / 500 characters</p>
              </div>

              {refundError && (
                <p className="text-sm text-red-600 bg-red-50 px-4 py-3 rounded-xl border border-red-100">{refundError}</p>
              )}

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={closeRefundModal}
                  className="flex-1 px-6 py-3 bg-muted text-foreground rounded-xl font-semibold hover:bg-muted/80 transition"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleRefundSubmit}
                  disabled={refundSubmitting}
                  className="flex-1 px-6 py-3 bg-amber-500 text-white rounded-xl font-semibold hover:bg-amber-600 transition disabled:opacity-60"
                >
                  {refundSubmitting ? 'Submitting…' : 'Submit Request'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}