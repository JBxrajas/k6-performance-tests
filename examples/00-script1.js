import http from 'k6/http';

export default function () {
  // Make an HTTP GET request
  http.get('https://test.k6.io');
}