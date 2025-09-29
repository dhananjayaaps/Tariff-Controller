import type { NextPage } from 'next';
import Navbar from '../components/NavBar';
import FileUpload from '../components/FileUpload';
import TariffInputs from '../components/TariffInputs';
import ModelSelector from '../components/ModelSelector';
import Visualization from '../components/Visualization';

const Home: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center">
        <h1 className="text-2xl font-bold">Household Tariff Analysis</h1>
      </header>
      <div className="flex">
        <Navbar />
        <main className="flex-1 p-6">
          <FileUpload />
          <TariffInputs />
          <ModelSelector />
          <Visualization />
        </main>
      </div>
    </div>
  );
};

export default Home;