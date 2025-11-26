#!/usr/bin/env python3
"""
Generate detailed HTML report from k6 test results
"""
import json
import os
from pathlib import Path
from datetime import datetime

def load_summary(file_path):
    """Load k6 summary JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return None

def format_duration(ms):
    """Format milliseconds to human readable"""
    if ms < 1000:
        return f"{ms:.2f}ms"
    return f"{ms/1000:.2f}s"

def format_bytes(bytes_val):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f}TB"

def get_metric_value(metrics, metric_name, stat='avg'):
    """Extract metric value safely"""
    try:
        if metric_name in metrics:
            if 'values' in metrics[metric_name]:
                return metrics[metric_name]['values'].get(stat, 0)
            return metrics[metric_name].get(stat, 0)
        return 0
    except:
        return 0

def generate_test_card(test_name, summary, file_name):
    """Generate HTML for a single test card"""
    if not summary:
        return f"""
        <div class="test-card error">
            <div class="test-header">
                <h3>{test_name}</h3>
                <span class="status-badge error">❌ Error</span>
            </div>
            <p class="test-description">Test failed to complete or parse results</p>
        </div>
        """
    
    metrics = summary.get('metrics', {})
    
    # Extract key metrics
    http_reqs = get_metric_value(metrics, 'http_reqs', 'count')
    http_req_duration_avg = get_metric_value(metrics, 'http_req_duration', 'avg')
    http_req_duration_p95 = get_metric_value(metrics, 'http_req_duration', 'p(95)')
    http_req_failed = get_metric_value(metrics, 'http_req_failed', 'rate')
    iterations = get_metric_value(metrics, 'iterations', 'count')
    vus_max = get_metric_value(metrics, 'vus_max', 'max')
    
    # Determine status
    status = "success"
    status_text = "✓ Passed"
    if http_req_failed > 0.05:  # More than 5% errors
        status = "warning"
        status_text = "⚠ Warning"
    
    return f"""
    <div class="test-card {status}">
        <div class="test-header">
            <h3>{test_name}</h3>
            <span class="status-badge {status}">{status_text}</span>
        </div>
        <div class="test-metrics">
            <div class="metric">
                <span class="metric-label">Requests</span>
                <span class="metric-value">{int(http_reqs)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Avg Duration</span>
                <span class="metric-value">{format_duration(http_req_duration_avg)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">P95 Duration</span>
                <span class="metric-value">{format_duration(http_req_duration_p95)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Error Rate</span>
                <span class="metric-value">{http_req_failed*100:.2f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Iterations</span>
                <span class="metric-value">{int(iterations)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Max VUs</span>
                <span class="metric-value">{int(vus_max)}</span>
            </div>
        </div>
        <a href="details.html?test={file_name}" class="details-link">View Details →</a>
    </div>
    """

def generate_html_report():
    """Generate complete HTML report"""
    results_dir = Path('test-results')
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Load all test summaries
    tests = []
    test_files = {
        '01-hello-world-summary.json': '01. Hello World',
        '02-http-requests-summary.json': '02. HTTP Requests',
        '03-checks-summary.json': '03. Checks & Validations',
        '04-thresholds-summary.json': '04. Thresholds',
        '05-stages-summary.json': '05. Load Stages',
        'api-load-test-summary.json': 'API Load Test',
        'spike-test-summary.json': 'Spike Test',
    }
    
    total_requests = 0
    total_errors = 0
    test_cards_html = ""
    
    for file_name, test_name in test_files.items():
        summary = load_summary(results_dir / file_name)
        tests.append({'name': test_name, 'summary': summary, 'file': file_name})
        test_cards_html += generate_test_card(test_name, summary, file_name.replace('-summary.json', ''))
        
        if summary:
            metrics = summary.get('metrics', {})
            total_requests += get_metric_value(metrics, 'http_reqs', 'count')
            failed_rate = get_metric_value(metrics, 'http_req_failed', 'rate')
            reqs = get_metric_value(metrics, 'http_reqs', 'count')
            total_errors += int(failed_rate * reqs)
    
    success_rate = ((total_requests - total_errors) / total_requests * 100) if total_requests > 0 else 0
    
    # Generate main HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K6 Performance Test Results</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .timestamp {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            margin-top: 20px;
            display: inline-block;
        }}
        .stats-overview {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .content {{
            padding: 40px;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 25px;
            font-weight: 600;
        }}
        .test-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        .test-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
        }}
        .test-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .test-card.success {{
            border-color: #10b981;
        }}
        .test-card.warning {{
            border-color: #f59e0b;
        }}
        .test-card.error {{
            border-color: #ef4444;
        }}
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .test-header h3 {{
            font-size: 1.3em;
            color: #333;
        }}
        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .status-badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        .status-badge.warning {{
            background: #fef3c7;
            color: #92400e;
        }}
        .status-badge.error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .test-metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 15px;
        }}
        .metric {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .metric-label {{
            display: block;
            font-size: 0.75em;
            color: #666;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        .metric-value {{
            display: block;
            font-size: 1.3em;
            font-weight: 700;
            color: #333;
        }}
        .details-link {{
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        .details-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 K6 Performance Test Results</h1>
            <p class="subtitle">Automated performance testing with Grafana k6</p>
            <div class="timestamp">
                <strong>Last Run:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
            </div>
        </div>
        
        <div class="stats-overview">
            <div class="stat-card">
                <div class="stat-value">{len(tests)}</div>
                <div class="stat-label">Tests Executed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{int(total_requests):,}</div>
                <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{success_rate:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_errors}</div>
                <div class="stat-label">Failed Requests</div>
            </div>
        </div>

        <div class="content">
            <h2 class="section-title">📊 Test Results</h2>
            <div class="test-grid">
                {test_cards_html}
            </div>
        </div>

        <div class="footer">
            <p>Generated by GitHub Actions | Powered by Grafana k6</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/JBxrajas/k6-performance-tests" target="_blank">
                    View Repository →
                </a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(docs_dir / 'index.html', 'w') as f:
        f.write(html_content)
    
    print(f"✓ Generated report: {docs_dir / 'index.html'}")
    print(f"  Total tests: {len(tests)}")
    print(f"  Total requests: {int(total_requests):,}")
    print(f"  Success rate: {success_rate:.1f}%")

if __name__ == '__main__':
    generate_html_report()
