import mlflow

def main():
    mlflow.set_tracking_uri("file:./mlflow")
    mlflow.set_experiment("init_test")

    with mlflow.start_run():
        mlflow.log_param("system", "macOS + Poetry")
        mlflow.log_metric("metric_example", 0.42)

if __name__ == "__main__":
    main()

