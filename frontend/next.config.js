/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  webpack: (config) => {
    // Disable filesystem cache to avoid disk-space issues in dev
    config.cache = false;
    return config;
  },
};

module.exports = nextConfig;
