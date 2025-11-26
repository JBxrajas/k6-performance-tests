import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend } from 'k6/metrics';

/**
 * EXERCISE 3: Advanced Metrics & Custom Checks
 * 
 * GOAL: Create a comprehensive test with custom metrics and sophisticated checks
 * 
 * SCENARIO:
 * Test a REST API with POST requests and track custom business metrics
 * 
 * TASKS:
 * 1. Configure the test with:
 *    - 15 VUs for 1 minute
 *    - Custom thresholds for your metrics
 * 
 * 2. Implement these custom metrics:
 *    - Counter: Track successful posts created
 *    - Counter: Track failed validations
 *    - Trend: Track post payload size
 * 
 * 3. Create POST requests to: https://jsonplaceholder.typicode.com/posts
 *    With payload:
 *    {
 *      title: 'Performance Test Post [random number]',
 *      body: 'This is a test post body with [random] content',
 *      userId: [random 1-10]
 *    }
 * 
 * 4. Add comprehensive checks:
 *    - Status is 201 (Created)
 *    - Response contains an 'id' field
 *    - Response time < 800ms
 *    - Response body matches request data
 * 
 * 5. Add error handling:
 *    - Check for non-200/201 responses
 *    - Validate response structure
 *    - Track errors with custom metrics
 * 
 * BONUS CHALLENGES:
 * - Add tags to requests for better filtering
 * - Implement retry logic for failed requests
 * - Add response body size validation
 * 
 * HINTS:
 * - Create metrics outside the default function
 * - Use metrics.add() to record values
 * - JSON.stringify() to prepare payload
 * - Use params object for headers
 */

// TODO: Create custom metrics
const successfulPosts = new Counter('successful_posts');
// Add more metrics...

export const options = {
  // TODO: Add configuration
  vus: 15,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    // TODO: Add thresholds for custom metrics
    // 'successful_posts': ['count>100'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  
  // TODO: Create random payload
  const payload = {
    // Add your payload here
  };
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: {
      // TODO: Add custom tags
    },
  };
  
  // TODO: Make POST request
  
  // TODO: Add comprehensive checks
  
  // TODO: Update custom metrics
  
  // TODO: Add error handling
  
  sleep(1);
}

// Run your solution with: k6 run exercises/exercise-3.js
//
// SUCCESS CRITERIA:
// - Custom metrics are tracked correctly
// - All checks pass with >95% success rate
// - Error handling works properly
// - Thresholds are met
// - At least 100 successful posts created
