const fs = require('fs');
const path = require('path');

// Create .env file if it doesn't exist
const envPath = path.join(__dirname, '..', '.env');
if (!fs.existsSync(envPath)) {
  const envContent = `
FAST_REFRESH=false
GENERATE_SOURCEMAP=false
NODE_OPTIONS=--openssl-legacy-provider
`;
  fs.writeFileSync(envPath, envContent.trim());
}

// Set environment variable
process.env.NODE_OPTIONS = '--openssl-legacy-provider';