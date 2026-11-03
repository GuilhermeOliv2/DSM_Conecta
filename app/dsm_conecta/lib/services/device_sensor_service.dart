import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:geolocator/geolocator.dart';
import 'package:light/light.dart';
import 'package:sensors_plus/sensors_plus.dart';

import '../models/device_sensor_reading.dart';

typedef SensorReadingListener = void Function(DeviceSensorReading reading);

class SensorAccessException implements Exception {
  const SensorAccessException(this.message);

  final String message;

  @override
  String toString() => message;
}

class DeviceSensorService {
  DeviceSensorService({required this.onReading});

  final SensorReadingListener onReading;

  StreamSubscription<AccelerometerEvent>? _accelerometerSubscription;
  StreamSubscription<int>? _lightSubscription;
  final Light _lightSensor = Light();
  Timer? _locationTimer;
  Position? _lastPosition;
  AccelerometerEvent? _lastAccelerometer;
  int? _lastLux;
  bool _isCollecting = false;

  bool get isCollecting => _isCollecting;

  Future<void> start() async {
    if (_isCollecting) return;

    await _ensureLocationPermission();
    _isCollecting = true;

    _accelerometerSubscription =
        accelerometerEventStream(samplingPeriod: SensorInterval.normalInterval)
            .listen((event) {
              _lastAccelerometer = event;
              _emitReading();
            });

    if (defaultTargetPlatform == TargetPlatform.android) {
      try {
        await _lightSensor.requestAuthorization();
        _lightSubscription = _lightSensor.lightSensorStream.listen((lux) {
          _lastLux = lux;
          _emitReading();
        });
      } on PlatformException {
        // A device without a light sensor remains usable with the other readers.
      } on MissingPluginException {
        // The plugin is unavailable on platforms other than Android.
      }
    }

    _locationTimer = Timer.periodic(const Duration(seconds: 10), (_) {
      unawaited(_readLocation());
    });
    await _readLocation();
  }

  Future<void> stop() async {
    _isCollecting = false;
    _locationTimer?.cancel();
    await _accelerometerSubscription?.cancel();
    await _lightSubscription?.cancel();
    _locationTimer = null;
    _accelerometerSubscription = null;
    _lightSubscription = null;
  }

  Future<void> _readLocation() async {
    if (!_isCollecting) return;
    try {
      _lastPosition = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.low,
        ),
      );
      _emitReading();
    } on LocationServiceDisabledException {
      throw const SensorAccessException(
        'O serviço de localização foi desativado.',
      );
    } on PermissionDeniedException {
      await stop();
      throw const SensorAccessException(
        'A permissão de localização foi revogada.',
      );
    }
  }

  Future<void> _ensureLocationPermission() async {
    if (!await Geolocator.isLocationServiceEnabled()) {
      throw const SensorAccessException(
        'Ative o serviço de localização para continuar.',
      );
    }

    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.denied ||
        permission == LocationPermission.deniedForever) {
      throw const SensorAccessException(
        'Permissão de localização não concedida.',
      );
    }
  }

  void _emitReading() {
    if (!_isCollecting) return;
    final position = _lastPosition;
    final accelerometer = _lastAccelerometer;
    if (position == null && accelerometer == null && _lastLux == null) return;

    onReading(
      DeviceSensorReading(
        generatedAt: DateTime.now(),
        latitude: position?.latitude,
        longitude: position?.longitude,
        accuracyMeters: position?.accuracy,
        lux: _lastLux,
        accelerometerX: accelerometer?.x,
        accelerometerY: accelerometer?.y,
        accelerometerZ: accelerometer?.z,
      ),
    );
  }
}
