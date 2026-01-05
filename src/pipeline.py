import subprocess
import sys
import time

SERVICE_NAME = "heart-disease-service"
DEPLOYMENT_NAME = "heart-disease-api"
LOCAL_PORT = 8080
TARGET_PORT = 5001

DOCKER_IMAGE = "2023ac05057/heart-disease-api:v3"  # change if needed

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Pipeline failed at step: {cmd}")
        sys.exit(result.returncode)

def try_capture(cmd):
    print(f"\n▶ Running (non-blocking): {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()

    if out:
        print(out)
    if err:
        print(err)

    if result.returncode != 0:
        print(f"⚠️ Verification step returned exit code {result.returncode} (continuing)")

def main():
    print("🚀 Starting End-to-End MLOps Pipeline (Task 1 → Task 8)")

    # Task 5
    run("pytest -q")

    # Task 1–4
    run("python -m src.train")

    # Task 6 (pull image proof)
    run(f"docker pull {DOCKER_IMAGE}")

    # Task 7
    run("kubectl apply -f k8s/deployment.yaml")
    run("kubectl apply -f k8s/service.yaml")
    run(f"kubectl rollout status deploy/{DEPLOYMENT_NAME} --timeout=180s")

    # ---- Verify endpoints inside pipeline ----
    print("\n▶ Starting port-forward in background...")
    pf = subprocess.Popen(
        f"kubectl port-forward svc/{SERVICE_NAME} {LOCAL_PORT}:{TARGET_PORT}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    time.sleep(3)

    # Optional: print one line from port-forward output
    try:
        if pf.stdout:
            line = pf.stdout.readline().strip()
            if line:
                print(line)
    except Exception:
        pass

    # Optional /metrics check (non-blocking)
    try_capture(f'curl -s http://localhost:{LOCAL_PORT}/metrics')

    # ✅ Use YOUR working curl format (single-line, escaped JSON)
    predict_cmd = (
        f'curl -X POST http://localhost:{LOCAL_PORT}/predict '
        f'-H "Content-Type: application/json" '
        f'-d "{{\\"age\\":55,\\"sex\\":1,\\"cp\\":2,\\"trestbps\\":140,\\"chol\\":250,'
        f'\\"fbs\\":0,\\"restecg\\":1,\\"thalach\\":150,\\"exang\\":0,\\"oldpeak\\":1.5,'
        f'\\"slope\\":2,\\"ca\\":0,\\"thal\\":2}}"'
    )

    try_capture(predict_cmd)

    print("\n▶ Stopping port-forward...")
    try:
        pf.terminate()
        time.sleep(1)
    except Exception:
        pass

    # Task 8 logs
    run(f"kubectl logs deploy/{DEPLOYMENT_NAME} --tail=20")

    print("\n✅ Pipeline completed successfully (Task 1 → Task 8)")

if __name__ == "__main__":
    main()