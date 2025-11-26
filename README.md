# Grafana k6 Performance Testing Exercise

Welcome to the k6 performance testing exercise! This project is designed to help you learn and practice performance testing with Grafana k6.

## 📚 What is k6?

k6 is a modern, developer-friendly load testing tool built for testing the performance and reliability of APIs, microservices, and websites. It's written in Go and uses JavaScript for scripting tests.

## 🎯 Learning Objectives

By completing these exercises, you will learn to:
- Write basic load tests with k6
- Use checks and thresholds to validate performance
- Configure different load patterns (constant, ramping, spike)
- Work with virtual users (VUs) and iterations
- Analyze test results and metrics
- Integrate custom metrics and tags

## 🚀 Prerequisites

1. **Install k6**: 
   - Windows: `choco install k6` or `winget install k6`
   - macOS: `brew install k6`
   - Linux: See [k6 installation docs](https://k6.io/docs/get-started/installation/)

2. **Verify installation**:
   ```bash
   k6 version
   ```

## 📁 Project Structure

```
k6-performance/
├── examples/           # Basic examples to learn from
│   ├── 01-hello-world.js
│   ├── 02-http-requests.js
│   ├── 03-checks.js
│   ├── 04-thresholds.js
│   └── 05-stages.js
├── scenarios/          # Real-world test scenarios
│   ├── api-load-test.js
│   ├── spike-test.js
│   └── stress-test.js
├── exercises/          # Hands-on challenges
│   ├── exercise-1.js
│   ├── exercise-2.js
│   └── exercise-3.js
└── utils/              # Helper functions
    └── helpers.js
```

## 🏃 Running Tests

### Run a basic test:
```bash
k6 run examples/01-hello-world.js
```

### Run with custom VUs and duration:
```bash
k6 run --vus 10 --duration 30s examples/02-http-requests.js
```

### Run with output to JSON:
```bash
k6 run --out json=results.json examples/03-checks.js
```

## 📊 Understanding k6 Metrics

k6 provides several built-in metrics:
- **http_req_duration**: Total time for the request
- **http_req_waiting**: Time waiting for response (TTFB)
- **http_req_blocked**: Time spent blocked before initiating request
- **http_reqs**: Total HTTP requests
- **vus**: Current number of active virtual users
- **iterations**: Total iterations completed

## 🎓 Exercise Path

1. **Start with Examples**: Go through `examples/` to understand k6 basics
2. **Study Scenarios**: Review `scenarios/` for real-world patterns
3. **Complete Exercises**: Work through `exercises/` to test your knowledge

##  Tips

- Start with low VU counts and gradually increase
- Always use checks to validate responses
- Set thresholds to define success criteria
- Use meaningful tags for better metrics organization
- Comment your tests for clarity

##  Resources

- [k6 Official Documentation](https://k6.io/docs/)
- [k6 Examples](https://k6.io/docs/examples/)
- [k6 Community Forum](https://community.k6.io/)

##  Contributing

Feel free to add more examples, scenarios, or exercises to this project!

Happy load testing! 🚀
