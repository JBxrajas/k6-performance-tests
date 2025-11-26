import http from 'k6/http';
import { sleep } from 'k6';

// Stages allow you to ramp VUs up and down over time
// This creates more realistic load patterns
export const options = {
  stages: [
    { duration: '10s', target: 5 },   // Ramp up to 5 VUs over 10 seconds
    { duration: '20s', target: 5 },   // Stay at 5 VUs for 20 seconds
    { duration: '10s', target: 10 },  // Ramp up to 10 VUs over 10 seconds
    { duration: '20s', target: 10 },  // Stay at 10 VUs for 20 seconds
    { duration: '10s', target: 0 },   // Ramp down to 0 VUs over 10 seconds
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  http.get('https://test.k6.io');
  sleep(1);
}

// This test simulates gradually increasing load
// Useful for finding breaking points and capacity limits
//
// Run with: k6 run 05-stages.js
