import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Don't set Content-Type for FormData, let axios handle it
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/admin/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  me: () => api.get('/auth/me'),
  changePassword: (oldPassword, newPassword) =>
    api.post('/auth/change-password', { old_password: oldPassword, new_password: newPassword }),
};

// Content API
export const contentAPI = {
  getAll: () => api.get('/content'),
  getByType: (type) => api.get(`/content/${type}`),
  update: (type, data) => api.put(`/content/${type}`, data),
};

// Services API
export const servicesAPI = {
  getAll: () => api.get('/services'),
  create: (data) => api.post('/services', data),
  update: (id, data) => api.put(`/services/${id}`, data),
  delete: (id) => api.delete(`/services/${id}`),
};

// Infrastructure API
export const infrastructureAPI = {
  getAll: () => api.get('/infrastructure'),
  create: (data) => api.post('/infrastructure', data),
  update: (id, data) => api.put(`/infrastructure/${id}`, data),
  delete: (id) => api.delete(`/infrastructure/${id}`),
};

// Industries API
export const industriesAPI = {
  getAll: () => api.get('/industries'),
  create: (data) => api.post('/industries', data),
  update: (id, data) => api.put(`/industries/${id}`, data),
  delete: (id) => api.delete(`/industries/${id}`),
};

// Gallery API
export const galleryAPI = {
  getAll: () => api.get('/gallery'),
  create: (data) => api.post('/gallery', data),
  update: (id, data) => api.put(`/gallery/${id}`, data),
  delete: (id) => api.delete(`/gallery/${id}`),
};

// Stats API
export const statsAPI = {
  getAll: () => api.get('/stats'),
  update: (data) => api.put('/stats', data),
};

// Contact API
export const contactAPI = {
  submit: (data) => api.post('/contact', data),
  getAllInquiries: () => api.get('/contact/inquiries'),
  updateInquiry: (id, status) => api.put(`/contact/inquiries/${id}`, { status }),
};

// Quote API
export const quoteAPI = {
  submit: (data) => api.post('/quote', data),
  getAllRequests: () => api.get('/quote/requests'),
  updateRequest: (id, status) => api.put(`/quote/requests/${id}`, { status }),
};

export default api;



