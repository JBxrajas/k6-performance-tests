import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '20s',
};

export default function () {
  const response = http.get('https://test.k6.io');
  
  // Checks are used to verify that the response meets expectations
  // They don't stop the test if they fail, but are reported in the results
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body contains text': (r) => r.body.includes('Collection of simple web-pages'),
    'content-type is HTML': (r) => r.headers['Content-Type'].includes('text/html'),
  });
  
  sleep(1);
}

// After running, you'll see check success rate in the output:
// ✓ status is 200
// ✓ response time < 500ms
// ✓ body contains text
// ✓ content-type is HTML
//
// Run with: k6 run 03-checks.js
