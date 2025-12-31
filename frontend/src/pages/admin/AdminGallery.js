import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import { galleryAPI } from '../../services/api';
import { Plus, Edit, Trash2, Save } from 'lucide-react';

const AdminGallery = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMethod, setUploadMethod] = useState('url'); // 'url' or 'file'
  const [formData, setFormData] = useState({
    url: '',
    title: '',
    category: 'machinery',
    order: 0,
  });

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const res = await galleryAPI.getAll();
      setImages(res.data);
    } catch (error) {
      console.error('Error fetching gallery:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await galleryAPI.update(editing.id, formData);
      } else {
        if (uploadMethod === 'file' && selectedFile) {
          // File upload
          const formDataToSend = new FormData();
          formDataToSend.append('title', formData.title);
          formDataToSend.append('category', formData.category);
          formDataToSend.append('order', formData.order.toString());
          formDataToSend.append('file', selectedFile);
          await galleryAPI.create(formDataToSend);
        } else if (uploadMethod === 'url' && formData.url) {
          // URL upload
          const formDataToSend = new FormData();
          formDataToSend.append('title', formData.title);
          formDataToSend.append('category', formData.category);
          formDataToSend.append('order', formData.order.toString());
          formDataToSend.append('url', formData.url);
          await galleryAPI.create(formDataToSend);
        } else {
          alert('Please provide either a URL or select a file');
          return;
        }
      }
      fetchImages();
      setShowForm(false);
      setEditing(null);
      setSelectedFile(null);
      setUploadMethod('url');
      setFormData({ url: '', title: '', category: 'machinery', order: 0 });
    } catch (error) {
      console.error('Error saving:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this image?')) {
      try {
        await galleryAPI.delete(id);
        fetchImages();
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
          <h2 className="text-3xl font-bold text-gray-900">Gallery Management</h2>
          <button
            onClick={() => {
              setShowForm(true);
              setEditing(null);
              setSelectedFile(null);
              setUploadMethod('url');
              setFormData({ url: '', title: '', category: 'machinery', order: 0 });
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Image
          </button>
        </div>

        {showForm && (
          <div className="bg-white p-6 rounded-lg shadow mb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              {!editing && (
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Upload Method</label>
                  <div className="flex space-x-4">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="url"
                        checked={uploadMethod === 'url'}
                        onChange={(e) => setUploadMethod(e.target.value)}
                        className="mr-2"
                      />
                      URL
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="file"
                        checked={uploadMethod === 'file'}
                        onChange={(e) => setUploadMethod(e.target.value)}
                        className="mr-2"
                      />
                      Upload File
                    </label>
                  </div>
                </div>
              )}
              
              {!editing && uploadMethod === 'url' && (
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Image URL</label>
                  <input
                    type="url"
                    value={formData.url || ''}
                    onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                    required={uploadMethod === 'url'}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              )}
              
              {!editing && uploadMethod === 'file' && (
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Image File</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    required={uploadMethod === 'file'}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              )}
              
              {editing && (
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Image URL</label>
                  <input
                    type="url"
                    value={formData.url}
                    onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              )}
              
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
                <label className="block text-gray-700 font-semibold mb-2">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="machinery">Machinery</option>
                  <option value="products">Products</option>
                  <option value="facility">Facility</option>
                </select>
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

        <div className="grid md:grid-cols-3 gap-6">
          {images.map((image) => (
            <div key={image.id} className="bg-white rounded-lg shadow overflow-hidden">
              <img src={image.url} alt={image.title} className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="font-bold text-gray-900 mb-2">{image.title}</h3>
                <p className="text-sm text-gray-600 mb-4 capitalize">{image.category}</p>
                <div className="flex space-x-2">
                  <button
                    onClick={() => {
                      setEditing(image);
                      setFormData(image);
                      setShowForm(true);
                    }}
                    className="text-blue-600 text-sm"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button onClick={() => handleDelete(image.id)} className="text-red-600 text-sm">
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminGallery;



