import http from 'k6/http';
import { sleep } from 'k6';

// This is the simplest k6 test
// It makes a single HTTP request to test.k6.io

export const options = {

    stages: [
        { duration: '5s', target: 5 }, // Ramp up to 5 VUs over 10 seconds
        { duration: '10s', target: 5 }, // Stay at 5 VUs for 20 seconds
        { duration: '5s', target: 0 }, // Ramp down to 0 VUs over 10 seconds
    ],
};  
export default function () {
  // Make an HTTP GET request
  http.get('https://test.k6.io');
  
  // Wait 1 second between iterations
  sleep(1);
}

