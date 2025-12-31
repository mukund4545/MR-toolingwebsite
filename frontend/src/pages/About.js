import React, { useState, useEffect } from 'react';
import { Award, Target, Users } from 'lucide-react';
import { contentAPI } from '../services/api';
import logo from '../assets/logo.jpeg';

const About = () => {
  const [aboutContent, setAboutContent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await contentAPI.getByType('about_content');
        setAboutContent(res.data.content_data);
      } catch (error) {
        console.error('Error fetching about content:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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

  const values = [
    { icon: Award, title: 'Quality Excellence', desc: 'ISO 9001:2015 certified processes' },
    { icon: Target, title: 'Customer Focus', desc: 'Committed to exceeding expectations' },
    { icon: Users, title: 'Expert Team', desc: 'Skilled professionals with years of experience' },
  ];

  return (
    <div className="py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="mb-8">
            <img src={logo} alt="MR Tooling Industries Logo" className="h-24 w-auto mx-auto" />
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-6">About MR Tooling Industries</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {aboutContent?.description || 'Leading plastic injection molding workshop in Maharashtra, India.'}
          </p>
        </div>

        {/* Mission & Vision */}
        <div className="grid md:grid-cols-2 gap-12 mb-20">
          <div className="bg-blue-50 p-8 rounded-lg">
            <Target className="h-12 w-12 text-blue-600 mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-gray-700 text-lg">
              {aboutContent?.mission || 'To deliver world-class plastic injection molding solutions.'}
            </p>
          </div>
          <div className="bg-gray-50 p-8 rounded-lg">
            <Award className="h-12 w-12 text-blue-600 mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Vision</h2>
            <p className="text-gray-700 text-lg">
              {aboutContent?.vision || 'To be the most trusted partner in plastic component manufacturing.'}
            </p>
          </div>
        </div>

        {/* Core Values */}
        <div className="mb-20">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-12">Core Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {values.map((value, idx) => (
              <div key={idx} className="text-center">
                <value.icon className="h-16 w-16 text-blue-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{value.title}</h3>
                <p className="text-gray-600">{value.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Experience */}
        {aboutContent?.experience && (
          <div className="bg-blue-600 text-white p-12 rounded-lg text-center">
            <h2 className="text-4xl font-bold mb-4">{aboutContent.experience} Years of Excellence</h2>
            <p className="text-xl text-blue-100">
              Delivering quality plastic components for automotive and industrial sectors
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default About;



