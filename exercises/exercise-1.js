import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * EXERCISE 1: Basic Load Test
 * 
 * GOAL: Create a load test that verifies the JSONPlaceholder API
 * 
 * TASKS:
 * 1. Configure the test to run with 10 VUs for 30 seconds
 * 2. Make a GET request to: https://jsonplaceholder.typicode.com/posts/1
 * 3. Add checks to verify:
 *    - Status is 200
 *    - Response time is less than 500ms
 *    - Response body contains the word "sunt"
 *    - Response has a 'userId' property
 * 4. Add thresholds:
 *    - 95% of requests must complete within 600ms
 *    - Error rate must be less than 1%
 * 
 * HINTS:
 * - Use export const options = {} to configure the test
 * - Parse JSON with: const data = JSON.parse(response.body)
 * - Check for properties with: data.hasOwnProperty('userId')
 */

// TODO: Add your options configuration here
export const options = {
  // Add VUs, duration, and thresholds
};

export default function () {
  // TODO: Make the HTTP request
  
  // TODO: Add checks
  
  // TODO: Add sleep
}

// Run your solution with: k6 run exercises/exercise-1.js
// 
// SUCCESS CRITERIA:
// - Test runs for 30 seconds
// - All checks pass
// - Thresholds are met
