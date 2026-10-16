// ignore_for_file: avoid_print

import 'dart:async';
import 'dart:convert';
import 'dart:math';

// Console output is the simulator's intended interface.
// ignore_for_file: avoid_print

void main() {
  final aleatorio = Random();

  int totalVisitantes = 0;
  int leituras = 0;

  print(' SENSOR SIMULADO DSM CONECTA \n');

  Timer.periodic(const Duration(seconds: 5), (timer) {
    final novosVisitantes = aleatorio.nextInt(4);
    totalVisitantes += novosVisitantes;
    leituras++;

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

    print('Leitura: $leituras');
    print('Mensagem JSON:');
    print(const JsonEncoder.withIndent('  ').convert(mensagem));
    print('-------------------------------');

    if (leituras >= 10) {
      timer.cancel();

      print('\nSimulação encerrada!');
      print('Total final: $totalVisitantes visitantes.');
    }
  });
}
