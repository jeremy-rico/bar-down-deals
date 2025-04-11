## Description

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

It comprises the frontend of bardowndeals.com. Most of the routes can be found
in the src/app/deals.

## Deployment

This app is deployed using AWS Amplify. It is serverless and deploys
automatically when changes are detected on the main branch inside /frontend.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Getting images from s3

Your s3 bucket is set to private by default. To make the bucket public:

1. AWS Console
2. Go to your bucker > Permissions
3. Scroll to Block Public access > disable
4. Add the following policy under Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bar-down-deals-bucket/images/full/*.jpg"
    }
  ]
}
```

This ensures only puublic access for read and not other CORS methods (PUT,
UPDATE, DELETE)
