# Leitor de luminosidade

## Objetivo

O leitor usa o pacote `light` para obter a iluminância ambiente em lux. No
Android, o plugin acessa o sensor de luz ambiente sem solicitar uma permissão
runtime adicional.

## Código principal

```dart
await _lightSensor.requestAuthorization();
_lightSubscription = _lightSensor.lightSensorStream.listen((lux) {
  _lastLux = lux;
  _emitReading();
});
```

Antes de criar a assinatura, o aplicativo solicita autorização pela API do
plugin. No Android essa chamada não exibe um diálogo de permissão. Assim, a
ausência do sensor não impede a leitura de localização e movimento.

## Entrada esperada

- Consentimento explícito do usuário.
- Plataforma Android.
- Sensor de luz ambiente disponível.

## Saída esperada

Um inteiro com a iluminância em lux:

```text
320 lux
```

Em aparelhos sem sensor, o valor permanece indisponível e a interface mostra
`indisponível`. Isso é diferente de assumir `0 lux`, que poderia representar
uma medição incorreta.
