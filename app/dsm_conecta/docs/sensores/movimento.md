# Leitor de movimento

## Objetivo

O leitor usa o `sensors_plus` para acompanhar o acelerômetro do dispositivo.
Os três eixos representam a aceleração medida em `m/s²`.

## Código principal

```dart
_accelerometerSubscription = accelerometerEventStream(
  samplingPeriod: SensorInterval.normalInterval,
).listen((event) {
  _lastAccelerometer = event;
  _emitReading();
});
```

A assinatura é cancelada quando o consentimento é revogado ou quando o serviço
é descartado, evitando que o aplicativo continue lendo o sensor.

## Entrada esperada

- Consentimento explícito do usuário.
- Dispositivo com acelerômetro disponível.
- Eventos emitidos pela plataforma em intervalos normais.

## Saída esperada

Um `AccelerometerEvent` com três valores:

```text
x: 0.12 m/s²
y: 9.71 m/s²
z: 0.34 m/s²
```

Os valores podem mudar conforme a orientação e o movimento do dispositivo. O
valor próximo de `9,8 m/s²` em um eixo pode representar a gravidade.
