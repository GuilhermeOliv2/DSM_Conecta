// ignore_for_file: avoid_print

import 'dart:convert';
import 'dart:math';

import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

const mqttHost = String.fromEnvironment('MQTT_HOST', defaultValue: '127.0.0.1');
const mqttPort = int.fromEnvironment('MQTT_PORT', defaultValue: 1883);
const mqttUser = String.fromEnvironment('MQTT_USER');
const mqttPassword = String.fromEnvironment('MQTT_PASSWORD');
const mqttTopic = 'dsm/prod/totem/sensor/contagem';
const mqttStatusTopic = 'dsm/prod/totem/sensor/status';

Future<void> main() async {
  final aleatorio = Random();
  int totalVisitantes = 0;

  print(' SENSOR SIMULADO DSM CONECTA \n');

  final client = MqttServerClient(mqttHost, 'sensor-simulado');
  client.port = mqttPort;
  client.logging(on: false);
  client.keepAlivePeriod = 30;
  client.connectionMessage = MqttConnectMessage()
      .withClientIdentifier(
        'sensor-simulado-${DateTime.now().millisecondsSinceEpoch}',
      )
      .authenticateAs(mqttUser, mqttPassword)
      .withWillTopic(mqttStatusTopic)
      .withWillMessage('{"status":"offline","sensor_id":"totem-01"}')
      .withWillQos(MqttQos.atLeastOnce)
      .withWillRetain();

  try {
    await client.connect();
  } catch (error) {
    print('RECUSADO: falha ao conectar ao broker MQTT: $error');
    client.disconnect();
    return;
  }

  if (client.connectionStatus?.state != MqttConnectionState.connected) {
    print(
      'RECUSADO: broker MQTT rejeitou a conexão '
      '(${client.connectionStatus?.returnCode})',
    );
    client.disconnect();
    return;
  }

  final statusBuilder = MqttClientPayloadBuilder()
    ..addString('{"status":"online","sensor_id":"totem-01"}');
  client.publishMessage(
    mqttStatusTopic,
    MqttQos.atLeastOnce,
    statusBuilder.payload!,
    retain: true,
  );

  print('Conectado ao broker MQTT em $mqttHost:$mqttPort');
  print('Publicando em $mqttTopic\n');

  for (var leitura = 1; leitura <= 10; leitura++) {
    final novosVisitantes = aleatorio.nextInt(4);
    totalVisitantes += novosVisitantes;
    final agora = DateTime.now().toUtc();
    final eventId =
        '${agora.microsecondsSinceEpoch}-${aleatorio.nextInt(1000000)}';
    final mensagem = {
      'event_id': eventId,
      'session_id': 'sensor',
      'category': 'sensor',
      'origin': 'totem',
      'timestamp': agora.toIso8601String(),
      'schema_version': '1.0',
      'payload': {
        'sensor_id': 'totem-01',
        'novos_visitantes': novosVisitantes,
        'total_visitantes': totalVisitantes,
      },
    };

    final payload = jsonEncode(mensagem);
    final builder = MqttClientPayloadBuilder()..addString(payload);
    client.publishMessage(
      mqttTopic,
      MqttQos.atLeastOnce,
      builder.payload!,
      retain: true,
    );

    print('Leitura: $leitura publicada (event_id: $eventId)');
    print(const JsonEncoder.withIndent('  ').convert(mensagem));
    print('-------------------------------');

    await Future<void>.delayed(const Duration(seconds: 5));
  }

  final offlineBuilder = MqttClientPayloadBuilder()
    ..addString('{"status":"offline","sensor_id":"totem-01"}');
  client.publishMessage(
    mqttStatusTopic,
    MqttQos.atLeastOnce,
    offlineBuilder.payload!,
    retain: true,
  );
  client.disconnect();
  print('\nSimulação encerrada!');
  print('Total final: $totalVisitantes visitantes.');
}
