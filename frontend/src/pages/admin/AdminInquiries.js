import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import { contactAPI } from '../../services/api';
import { Mail, Phone, Calendar } from 'lucide-react';

const AdminInquiries = () => {
  const [inquiries, setInquiries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInquiries();
  }, []);

  const fetchInquiries = async () => {
    try {
      const res = await contactAPI.getAllInquiries();
      setInquiries(res.data);
    } catch (error) {
      console.error('Error fetching inquiries:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await contactAPI.updateInquiry(id, status);
      fetchInquiries();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      read: 'bg-yellow-100 text-yellow-800',
      contacted: 'bg-green-100 text-green-800',
      closed: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || colors.new;
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Contact Inquiries</h2>

        <div className="space-y-6">
          {inquiries.map((inquiry) => (
            <div key={inquiry.id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{inquiry.name}</h3>
                  <div className="flex items-center text-gray-600 mt-2 space-x-4">
                    <span className="flex items-center">
                      <Mail className="h-4 w-4 mr-1" />
                      {inquiry.email}
                    </span>
                    {inquiry.phone && (
                      <span className="flex items-center">
                        <Phone className="h-4 w-4 mr-1" />
                        {inquiry.phone}
                      </span>
                    )}
                    <span className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(inquiry.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <select
                  value={inquiry.status}
                  onChange={(e) => updateStatus(inquiry.id, e.target.value)}
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(inquiry.status)}`}
                >
                  <option value="new">New</option>
                  <option value="read">Read</option>
                  <option value="contacted">Contacted</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div className="mb-4">
                <h4 className="font-semibold text-gray-900 mb-2">Subject: {inquiry.subject}</h4>
                <p className="text-gray-700">{inquiry.message}</p>
              </div>
              {inquiry.request_quote && (
                <div className="bg-blue-50 p-3 rounded-lg">
                  <span className="text-blue-800 font-semibold">✓ Customer also requested a quote</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminInquiries;



