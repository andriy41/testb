// src/components/IconTest.tsx

import React from 'react';
import { FaWallet } from 'react-icons/fa'; // Using Font Awesome's Wallet icon

const IconTest: React.FC = () => {
  return (
    <div>
      <FaWallet className="w-6 h-6" />
    </div>
  );
};

export default IconTest;

