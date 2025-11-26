import http from 'k6/http';
import { check, sleep } from 'k6';

// Stress test: gradually increase load beyond normal capacity
// to find the breaking point
export const options = {
  stages: [
    { duration: '1m', target: 10 },   // Warm up
    { duration: '2m', target: 20 },   // Moderate load
    { duration: '2m', target: 50 },   // Heavy load
    { duration: '2m', target: 100 },  // Stress load
    { duration: '2m', target: 150 },  // Extreme load
    { duration: '2m', target: 200 },  // Breaking point
    { duration: '2m', target: 0 },    // Recovery
  ],
  thresholds: {
    // More lenient thresholds since we expect degradation
    http_req_duration: ['p(95)<5000'],
    http_req_failed: ['rate<0.3'], // Up to 30% errors acceptable
  },
};

export default function () {
  const response = http.get('https://test.k6.io');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
  
  // Vary sleep time to simulate different user behaviors
  sleep(Math.random() * 3 + 1); // 1-4 seconds
}

// Stress tests help identify:
// - Maximum capacity of the system
// - How the system fails under extreme load
// - When and how performance degrades
// - Recovery behavior after stress
//
// Run with: k6 run scenarios/stress-test.js
// Note: This test takes ~13 minutes to complete
