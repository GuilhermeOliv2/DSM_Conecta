import 'package:flutter/material.dart';

import 'screens/sensor_consent_page.dart';

void main() {
  runApp(const DsmConectaApp());
}

class DsmConectaApp extends StatelessWidget {
  const DsmConectaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DSM Conecta',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
      ),
      home: SensorConsentPage(onConsentChanged: _handleConsentChanged),
    );
  }

  static void _handleConsentChanged(bool consentGiven) {
    // A próxima etapa conectará este callback ao serviço de sensores.
  }
}
