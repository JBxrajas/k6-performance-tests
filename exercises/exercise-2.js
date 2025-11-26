import http from 'k6/http';
import { check, sleep, group } from 'k6';

/**
 * EXERCISE 2: User Journey Test
 * 
 * GOAL: Simulate a realistic user journey through an API
 * 
 * SCENARIO:
 * A user performs the following actions:
 * 1. Fetches a list of users
 * 2. Selects a random user
 * 3. Fetches that user's posts
 * 4. Reads a random post from that user
 * 5. Fetches comments for that post
 * 
 * TASKS:
 * 1. Configure stages:
 *    - Ramp up to 5 VUs over 10s
 *    - Stay at 5 VUs for 30s
 *    - Ramp down to 0 over 10s
 * 
 * 2. Implement the user journey using the JSONPlaceholder API:
 *    - GET /users (fetch all users)
 *    - GET /users/{userId}/posts (fetch user's posts)
 *    - GET /posts/{postId} (fetch specific post)
 *    - GET /posts/{postId}/comments (fetch post comments)
 * 
 * 3. Use groups to organize the workflow
 * 4. Add appropriate checks for each request
 * 5. Add realistic sleep times between requests (1-3 seconds)
 * 
 * HINTS:
 * - Base URL: https://jsonplaceholder.typicode.com
 * - Use Math.floor(Math.random() * array.length) to pick random items
 * - Use group() to organize related requests
 * - Check that arrays have length > 0
 */

export const options = {
  stages: [
    // TODO: Add your stages configuration
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    'group_duration{group:::User List}': ['avg<500'],
    'group_duration{group:::User Posts}': ['avg<800'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  
  // TODO: Implement Step 1 - Fetch users list
  group('User List', function () {
    
  });
  
  sleep(1);
  
  // TODO: Implement Step 2 & 3 - Fetch user's posts and select one
  group('User Posts', function () {
    
  });
  
  sleep(2);
  
  // TODO: Implement Step 4 & 5 - Fetch post and its comments
  group('Post Details', function () {
    
  });
  
  sleep(1);
}

// Run your solution with: k6 run exercises/exercise-2.js
//
// SUCCESS CRITERIA:
// - All groups execute successfully
// - Random selection works (different users/posts each iteration)
// - All checks pass
// - Realistic timing between requests
