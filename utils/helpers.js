/**
 * Helper functions for k6 tests
 */

/**
 * Generate a random integer between min and max (inclusive)
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Random integer
 */
export function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Generate a random string of specified length
 * @param {number} length - Length of string
 * @returns {string} Random string
 */
export function randomString(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Pick a random element from an array
 * @param {Array} array - Array to pick from
 * @returns {*} Random element
 */
export function randomItem(array) {
  return array[Math.floor(Math.random() * array.length)];
}

/**
 * Sleep for a random duration between min and max seconds
 * @param {number} min - Minimum seconds
 * @param {number} max - Maximum seconds
 */
export function randomSleep(min, max) {
  const duration = Math.random() * (max - min) + min;
  return duration;
}

/**
 * Format bytes to human readable format
 * @param {number} bytes - Number of bytes
 * @returns {string} Formatted string
 */
export function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Create a summary of response metrics
 * @param {Response} response - k6 HTTP response object
 * @returns {Object} Summary object
 */
export function responseSummary(response) {
  return {
    status: response.status,
    duration: Math.round(response.timings.duration),
    size: formatBytes(response.body.length),
    blocked: Math.round(response.timings.blocked),
    connecting: Math.round(response.timings.connecting),
    sending: Math.round(response.timings.sending),
    waiting: Math.round(response.timings.waiting),
    receiving: Math.round(response.timings.receiving),
  };
}

/**
 * Generate realistic user data
 * @returns {Object} User object
 */
export function generateUser() {
  const firstNames = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Davis'];
  
  return {
    firstName: randomItem(firstNames),
    lastName: randomItem(lastNames),
    email: `${randomString(8)}@example.com`,
    age: randomInt(18, 65),
  };
}

/**
 * Validate JSON response structure
 * @param {Response} response - k6 HTTP response object
 * @param {Array} requiredFields - Array of required field names
 * @returns {boolean} True if all fields exist
 */
export function validateJsonStructure(response, requiredFields) {
  try {
    const data = JSON.parse(response.body);
    return requiredFields.every(field => data.hasOwnProperty(field));
  } catch (e) {
    return false;
  }
}
