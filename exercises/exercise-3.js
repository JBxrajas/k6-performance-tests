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
const failedValidations = new Counter('failed_validations');
const payloadSizeTrend = new Trend('payload_size');
const responseSizeTrend = new Trend('response_size');
const responseTimeTrend = new Trend('response_time');
const errorCount = new Counter('error_count');
const validationErrorCount = new Counter('validation_error_count');
// Add more metrics...

export const options = {
  // TODO: Add configuration
  vus: 15,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    // TODO: Add thresholds for custom metrics
    'successful_posts': ['count>100'],
    'failed_validations': ['count<10'],
    'error_count': ['count<20'],
    'validation_error_count': ['count<15'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  
  // TODO: Create random payload
  const payload = {
    title: `Performance Test Post ${Math.floor(Math.random() * 1000)}`,
    body: `This is a test post body with random content ${Math.random()}`,
    userId: Math.floor(Math.random() * 10) + 1, 
  };
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: {
        endpoint: 'create_post',    
        method: 'POST',
        payload_size: JSON.stringify(payload).length,
        response_size: 0, // Placeholder, will update after response
        response_time: 0, // Placeholder, will update after response
    },
  };
  
  // TODO: Make POST request
    const startTime = new Date().getTime();
    const response = http.post(`${BASE_URL}/posts`, JSON.stringify(payload), params);
    const endTime = new Date().getTime();
    const responseTime = endTime - startTime;
    params.tags.response_time = responseTime;
    params.tags.response_size = response.body.length;
  
  // TODO: Add comprehensive checks
    const success = check(response, {
        'status is 201': (r) => r.status === 201,
        'response contains id field': (r) => r.json().hasOwnProperty('id'),
        'response time < 800ms': (r) => r.timings.duration < 800,
        'response body matches request data': (r) => {
            const responseData = r.json();  
            return responseData.title === payload.title &&
                   responseData.body === payload.body &&
                   responseData.userId === payload.userId;
        }
    });
  
  // TODO: Update custom metrics
    if (success) {
        successfulPosts.add(1);
    } else {
        failedValidations.add(1);
    }   
  // TODO: Add error handling
    if (response.status !== 201) {
        errorCount.add(1);
    }               
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
