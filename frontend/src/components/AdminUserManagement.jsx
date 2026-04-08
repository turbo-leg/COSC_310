import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Trash2, UserX, Shield, Utensils } from 'lucide-react';

const AdminUserManagement = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await api.get('/users/');
      setUsers(res.data);
    } catch (err) {
      setError('Failed to fetch users list.');
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await api.delete(`/users/${userId}`);
      setUsers(users.filter(u => u.userId !== userId));
    } catch (err) {
      alert('Failed to delete user.');
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  if (loading) {
    return <div className="text-gray-500 py-8 text-center animate-pulse">Loading users...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50/50 text-sm tracking-wider text-gray-500 uppercase">
            <th className="py-4 px-6 font-semibold">User details</th>
            <th className="py-4 px-6 font-semibold">Role</th>
            <th className="py-4 px-6 font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {users.map((user) => (
            <tr key={user.userId} className="hover:bg-gray-50/50 transition-colors group">
              <td className="py-4 px-6">
                <div className="flex flex-col">
                  <span className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">{user.name}</span>
                  <span className="text-sm text-gray-500">{user.email}</span>
                </div>
              </td>
              <td className="py-4 px-6">
                <div className="flex items-center gap-2">
                  {user.role === 'admin' && <Shield className="w-4 h-4 text-purple-500" />}
                  {user.role === 'restaurant_owner' && <Utensils className="w-4 h-4 text-orange-500" />}
                  {(!user.role || user.role === 'customer') && <UserX className="w-4 h-4 text-gray-400" />}
                  <span className="text-sm font-medium capitalize text-gray-700 bg-gray-100 px-2.5 py-1 rounded-full">
                    {user.role || 'Customer'}
                  </span>
                </div>
              </td>
              <td className="py-4 px-6">
                <button
                  onClick={() => deleteUser(user.userId)}
                  className="flex items-center gap-2 text-red-500 hover:text-red-700 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  <span className="text-sm font-medium">Delete</span>
                </button>
              </td>
            </tr>
          ))}
          {users.length === 0 && (
            <tr>
              <td colSpan="3" className="py-8 text-center text-gray-500">No users found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default AdminUserManagement;
