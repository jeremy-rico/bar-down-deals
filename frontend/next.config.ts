import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'bar-down-deals-bucket.s3.us-west-1.amazonaws.com',
        //port: '',
        pathname: '/images/**',
        //search: '',
      },
    ],
  },
};

export default nextConfig;
