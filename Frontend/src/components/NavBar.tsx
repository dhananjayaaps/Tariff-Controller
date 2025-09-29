import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="w-64 bg-gray-800 text-white p-4">
      <ul>
        <li className="mb-2"><Link href="/" className="hover:bg-gray-700 p-2 block rounded">Home</Link></li>
        <li className="mb-2"><Link href="#upload" className="hover:bg-gray-700 p-2 block rounded">Upload Data</Link></li>
        <li className="mb-2"><Link href="#calculate" className="hover:bg-gray-700 p-2 block rounded">Calculate</Link></li>
        <li className="mb-2"><Link href="#compare" className="hover:bg-gray-700 p-2 block rounded">Compare</Link></li>
        <li className="mb-2"><Link href="#reports" className="hover:bg-gray-700 p-2 block rounded">User Reports</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;