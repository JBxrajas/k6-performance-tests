import http from 'k6/http';
import { check, sleep } from 'k6';

// Spike test: sudden increase in load to test system resilience
export const options = {
  stages: [
    { duration: '10s', target: 5 },    // Start with 5 users
    { duration: '10s', target: 5 },    // Stay at 5 users
    { duration: '10s', target: 100 },  // SPIKE to 100 users
    { duration: '30s', target: 100 },  // Stay at 100 users
    { duration: '10s', target: 5 },    // Drop back to 5 users
    { duration: '10s', target: 5 },    // Recover at 5 users
    { duration: '10s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% under 2s even during spike
    http_req_failed: ['rate<0.1'],     // Less than 10% errors
  },
};

export default function () {
  const response = http.get('https://test.k6.io');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time acceptable': (r) => r.timings.duration < 3000,
  });
  
  sleep(1);
}

// Spike tests verify that:
// - The system can handle sudden traffic increases
// - Performance degrades gracefully
// - System recovers after the spike
//
// Run with: k6 run scenarios/spike-test.js
