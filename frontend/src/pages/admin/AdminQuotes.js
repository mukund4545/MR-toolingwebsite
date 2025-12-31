import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import { quoteAPI } from '../../services/api';
import { Mail, Phone, Building, Calendar } from 'lucide-react';

const AdminQuotes = () => {
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuotes();
  }, []);

  const fetchQuotes = async () => {
    try {
      const res = await quoteAPI.getAllRequests();
      setQuotes(res.data);
    } catch (error) {
      console.error('Error fetching quotes:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await quoteAPI.updateRequest(id, status);
      fetchQuotes();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      reviewed: 'bg-yellow-100 text-yellow-800',
      quoted: 'bg-green-100 text-green-800',
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
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Quote Requests</h2>

        <div className="space-y-6">
          {quotes.map((quote) => (
            <div key={quote.id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{quote.name}</h3>
                  <div className="flex items-center text-gray-600 mt-2 space-x-4 flex-wrap">
                    {quote.company && (
                      <span className="flex items-center">
                        <Building className="h-4 w-4 mr-1" />
                        {quote.company}
                      </span>
                    )}
                    <span className="flex items-center">
                      <Mail className="h-4 w-4 mr-1" />
                      {quote.email}
                    </span>
                    <span className="flex items-center">
                      <Phone className="h-4 w-4 mr-1" />
                      {quote.phone}
                    </span>
                    <span className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(quote.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <select
                  value={quote.status}
                  onChange={(e) => updateStatus(quote.id, e.target.value)}
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(quote.status)}`}
                >
                  <option value="new">New</option>
                  <option value="reviewed">Reviewed</option>
                  <option value="quoted">Quoted</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Service Type</h4>
                  <p className="text-gray-700">{quote.service_type}</p>
                </div>
                {quote.material_type && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Material Type</h4>
                    <p className="text-gray-700">{quote.material_type}</p>
                  </div>
                )}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Quantity</h4>
                  <p className="text-gray-700">{quote.quantity}</p>
                </div>
                {quote.timeline && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Timeline</h4>
                    <p className="text-gray-700">{quote.timeline}</p>
                  </div>
                )}
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
                <p className="text-gray-700">{quote.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminQuotes;



