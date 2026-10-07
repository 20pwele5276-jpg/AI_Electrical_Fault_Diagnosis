from app.services.fault_detector import predict_fault


fault, confidence = predict_fault(
    voltage=255,
    current=4.0,
    frequency=50.0,
    power_factor=0.90,
    temperature=40,
)

print(f"Predicted fault: {fault}")
print(f"Confidence: {confidence:.2%}")