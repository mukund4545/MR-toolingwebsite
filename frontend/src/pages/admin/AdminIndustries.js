import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import { industriesAPI } from '../../services/api';
import { Plus, Edit, Trash2, Save } from 'lucide-react';

const AdminIndustries = () => {
  const [industries, setIndustries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    icon: 'building',
    clients: [],
    order: 0,
  });

  useEffect(() => {
    fetchIndustries();
  }, []);

  const fetchIndustries = async () => {
    try {
      const res = await industriesAPI.getAll();
      setIndustries(res.data);
    } catch (error) {
      console.error('Error fetching industries:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await industriesAPI.update(editing.id, formData);
      } else {
        await industriesAPI.create(formData);
      }
      fetchIndustries();
      setShowForm(false);
      setEditing(null);
      setFormData({ title: '', description: '', icon: 'building', clients: [], order: 0 });
    } catch (error) {
      console.error('Error saving:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this industry?')) {
      try {
        await industriesAPI.delete(id);
        fetchIndustries();
      } catch (error) {
        console.error('Error deleting:', error);
      }
    }
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
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Industries Management</h2>
          <button
            onClick={() => {
              setShowForm(true);
              setEditing(null);
              setFormData({ title: '', description: '', icon: 'building', clients: [], order: 0 });
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Industry
          </button>
        </div>

        {showForm && (
          <div className="bg-white p-6 rounded-lg shadow mb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Clients (one per line)</label>
                <textarea
                  value={formData.clients.join('\n')}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      clients: e.target.value.split('\n').filter((c) => c.trim()),
                    })
                  }
                  rows="4"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg"
                >
                  Cancel
                </button>
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center">
                  <Save className="h-5 w-5 mr-2" />
                  Save
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6">
          {industries.map((industry) => (
            <div key={industry.id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-gray-900">{industry.title}</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={() => {
                      setEditing(industry);
                      setFormData(industry);
                      setShowForm(true);
                    }}
                    className="text-blue-600"
                  >
                    <Edit className="h-5 w-5" />
                  </button>
                  <button onClick={() => handleDelete(industry.id)} className="text-red-600">
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
              <p className="text-gray-600 mb-4">{industry.description}</p>
              <ul className="list-disc list-inside text-sm text-gray-600">
                {industry.clients?.map((client, idx) => (
                  <li key={idx}>{client}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminIndustries;



