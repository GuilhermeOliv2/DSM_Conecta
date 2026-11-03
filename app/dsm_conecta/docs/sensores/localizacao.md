# Leitor de localização

## Objetivo

O leitor usa o `geolocator` para obter a posição atual do dispositivo. A
localização só é consultada depois que o usuário marca o consentimento e o
sistema concede a permissão de localização.

## Código principal

```dart
await _ensureLocationPermission();

_lastPosition = await Geolocator.getCurrentPosition(
  locationSettings: const LocationSettings(
    accuracy: LocationAccuracy.low,
  ),
);
```

`LocationAccuracy.low` é usado porque o requisito pede localização aproximada e
reduz o consumo em comparação com uma leitura de alta precisão.

## Entrada esperada

- Consentimento explícito do usuário.
- Serviço de localização ativo no dispositivo.
- Permissão `ACCESS_COARSE_LOCATION` ou `ACCESS_FINE_LOCATION`.

## Saída esperada

Um `Position` contendo, entre outros campos:

```text
latitude: -23.55052
longitude: -46.63331
accuracy: 18.4 metros
```

Se o serviço estiver desativado ou a permissão for negada, a coleta é
interrompida e a interface exibe o erro. Nenhuma posição é usada antes do
consentimento.
