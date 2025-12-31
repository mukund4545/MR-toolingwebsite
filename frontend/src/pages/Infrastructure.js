import React, { useState, useEffect } from 'react';
import { Settings, ShieldCheck, Users, Award } from 'lucide-react';
import { infrastructureAPI } from '../services/api';
import companyImage from '../assets/company.jpeg';

const Infrastructure = () => {
  const [infrastructure, setInfrastructure] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInfrastructure = async () => {
      try {
        const res = await infrastructureAPI.getAll();
        setInfrastructure(res.data);
      } catch (error) {
        console.error('Error fetching infrastructure:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchInfrastructure();
  }, []);

  const getIcon = (iconName) => {
    const icons = { settings: Settings, 'shield-check': ShieldCheck, users: Users, award: Award };
    const Icon = icons[iconName] || Settings;
    return <Icon className="h-12 w-12 text-blue-600" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section with Company Background */}
      <section 
        className="relative bg-cover bg-center bg-no-repeat text-white py-32"
        style={{ backgroundImage: `url(${companyImage})` }}
      >
        {/* Overlay for better text readability */}
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">Infrastructure & Capabilities</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            State-of-the-art facilities and technology for superior manufacturing
          </p>
        </div>
      </section>

      {/* Infrastructure Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {infrastructure.map((item) => (
              <div key={item.id} className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow text-center">
                <div className="mb-4 flex justify-center">{getIcon(item.icon)}</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">{item.title}</h2>
                <p className="text-gray-600">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Infrastructure;



