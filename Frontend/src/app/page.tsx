"use client";
import type { NextPage } from 'next';
import { useState } from 'react';
import Navbar from '../components/NavBar';
import FileUpload from '../components/FileUpload';
import TariffConfig from '../components/TariffConfig';
import ModelSelector from '../components/ModelSelector';
import Visualization from '../components/Visualization';

const Home: NextPage = () => {
  const [refetchTrigger, setRefetchTrigger] = useState(0);

  const handleRefetch = () => {
    setRefetchTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center">
        <h1 className="text-2xl font-bold">Household Tariff Analysis</h1>
      </header>
      <div className="flex">
        <Navbar />
        <main className="flex-1 p-6">
          <FileUpload onUploadSuccess={handleRefetch} />
          <TariffConfig onConfigUpdate={handleRefetch} />
          <ModelSelector onCalculateSuccess={handleRefetch} />
          <Visualization refetch={handleRefetch} key={refetchTrigger} />
        </main>
      </div>
    </div>
  );
};

export default Home;