import React, { useState, useEffect } from 'react';
import { Car, Building, CheckCircle } from 'lucide-react';
import { industriesAPI } from '../services/api';

const Industries = () => {
  const [industries, setIndustries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
    fetchIndustries();
  }, []);

  const getIcon = (iconName) => {
    const icons = { car: Car, building: Building };
    const Icon = icons[iconName] || Building;
    return <Icon className="h-16 w-16 text-blue-600" />;
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
          <h1 className="text-5xl font-bold text-gray-900 mb-6">Industries We Serve</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Providing high-quality plastic components across diverse sectors
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          {industries.map((industry) => (
            <div key={industry.id} className="bg-white p-8 rounded-lg shadow-lg">
              <div className="mb-6 flex justify-center">{getIcon(industry.icon)}</div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4 text-center">{industry.title}</h2>
              <p className="text-gray-600 mb-6 text-lg text-center">{industry.description}</p>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Key Clients:</h3>
                <ul className="space-y-2">
                  {industry.clients?.map((client, idx) => (
                    <li key={idx} className="flex items-center text-gray-700">
                      <CheckCircle className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0" />
                      {client}
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

export default Industries;



