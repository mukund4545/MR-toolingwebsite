import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import { contentAPI } from '../../services/api';
import { Save } from 'lucide-react';

const AdminContent = () => {
  const [content, setContent] = useState({ company_info: null, about_content: null });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const [companyRes, aboutRes] = await Promise.all([
          contentAPI.getByType('company_info'),
          contentAPI.getByType('about_content'),
        ]);
        setContent({
          company_info: companyRes.data.content_data,
          about_content: aboutRes.data.content_data,
        });
      } catch (error) {
        console.error('Error fetching content:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchContent();
  }, []);

  const handleSave = async (type) => {
    setSaving(true);
    setMessage('');
    try {
      await contentAPI.update(type, { content_data: content[type] });
      setMessage(`${type.replace('_', ' ')} saved successfully!`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error saving content');
    } finally {
      setSaving(false);
    }
  };

  const updateContent = (type, field, value) => {
    setContent((prev) => ({
      ...prev,
      [type]: { ...prev[type], [field]: value },
    }));
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Content Management</h2>

        {message && (
          <div className={`mb-6 p-4 rounded-lg ${
            message.includes('Error') ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'
          }`}>
            {message}
          </div>
        )}

        {/* Company Info */}
        <div className="bg-white p-6 rounded-lg shadow mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Company Information</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Company Name</label>
              <input
                type="text"
                value={content.company_info?.name || ''}
                onChange={(e) => updateContent('company_info', 'name', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Tagline</label>
              <input
                type="text"
                value={content.company_info?.tagline || ''}
                onChange={(e) => updateContent('company_info', 'tagline', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Address</label>
              <textarea
                value={content.company_info?.address || ''}
                onChange={(e) => updateContent('company_info', 'address', e.target.value)}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Phone</label>
                <input
                  type="text"
                  value={content.company_info?.phone || ''}
                  onChange={(e) => updateContent('company_info', 'phone', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Email</label>
                <input
                  type="email"
                  value={content.company_info?.email || ''}
                  onChange={(e) => updateContent('company_info', 'email', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
            <button
              onClick={() => handleSave('company_info')}
              disabled={saving}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 flex items-center"
            >
              <Save className="h-5 w-5 mr-2" />
              Save Company Info
            </button>
          </div>
        </div>

        {/* About Content */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">About Page Content</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Mission</label>
              <textarea
                value={content.about_content?.mission || ''}
                onChange={(e) => updateContent('about_content', 'mission', e.target.value)}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Vision</label>
              <textarea
                value={content.about_content?.vision || ''}
                onChange={(e) => updateContent('about_content', 'vision', e.target.value)}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Description</label>
              <textarea
                value={content.about_content?.description || ''}
                onChange={(e) => updateContent('about_content', 'description', e.target.value)}
                rows="5"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <button
              onClick={() => handleSave('about_content')}
              disabled={saving}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 flex items-center"
            >
              <Save className="h-5 w-5 mr-2" />
              Save About Content
            </button>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminContent;



