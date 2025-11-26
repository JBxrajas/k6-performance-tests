import http from 'k6/http';
import { sleep } from 'k6';

// Configure the test to run with 10 VUs for 30 seconds
export const options = {
  vus: 60,
  duration: '60s',
};

export default function () {
  // GET request
  const getResponse = http.get('https://test.k6.io');
  console.log(`GET Status: ${getResponse.status}`);
  
  // POST request with JSON payload
  const payload = JSON.stringify({
    name: 'k6 user',
    email: 'user@example.com',
  });
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const postResponse = http.post('https://test.k6.io/post', payload, params);
  console.log(`POST Status: ${postResponse.status}`);
  
  sleep(1);
}

// Run this test with:
// k6 run 02-http-requests.js
