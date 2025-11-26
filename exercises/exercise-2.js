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
    { duration: '10s', target: 5 }, // Ramp up to 5 VUs
    { duration: '30s', target: 5 }, // Stay at 5 VUs
    { duration: '10s', target: 0 }, // Ramp down to 0 VUs   
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    'group_duration{group:::User List}': ['avg<500'],
    'group_duration{group:::User Posts}': ['avg<800'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  let randomUser, randomPost;
  
  // Step 1 - Fetch users list
  group('User List', function () {
    const response = http.get(`${BASE_URL}/users`);
    const users = response.json();
    check(response, {
      'status is 200': (r) => r.status === 200,
      'users list is not empty': () => users.length > 0,
    });
    
    // Select a random user for the next step
    randomUser = users[Math.floor(Math.random() * users.length)];
  });
  
  sleep(Math.floor(Math.random() * 3) + 1);
  
  // Step 2 & 3 - Fetch user's posts and select one
  group('User Posts', function () {
    const postsResponse = http.get(`${BASE_URL}/users/${randomUser.id}/posts`);
    const posts = postsResponse.json();
    check(postsResponse, {
      'posts status is 200': (r) => r.status === 200,
      'posts list is not empty': () => posts.length > 0,
    });
    
    // Select a random post from this user
    randomPost = posts[Math.floor(Math.random() * posts.length)];
  });
  
  sleep(Math.floor(Math.random() * 3) + 1);
  
  // Step 4 & 5 - Fetch post and its comments
  group('Post Details', function () {
    const postResponse = http.get(`${BASE_URL}/posts/${randomPost.id}`);
    const post = postResponse.json();
    check(postResponse, {
      'post status is 200': (r) => r.status === 200,
      'post id matches': () => post.id === randomPost.id,
    });
    
    const commentsResponse = http.get(`${BASE_URL}/posts/${randomPost.id}/comments`);
    const comments = commentsResponse.json();
    check(commentsResponse, {
      'comments status is 200': (r) => r.status === 200,
      'comments list is not empty': () => comments.length > 0,
    }); 
  });
  
  sleep(Math.floor(Math.random() * 3) + 1);
}

// Run your solution with: k6 run exercises/exercise-2.js
//
// SUCCESS CRITERIA:
// - All groups execute successfully
// - Random selection works (different users/posts each iteration)
// - All checks pass
// - Realistic timing between requests
