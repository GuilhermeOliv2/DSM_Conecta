class DeviceSensorReading {
  const DeviceSensorReading({
    required this.generatedAt,
    this.latitude,
    this.longitude,
    this.accuracyMeters,
    this.lux,
    this.accelerometerX,
    this.accelerometerY,
    this.accelerometerZ,
  });

  final DateTime generatedAt;
  final double? latitude;
  final double? longitude;
  final double? accuracyMeters;
  final int? lux;
  final double? accelerometerX;
  final double? accelerometerY;
  final double? accelerometerZ;
}
