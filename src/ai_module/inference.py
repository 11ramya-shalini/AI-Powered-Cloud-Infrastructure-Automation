from fetch_metrics import get_cpu_metrics
import subprocess
import time 

# Set your threshold values
CPU_THRESHOLD = 0.15  # Adjust based on what you saw in Grafana
MAX_PODS = 5
MIN_PODS = 2

def scale_deployment(replicas):
    deployment_name = "cloud-auto-deployment"
    namespace = "default"

    print(f"[⚙️ Scaling] Setting replicas to {replicas}")
    subprocess.run([
        "kubectl", "scale", f"deployment/{deployment_name}",
        f"--replicas={replicas}", f"-n", namespace
    ])

def ai_scaling_decision():
    metrics = get_cpu_metrics()

    if not metrics:
        print("[⚠️] No CPU metrics received.")
        return

    avg_cpu = sum(metrics.values()) / len(metrics)
    print(f"[📊 AI Decision] Avg CPU usage: {avg_cpu:.4f}")

    if avg_cpu > CPU_THRESHOLD:
        print("[📈] High CPU detected. Scaling up.")
        scale_deployment(MAX_PODS)
    else:
        print("[📉] Low CPU detected. Scaling down.")
        scale_deployment(MIN_PODS)

if __name__ == "__main__":
     for i in range(3):  # ⬅️ Retry 3 times
        print(f"\n🔁 [Try {i + 1}/3] Rechecking CPU usage in cluster...")
        ai_scaling_decision()
        if i < 2:  # ⬅️ Avoid waiting after the final run
            time.sleep(30)  # ⏳ Wait 30 seconds between checks
