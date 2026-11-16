import 'package:material_ui/material_ui.dart';

import 'models/device_sensor_reading.dart';
import 'screens/sensor_consent_page.dart';
import 'services/device_sensor_service.dart';

void main() {
  runApp(const DsmConectaApp());
}

class DsmConectaApp extends StatefulWidget {
  const DsmConectaApp({super.key, this.onConsentChanged});

  final Future<void> Function(bool)? onConsentChanged;

  @override
  State<DsmConectaApp> createState() => _DsmConectaAppState();
}

class _DsmConectaAppState extends State<DsmConectaApp> {
  late final DeviceSensorService _sensorService;
  DeviceSensorReading? _latestReading;
  String? _sensorError;

  @override
  void initState() {
    super.initState();
    _sensorService = DeviceSensorService(
      onReading: (reading) {
        if (mounted) {
          setState(() {
            _latestReading = reading;
          });
        }
      },
    );
  }

  @override
  void dispose() {
    _sensorService.stop();
    super.dispose();
  }

  Future<void> _handleConsentChanged(bool consentGiven) async {
    if (!consentGiven) {
      await _sensorService.stop();
      setState(() => _sensorError = null);
      return;
    }

    try {
      await _sensorService.start();
      if (mounted) setState(() => _sensorError = null);
    } on SensorAccessException catch (error) {
      await _sensorService.stop();
      if (mounted) setState(() => _sensorError = error.toString());
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DSM Conecta',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
      ),
      home: SensorConsentPage(
        onConsentChanged: widget.onConsentChanged ?? _handleConsentChanged,
        latestReading: _latestReading,
        sensorError: _sensorError,
      ),
    );
  }
}
