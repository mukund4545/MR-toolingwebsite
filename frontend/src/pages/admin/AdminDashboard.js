import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, Settings, Building, Globe, Image, BarChart3, 
  Mail, FileCheck, LogOut 
} from 'lucide-react';
import { contactAPI, quoteAPI } from '../../services/api';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ inquiries: 0, quotes: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [inquiriesRes, quotesRes] = await Promise.all([
          contactAPI.getAllInquiries(),
          quoteAPI.getAllRequests(),
        ]);
        setStats({
          inquiries: inquiriesRes.data.length,
          quotes: quotesRes.data.length,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/admin/login');
  };

  const menuItems = [
    { icon: FileText, label: 'Content', path: '/admin/content' },
    { icon: Settings, label: 'Services', path: '/admin/services' },
    { icon: Building, label: 'Infrastructure', path: '/admin/infrastructure' },
    { icon: Globe, label: 'Industries', path: '/admin/industries' },
    { icon: Image, label: 'Gallery', path: '/admin/gallery' },
    { icon: BarChart3, label: 'Stats', path: '/admin/stats' },
    { icon: Mail, label: 'Inquiries', path: '/admin/inquiries', badge: stats.inquiries },
    { icon: FileCheck, label: 'Quotes', path: '/admin/quotes', badge: stats.quotes },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <button
            onClick={handleLogout}
            className="flex items-center text-gray-700 hover:text-red-600 transition-colors"
          >
            <LogOut className="h-5 w-5 mr-2" />
            Logout
          </button>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600">Contact Inquiries</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.inquiries}</p>
                  </div>
                  <Mail className="h-12 w-12 text-blue-600" />
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600">Quote Requests</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.quotes}</p>
                  </div>
                  <FileCheck className="h-12 w-12 text-green-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b">
                <h2 className="text-xl font-bold text-gray-900">Management Sections</h2>
              </div>
              <div className="p-6 grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                {menuItems.map((item) => (
                  <button
                    key={item.path}
                    onClick={() => navigate(item.path)}
                    className="p-6 border-2 border-gray-200 rounded-lg hover:border-blue-600 hover:bg-blue-50 transition-colors text-left group"
                  >
                    <item.icon className="h-8 w-8 text-gray-600 group-hover:text-blue-600 mb-3" />
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-gray-900">{item.label}</span>
                      {item.badge !== undefined && (
                        <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
                          {item.badge}
                        </span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;



