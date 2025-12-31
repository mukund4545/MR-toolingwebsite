import React, { useState, useEffect } from 'react';
import { Factory, Package, Car, CheckCircle } from 'lucide-react';
import { servicesAPI } from '../services/api';
import servicesImage from '../assets/services.jpeg';
import plasticComponentsImage from '../assets/componenets.jpeg';
import automotiveComponentsImage from '../assets/automobile component.jpeg';

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const res = await servicesAPI.getAll();
        setServices(res.data);
      } catch (error) {
        console.error('Error fetching services:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchServices();
  }, []);

  const getServiceIcon = (iconName) => {
    const icons = { factory: Factory, package: Package, car: Car };
    const Icon = icons[iconName] || Factory;
    return <Icon className="h-16 w-16 text-blue-600" />;
  };

  const getServiceImage = (serviceTitle) => {
    if (serviceTitle.toLowerCase().includes('plastic components')) {
      return plasticComponentsImage;
    } else if (serviceTitle.toLowerCase().includes('automotive components')) {
      return automotiveComponentsImage;
    } else {
      return servicesImage;
    }
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
    <div className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">Our Services</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Comprehensive plastic injection molding solutions for your business needs
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {services.map((service) => (
            <div key={service.id} className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
              <div className="mb-6">
                <img src={getServiceImage(service.title)} alt={service.title} className="w-full h-48 object-cover rounded-lg mb-4" />
                <div className="flex justify-center">{getServiceIcon(service.icon)}</div>
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">{service.title}</h2>
              <p className="text-gray-600 mb-6 text-lg">{service.description}</p>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Key Features:</h3>
                <ul className="space-y-2">
                  {service.features?.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-gray-700">
                      <CheckCircle className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;



