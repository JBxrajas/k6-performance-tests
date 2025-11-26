import http from 'k6/http';
import { sleep } from 'k6';

// Thresholds define pass/fail criteria for your test
// If thresholds are not met, k6 will exit with a non-zero exit code
export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    // 95% of requests must complete within 500ms
    http_req_duration: ['p(95)<500'],
    
    // Less than 1% of requests should fail
    'http_req_failed': ['rate<0.01'],
    
    // Average response time should be below 300ms
    'http_req_duration': ['avg<300'],
    
    // At least 8 requests per second (realistic with 10 VUs and 1s sleep)
    'http_reqs': ['rate>8'],
  },
};

export default function () {
  http.get('https://test.k6.io');
  
}

// Thresholds will be evaluated at the end of the test
// If any threshold fails, the test is considered failed
//
// Run with: k6 run 04-thresholds.js
