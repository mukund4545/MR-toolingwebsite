import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import About from './pages/About';
import Services from './pages/Services';
import Infrastructure from './pages/Infrastructure';
import Gallery from './pages/Gallery';
import Industries from './pages/Industries';
import Contact from './pages/Contact';
import Quote from './pages/Quote';
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminContent from './pages/admin/AdminContent';
import AdminServices from './pages/admin/AdminServices';
import AdminInfrastructure from './pages/admin/AdminInfrastructure';
import AdminIndustries from './pages/admin/AdminIndustries';
import AdminGallery from './pages/admin/AdminGallery';
import AdminStats from './pages/admin/AdminStats';
import AdminInquiries from './pages/admin/AdminInquiries';
import AdminQuotes from './pages/admin/AdminQuotes';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="services" element={<Services />} />
          <Route path="infrastructure" element={<Infrastructure />} />
          <Route path="gallery" element={<Gallery />} />
          <Route path="industries" element={<Industries />} />
          <Route path="contact" element={<Contact />} />
          <Route path="quote" element={<Quote />} />
        </Route>

        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/content"
          element={
            <ProtectedRoute>
              <AdminContent />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/services"
          element={
            <ProtectedRoute>
              <AdminServices />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/infrastructure"
          element={
            <ProtectedRoute>
              <AdminInfrastructure />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/industries"
          element={
            <ProtectedRoute>
              <AdminIndustries />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/gallery"
          element={
            <ProtectedRoute>
              <AdminGallery />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/stats"
          element={
            <ProtectedRoute>
              <AdminStats />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/inquiries"
          element={
            <ProtectedRoute>
              <AdminInquiries />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/quotes"
          element={
            <ProtectedRoute>
              <AdminQuotes />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;

