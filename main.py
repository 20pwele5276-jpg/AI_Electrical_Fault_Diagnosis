from app.services.fault_detector import train_model


if __name__ == "__main__":
    accuracy = train_model()
    print(f"Model accuracy: {accuracy:.2%}")