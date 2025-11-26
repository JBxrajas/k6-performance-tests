# Exercise Solutions

This directory contains solution files for the exercises. Try to complete the exercises on your own before looking at the solutions!

## Exercise 1 Solution

<details>
<summary>Click to reveal solution</summary>

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<600'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const response = http.get('https://jsonplaceholder.typicode.com/posts/1');
  
  const data = JSON.parse(response.body);
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body contains "sunt"': (r) => r.body.includes('sunt'),
    'has userId property': () => data.hasOwnProperty('userId'),
  });
  
  sleep(1);
}
```

</details>

## Exercise 2 Solution

<details>
<summary>Click to reveal solution</summary>

```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '30s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    'group_duration{group:::User List}': ['avg<500'],
    'group_duration{group:::User Posts}': ['avg<800'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  let userId, postId;
  
  group('User List', function () {
    const response = http.get(`${BASE_URL}/users`);
    check(response, {
      'users fetched': (r) => r.status === 200,
      'has users': (r) => JSON.parse(r.body).length > 0,
    });
    
    const users = JSON.parse(response.body);
    userId = users[Math.floor(Math.random() * users.length)].id;
  });
  
  sleep(1);
  
  group('User Posts', function () {
    const response = http.get(`${BASE_URL}/users/${userId}/posts`);
    check(response, {
      'posts fetched': (r) => r.status === 200,
      'has posts': (r) => JSON.parse(r.body).length > 0,
    });
    
    const posts = JSON.parse(response.body);
    postId = posts[Math.floor(Math.random() * posts.length)].id;
  });
  
  sleep(2);
  
  group('Post Details', function () {
    let response = http.get(`${BASE_URL}/posts/${postId}`);
    check(response, {
      'post fetched': (r) => r.status === 200,
    });
    
    response = http.get(`${BASE_URL}/posts/${postId}/comments`);
    check(response, {
      'comments fetched': (r) => r.status === 200,
      'has comments': (r) => JSON.parse(r.body).length > 0,
    });
  });
  
  sleep(1);
}
```

</details>

## Exercise 3 Solution

<details>
<summary>Click to reveal solution</summary>

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend } from 'k6/metrics';

const successfulPosts = new Counter('successful_posts');
const failedValidations = new Counter('failed_validations');
const payloadSize = new Trend('payload_size');

export const options = {
  vus: 15,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    successful_posts: ['count>100'],
    failed_validations: ['count<10'],
  },
};

export default function () {
  const BASE_URL = 'https://jsonplaceholder.typicode.com';
  
  const payload = JSON.stringify({
    title: `Performance Test Post ${Math.floor(Math.random() * 10000)}`,
    body: `This is a test post body with ${Math.random().toString(36).substring(7)} content`,
    userId: Math.floor(Math.random() * 10) + 1,
  });
  
  payloadSize.add(payload.length);
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: {
      test_type: 'create_post',
    },
  };
  
  const response = http.post(`${BASE_URL}/posts`, payload, params);
  
  const success = check(response, {
    'status is 201': (r) => r.status === 201,
    'has id field': (r) => {
      try {
        return JSON.parse(r.body).hasOwnProperty('id');
      } catch (e) {
        return false;
      }
    },
    'response time < 800ms': (r) => r.timings.duration < 800,
  });
  
  if (response.status === 201) {
    successfulPosts.add(1);
  } else {
    failedValidations.add(1);
  }
  
  if (!success) {
    console.error(`Failed request: status ${response.status}`);
  }
  
  sleep(1);
}
```

</details>

## Tips for Learning

1. Start with Exercise 1 and work your way up
2. Try to solve each exercise without looking at the solution
3. Run the tests and use the output to debug issues
4. Compare your solution with the provided one
5. Experiment with different configurations and thresholds
