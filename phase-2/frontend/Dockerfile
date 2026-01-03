# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=production

# Set work directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install --only=production

# Copy project files
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]