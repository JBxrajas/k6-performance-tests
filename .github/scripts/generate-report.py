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
            data = json.load(f)
            # Debug: print first level keys to understand structure
            if data and 'metrics' in data:
                print(f"  📊 Loaded {file_path.name} with {len(data['metrics'])} metrics")
            return data
    except Exception as e:
        print(f"  ❌ Error loading {file_path}: {e}")
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

def generate_test_card(test_name, summary, file_name, error_msg=None):
    """Generate HTML for a single test card"""
    if not summary:
        error_text = error_msg if error_msg else "Test failed to complete or parse results"
        return f"""
        <div class="test-card error">
            <div class="test-header">
                <h3>{test_name}</h3>
                <span class="status-badge error">❌ Error</span>
            </div>
            <p class="test-description">{error_text}</p>
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
    
    # Create a safe filename for the detail page
    detail_page = file_name.replace('-summary.json', '') + '.html'
    
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
        <a href="{detail_page}" class="details-link">View Details →</a>
    </div>
    """

def generate_detail_page(test_name, summary, file_name, docs_dir):
    """Generate detailed HTML page for a single test"""
    if not summary:
        return
    
    metrics = summary.get('metrics', {})
    
    # Helper to safely extract metric values
    def get_metric_dict(metric_name):
        """Extract metric values whether they're in 'values' dict or direct"""
        if metric_name not in metrics:
            return {}
        metric_data = metrics[metric_name]
        if isinstance(metric_data, dict):
            return metric_data.get('values', metric_data)
        return {}
    
    # Extract all available metrics
    http_req_duration = get_metric_dict('http_req_duration')
    http_req_waiting = get_metric_dict('http_req_waiting')
    http_req_connecting = get_metric_dict('http_req_connecting')
    http_req_blocked = get_metric_dict('http_req_blocked')
    http_req_sending = get_metric_dict('http_req_sending')
    http_req_receiving = get_metric_dict('http_req_receiving')
    iteration_duration = get_metric_dict('iteration_duration')
    
    # Extract count/rate metrics
    http_reqs = get_metric_value(metrics, 'http_reqs', 'count')
    http_req_failed = get_metric_value(metrics, 'http_req_failed', 'rate')
    iterations = get_metric_value(metrics, 'iterations', 'count')
    vus = get_metric_value(metrics, 'vus', 'value')
    vus_max = get_metric_value(metrics, 'vus_max', 'max')
    data_received = get_metric_value(metrics, 'data_received', 'count')
    data_sent = get_metric_value(metrics, 'data_sent', 'count')
    
    # Build metrics table
    metrics_rows = ""
    
    # Helper function to add metric row
    def add_metric_row(name, values):
        if values and any(values.values()):  # Check if dict has any non-zero values
            return f"""
        <tr>
            <td><strong>{name}</strong></td>
            <td>{format_duration(values.get('avg', 0))}</td>
            <td>{format_duration(values.get('min', 0))}</td>
            <td>{format_duration(values.get('med', 0))}</td>
            <td>{format_duration(values.get('max', 0))}</td>
            <td>{format_duration(values.get('p(90)', 0))}</td>
            <td>{format_duration(values.get('p(95)', 0))}</td>
        </tr>
        """
        return ""
    
    # Add all available metrics
    metrics_rows += add_metric_row('http_req_duration', http_req_duration)
    metrics_rows += add_metric_row('http_req_blocked', http_req_blocked)
    metrics_rows += add_metric_row('http_req_connecting', http_req_connecting)
    metrics_rows += add_metric_row('http_req_sending', http_req_sending)
    metrics_rows += add_metric_row('http_req_waiting', http_req_waiting)
    metrics_rows += add_metric_row('http_req_receiving', http_req_receiving)
    metrics_rows += add_metric_row('iteration_duration', iteration_duration)
    
    # If no metrics rows, show a message
    if not metrics_rows.strip():
        metrics_rows = """
        <tr>
            <td colspan="7" style="text-align: center; color: #999;">
                No detailed timing metrics available for this test
            </td>
        </tr>
        """
    
    detail_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{test_name} - Details</title>
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
        .back-link {{
            display: inline-block;
            color: white;
            text-decoration: none;
            margin-bottom: 20px;
            opacity: 0.9;
        }}
        .back-link:hover {{
            opacity: 1;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="index.html" class="back-link">← Back to Overview</a>
            <h1>📊 {test_name}</h1>
        </div>
        
        <div class="content">
            <div class="section">
                <h2 class="section-title">Summary Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{int(http_reqs):,}</div>
                        <div class="stat-label">HTTP Requests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{http_req_failed*100:.2f}%</div>
                        <div class="stat-label">Error Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{int(iterations):,}</div>
                        <div class="stat-label">Iterations</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{int(vus_max)}</div>
                        <div class="stat-label">Max VUs</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{format_bytes(data_received)}</div>
                        <div class="stat-label">Data Received</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{format_bytes(data_sent)}</div>
                        <div class="stat-label">Data Sent</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">Detailed Metrics</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Avg</th>
                            <th>Min</th>
                            <th>Med</th>
                            <th>Max</th>
                            <th>P90</th>
                            <th>P95</th>
                        </tr>
                    </thead>
                    <tbody>
                        {metrics_rows}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <a href="index.html" style="color: #667eea; text-decoration: none; font-weight: 600;">← Back to Overview</a>
        </div>
    </div>
</body>
</html>
"""
    
    # Write detail page
    detail_filename = file_name.replace('-summary.json', '') + '.html'
    with open(docs_dir / detail_filename, 'w') as f:
        f.write(detail_html)
    
    print(f"  ✓ Generated detail page: {detail_filename}")

def generate_html_report():
    """Generate complete HTML report"""
    results_dir = Path('test-results')
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Load all test summaries
    tests = []
    test_files = {
        '00-script1-summary.json': '00. Simple Script',
        '01-ramp-summary.json': '01. Ramping Load',
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
        file_path = results_dir / file_name
        error_msg = None
        
        if not file_path.exists():
            error_msg = f"Summary file not found: {file_name}"
            print(f"  ⚠ Warning: {error_msg}")
            summary = None
        else:
            summary = load_summary(file_path)
            if not summary:
                error_msg = f"Failed to parse {file_name}"
                print(f"  ⚠ Warning: {error_msg}")
        
        tests.append({'name': test_name, 'summary': summary, 'file': file_name})
        test_cards_html += generate_test_card(test_name, summary, file_name, error_msg)
        
        # Generate detail page for each test
        if summary:
            generate_detail_page(test_name, summary, file_name, docs_dir)
        
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
