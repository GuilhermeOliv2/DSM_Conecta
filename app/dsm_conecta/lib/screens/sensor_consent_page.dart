import 'package:flutter/material.dart';

class SensorConsentPage extends StatefulWidget {
  const SensorConsentPage({super.key, required this.onConsentChanged});

  final ValueChanged<bool> onConsentChanged;

  @override
  State<SensorConsentPage> createState() => _SensorConsentPageState();
}

class _SensorConsentPageState extends State<SensorConsentPage> {
  bool _hasReadTerms = false;
  bool _consentGiven = false;

  void _updateConsent(bool value) {
    setState(() {
      _consentGiven = value;
      if (!value) {
        _hasReadTerms = false;
      }
    });
    widget.onConsentChanged(value);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Uso dos sensores')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            Icon(
              Icons.sensors_outlined,
              size: 56,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 20),
            Text(
              'Consentimento para coleta',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 12),
            const Text(
              'O DSM Conecta pode usar sensores do dispositivo para '
              'produzir dados de telemetria da aplicação.',
            ),
            const SizedBox(height: 20),
            const _SensorInfoTile(
              icon: Icons.location_on_outlined,
              title: 'Localização aproximada',
              description:
                  'Usada para validar a proximidade do visitante ao evento.',
            ),
            const _SensorInfoTile(
              icon: Icons.light_mode_outlined,
              title: 'Luminosidade',
              description: 'Usada para registrar a intensidade de luz detectada pelo aparelho.',
            ),
            const _SensorInfoTile(
              icon: Icons.screen_rotation_outlined,
              title: 'Movimento',
              description:
                  'Usado para registrar variações captadas pelo acelerômetro.',
            ),
            const SizedBox(height: 12),
            const Text(
              'A coleta só será iniciada após sua autorização. '
              'Você pode revogar o consentimento a qualquer momento.',
            ),
            const SizedBox(height: 12),
            CheckboxListTile(
              contentPadding: EdgeInsets.zero,
              value: _hasReadTerms,
              onChanged: _consentGiven
                  ? null
                  : (value) {
                      setState(() => _hasReadTerms = value ?? false);
                    },
              title: const Text(
                'Li e compreendi quais dados poderão ser coletados.',
              ),
              controlAffinity: ListTileControlAffinity.leading,
            ),
            const SizedBox(height: 8),
            FilledButton(
              onPressed: _hasReadTerms && !_consentGiven
                  ? () => _updateConsent(true)
                  : null,
              child: const Text('Autorizar uso dos sensores'),
            ),
            OutlinedButton(
              onPressed: _consentGiven ? () => _updateConsent(false) : null,
              child: const Text('Revogar consentimento'),
            ),
            const SizedBox(height: 12),
            Text(
              _consentGiven
                  ? 'Consentimento concedido. A integração dos sensores '
                        'poderá ser iniciada.'
                  : 'Consentimento não concedido. Nenhum sensor será iniciado.',
              style: TextStyle(
                color: _consentGiven
                    ? Colors.green.shade700
                    : Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SensorInfoTile extends StatelessWidget {
  const _SensorInfoTile({
    required this.icon,
    required this.title,
    required this.description,
  });

  final IconData icon;
  final String title;
  final String description;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: Icon(icon),
      title: Text(title),
      subtitle: Text(description),
    );
  }
}
