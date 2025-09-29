import type { NextPage } from 'next';
import Layout from '../components/Layout';
import FileUpload from '../components/FileUpload';
import TariffInputs from '../components/TariffInputs';
import ModelSelector from '../components/ModelSelector';
import Visualization from '../components/Visualization';

const Home: NextPage = () => {
  return (
    <Layout>
      <FileUpload />
      <TariffInputs />
      <ModelSelector />
      <Visualization />
    </Layout>
  );
};

export default Home;