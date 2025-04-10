from flask import Flask, render_template_string
import sys
import os
import plotly.graph_objs as go
import plotly.offline as pyo
from kubernetes import client, config

# Include AI module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai_module')))
from fetch_metrics import get_cpu_metrics

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to AI Dashboard!"

@app.route('/dashboard')
def dashboard():
    try:
        # 1. Load in-cluster config (or local config for dev)
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()

        # 2. Use AppsV1 API to get deployment info
        apps_v1 = client.AppsV1Api()
        namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read().strip() \
            if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace") else "default"
        
        deployment_name = "cloud-auto-deployment"
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        current_replicas = deployment.status.replicas or 0

        # 3. AI logic
        metrics = get_cpu_metrics()
        avg_cpu = sum(metrics.values()) / len(metrics) if metrics else 0
        decision = "📈 Scale Up" if avg_cpu > 0.15 else "📉 Scale Down"

        # 4. Plotly chart
        fig = go.Figure(data=[
            go.Bar(x=list(metrics.keys()), y=list(metrics.values()), marker_color='lightskyblue')
        ])
        fig.update_layout(title="CPU Usage by Pod", xaxis_title="Pod", yaxis_title="CPU Usage", height=400)
        plot_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

        # 5. Return the dashboard HTML
        return render_template_string("""
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial; margin: 40px; }
                h2 { color: #2e6da4; }
            </style>
        </head>
        <body>
            <h2>🚀 AI Scaling Dashboard</h2>
            <p><b>Average CPU:</b> {{ avg_cpu }}</p>
            <p><b>AI Decision:</b> {{ decision }}</p>
            <p><b>Current Replicas:</b> {{ replicas }}</p>
            {{ plot_html|safe }}
        </body>
        </html>
        """, avg_cpu=round(avg_cpu, 4), decision=decision, replicas=current_replicas, plot_html=plot_html)

    except Exception as e:
        return f"<h2 style='color:red;'>🔥 Error in dashboard:</h2><pre>{e}</pre>"