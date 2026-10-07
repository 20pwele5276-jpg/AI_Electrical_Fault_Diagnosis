from app.services.fault_detector import predict_fault


def test_overvoltage_prediction():
    fault, confidence = predict_fault(
        voltage=255,
        current=4,
        frequency=50,
        power_factor=0.90,
        temperature=40,
    )

    assert fault == "Overvoltage"
    assert confidence > 0.5


def test_normal_prediction():
    fault, confidence = predict_fault(
        voltage=230,
        current=5,
        frequency=50,
        power_factor=0.96,
        temperature=35,
    )

    assert fault == "Normal"
    assert confidence > 0.5