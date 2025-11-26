import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metric to track error rate
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up to 20 users
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000', 'p(99)<2000'],
    http_req_failed: ['rate<0.05'], // Less than 5% errors
    errors: ['rate<0.1'], // Less than 10% custom errors
  },
};

// Sample API endpoints
const BASE_URL = 'https://test.k6.io';

export default function () {
  // Test homepage
  let response = http.get(`${BASE_URL}/`);
  let success = check(response, {
    'homepage status is 200': (r) => r.status === 200,
    'homepage loads fast': (r) => r.timings.duration < 1000,
  });
  errorRate.add(!success);
  
  sleep(1);
  
  // Test contacts page
  response = http.get(`${BASE_URL}/contacts.php`);
  success = check(response, {
    'contacts status is 200': (r) => r.status === 200,
    'contacts has form': (r) => r.body.includes('form'),
  });
  errorRate.add(!success);
  
  sleep(1);
  
  // Submit form
  const formData = {
    name: 'Test User',
    email: 'test@example.com',
    message: 'This is a load test message',
  };
  
  response = http.post(`${BASE_URL}/contacts.php`, formData);
  success = check(response, {
    'form submission status is 200': (r) => r.status === 200,
  });
  errorRate.add(!success);
  
  sleep(2);
}

// This simulates a typical user journey through an API/website
// Run with: k6 run scenarios/api-load-test.js
